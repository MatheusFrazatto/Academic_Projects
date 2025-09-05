from dataclasses import dataclass
from enum import Enum
import sys
sys.setrecursionlimit(10**4)

# Tipos Compostos/Enumerados ----------/


class Medalhas_Tipo(Enum):
    OURO = 1
    PRATA = 2
    BRONZE = 3


class Genero_Tipo(Enum):
    # M= masculino, W= feminino, X= misto e O= Juntos.
    M = 1
    W = 2
    X = 3
    O = 4


@dataclass
class Atleta:
    MEDALHA: Medalhas_Tipo
    PAÍS: str
    GENERO: Genero_Tipo


@dataclass
class País:
    NOME: str
    OURO: int
    PRATA: int
    BRONZE: int
    TOTAL: int


# Função Main ----------/


def main():
    if len(sys.argv) < 2:
        print('Nenhum nome de arquivo informado.')
        sys.exit(1)

    if len(sys.argv) > 2:
        print('Muitos parâmetro. Informe apenas um nome de arquivo.')
        sys.exit(1)

    tabela = le_arquivo(sys.argv[1])
    # Lista Usadas ----------/
    matriz_atleta = atribui_dados(tabela)
    lista_paises = todos_paises(matriz_atleta)
    # ----------/
    # TODO: computar e exibir o quadro de medalhas.
    contador_medalha(matriz_atleta, lista_paises, tabela)
    # TODO: computar e exibir os países que tiverem apenas atletas de um único gênero premiados.)
    matriz_atleta = remove_xo(matriz_atleta)
    paises_MW(matriz_atleta, lista_paises)
# Leitor De Arquivo ----------/


def le_arquivo(nome: str) -> list[list[str]]:
    '''
    Lê o conteúdo do arquivo <nome> e devolve uma lista onde cada elemento é
    uma lista com os valores das colunas de uma linha (valores separados por
    vírgula). A primeira linha do arquivo, que deve conter o nome das
    colunas, é descartado.
    '''
    try:
        with open(nome) as f:
            tabela = []
            linhas = f.readlines()
            for i in range(1, len(linhas)):
                tabela.append(linhas[i].split(','))
            return tabela
    except IOError as e:
        print(f'Erro na leitura do arquivo "{
              nome}": {e.errno} - {e.strerror}.')
        sys.exit(1)


# Função Atribui Dados ----------/


def atribui_dados(tabela: list[list[str]]) -> list[list[Atleta]]:
    '''Atribui os valores ao Dado Composto(@dataclass) Atleta, e depois adiciona o Dados Composto(Atleta) a uma lista de lista.'''
    matriz_atleta = []
    for lista in tabela:
        if lista[0] == "Gold Medal":
            Medalhas = Medalhas_Tipo.OURO.value
        elif lista[0] == "Silver Medal":
            Medalhas = Medalhas_Tipo.PRATA.value
        elif lista[0] == "Bronze Medal":
            Medalhas = Medalhas_Tipo.BRONZE.value
        # ----------/
        País = lista[10]
        if len(País) > 3:
            País = lista[11]
        # ----------/
        if lista[4] == "M":
            Gênero = Genero_Tipo.M.value
        elif lista[4] == "W":
            Gênero = Genero_Tipo.W.value
        elif lista[4] == "X":
            Gênero = Genero_Tipo.X.value
        elif lista[4] == "O":
            Gênero = Genero_Tipo.O.value
        # Append - Lista de Lista ----------/
        matriz_atleta.append([Atleta(Medalhas, País, Gênero)])
        # ----------/
    return matriz_atleta


# Função Todos Países ----------/


def todos_paises(matriz_atleta: list[list[Atleta]]) -> list:
    '''retorna todos os países presentes na lista matriz_atleta, sem repetições daqueles que já estão na lista_paises.
    Exemplo:
    >>> todos_paises([[Atleta(1, 'USA', 1), Atleta(1, 'USA', 1)], [Atleta(1, 'BRA', 1), Atleta(1, 'BRA', 1)]])
    ['USA', 'BRA']
    '''
    lista_paises = []
    for linha in matriz_atleta:
        for elemento in linha:
            pais = elemento.PAÍS
            if pais not in lista_paises:
                lista_paises.append(pais)
    return lista_paises


