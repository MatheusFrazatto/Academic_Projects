from enum import Enum, auto
from dataclasses import dataclass


# ----------/


class Tipo_Usuario(Enum):
    ALUNO = auto()
    SERVIDOR_ATE_3 = auto()
    SERVIDOR_MAIS_3 = auto()
    DOCENTE = auto()
    EXTERNO = auto()


class Forma_Pagamento(Enum):
    DINHEIRO = auto()
    CARTAO = auto()
    PIX = auto()


@dataclass
class Dados_Vendas:
    TIPO_USUARIO: Tipo_Usuario
    QUANTIDADE_TIQUETES: int
    FORMA_PAGAMENTO: Forma_Pagamento
    PRECO_TOTAL: int

# ----------/


# Função registrar_venda ----------/


def registrar_venda(lista_registro: list):
    # Registra as vendas por meio de inputs, alem disso usa tipos enumerados para garantir valores singulares das variáveis usadas, e calcula o valor final da compra, mostrando todos os dados necessários, dados esses que são enviados pra função <append.lista>.
    # Menu 1 ----------/
    print("\n|Tipos de Usuários: |")
    print("|[1]-> Aluno        |")
    print("|[2]-> Servidor<=3  |")
    print("|[3]-> Servidor>3   |")
    print("|[4]-> Docente      |")
    print("|[5]-> Externa      |")
    # ----------/
    tipo_usuario = int(input("-> "))
    if tipo_usuario == 1:
        valor_tiquete = 5
        usuario = Tipo_Usuario.ALUNO
    elif tipo_usuario == 2:
        valor_tiquete = 5
        usuario = Tipo_Usuario.SERVIDOR_ATE_3
    elif tipo_usuario == 3:
        valor_tiquete = 10
        usuario = Tipo_Usuario.SERVIDOR_MAIS_3
    elif tipo_usuario == 4:
        valor_tiquete = 10
        usuario = Tipo_Usuario.DOCENTE
    elif tipo_usuario == 5:
        valor_tiquete = 19
        usuario = Tipo_Usuario.EXTERNO
    else:
        print("***Essa opção não Existe.***")
        return
    # ----------/
    quantidade_tiquetes = int(input("Quantidade de Tíquetes: "))
    preco_total = valor_tiquete*quantidade_tiquetes
    # Menu 2 ----------/
    print("\n|Forma De Pagamento:|")
    print("|[1]-> Dinheiro     |")
    print("|[2]-> Cartão       |")
    print("|[3]-> PIX          |")
    # ----------/
    forma_pagamento = int(input("-> "))
    if forma_pagamento == 1:
        pagamento = Forma_Pagamento.DINHEIRO
    elif forma_pagamento == 2:
        pagamento = Forma_Pagamento.CARTAO
    elif forma_pagamento == 3:
        pagamento = Forma_Pagamento.PIX
    else:
        print("***Essa opção não Existe.***")
        return
    # Menu 3 ----------/
    print("\n|-->->--Finalização--<-<--")
    print("|Usuário:", usuario.name)
    print("|Tiquetes:", quantidade_tiquetes)
    print("|Pagamento:", pagamento.name)
    print("|>>Total: R$", preco_total, "<<")
    # Menu 4 ----------/
    print("\n|Finalizar Venda? |")
    print("|[1]->Sim         |")
    print("|[2]->Não         |")
    # ----------/
    finalizar = int(input("-> "))
    if finalizar == 1:
        append_lista(lista_registro, usuario,
                     quantidade_tiquetes, pagamento, preco_total)
        print("<<Venda Registrada!>>\n")
    elif finalizar == 2:
        print("<<Venda Cancelada!>>\n")
        return


# Função append_lista ----------/


