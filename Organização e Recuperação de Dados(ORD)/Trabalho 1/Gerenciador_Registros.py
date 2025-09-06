import struct
import sys
import os

# =========================================================================


MARC_DEL = b'*-1'
TAM_MARC_DEL = len(MARC_DEL)
TAM_PONT_LED = 4


# =========================================================================


def executa_operacoes(arq_op):
    with open(arq_op, "r", encoding='utf-8') as file:
        for line in file:
            linha = line.strip()
            if not linha:
                continue
            op = linha[0]
            conteudo = linha[2:]
            if op == "b":
                print(f'Busca pelo registro de chave "{conteudo}"')
                busca_por_id(int(conteudo))
            elif op == "i":
                insere_filme(conteudo)
            elif op == 'r':
                print(f'Remoção do registro de chave "{conteudo}"')
                remove_filme(conteudo)


# =========================================================================


def busca_por_id(id_buscado, caminho_arquivo="filmes.dat"):
    try:
        with open(caminho_arquivo, "rb") as f:
            f.seek(TAM_PONT_LED)
            while True:
                posicao_inicio_registro = f.tell()
                tamanho_bytes = f.read(2)
                if not tamanho_bytes or len(tamanho_bytes) < 2:
                    break
                tamanho_payload = struct.unpack(">H", tamanho_bytes)[0]
                if tamanho_payload == 0:
                    continue
                payload_bytes = f.read(tamanho_payload)
                if len(payload_bytes) < tamanho_payload:
                    break
                if payload_bytes.startswith(MARC_DEL):
                    continue
                try:
                    payload_completo_str = payload_bytes.decode(
                        'utf-8', errors='replace')
                    id_filme_extraido_str = payload_completo_str.split('|', 1)[
                        0]
                    if id_filme_extraido_str.strip().isdigit():
                        if int(id_filme_extraido_str.strip()) == id_buscado:
                            print(f"{payload_completo_str}")
                            print(f"({tamanho_payload} bytes)")
                            print(
                                f"Local: offset = {posicao_inicio_registro} bytes (0x{posicao_inicio_registro:x})")
                            return
                except Exception:
                    pass
            print(f'Erro: registro com ID "{id_buscado}" nao encontrado!')
    except FileNotFoundError:
        print(f"Erro: arquivo {caminho_arquivo} não encontrado.")
    except Exception as e:
        print(
            f"Ocorreu um erro inesperado ao buscar pelo ID {id_buscado}: {e}")


# =========================================================================


def insere_filme(dados_filme_str, caminho_arquivo="filmes.dat"):
    id_filme_str = dados_filme_str.split('|', 1)[0]
    payload_bytes_novo_filme = dados_filme_str.encode('utf-8')
    tamanho_payload_necessario = len(payload_bytes_novo_filme)
    try:
        with open(caminho_arquivo, "r+b") as f:
            f.seek(0)
            led_head_bytes = f.read(TAM_PONT_LED)
            led_head_offset = struct.unpack(">i", led_head_bytes)[0]
            best_fit_info = {
                'slot_offset': -1,
                'slot_payload_size': float('inf'),
                'prev_slot_led_pointer_location': -1,
                'next_pointer_val_in_slot': -1
            }
            current_slot_offset = led_head_offset
            location_of_pointer_to_current_slot = 0
            while current_slot_offset != -1:
                f.seek(current_slot_offset)
                slot_payload_size_bytes = f.read(2)
                if not slot_payload_size_bytes or len(slot_payload_size_bytes) < 2:
                    print(
                        f"Erro: Falha ao ler tamanho do slot na LED em offset {current_slot_offset}.")
                    break
                slot_payload_size = struct.unpack(
                    ">H", slot_payload_size_bytes)[0]
                f.seek(current_slot_offset + 2)
                marker = f.read(TAM_MARC_DEL)
                if marker == MARC_DEL:
                    next_led_pointer_bytes = f.read(TAM_PONT_LED)
                    if not next_led_pointer_bytes or len(next_led_pointer_bytes) < TAM_PONT_LED:
                        print(
                            f"Erro: Falha ao ler ponteiro LED no slot em offset {current_slot_offset}.")
                        break
                    next_led_pointer_val = struct.unpack(
                        ">i", next_led_pointer_bytes)[0]
                    if slot_payload_size >= tamanho_payload_necessario:
                        if slot_payload_size < best_fit_info['slot_payload_size']:
                            best_fit_info['slot_offset'] = current_slot_offset
                            best_fit_info['slot_payload_size'] = slot_payload_size
                            best_fit_info['prev_slot_led_pointer_location'] = location_of_pointer_to_current_slot
                            best_fit_info['next_pointer_val_in_slot'] = next_led_pointer_val
                else:
                    print(
                        f"Aviso: Bloco na LED em {current_slot_offset} não tem marcador '{MARC_DEL.decode()}'. Pulando.")
                    break
                location_of_pointer_to_current_slot = current_slot_offset + \
                    2 + TAM_MARC_DEL
                current_slot_offset = next_led_pointer_val
            if best_fit_info['slot_offset'] != -1:
                target_offset = best_fit_info['slot_offset']
                original_slot_payload_size = best_fit_info['slot_payload_size']
                f.seek(target_offset + 2)
                f.write(payload_bytes_novo_filme)
                padding_size = original_slot_payload_size - tamanho_payload_necessario
                if padding_size > 0:
                    f.write(b'\0' * padding_size)
                f.seek(best_fit_info['prev_slot_led_pointer_location'])
                f.write(struct.pack(
                    ">i", best_fit_info['next_pointer_val_in_slot']))
                f.flush()

                print(
                    f'Inserção do registro de chave "{id_filme_str}" ({tamanho_payload_necessario} bytes)')
                print(
                    f"Tamanho do espaço reutilizado: {original_slot_payload_size} bytes")
                print(
                    f"Local: offset = {target_offset} bytes (0x{target_offset:x})")
            else:
                f.seek(0, 2)
                f.write(struct.pack(">H", tamanho_payload_necessario))
                f.write(payload_bytes_novo_filme)
                f.flush()
                print(
                    f'Inserção do registro de chave "{id_filme_str}" ({tamanho_payload_necessario} bytes)')
                print(f"Local: fim do arquivo")
    except FileNotFoundError:
        print(
            f"Erro crítico: Arquivo {caminho_arquivo} não encontrado durante a inserção.")
    except Exception as e:
        print(
            f"Ocorreu um erro inesperado durante a inserção do filme ID {id_filme_str}: {e}")