# Função Todos Países ----------/


def contador_medalha(matriz_atleta: list[list[Atleta]], lista_paises: list, tabela: list) -> list[País]:
    '''retorna uma lista de País com os dados de medalhas de cada país, usando a lista_paises. Alem disso, para não criar muitas listas desnecessárias, o código esvazia a lista <tabela> para o 
    armazenamento dos dados
    Exemplo:
    >>> contador_medalha([[Atleta(MEDALHA=1, PAÍS='USA', GENERO=1), Atleta(MEDALHA=1, PAÍS='USA', GENERO=1)], [Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1), Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1)]], ['USA', 'BRA'], [1,1,1,1,1,1,1,1,1,])
    País  Ouro  Prata  Bronze  Total
    USA   2     0      0       2  
    BRA   2     0      0       2  
    '''
    # ----------/
    while tabela:
        tamanho = len(tabela) - 1
        tabela = tabela[:tamanho]
    # ----------/
    for pais in lista_paises:
        if len(pais) <= 3:
            pais_obj = País(pais, 0, 0, 0, 0)
            for elemento in matriz_atleta:
                for atleta in elemento:
                    if atleta.PAÍS == pais:
                        if atleta.MEDALHA == Medalhas_Tipo.OURO.value:
                            pais_obj.OURO += 1
                        elif atleta.MEDALHA == Medalhas_Tipo.PRATA.value:
                            pais_obj.PRATA += 1
                        elif atleta.MEDALHA == Medalhas_Tipo.BRONZE.value:
                            pais_obj.BRONZE += 1
                        pais_obj.TOTAL += 1
            if pais_obj is not None:
                tabela.append(pais_obj)
    # ----------/
    selectionsort(tabela)


# Função Selection Sort ----------/


def selectionsort(tabela: list[País]) -> list[País]:
    '''Ordena a lista de País de acordo com a quantidade de medalhas de ouro. Caso haja empate, a quantidade de medalhas de prata é considerada, e se necessário, a quantidade de medalhas de bronze
    é considerada.
    Função Baseada no Selection Sort fornecido.
    Exemplo:
    >>> selectionsort([País('USA', 1, 2, 3, 6), País('BRA', 2, 1, 3, 6)])
    País  Ouro  Prata  Bronze  Total
    BRA   2     1      3       6  
    USA   1     2      3       6  
    [País(NOME='BRA', OURO=2, PRATA=1, BRONZE=3, TOTAL=6), País(NOME='USA', OURO=1, PRATA=2, BRONZE=3, TOTAL=6)]
    '''
    n: int = len(tabela)
    for i in range(n):
        maximo: int = i
        for j in range(i + 1, n):
            if tabela[j].OURO > tabela[maximo].OURO:
                maximo = j
            elif tabela[j].OURO == tabela[maximo].OURO:
                if tabela[j].PRATA > tabela[maximo].PRATA:
                    maximo = j
                elif tabela[j].PRATA == tabela[maximo].PRATA:
                    if tabela[j].BRONZE > tabela[maximo].BRONZE:
                        maximo = j
        tabela[i], tabela[maximo] = tabela[maximo], tabela[i]
    # ----------/
    quadro_medalhas(tabela)
    # ----------/
    return tabela


# Função Quadro Medalhas ----------/


