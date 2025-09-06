# 🎬 Trabalho 1 - Organização e Recuperação de Dados  

Este projeto foi desenvolvido para a disciplina **Organização e Recuperação de Dados** da Universidade Estadual de Maringá, com o objetivo de aplicar conceitos de **manipulação de arquivos binários e gerenciamento de espaços disponíveis (LED)** em Python.  

## 🎯 Objetivo  
Construir um sistema para gerenciar registros de filmes armazenados no arquivo **filmes.dat**, com suporte a busca, inserção, remoção, impressão da LED e compactação.  

## 🔧 Funcionalidades  
- **Execução via linha de comando**:  
  - `-e <arquivo_operacoes>`: executa as operações especificadas em um arquivo de entrada.  
  - `-p`: imprime a Lista de Espaços Disponíveis (LED).  
  - `-c`: compacta o arquivo, removendo fisicamente os espaços livres.  

- **Operações suportadas**:  
  - **Busca** de um filme pelo ID.  
  - **Inserção** de novos filmes.  
  - **Remoção** de filmes (remoção lógica).  
  - **Gerenciamento da LED** com estratégia **Best-Fit**, reaproveitando os espaços disponíveis.  
  - **Compactação** do arquivo para eliminar fragmentação externa.  

## 🛠️ Detalhes técnicos  
- Estrutura de registros com tamanho variável.  
- Arquivo possui cabeçalho de 4 bytes (ponteiro da LED).  
- Campos de tamanho armazenados em 2 bytes.  
- Ponteiros da LED representados por inteiros de 4 bytes.  
- Remoções são lógicas, com manutenção da LED no próprio arquivo.  

## 📂 Exemplo de uso  
Executar operações a partir de um arquivo:  
```bash
python programa.py -e operacoes.txt
python programa.py -p
python programa.py -c