# =========================================================================


def remove_filme(id_remover_str, caminho_arquivo="filmes.dat"):
    registro_encontrado = False
    offset_inicio_registro_encontrado = -1
    tamanho_payload_encontrado = -1
    try:
        id_remover = int(id_remover_str)
        with open(caminho_arquivo, "r+b") as f:
            f.seek(TAM_PONT_LED)
            while True:
                posicao_atual_leitura = f.tell()
                tamanho_bytes = f.read(2)
                if not tamanho_bytes or len(tamanho_bytes) < 2:
                    break
                tamanho_payload = struct.unpack(">H", tamanho_bytes)[0]
                if tamanho_payload == 0:
                    continue
                payload_bytes = f.read(tamanho_payload)
                if len(payload_bytes) < tamanho_payload:
                    break
                if payload_bytes.startswith(MARC_DEL):
                    continue
                try:
                    id_filme_extraido_str = payload_bytes.decode(
                        'utf-8', errors='replace').split('|', 1)[0]
                    if id_filme_extraido_str.strip().isdigit():
                        if int(id_filme_extraido_str.strip()) == id_remover:
                            registro_encontrado = True
                            offset_inicio_registro_encontrado = posicao_atual_leitura
                            tamanho_payload_encontrado = tamanho_payload
                            break
                except Exception:
                    pass
            if registro_encontrado:
                f.seek(offset_inicio_registro_encontrado + 2)
                f.write(MARC_DEL)
                f.seek(0)
                current_led_head_bytes = f.read(TAM_PONT_LED)
                old_led_head_offset = struct.unpack(
                    ">i", current_led_head_bytes)[0]
                f.seek(offset_inicio_registro_encontrado +
                       2 + TAM_MARC_DEL)
                f.write(struct.pack(">i", old_led_head_offset))
                f.seek(0)
                f.write(struct.pack(">i", offset_inicio_registro_encontrado))
                f.flush()
                print("Registro removido!")
                print(f"({tamanho_payload_encontrado} bytes)")
                print(
                    f"Local: offset = {offset_inicio_registro_encontrado} bytes (0x{offset_inicio_registro_encontrado:x})")
            else:
                print(f"Erro: registro nao encontrado!")
    except FileNotFoundError:
        print(
            f"Erro: arquivo {caminho_arquivo} não encontrado durante a remoção.")
    except ValueError:
        print(f"Erro: ID '{id_remover_str}' inválido para remoção.")
    except Exception as e:
        print(
            f"Ocorreu um erro inesperado durante a remoção do ID {id_remover_str}: {e}")


# =========================================================================


