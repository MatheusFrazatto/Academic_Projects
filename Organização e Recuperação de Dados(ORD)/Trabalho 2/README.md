# 🔑 Trabalho 2 - Hashing Extensível  

Este projeto foi desenvolvido para a disciplina **Organização e Recuperação de Dados** da Universidade Estadual de Maringá, com o objetivo de implementar um sistema de **hashing extensível** para armazenamento e gerenciamento de chaves numéricas.  

## 🎯 Objetivo  
Construir um programa em Python que utilize **hashing extensível(utilizando PED)**, armazenando os dados em arquivos binários (`diretorio.dat` e `buckets.dat`) e oferecendo operações de manipulação e diagnóstico da estrutura.  

## 🔧 Funcionalidades  
- **Execução de operações (-e)** a partir de um arquivo de entrada:  
  - `i <chave>` → insere uma chave (sem duplicatas).  
  - `b <chave>` → busca por uma chave, informando se foi encontrada e em qual bucket está.  
  - `r <chave>` → remove uma chave do hashing.  

- **Impressão do diretório (-pd)**:  
  - Mostra todas as células do diretório.  
  - Exibe informações adicionais: profundidade global, tamanho atual e número total de buckets ativos.  

- **Impressão dos buckets (-pb)**:  
  - Exibe o conteúdo de todos os buckets ativos no arquivo `buckets.dat`.  
  - Buckets removidos logicamente aparecem como **"Removido"**.  

## 🛠️ Detalhes técnicos  
- Estrutura baseada em **dois arquivos binários**:  
  - `diretorio.dat` → armazena o diretório.  
  - `buckets.dat` → armazena os buckets com tamanho fixo de chaves.  
- O tamanho máximo de chaves por bucket (`TAM_MAX_BUCKET`) é configurável no código.  
- Diretório carregado em memória durante a execução e persistido ao final.  
- Suporte a concatenação de buckets amigos em remoções (buckets inativos são mantidos como fragmentação externa).  

## 📂 Exemplos de uso  
Executar operações:  
```bash
python programa.py -e operacoes.txt
python programa.py -pd
python programa.py -pb

