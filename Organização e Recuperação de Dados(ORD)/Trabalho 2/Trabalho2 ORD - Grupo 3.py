import os
import struct
import argparse

# =========================================================================

TAM_MAX_BUCKET = 5
EMPTY_KEY = -1
DIR_FILE = 'diretorio.dat'
BUCKET_FILE = 'buckets.dat'

# =========================================================================


class Bucket:
    def __init__(self, prof_local, chaves=None, prox_livre=-1):
        self.prof_local = prof_local
        self.chaves = chaves or [EMPTY_KEY] * TAM_MAX_BUCKET
        self.prox_livre = prox_livre

    @property
    def cont(self):
        return sum(1 for chave in self.chaves if chave != EMPTY_KEY)

    def esta_cheio(self):
        return self.cont >= TAM_MAX_BUCKET

    def inserir(self, chave):
        if chave in self.chaves:
            return False
        for i in range(TAM_MAX_BUCKET):
            if self.chaves[i] == EMPTY_KEY:
                self.chaves[i] = chave
                return True
        return False

    def remover(self, chave):
        for i in range(TAM_MAX_BUCKET):
            if self.chaves[i] == chave:
                self.chaves[i] = EMPTY_KEY
                self.chaves.sort(key=lambda x: x == EMPTY_KEY)
                return True
        return False

    def serialize(self):
        return struct.pack(f'i{TAM_MAX_BUCKET}ii', self.prof_local, *self.chaves, self.prox_livre)

    @staticmethod
    def deserialize(data):
        unpacked = struct.unpack(f'i{TAM_MAX_BUCKET}ii', data)
        return Bucket(unpacked[0], list(unpacked[1:TAM_MAX_BUCKET+1]), unpacked[-1])

    @staticmethod
    def size():
        return struct.calcsize(f'i{TAM_MAX_BUCKET}ii')

# =========================================================================


class Diretorio:
    def __init__(self, profundidade, refs):
        self.profundidade = profundidade
        self.refs = refs

    def serialize(self):
        return struct.pack('i', self.profundidade) + struct.pack(f'{len(self.refs)}i', *self.refs)

    @staticmethod
    def deserialize(data):
        profundidade = struct.unpack('i', data[:4])[0]
        num_refs = 2 ** profundidade
        refs = list(struct.unpack(f'{num_refs}i', data[4:4 + 4 * num_refs]))
        return Diretorio(profundidade, refs)

    def size(self):
        return 4 + len(self.refs) * 4

# =========================================================================