def imprime_led(caminho_arquivo="filmes.dat"):
    try:
        with open(caminho_arquivo, "rb") as f:
            f.seek(0)
            led_head_bytes = f.read(TAM_PONT_LED)
            if len(led_head_bytes) < TAM_PONT_LED:
                print(
                    f"Erro: Arquivo {caminho_arquivo} muito pequeno para conter o cabeçalho da LED.")
                return
            current_led_offset = struct.unpack(">i", led_head_bytes)[
                0]
            led_output_parts = ["LED"]
            espacos_disponiveis_count = 0
            while current_led_offset != -1:
                espacos_disponiveis_count += 1
                f.seek(current_led_offset)
                slot_payload_size_bytes = f.read(2)
                if not slot_payload_size_bytes or len(slot_payload_size_bytes) < 2:
                    print(
                        f"\nErro: Falha ao ler tamanho do slot na LED em offset {current_led_offset}. LED pode estar inconsistente.")
                    led_output_parts.append(
                        f"[offset: {current_led_offset}, ERRO AO LER TAMANHO]")
                    break
                slot_payload_size = struct.unpack(">H", slot_payload_size_bytes)[
                    0]
                led_output_parts.append(
                    f"[offset: {current_led_offset}, tam: {slot_payload_size}]")
                f.seek(current_led_offset + 2)
                marker = f.read(TAM_MARC_DEL)
                if marker != MARC_DEL:
                    print(
                        f"\nAviso: Bloco na LED em {current_led_offset} (tam: {slot_payload_size}) não tem marcador '{MARC_DEL.decode()}' esperado no início do payload. LED pode estar inconsistente.")
                    led_output_parts.append("ERRO DE MARCADOR NO BLOCO")
                    break
                next_led_pointer_bytes = f.read(TAM_PONT_LED)
                if not next_led_pointer_bytes or len(next_led_pointer_bytes) < TAM_PONT_LED:
                    print(
                        f"\nErro: Falha ao ler ponteiro LED no slot em offset {current_led_offset}. LED pode estar inconsistente.")
                    led_output_parts.append(
                        f"[offset: {current_led_offset}, tam: {slot_payload_size}, ERRO AO LER PRÓXIMO PONTEIRO]")
                    break
                current_led_offset = struct.unpack(
                    ">i", next_led_pointer_bytes)[0]
            led_output_parts.append("fim")
            print(" -> ".join(led_output_parts))
            print(f"Total: {espacos_disponiveis_count} espaços disponíveis")
            print("A LED foi impressa com sucesso!")
    except FileNotFoundError:
        print(f"Erro: arquivo {caminho_arquivo} não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao imprimir a LED: {e}")


# =========================================================================


def compactacao(caminho_arquivo="filmes.dat"):
    try:
        with open(caminho_arquivo, "r+b") as f:
            ponteiro_leitura = TAM_PONT_LED
            ponteiro_escrita = TAM_PONT_LED
            f.seek(ponteiro_leitura)
            while True:
                offset_leitura_atual = f.tell()
                tamanho_bytes = f.read(2)
                if not tamanho_bytes or len(tamanho_bytes) < 2:
                    break
                tamanho_payload = struct.unpack(">H", tamanho_bytes)[0]
                if tamanho_payload == 0:
                    ponteiro_leitura = f.tell()
                    continue
                payload_bytes = f.read(tamanho_payload)
                ponteiro_leitura = f.tell()
                if len(payload_bytes) < tamanho_payload:
                    print(
                        f"Aviso: Leitura incompleta no arquivo original. Offset: {offset_leitura_atual}")
                    break
                if not payload_bytes.startswith(MARC_DEL):
                    f.seek(ponteiro_escrita)
                    f.write(tamanho_bytes)
                    f.write(payload_bytes)
                    ponteiro_escrita = f.tell()
                f.seek(ponteiro_leitura)
            f.truncate(ponteiro_escrita)
            f.seek(0)
            f.write(struct.pack(">i", -1))
            f.flush()
            print(
                f"Arquivo {caminho_arquivo} compactado com sucesso!")
    except FileNotFoundError:
        print(
            f"Erro: arquivo {caminho_arquivo} não encontrado para compactação.")
    except Exception as e:
        print(f"Ocorreu um erro durante a compactação in-place: {e}")


# =========================================================================


def main():
    if len(sys.argv) < 2:
        print("Erro: Modo de operação não especificado (-e, -p, ou -c).")
        print("Uso: python principal.py -e <arquivo_operacoes>")
        print("     python principal.py -p")
        print("     python principal.py -c")
        return
    arg = sys.argv[1]
    caminho_arquivo_filmes = "filmes.dat"
    if arg in ["-e", "-p", "-c"]:
        if not os.path.exists(caminho_arquivo_filmes):
            print(f"Erro: arquivo {caminho_arquivo_filmes} não encontrado.")
            return
    if arg == "-e":
        if len(sys.argv) == 3:
            arquivo_operacoes = sys.argv[2]
            executa_operacoes(arquivo_operacoes)
        else:
            print(
                "Erro: Para o modo -e, você precisa fornecer o nome do arquivo de operações.")
            print("Uso: python principal.py -e <arquivo_operacoes>")
    elif arg == "-p":
        imprime_led()
    elif arg == "-c":
        compactacao()
    else:
        print(f"Erro: Modo de operação '{arg}' desconhecido.")
        print("Use -e, -p ou -c.")


if __name__ == "__main__":
    main()
