from __future__ import annotations


class Array:
    def __init__(self, tamanho: int, valor_preenchimento=None) -> None:
        ''' 
        Cria um arranjo com quantidade de elementos igual a <tamanho>
        (inteiro maior ou igual a zero) e preenchido com 
        <valor_preenchimento> em cada posição.  

        Exemplos:
        >>> a = Array(5)
        >>> print(a)
        [None, None, None, None, None]
        '''
        self.__itens = []
        for _ in range(tamanho):
            self.__itens.append(valor_preenchimento)

    def __len__(self) -> int:
        '''
        Devolve a quantidade de elementos contidos no arranjo.

        Exemplos:
        >>> a = Array(10)
        >>> a.__len__()
        10
        >>> a = Array(2, 'a')
        >>> a.__len__()
        2
        '''
        return len(self.__itens)

    def __iter__(self):
        '''
        Método que permite iterar sobre os objetos.
        '''
        return iter(self.__itens)

    def __getitem__(self, indice: int):
        '''
        Devolve valores contidos em posições indexadas no arranjo.

        Exemplos:
        >>> a = Array(5, -1)
        >>> a[2]
        -1
        >>> a[2] = 10
        >>> a[2]
        10
        '''
        return self.__itens[indice]

    def __setitem__(self, indice: int, valor) -> None:
        '''
        Atribui uma referência a **valor** à posição definida
        por **indice** no arranjo.

        Exemplos:
        >>> a = Array(5, -1)
        >>> a[2] = 10
        >>> a[2]
        10
        '''
        self.__itens[indice] = valor

    def __str__(self):
        '''
        Devolve a representação do arranjo em formato de string.
        '''
        return str(self.__itens)