def append_lista(lista_registro: list[Dados_Vendas], usuario: Tipo_Usuario, quantidade_tiquetes: int, pagamento: Forma_Pagamento, preco_total: int) -> list:
    '''Coleta os valores da função <registra_venda> e, atribui os dados a um tipo composto, que por fim, adiciona o dado composto a <lista_registro>, para o funcionamento da função <relatorio_vendas>.
    Exemplos:
    >>> append_lista([], Tipo_Usuario.ALUNO, 1, Forma_Pagamento.DINHEIRO, 5)
    [Dados_Vendas(TIPO_USUARIO=<Tipo_Usuario.ALUNO: 1>, QUANTIDADE_TIQUETES=1, FORMA_PAGAMENTO=<Forma_Pagamento.DINHEIRO: 1>, PRECO_TOTAL=5)]
    >>> append_lista([], Tipo_Usuario.EXTERNO, 2, Forma_Pagamento.PIX, 38)
    [Dados_Vendas(TIPO_USUARIO=<Tipo_Usuario.EXTERNO: 5>, QUANTIDADE_TIQUETES=2, FORMA_PAGAMENTO=<Forma_Pagamento.PIX: 3>, PRECO_TOTAL=38)]
    '''
    dados_vendas = Dados_Vendas(
        usuario, quantidade_tiquetes, pagamento, preco_total)
    lista_registro.append(dados_vendas)
    return lista_registro


# Função registro_vendas ----------/


def relatorio_vendas(lista_registro: list[Dados_Vendas]):
    # Realiza diversos cálculos relacionados a <lista_registro> como(mas não apenas), total de usuários e total de pagamentos. Dados esses que futuramente serão usados nas funções <grafico_horizontal> e <grafico_vertical>.
    total_tiquetes = 0
    receita_total = 0
    for vendas in lista_registro:
        total_tiquetes += vendas.QUANTIDADE_TIQUETES
        receita_total += vendas.PRECO_TOTAL
    # Resumo Das Vendas/Menu ----------/
    print("\n|-->->--Resumo Das Vendas Do Dia--<-<--")
    print("|Total De Tíquetes Vendidos:")
    print("|>>", total_tiquetes, "<<")
    print("|Receita Gerada:")
    print("|>>R$", receita_total, "<<\n")
    # ----------/
    total_usuarios = 0
    total_aluno = 0
    total_servidor_ate_3 = 0
    total_servidor_mais_3 = 0
    total_docente = 0
    total_externa = 0
    for user in lista_registro:
        if user.TIPO_USUARIO == Tipo_Usuario.ALUNO:
            total_aluno += 1
        elif user.TIPO_USUARIO == Tipo_Usuario.SERVIDOR_ATE_3:
            total_servidor_ate_3 += 1
        elif user.TIPO_USUARIO == Tipo_Usuario.SERVIDOR_MAIS_3:
            total_servidor_mais_3 += 1
        elif user.TIPO_USUARIO == Tipo_Usuario.DOCENTE:
            total_docente += 1
        elif user.TIPO_USUARIO == Tipo_Usuario.EXTERNO:
            total_externa += 1
    total_usuarios = total_aluno+total_servidor_ate_3 + \
        total_servidor_mais_3+total_docente+total_externa
    # ----------/
    total_pagamento = 0
    total_dinheiro = 0
    total_cartao = 0
    total_pix = 0
    for pag in lista_registro:
        if pag.FORMA_PAGAMENTO == Forma_Pagamento.DINHEIRO:
            total_dinheiro += 1
        elif pag.FORMA_PAGAMENTO == Forma_Pagamento.CARTAO:
            total_cartao += 1
        elif pag.FORMA_PAGAMENTO == Forma_Pagamento.PIX:
            total_pix += 1
    total_pagamento = total_dinheiro+total_cartao+total_pix
    grafico_horizontal(total_usuarios, total_aluno, total_servidor_ate_3,
                       total_servidor_mais_3, total_docente, total_externa)
    grafico_vertical(total_pagamento, total_dinheiro, total_cartao, total_pix)
    return


# Função grafico_vertical ----------/


