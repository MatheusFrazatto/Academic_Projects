# 🏅 Trabalho 2 / FA - Levantamento de Medalhas Olímpicas  

Este projeto foi desenvolvido para a disciplina **Fundamentos de Algoritmos** da Universidade Estadual de Maringá, com o objetivo de aplicar conceitos de programação em Python utilizando listas de listas, passagem de parâmetros por referência e funções recursivas.  

## 🎯 Objetivo  
Construir um programa capaz de processar os dados das **Olimpíadas de Paris 2024**, consolidados em um arquivo CSV, e gerar análises sobre as medalhas conquistadas.  

## 🔧 Funcionalidades  
- **Leitura de dados**: importar um arquivo `.csv` contendo informações detalhadas sobre as medalhas (tipo, código, data, atleta, país, gênero, disciplina, evento, etc).  
- **Quadro de medalhas**:  
  - Contabilizar medalhas de ouro, prata, bronze e o total por país.  
  - Classificação ordenada por número de ouros, depois pratas e depois bronzes.  
- **Análise de gênero**:  
  - Identificar países que conquistaram medalhas apenas com atletas de um único gênero.  
  - Implementação obrigatória com **funções recursivas** (sem uso de `for` ou `while`).  

## 🛠️ Requisitos técnicos  
- Utilizar **listas de listas** para manipulação dos dados.  
- Criar funções bem definidas, incluindo exemplos de uso.  
- Empregar **passagem de parâmetros por referência** quando necessário.  
- Evitar o uso de funções prontas além das vistas em sala.  
- Executar o programa informando o arquivo de dados como parâmetro:  

```bash
python3 Medalhas_Olímpicas.py medals.csv
