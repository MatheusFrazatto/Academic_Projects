from __future__ import annotations
from typing import Any
from dataclasses import dataclass


class Cliente:
    def __init__(self, idade):
        '''
        Cria um cliente com identificador,idade e um contador:
        - Identificador: Ordem de chegada do cliente(Fornecida pelo próprio código).
        - Idade: Idade do cliente.
        - Contador: indica quantos idosos podem passar na frente de um não idoso (Caso o cliente seja idoso, o contador=0, caso contrário, contador=2).
        '''
        self.identificador = 0
        self.idade = idade
        self.contador = 0

    def __str__(self):
        '''Devolve a representação da classe <Cliente> em formato de string.'''
        return f"{self.identificador} - {self.idade}"


@dataclass
class No:
    '''
    Classe Nó, utilizada para o funcionamento da lista duplamente encadeada.
    '''
    elemento: Any
    anterior: No | None = None
    proximo: No | None = None


class FilaBanco:
    def __init__(self) -> None:
        '''
        Cria uma lista duplamente encadeada vazia.
        '''
        self.__inicio = None
        self.__fim = None

    def vazia(self) -> bool:
        '''
        Verifica se a lista duplamente encadeada está vazia, isto é, devolve True se 
        não possui elementos e False caso contrário.

        Exemplos:
        >>> lista = FilaBanco()
        >>> lista.vazia()
        True
        >>> lista.adiciona_ordena(65)
        >>> lista.vazia()
        False
        '''
        return self.__inicio == None

    def numero_elementos(self) -> int:
        '''
        Devolve a quantidade de elementos(Clientes) que estão na fila(None não são contabilizados).

        Exemplos:
        >>> lista = FilaBanco()
        >>> lista.numero_elementos()
        0
        >>> lista.adiciona_ordena(23)
        >>> lista.numero_elementos()
        1
        >>> lista.adiciona_ordena(34)
        >>> lista.adiciona_ordena(76)
        >>> lista.numero_elementos()
        3
        '''
        if self.vazia():
            return 0
        it = self.__inicio
        contador = 1
        while it != self.__fim:
            contador += 1
            it = it.proximo
        return contador

    def __str__(self) -> str:
        '''Devolve a representação da lista em formato de string.'''
        if self.vazia():
            return '[]'
        it = self.__inicio
        repr = f'[{it.elemento}'
        while it != self.__fim:
            repr += ', '
            it = it.proximo
            repr += f'{it.elemento}'
        repr += ']'
        return repr

    def consulta_primeiro(self) -> Any:
        '''Devolve o conteúdo do primeiro nó da lista duplamente encadeada sem removê-lo.

        Exemplos:
        >>> lista = FilaBanco()
        >>> lista.consulta_primeiro()
        Traceback (most recent call last):
            ...
        ValueError: Lista vazia.
        >>> lista.adiciona_ordena(33)
        >>> lista.adiciona_ordena(45)
        >>> lista.adiciona_ordena(23)
        >>> print(lista)
        [1 - 33, 2 - 45, 3 - 23]
        >>> print(lista.consulta_primeiro())
        1 - 33
        >>> lista.desenfileira()
        >>> print(lista.consulta_primeiro())
        2 - 45
        >>> lista.desenfileira()
        >>> print(lista.consulta_primeiro())
        3 - 23
        '''
        if self.vazia():
            raise ValueError('Lista vazia.')
        return self.__inicio.elemento

    def adiciona_ordena(self, idade: int) -> None:
        '''
        Adiciona um cliente, usando a classe <Cliente>, na fila>:
        1. Se a idade for maior ou igual a 60, o cliente é um idoso. Logo, seu o contador é 0.
        2. Se a idade for menor que 60, o cliente é um não idoso. Logo, seu o contador é 2
        Após adicionar os clientes, Utiliza a <fila_inicial> para organizar a orden e garantir preferências, 
        seguindo as regras de atendimento fornecidas:
        1. As pessoas são atendidas conforme a ordem de chegada.
        2. No máximo duas pessoas idosas podem ser atendidas antes (“passar na frente”) de uma pessoa não idosa.
        Em seguida, imprime a fila em sua nova ordem.

        Exemplos:
        1)
        >>> fila = FilaBanco()
        >>> fila.adiciona_ordena(21)
        >>> fila.adiciona_ordena(34)
        >>> fila.adiciona_ordena(67)
        >>> fila.adiciona_ordena(61)
        >>> fila.adiciona_ordena(72)
        >>> fila.adiciona_ordena(54)
        >>> fila.adiciona_ordena(75)
        >>> print(fila)
        [3 - 67, 4 - 61, 1 - 21, 2 - 34, 5 - 72, 7 - 75, 6 - 54]

        2)
        >>> fila = FilaBanco()
        >>> fila.adiciona_ordena(21)
        >>> fila.adiciona_ordena(34)
        >>> fila.adiciona_ordena(54)
        >>> fila.adiciona_ordena(37)
        >>> fila.adiciona_ordena(18)
        >>> fila.adiciona_ordena(45)
        >>> fila.adiciona_ordena(75)
        >>> print(fila)
        [7 - 75, 1 - 21, 2 - 34, 3 - 54, 4 - 37, 5 - 18, 6 - 45]

        3)
        >>> fila = FilaBanco()
        >>> fila.adiciona_ordena(21)
        >>> fila.adiciona_ordena(34)
        >>> fila.adiciona_ordena(54)
        >>> fila.adiciona_ordena(37)
        >>> fila.adiciona_ordena(18)
        >>> fila.adiciona_ordena(45)
        >>> fila.adiciona_ordena(42)
        >>> print(fila)
        [1 - 21, 2 - 34, 3 - 54, 4 - 37, 5 - 18, 6 - 45, 7 - 42]

        4)
        >>> fila = FilaBanco()
        >>> fila.adiciona_ordena(100)
        >>> fila.adiciona_ordena(72)
        >>> fila.adiciona_ordena(60)
        >>> fila.adiciona_ordena(91)
        >>> fila.adiciona_ordena(87)
        >>> fila.adiciona_ordena(64)
        >>> fila.adiciona_ordena(75)
        >>> print(fila)
        [1 - 100, 2 - 72, 3 - 60, 4 - 91, 5 - 87, 6 - 64, 7 - 75]

        '''
        cliente = Cliente(idade)
        cliente.identificador = self.numero_elementos() + 1
        if idade < 60:
            cliente.contador = 2
        novo = No(cliente)

        if self.vazia():
            self.__inicio = novo
            self.__fim = novo
        else:
            if cliente.idade >= 60:
                posicao = self.__fim
                while posicao is not None and posicao.elemento.contador > 0:
                    posicao.elemento.contador -= 1
                    posicao = posicao.anterior
                if posicao is None:
                    novo.proximo = self.__inicio
                    self.__inicio.anterior = novo
                    self.__inicio = novo
                else:
                    novo.anterior = posicao
                    novo.proximo = posicao.proximo
                    if posicao.proximo is not None:
                        posicao.proximo.anterior = novo
                    posicao.proximo = novo
                    if posicao == self.__fim:
                        self.__fim = novo
            else:
                novo.anterior = self.__fim
                self.__fim.proximo = novo
                self.__fim = novo

    def desenfileira(self) -> None:
        '''
        Remove o nó que está no início da lista.
        >>> lista = FilaBanco()
        >>> for i in range(3):
        ...     lista.adiciona_ordena(i * 10)
        >>> print(lista)
        [1 - 0, 2 - 10, 3 - 20]
        >>> lista.desenfileira()
        >>> print(lista)
        [2 - 10, 3 - 20]
        >>> lista.desenfileira()
        >>> print(lista)
        [3 - 20]
        >>> lista.desenfileira()
        >>> print(lista)
        []
        >>> lista.desenfileira()
        Traceback (most recent call last):
            ...
        ValueError: Lista vazia.
        '''
        if self.vazia():
            raise ValueError('Lista vazia.')
        if self.numero_elementos() == 1:
            self.__inicio = None
            self.__fim = None
        else:
            self.__inicio = self.__inicio.proximo
            self.__inicio.anterior = None