def grafico_horizontal(total_usuarios: int, total_aluno: int, total_servidor_ate_3: int, total_servidor_mais_3: int, total_docente: int, total_externa: int):
    '''Gera um gráfico horizontal usando a quantidade total de usuários para realizar o cálculo de porcentagem de cada tipo de usuário disponível, e por fim montar o gráfico usando caracteres ascii.
    Exemplos:
    >>> grafico_horizontal(5, 1, 1, 1, 1, 1)
    Aluno     | [====                ] 20%
    Servidor<3| [====                ] 20%
    Servidor>3| [====                ] 20%
    Docente   | [====                ] 20%
    Externa   | [====                ] 20%
    <BLANKLINE>
    '''
    if total_usuarios > 0:
        AL: int = round((total_aluno / total_usuarios) * 100)
        SME: int = round((total_servidor_ate_3 / total_usuarios) * 100)
        SMA: int = round((total_servidor_mais_3 / total_usuarios) * 100)
        DO: int = round((total_docente / total_usuarios) * 100)
        EX: int = round((total_externa / total_usuarios) * 100)

        def grafico_horizontal_interno(nome, porcentagem):
            quantidade_iguais = "=" * (porcentagem // 5)
            print(f"{nome:<10}| [{quantidade_iguais:<20}] {porcentagem}%")
        grafico_horizontal_interno("Aluno", AL)
        grafico_horizontal_interno("Servidor<3", SME)
        grafico_horizontal_interno("Servidor>3", SMA)
        grafico_horizontal_interno("Docente", DO)
        grafico_horizontal_interno("Externa", EX)
        print("")
    else:
        print("Não há dados suficientes para a produção do gráfico.\n")


# Função grafico_vertical ----------/


def grafico_vertical(total_pagamento: int, total_dinheiro: int, total_cartao: int, total_pix: int):
    '''Gera um gráfico vertical usando a quantidade total de pagamentos para realizar o cálculo de porcentagem de cada tipo de pagamento disponível, e por fim montar o gráfico usando blocos do Unicode.
    Exemplos:
    >>> grafico_vertical(1, 1, 0, 0)
    Dinheiro: 100%, Cartão: 0%, PIX: 0%
    10|  ███        
     9|  ███        
     8|  ███        
     7|  ███        
     6|  ███        
     5|  ███        
     4|  ███        
     3|  ███        
     2|  ███        
     1|  ███        
    ----------------->
         DIN CAR PIX
    '''
    if total_pagamento > 0:
        DI: int = round((total_dinheiro / total_pagamento) * 100)
        CA: int = round((total_cartao / total_pagamento) * 100)
        PI: int = round((total_pix / total_pagamento) * 100)
        total_percent = DI + CA + PI
        while total_percent != 100:
            if total_percent > 100:
                if DI >= CA and DI >= PI and DI > 0:
                    DI -= 1
                elif CA >= DI and CA >= PI and CA > 0:
                    CA -= 1
                elif PI > 0:
                    PI -= 1
            else:
                if DI <= CA and DI <= PI:
                    DI += 1
                elif CA <= DI and CA <= PI:
                    CA += 1
                else:
                    PI += 1
            total_percent = DI + CA + PI

        def grafico_vertical_interno():
            print(f"Dinheiro: {DI}%, Cartão: {CA}%, PIX: {PI}%")
            for i in range(10, 0, -1):
                linha = " "
                linha += 3*"\u2588" if DI >= i * 10 else "   "
                linha += " "
                linha += 3*"\u2588" if CA >= i * 10 else "   "
                linha += " "
                linha += 3*"\u2588" if PI >= i * 10 else "   "
                print(f"{i:2}| {linha}")
            print("----------------->")
            print("     DIN CAR PIX")
        grafico_vertical_interno()
    else:
        print("Não há dados suficientes para a produção do gráfico.")


# Função MAIN ----------/


def main():
    # Recebe o Input do Usuário(Sair ,Venda ou Relatório) e chama a função correspondente com a resposta(0 -> para o loop, 1 -> registrar_venda , 2 -> relatorio_vendas)para a continuidade do código.
    lista_registro: list[Dados_Vendas] = []
    sair = True
    while sair == True:
        # Menu ----------/
        print("\n|Deseja realizar uma <Venda> ou exibir um <Relatório>?|")
        print("|[0]-> Sair                                           |")
        print("|[1]-> Venda                                          |")
        print("|[2]-> Relatório                                      |")
        # ----------/
        venda_ou_exibir = int(input("-> "))
        if venda_ou_exibir == 1:
            registrar_venda(lista_registro)
        elif venda_ou_exibir == 2:
            relatorio_vendas(lista_registro)
        elif venda_ou_exibir == 0:
            print("<Código Fechado Com Sucesso!>")
            sair = False
        else:
            return print("***Essa opção não Existe.***")


if __name__ == "__main__":
    main()
