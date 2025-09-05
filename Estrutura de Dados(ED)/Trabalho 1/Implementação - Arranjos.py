from Arranjo import Array


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


class FilaBanco:
    def __init__(self, capacidade: int):
        '''
        Cria uma fila de banco utilizando um arranjo estático, contém os seguintes atributos:

        OBS: A Fila contém apenas <capacidade> posições, ou seja, só é possível adicionar <capacidade> clientes na fila
        '''
        if capacidade <= 0:
            raise ValueError("Capacidade deve ser maior que zero")
        self.__fila = Array(capacidade+1)
        self.__inicio = 0
        self.__fim = 0

    def vazia(self) -> bool:
        '''
        Informa se há elementos na fila, isto é, devolve True se a fila está vazia e False caso contrário.

        Exemplos:
        >>> fila = FilaBanco(5)
        >>> fila.vazia()
        True
        >>> fila.adiciona_ordena(10)
        >>> fila.vazia()
        False
        >>> fila.desenfileira()
        >>> fila.vazia()
        True
        '''
        return self.__inicio == self.__fim

    def cheia(self) -> bool:
        '''
        Informa se a quantidade de elementos na fila alcançou seu limite. Devolve True se a fila está cheia e
        False caso contrário.

        Exemplos:
        >>> fila = FilaBanco(2)
        >>> fila.adiciona_ordena(10)
        >>> fila.cheia()
        False
        >>> fila.adiciona_ordena(20)
        >>> fila.cheia()
        True
        '''
        return (self.__fim + 1) % len(self.__fila) == self.__inicio

    def desenfileira(self) -> None:
        '''
        Remove/Desenfileira o primeiro elemento(Cliente) da fila.

        Exemplo:
        >>> fila = FilaBanco(3)
        >>> fila.adiciona_ordena(10)
        >>> fila.adiciona_ordena(20)
        >>> fila.desenfileira()
        >>> print(fila)
        [2 - 20]
        '''
        if self.vazia():
            raise ValueError("Fila vazia")
        self.__inicio = (self.__inicio + 1) % len(self.__fila)

    def primeiro(self) -> Cliente:
        '''
        Devolve o primeiro elemento(Cliente) da fila sem removê-lo.

        Exemplo:
        >>> fila = FilaBanco(3)
        >>> fila.adiciona_ordena(10)
        >>> fila.adiciona_ordena(20)
        >>> print(fila.primeiro())
        1 - 10
        '''
        if self.vazia():
            raise ValueError("Fila vazia")
        return self.__fila[self.__inicio]

    def numero_elementos(self) -> int:
        '''
        Devolve a quantidade de elementos(Clientes) que estão na fila(None não são contabilizados).

        Exemplo:
        >>> fila = FilaBanco(3)
        >>> fila.numero_elementos()
        0
        >>> fila.adiciona_ordena(10)
        >>> fila.adiciona_ordena(20)
        >>> fila.numero_elementos()
        2
        >>> fila.desenfileira()
        >>> fila.numero_elementos()
        1
        '''
        return (len(self.__fila) - self.__inicio + self.__fim) % len(self.__fila)

    def esvazia(self) -> None:
        '''
        Esvazia a fila.

        Exemplo:
        >>> fila = FilaBanco(3)
        >>> fila.adiciona_ordena(10)
        >>> fila.adiciona_ordena(20)
        >>> fila.numero_elementos()
        2
        >>> fila.esvazia()
        >>> fila.numero_elementos()
        0
        '''
        self.__inicio = 0
        self.__fim = 0

    def __str__(self) -> str:
        '''
        Exibe todos os elementos que estão na fila em formato string.

        Exemplo:
        >>> fila = FilaBanco(3)
        >>> fila.adiciona_ordena(10)
        >>> fila.adiciona_ordena(20)
        >>> print(fila)
        [1 - 10, 2 - 20]
        '''
        if self.vazia():
            return "[]"
        else:
            repr = f"[{self.primeiro()}"
            for i in range(1, self.numero_elementos()):
                repr += f", {self.__fila[(self.__inicio + i) %
                                         len(self.__fila)]}"
            repr += "]"
            return repr

    def adiciona_ordena(self, idade: int) -> None:
        '''
        Adiciona um cliente, usando a classe <Cliente>, na <fila>:
        1. Se a idade for maior ou igual a 60, o cliente é um idoso. Logo, seu o contador é 0.
        2. Se a idade for menor que 60, o cliente é um não idoso. Logo, seu o contador é 2

        Após adicionar os clientes, Utiliza a <fila> para organizar a ordem e garantir preferências, 
        seguindo as regras de atendimento fornecidas:
        1. As pessoas são atendidas conforme a ordem de chegada.
        2. No máximo duas pessoas idosas podem ser atendidas antes (“passar na frente”) de uma pessoa não idosa.

        Em seguida, imprime a fila em sua nova ordem.

        Exemplos:
        1)
        >>> fila = FilaBanco(10)
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
        >>> fila = FilaBanco(10)
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
        >>> fila = FilaBanco(10)
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
        >>> fila = FilaBanco(10)
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
        if self.cheia():
            raise ValueError("Fila cheia")
        else:
            cliente = Cliente(idade)
            cliente.identificador = self.numero_elementos() + 1
            if idade < 60:
                cliente.contador = 2

        if cliente.idade >= 60:
            posicao = self.__fim
            while posicao != self.__inicio and self.__fila[(posicao - 1) % len(self.__fila)].contador > 0:
                self.__fila[posicao] = self.__fila[(
                    posicao - 1) % len(self.__fila)]
                self.__fila[(posicao - 1) % len(self.__fila)].contador -= 1
                posicao = (posicao - 1) % len(self.__fila)
            self.__fila[posicao] = cliente
        else:
            self.__fila[self.__fim] = cliente
        self.__fim = (self.__fim + 1) % len(self.__fila)

fila = FilaBanco()
fila.adiciona_ordena(67)
fila.adiciona_ordena(56)
fila.adiciona_ordena(67)
fila.adiciona_ordena(78)
fila.adiciona_ordena(45)
fila.adiciona_ordena(76)
fila.adiciona_ordena(67)
print(fila)