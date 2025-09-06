from __future__ import annotations
from typing import Any


class No:
    def __init__(self, chave):
        '''
        Representa um nó de uma árvore. Contém uma chave (dado de
        algum tipo, sujeito a uma relação de ordem),referências
        para subárvore esquerda e subárvore direita, e a altura (iniciada em 1).
        '''
        self.chave = chave
        self.esq: No | None = None
        self.dir: No | None = None
        self.altura = 1

    def __str__(self):
        '''
        Representação string de um nó.
        '''
        return str(self.chave)


class ArvoreAVL:
    def __init__(self):
        '''
        Representa uma árvore AVL, iniciando com uma raiz setada em None.
        '''
        self.raiz = None

    def vazia(self) -> bool:
        '''
        Verifica se a árvore está vazia, isto é, devolve True se não possui
        nenhum vértice; caso contrário, devolve False.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.vazia()
        True
        >>> _ = arvore.insere(10)
        >>> arvore.vazia()
        False
        '''
        return self.raiz == None

    def exibe_pre_ordem(self, raiz: No | None) -> str:
        '''Exibe a representação parentizada da estrutura em pré-ordem,
        isto é: 
        - uma árvore vazia é representada por vazio;
        - uma árvore não vazia é representada pelo conteúdo do nó **raiz**, 
        seguido da representação da subárvore esquerda, seguida da 
        representação da subárvore direita, circundados por parênteses.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        ''
        >>> for item in [1, 2, 3]:
        ...     arvore.insere(item)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(2 (1) (3))'
        '''
        repr = ''
        if raiz != None:
            repr += '(' + str(raiz.chave)
            if raiz.esq != None:
                repr += ' ' + str(self.exibe_pre_ordem(raiz.esq))
            if raiz.dir != None:
                repr += ' ' + str(self.exibe_pre_ordem(raiz.dir))
            repr += ')'
        return repr

    def altura_no(self, no: No | None) -> int:
        '''
        Dado um nó, a função devolve a altura do nó.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.altura_no(arvore.raiz)
        1
        >>> arvore.insere(5)
        >>> arvore.altura_no(arvore.raiz)
        2
        '''
        if no == None:
            return 0
        return no.altura

    def __balanceamento(self, no: No | None) -> int:
        '''
        Dado um nó, a função devolve o fator de balanceamento dele.
        '''
        if no == None:
            return 0
        return self.altura_no(no.esq) - self.altura_no(no.dir)

    def __insere_interno(self, raiz, chave):
        '''
        Função interna que realiza a inserção de um nó na árvore AVL, efetua também as rotações necessárias para garantir o balanceamento.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(20 (10) (30))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(20 (10) (30 (40)))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(20 (10) (40 (30) (50)))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(50)
        >>> arvore.insere(40)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(20 (10) (40 (30) (50)))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.insere(30)
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(40 (20 (10) (30)) (50))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(4)
        >>> arvore.insere(5)
        >>> arvore.insere(7)
        >>> arvore.insere(2)
        >>> arvore.insere(1)
        >>> arvore.insere(3)
        >>> arvore.insere(6)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(4 (2 (1) (3)) (6 (5) (7)))'
        '''
        if raiz == None:
            return No(chave)
        elif chave < raiz.chave:
            raiz.esq = self.__insere_interno(raiz.esq, chave)
        else:
            raiz.dir = self.__insere_interno(raiz.dir, chave)
        raiz.altura = 1+max(self.altura_no(raiz.esq), self.altura_no(raiz.dir))
        balanceamento = self.__balanceamento(raiz)
        if balanceamento > 1:
            if chave < raiz.esq.chave:
                return self.__rotacao_direita(raiz)
            if chave > raiz.esq.chave:
                raiz.esq = self.__rotacao_esquerda(raiz.esq)
                return self.__rotacao_direita(raiz)
        if balanceamento < -1:
            if chave > raiz.dir.chave:
                return self.__rotacao_esquerda(raiz)
            if chave < raiz.dir.chave:
                raiz.dir = self.__rotacao_direita(raiz.dir)
                return self.__rotacao_esquerda(raiz)
        return raiz

    def __remove_interno(self, raiz, chave):
        '''
        Função interna que realiza a remoção de um nó na árvore AVL, efetua também as rotações necessárias para garantir o balanceamento.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.remove(20)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(30 (10))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.remove(30)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(20 (10) (40))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.remove(40)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(20 (10) (50 (30)))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(50)
        >>> arvore.insere(40)
         >>> arvore.remove(20)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(30 (10) (40 (50)))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.insere(30)
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.remove(20)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(40 (30 (10)) (50))'
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(4)
        >>> arvore.insere(5)
        >>> arvore.insere(7)
        >>> arvore.insere(2)
        >>> arvore.insere(1)
        >>> arvore.insere(3)
        >>> arvore.insere(6)
        >>> arvore.remove(6)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(4 (2 (1) (3)) (7 (5)))'
        '''
        if raiz == None:
            return raiz
        if chave < raiz.chave:
            raiz.esq = self.__remove_interno(raiz.esq, chave)
        elif chave > raiz.chave:
            raiz.dir = self.__remove_interno(raiz.dir, chave)
        else:
            if raiz.esq == None:
                aux = raiz.dir
                raiz = None
                return aux
            elif raiz.dir == None:
                aux = raiz.esq
                raiz = None
                return aux
            aux = self.__minimo_interno(raiz.dir)
            raiz.chave = aux.chave
            raiz.dir = self.__remove_interno(raiz.dir, aux.chave)
        if raiz == None:
            return raiz
        raiz.altura = 1+max(self.altura_no(raiz.esq), self.altura_no(raiz.dir))
        balanceamento = self.__balanceamento(raiz)
        if balanceamento > 1:
            if self.__balanceamento(raiz.esq) >= 0:
                return self.__rotacao_direita(raiz)
            if self.__balanceamento(raiz.esq) < 0:
                raiz.esq = self.__rotacao_esquerda(raiz.esq)
                return self.__rotacao_direita(raiz)
        if balanceamento < -1:
            if self.__balanceamento(raiz.dir) <= 0:
                return self.__rotacao_esquerda(raiz)
            if self.__balanceamento(raiz.dir) > 0:
                raiz.dir = self.__rotacao_direita(raiz.dir)
                return self.__rotacao_esquerda(raiz)
        return raiz

    def __rotacao_esquerda(self, no: No) -> No:
        '''
        Realiza a rotação à esquerda de um nó.
        Exemplos presentes na função __insere_interno e __remove_interno.
        '''
        x = no.dir
        y = x.esq
        x.esq = no
        no.dir = y
        no.altura = 1+max(self.altura_no(no.esq), self.altura_no(no.dir))
        x.altura = 1+max(self.altura_no(x.esq), self.altura_no(x.dir))
        return x

    def __rotacao_direita(self, no: No) -> No:
        '''
        Realiza a rotação à direita de um nó.
        Exemplos presentes na função __insere_interno e __remove_interno.
        '''
        x = no.esq
        y = x.dir
        x.dir = no
        no.esq = y
        no.altura = 1+max(self.altura_no(no.esq), self.altura_no(no.dir))
        x.altura = 1+max(self.altura_no(x.esq), self.altura_no(x.dir))
        return x

    def __minimo_interno(self, raiz):
        '''
        Função interna que devolve o nó mais a esquerda da árvore.
        Exemplos presentes na função __insere_interno e __remove_interno.
        '''
        atual = raiz
        while atual.esq:
            atual = atual.esq
        return atual

    def insere(self, chave):
        '''
        Exemplos presentes na função __insere_interno.
        Chama a função interna de inserção.
        '''
        self.raiz = self.__insere_interno(self.raiz, chave)

    def remove(self, chave):
        '''
        Chama a função interna de remoção.
        Exemplos presentes na função e __remove_interno.
        '''
        self.raiz = self.__remove_interno(self.raiz, chave)

    def buscar(self, no: No, elemento: any) -> bool:
        '''
        Devolve o nó contendo o **elemento** se estiver na subárvore 
        enraizada por **no**; caso contrário, devolve None.
        Exemplo:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.buscar(arvore.raiz, 40)
        False
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.buscar(arvore.raiz, 40)
        40
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.buscar(arvore.raiz, 10)
        10
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(50)
        >>> arvore.insere(40)
        >>> arvore.buscar(arvore.raiz, 50)
        50
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.insere(30)
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.buscar(arvore.raiz, 30)
        30
        '''
        if no is None:
            return False
        if no.chave == elemento:
            return no.chave
        if no.chave < elemento:
            return self.buscar(no.dir, elemento)
        return self.buscar(no.esq, elemento)

    def conta_intervalo(self, inicio, fim) -> int:
        '''
        Dada uma AVL e um intervalo [inicio, fim], a função contará o número de nós na árvore que estão
        dentro do intervalo fornecido.
        OBS: Nós presentes tanto no início quanto no fim, serão contabilizados na contagem.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.conta_intervalo(40,50)
        0
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.conta_intervalo(10,30)
        3
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.conta_intervalo(20,50)
        4
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(50)
        >>> arvore.insere(40)
        >>> arvore.conta_intervalo(10,50)
        5
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.insere(30)
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.conta_intervalo(50,100)
        1
        '''
        def __conta_intervalo_interno(no: No | None) -> int:
            if no is None:
                return 0
            if inicio <= no.chave <= fim:
                return 1 + __conta_intervalo_interno(no.esq) + __conta_intervalo_interno(no.dir)
            elif no.chave < inicio:
                return __conta_intervalo_interno(no.dir)
            else:
                return __conta_intervalo_interno(no.esq)
        return __conta_intervalo_interno(self.raiz)