class HashingExtensivel:
    def __init__(self):
        self.dir = None
        self.ped_topo = -1
        self.buckets = open(
            BUCKET_FILE, 'r+b') if os.path.exists(BUCKET_FILE) else open(BUCKET_FILE, 'w+b')
        if os.path.exists(DIR_FILE) and os.path.getsize(DIR_FILE) > 0:
            with open(DIR_FILE, 'rb') as f:
                self.dir = Diretorio.deserialize(f.read())
        else:
            b = Bucket(0)
            self.dir = Diretorio(0, [0])
            self._write_bucket(0, b)

    def close(self):
        with open(DIR_FILE, 'wb') as f:
            f.write(self.dir.serialize())
        self.buckets.close()

    def _read_bucket(self, rrn):
        self.buckets.seek(rrn * Bucket.size())
        data = self.buckets.read(Bucket.size())
        if len(data) < Bucket.size():
            return Bucket(0)
        return Bucket.deserialize(data)

    def _write_bucket(self, rrn, bucket):
        self.buckets.seek(rrn * Bucket.size())
        self.buckets.write(bucket.serialize())

    def _new_bucket_rrn(self):
        if self.ped_topo != -1:
            rrn = self.ped_topo
            bucket_livre = self._read_bucket(rrn)
            self.ped_topo = bucket_livre.prox_livre
            return rrn
        else:
            self.buckets.seek(0, os.SEEK_END)
            return self.buckets.tell() // Bucket.size()

    def gerar_endereco(self, chave, profundidade):
        return chave & ((1 << profundidade) - 1)

    def buscar(self, chave):
        end = self.gerar_endereco(chave, self.dir.profundidade)
        rrn = self.dir.refs[end]
        b = self._read_bucket(rrn)
        return chave in b.chaves, rrn, b

    def inserir(self, chave):
        achou, _, _ = self.buscar(chave)
        if achou:
            return False
        while True:
            end = self.gerar_endereco(chave, self.dir.profundidade)
            rrn = self.dir.refs[end]
            bucket = self._read_bucket(rrn)
            if not bucket.esta_cheio():
                bucket.inserir(chave)
                self._write_bucket(rrn, bucket)
                return True
            self.dividir(rrn, bucket)

    def dividir(self, rrn, bucket):
        if bucket.prof_local == self.dir.profundidade:
            self._dobrar_diretorio()
        nova_prof = bucket.prof_local + 1
        novo_bucket = Bucket(nova_prof)
        novo_rrn = self._new_bucket_rrn()
        bucket.prof_local = nova_prof
        bit_diferenciador = 1 << (nova_prof - 1)
        for i, ref_rrn in enumerate(self.dir.refs):
            if ref_rrn == rrn:
                if i & bit_diferenciador:
                    self.dir.refs[i] = novo_rrn
        chaves_antigas = [k for k in bucket.chaves if k != EMPTY_KEY]
        bucket.chaves = [EMPTY_KEY] * TAM_MAX_BUCKET
        self._write_bucket(rrn, bucket)
        self._write_bucket(novo_rrn, novo_bucket)

        for ch in chaves_antigas:
            end = self.gerar_endereco(ch, self.dir.profundidade)
            destino_rrn = self.dir.refs[end]
            if destino_rrn == rrn:
                bucket.inserir(ch)
            else:
                novo_bucket.inserir(ch)
        self._write_bucket(rrn, bucket)
        self._write_bucket(novo_rrn, novo_bucket)

    def _dobrar_diretorio(self):
        self.dir.refs += self.dir.refs[:]
        self.dir.profundidade += 1

    def remover(self, chave):
        achou, rrn, bucket = self.buscar(chave)
        if not achou:
            return False
        bucket.remover(chave)
        self._write_bucket(rrn, bucket)
        self._tentar_fundir_buckets(rrn)
        return True

    def _tentar_fundir_buckets(self, rrn):
        bucket = self._read_bucket(rrn)
        prof_local = bucket.prof_local
        if prof_local == 0:
            return
        end_bucket = -1
        for i, ref in enumerate(self.dir.refs):
            if ref == rrn:
                end_bucket = i
                break
        if end_bucket == -1:
            return
        bit_amigo = 1 << (prof_local - 1)
        end_amigo = end_bucket ^ bit_amigo
        if end_amigo >= len(self.dir.refs):
            return
        rrn_amigo = self.dir.refs[end_amigo]
        if rrn_amigo == rrn:
            return
        bucket_amigo = self._read_bucket(rrn_amigo)
        if bucket_amigo.prof_local != prof_local:
            return
        if bucket.cont + bucket_amigo.cont <= TAM_MAX_BUCKET:
            rrn_destino = min(rrn, rrn_amigo)
            rrn_origem = max(rrn, rrn_amigo)
            bucket_destino = self._read_bucket(rrn_destino)
            bucket_origem = self._read_bucket(rrn_origem)
            for ch in bucket_origem.chaves:
                if ch != EMPTY_KEY:
                    bucket_destino.inserir(ch)
            bucket_destino.prof_local -= 1
            self._write_bucket(rrn_destino, bucket_destino)
            for i in range(len(self.dir.refs)):
                if self.dir.refs[i] == rrn_origem:
                    self.dir.refs[i] = rrn_destino
            bucket_origem.chaves = [EMPTY_KEY] * TAM_MAX_BUCKET
            bucket_origem.prox_livre = self.ped_topo
            self.ped_topo = rrn_origem
            self._write_bucket(rrn_origem, bucket_origem)
            print(f"> Bucket {rrn_origem} foi removido e adicionado à PED.")
            self._tentar_reduzir_diretorio()
            self._tentar_fundir_buckets(rrn_destino)

    def _tentar_reduzir_diretorio(self):
        while self.dir.profundidade > 0:
            metade = len(self.dir.refs) // 2
            if self.dir.refs[:metade] == self.dir.refs[metade:]:
                self.dir.refs = self.dir.refs[:metade]
                self.dir.profundidade -= 1
            else:
                break

    def imprimir_buckets(self):
        print("------- PED -------")
        print("RRN Topo:", self.ped_topo)
        print("----- Buckets -----")
        self.buckets.seek(0, os.SEEK_END)
        total_size = self.buckets.tell()
        self.buckets.seek(0)
        rrn = 0
        while self.buckets.tell() < total_size:
            data = self.buckets.read(Bucket.size())
            if not data or len(data) < Bucket.size():
                break
            b = Bucket.deserialize(data)
            is_referenced = rrn in self.dir.refs
            if b.cont == 0 and not is_referenced:
                print(f"Bucket {rrn} --> Removido (na PED = {b.prox_livre})")
            else:
                print(f"Bucket {rrn} (Prof = {b.prof_local}):")
                print(f"ContaChaves = {b.cont}")
                print(f"Chaves = {b.chaves}")
            rrn += 1

    def imprimir_diretorio(self):
        print("----- Diretório -----")
        for i, rrn in enumerate(self.dir.refs):
            print(f"dir[{i}] = bucket[{rrn}]")
        print(f"\nProfundidade = {self.dir.profundidade}")
        print(f"Tamanho atual = {len(self.dir.refs)}")
        usados = set(self.dir.refs)
        print(f"Total de buckets = {len(usados)}")

# =========================================================================


def processa_operacoes(path, h):
    with open(path) as f:
        for linha in f:
            if not linha.strip():
                continue
            op, valor = linha.strip().split()
            chave = int(valor)
            if op == 'i':
                if h.inserir(chave):
                    print(f"> Inserção da chave {chave}: Sucesso.")
                else:
                    print(
                        f"> Inserção da chave {chave}: Falha – Chave duplicada.")
            elif op == 'b':
                achou, rrn, _ = h.buscar(chave)
                if achou:
                    print(
                        f"> Busca pela chave {chave}: Chave encontrada no bucket {rrn}.")
                else:
                    print(f"> Busca pela chave {chave}: Chave não encontrada.")
            elif op == 'r':
                if h.remover(chave):
                    print(f"> Remoção da chave {chave}: Sucesso.")
                else:
                    print(
                        f"> Remoção da chave {chave}: Falha – Chave não encontrada.")

# =========================================================================


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', type=str)
    parser.add_argument('-pd', action='store_true')
    parser.add_argument('-pb', action='store_true')
    args = parser.parse_args()
    if args.e:
        if os.path.exists(DIR_FILE):
            os.remove(DIR_FILE)
        if os.path.exists(BUCKET_FILE):
            os.remove(BUCKET_FILE)
    h = HashingExtensivel()
    if args.e:
        processa_operacoes(args.e, h)
    if args.pd:
        h.imprimir_diretorio()
    if args.pb:
        h.imprimir_buckets()
    h.close()