def quadro_medalhas(tabela: list[País],) -> str:
    '''Imprime o quadro de medalhas usando os dados inserido dentro da tabela, e arruma os espaços para que o print saia de maneira correta.
    Exemplo:
    >>> quadro_medalhas([País('USA', 1, 2, 3, 6), País('BRA', 2, 1, 3, 6)])
    País  Ouro  Prata  Bronze  Total
    USA   1     2      3       6  
    BRA   2     1      3       6  
    '''
    print("País  Ouro  Prata  Bronze  Total")
    for pais in tabela:
        nome = pais.NOME + " " * (6 - len(pais.NOME))
        ouro = str(pais.OURO) + " " * (6 - len(str(pais.OURO)))
        prata = str(pais.PRATA) + " " * (7 - len(str(pais.PRATA)))
        bronze = str(pais.BRONZE) + " " * (8 - len(str(pais.BRONZE)))
        total = str(pais.TOTAL) + " " * (3 - len(str(pais.TOTAL)))
        print(nome + ouro + prata + bronze + total)


# Função Recursiva 1 (remove_xp) ----------/


def remove_xo(matriz_atleta: list[list[Atleta]], index: int = 0, paises_com_genero=None) -> list[list[Atleta]]:
    '''Remove todas as aparições de países na lista <matriz_atleta> se o país tiver medalhistas de mais de um gênero(Usando a função <remove_pais> para remover o pais da lista).
    Exemplo:
    >>> remove_xo([[Atleta(1, 'USA', 1), Atleta(1, 'USA', 1)], [Atleta(1, 'BRA', 1), Atleta(1, 'BRA', 1)]])
    [[Atleta(MEDALHA=1, PAÍS='USA', GENERO=1), Atleta(MEDALHA=1, PAÍS='USA', GENERO=1)], [Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1), Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1)]]
    '''
    if paises_com_genero is None:
        paises_com_genero = {}

    if index == len(matriz_atleta):
        return remove_pais(matriz_atleta, paises_com_genero)

    atleta = matriz_atleta[index][0]
    pais = atleta.PAÍS
    genero = atleta.GENERO

    if genero not in {Genero_Tipo.X.value, Genero_Tipo.O.value}:
        if pais not in paises_com_genero:
            paises_com_genero[pais] = set()
        paises_com_genero[pais].add(genero)

    return remove_xo(matriz_atleta, index + 1, paises_com_genero)


# Função Recursiva 2 (remove_pais) ----------/


def remove_pais(matriz_atleta: list[list[Atleta]], paises_com_genero: dict, index: int = 0) -> list[list[Atleta]]:
    '''É chamada para realizar a remoção dos paises encontrados na <remove_xo>:
    >>> remove_pais([[Atleta(MEDALHA=1, PAÍS='USA', GENERO=1), Atleta(MEDALHA=1, PAÍS='USA', GENERO=1)], [Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1), Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1)]], {'USA': {1}, 'BRA': {1}})
    [[Atleta(MEDALHA=1, PAÍS='USA', GENERO=1), Atleta(MEDALHA=1, PAÍS='USA', GENERO=1)], [Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1), Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1)]]
    '''
    if index == len(matriz_atleta):
        return matriz_atleta

    atleta = matriz_atleta[index][0]
    pais = atleta.PAÍS

    if pais in paises_com_genero and len(paises_com_genero[pais]) > 1:
        matriz_atleta.pop(index)
        return remove_pais(matriz_atleta, paises_com_genero, index)

    return remove_pais(matriz_atleta, paises_com_genero, index + 1)


# Função Países MW ----------/


def paises_MW(matriz_atleta: list[list[Atleta]], lista_paises: list) -> str:
    '''Garante que as os resultados das funções recursivas sejam impressos na tela sem repetições de países.
    Exemplo:
    >>> paises_MW([[Atleta(MEDALHA=1, PAÍS='USA', GENERO=1), Atleta(MEDALHA=1, PAÍS='USA', GENERO=1)], [Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1), Atleta(MEDALHA=1, PAÍS='BRA', GENERO=1)]], ['USA', 'BRA'])
    <BLANKLINE>
    Países Com Medalhistas De Um Único Gênero(M ou W):
    USA
    BRA
    '''
    print("\nPaíses Com Medalhistas De Um Único Gênero(M ou W):")
    for pais in lista_paises:
        achou = False
        for i in matriz_atleta:
            for j in i:
                if not achou and j.PAÍS == pais:
                    print(pais)
                    achou = True


if __name__ == '__main__':
    main()
