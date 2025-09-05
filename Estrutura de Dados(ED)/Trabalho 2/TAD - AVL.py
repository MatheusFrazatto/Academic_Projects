# Criação Das Clases
'''
classes que serão usadas para a implementação da AVL.
'''


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

# Operações Básicas -------------------- /
    '''
    Operações comuns a qualquer estrutura de árvore binária de busca, porém adaptadas para manter o balanceamento em uma AVL.
    '''
    # -------------------- /

    def insere(self, chave):
        '''
        Chama a função interna de inserção.
        '''
        self.raiz = self.__insere_interno(self.raiz, chave)

    def __insere_interno(self, raiz, chave):
        '''
        realiza a inserção de um nó na árvore AVL, pode também desencadear rotações (simples ou duplas) para garantir o balanceamento.
        Complexidade: O(logn).
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
        '''
        if raiz == None:
            return No(chave)
        elif chave < raiz.chave:
            raiz.esq = self.__insere_interno(raiz.esq, chave)
        else:
            raiz.dir = self.__insere_interno(raiz.dir, chave)
        raiz.altura = 1+max(self.altura_no(raiz.esq), self.altura_no(raiz.dir))
        balanceamento = self.balanceamento(raiz)
        if balanceamento > 1:
            if chave < raiz.esq.chave:
                return self.rotacao_direita(raiz)
            if chave > raiz.esq.chave:
                raiz.esq = self.rotacao_esquerda(raiz.esq)
                return self.rotacao_direita(raiz)
        if balanceamento < -1:
            if chave > raiz.dir.chave:
                return self.rotacao_esquerda(raiz)
            if chave < raiz.dir.chave:
                raiz.dir = self.rotacao_direita(raiz.dir)
                return self.rotacao_esquerda(raiz)
        return raiz

    def remove(self, chave):
        '''
        Chama a função interna de remoção.
        '''
        self.raiz = self.__remove_interno(self.raiz, chave)

    def __remove_interno(self, raiz, chave):
        '''
        realiza a remoção de um nó na árvore AVL, pode também desencadear rotações (simples ou duplas) para garantir o balanceamento.
        Complexidade: O(logn)
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
            aux = self.minimo(raiz.dir)
            raiz.chave = aux.chave
            raiz.dir = self.__remove_interno(raiz.dir, aux.chave)
        if raiz == None:
            return raiz
        raiz.altura = 1+max(self.altura_no(raiz.esq), self.altura_no(raiz.dir))
        balanceamento = self.balanceamento(raiz)
        if balanceamento > 1:
            if self.balanceamento(raiz.esq) >= 0:
                return self.rotacao_direita(raiz)
            if self.balanceamento(raiz.esq) < 0:
                raiz.esq = self.rotacao_esquerda(raiz.esq)
                return self.rotacao_direita(raiz)
        if balanceamento < -1:
            if self.balanceamento(raiz.dir) <= 0:
                return self.rotacao_esquerda(raiz)
            if self.balanceamento(raiz.dir) > 0:
                raiz.dir = self.rotacao_direita(raiz.dir)
                return self.rotacao_esquerda(raiz)
        return raiz

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

# Operações Auxiliares -------------------- /
    '''
    Operações que auxiliam no gerenciamento e na análise da árvore.
    '''
    # -------------------- /

    def balanceamento(self, no: No | None) -> int:
        '''
        Dado um nó, a função devolve o fator de balanceamento dele.
        FB = altura(SAD) - alturaSAE).
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.balanceamento(arvore.raiz)
        0
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.balanceamento(arvore.raiz)
        -1
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.balanceamento(arvore.raiz)
        -1
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(50)
        >>> arvore.insere(40)
        >>> arvore.balanceamento(arvore.raiz)
        -1
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.insere(30)
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.balanceamento(arvore.raiz)
        1
        '''
        if no == None:
            return 0
        return self.altura_no(no.esq) - self.altura_no(no.dir)

    def altura_no(self, no: No | None) -> int:
        '''
        Dado um nó, a função devolve a altura do nó.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.altura_no(arvore.raiz)
        2
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)   
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.altura_no(arvore.raiz)
        3
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.altura_no(arvore.raiz)
        3
        '''
        if no == None:
            return 0
        return no.altura
    # Rotações -------------------- /

    def rotacao_esquerda(self, no: No) -> No:
        '''
        Realiza a rotação à esquerda de um nó.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.rotacao_esquerda(arvore.raiz).chave
        30
        '''
        x = no.dir
        y = x.esq
        x.esq = no
        no.dir = y
        no.altura = 1+max(self.altura_no(no.esq), self.altura_no(no.dir))
        x.altura = 1+max(self.altura_no(x.esq), self.altura_no(x.dir))
        return x

    def rotacao_direita(self, no: No) -> No:
        '''
        Realiza a rotação à direita de um nó.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(30)
        >>> arvore.insere(20)
        >>> arvore.insere(10)
        >>> arvore.rotacao_direita(arvore.raiz).chave
        10
        '''
        x = no.esq
        y = x.dir
        x.dir = no
        no.esq = y
        no.altura = 1+max(self.altura_no(no.esq), self.altura_no(no.dir))
        x.altura = 1+max(self.altura_no(x.esq), self.altura_no(x.dir))
        return x

    # -------------------- /

    def sucessor(self, no: No) -> No:
        '''
        Devolve o sucessor de um **no**, isto é, o nó com o menor valor
        maior (ou igual) ao valor de no.chave.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.sucessor(arvore.raiz).chave
        30
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.sucessor(arvore.raiz).chave
        30
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.sucessor(arvore.raiz).chave
        30
        '''
        if no.dir != None:
            return self.minimo(no.dir)
        pai = no.pai
        while pai != None and no == pai.dir:
            no = pai
            pai = pai.pai
        return pai


# Operações Adicionais -------------------- /
    '''
    Operações frequentemente implementadas em um TAD AVL para facilitar a manipulação de dados.
    '''
    # -------------------- /
    # Máximo/Mínimo -------------------- /

    def minimo(self, raiz):
        '''
        Função interna que devolve o nó mais a esquerda da árvore.
        OBS: Pode ser usado na função **remove** para agilizar a remoção de um nó.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.minimo(arvore.raiz).chave
        10
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.minimo(arvore.raiz).chave
        10
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.minimo(arvore.raiz).chave
        10
        '''
        if raiz.esq == None:
            return raiz
        return self.minimo(raiz.esq)

    def maximo(self, raiz):
        '''
        Função interna que devolve o nó mais a direita da árvore.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.maximo(arvore.raiz).chave
        30
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.maximo(arvore.raiz).chave
        30
        >>> arvore = ArvoreAVL()
        >>> arvore.insere(10)
        >>> arvore.insere(20)
        >>> arvore.insere(30)
        >>> arvore.insere(40)
        >>> arvore.insere(50)
        >>> arvore.maximo(arvore.raiz).chave
        30
        '''
        if raiz.dir == None:
            return raiz
        return self.minimo(raiz.dir)
    # -------------------- /
    # Percursos -------------------- /

    def exibe_pre_ordem(self, raiz: No | None) -> str:
        '''
        Exibe a representuação parentizada da estrutura em pré-ordem,
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
        >>> arvore = ArvoreAVL()
        >>> for item in [2, 1, 3]:
        ...     arvore.insere(item)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(2 (1) (3))'
        >>> arvore = ArvoreAVL()
        >>> for item in [50, 30, 70, 20, 40, 60, 80, 10, 35, 65]:
        ...     arvore.insere(item)
        >>> arvore.exibe_pre_ordem(arvore.raiz)
        '(50 (30 (20 (10)) (40 (35))) (70 (60 (65)) (80)))'
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

    def exibe_em_ordem(self, raiz: No | None) -> str:
        '''
        Exibe a representuação parentizada da estrutura em-ordem,
        isto é: 
        - uma árvore vazia é representada por vazio;
        - uma árvore não vazia é representada pela representação da 
        subárvore esquerda, seguida do conteúdo do nó **raiz**, seguida
        da representação da subárvore direita, circundados por parênteses.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.exibe_em_ordem(arvore.raiz)
        ''
        >>> for item in [1, 2, 3]:
        ...     arvore.insere(item)
        >>> arvore.exibe_em_ordem(arvore.raiz)
        '((1) 2 (3))'
        >>> arvore = ArvoreAVL()
        >>> for item in [2, 1, 3]:
        ...     arvore.insere(item)
        >>> arvore.exibe_em_ordem(arvore.raiz)
        '((1) 2 (3))'
        >>> arvore = ArvoreAVL()
        >>> for item in [50, 30, 70, 20, 40, 60, 80, 10, 35, 65]:
        ...     arvore.insere(item)
        >>> arvore.exibe_em_ordem(arvore.raiz)
        '((((10) 20) 30 ((35) 40)) 50 ((60 (65)) 70 (80)))'
        '''
        repr = ''
        if raiz != None:
            repr += '('
            if raiz.esq != None:
                repr += str(self.exibe_em_ordem(raiz.esq)) + ' '
            repr += str(raiz.chave)
            if raiz.dir != None:
                repr += ' ' + str(self.exibe_em_ordem(raiz.dir))
            repr += ')'
        return repr

    def exibe_pos_ordem(self, raiz: No | None) -> str:
        '''
        Exibe a representuação parentizada da estrutura pos-ordem,
        isto é: 
        - uma árvore vazia é representada por vazio;
        - uma árvore não vazia é representada pela representação da 
        subárvore esquerda, seguida da representação da subárvore direita,
        seguida do conteúdo do nó **raiz**, circundados por parênteses.
        Exemplos:
        >>> arvore = ArvoreAVL()
        >>> arvore.exibe_pos_ordem(arvore.raiz)
        ''
        >>> for item in [1, 2, 3]:
        ...     arvore.insere(item)
        >>> arvore.exibe_pos_ordem(arvore.raiz)
        '((1) (3) 2)'
        >>> arvore = ArvoreAVL()
        >>> for item in [2, 1, 3]:
        ...     arvore.insere(item)
        >>> arvore.exibe_pos_ordem(arvore.raiz)
        '((1) (3) 2)'
        >>> arvore = ArvoreAVL()
        >>> for item in [50, 30, 70, 20, 40, 60, 80, 10, 35, 65]:
        ...     arvore.insere(item)
        >>> arvore.exibe_pos_ordem(arvore.raiz)
        '((((10) 20) ((35) 40) 30) (((65) 60) (80) 70) 50)'
        '''
        repr = ''
        if raiz != None:
            repr += '('
            if raiz.esq != None:
                repr += str(self.exibe_pos_ordem(raiz.esq)) + ' '
            if raiz.dir != None:
                repr += str(self.exibe_pos_ordem(raiz.dir)) + ' '
            repr += str(raiz.chave) + ')'
        return repr

    # Outras operações: Altura da árvore, quantidade de nós, tamanho da árvore, etc...
