import gleam/float
import gleam/string
import sgleam/check

// Exercicio 23
//Você está fazendo um programa e precisa verificar se um texto digitado pelo usuário está de acordo
//com algumas regras. A regra “sem espaços extras” requer que o texto não comece e não termine com
//espaços. Projete uma função que verifique se um texto qualquer está de acordo com a regra “sem
//espaços extras”.
pub fn sem_espacos_extras(texto: String) -> Bool {
  case string.starts_with(texto, " ") {
    True -> False
    False ->
      case string.ends_with(texto, " ") {
        True -> False
        False -> True
      }
  }
}

pub fn sem_espacos_extras_examples() {
  check.eq(sem_espacos_extras("Matheus"), True)
  check.eq(sem_espacos_extras(" Matheus"), False)
  check.eq(sem_espacos_extras("Matheus "), False)
  check.eq(sem_espacos_extras(" Matheus "), False)
}

// Exercicio 24
//Cada cidadão de um país, cuja moeda chama-se dinheiro, tem que pagar imposto sobre a sua renda.
//Cidadãos que recebem até 1000 dinheiros pagam 5% de imposto. Cidadãos que recebem entre 1000 e
//5000 dinheiros pagam 5% de imposto sobre 1000 dinheiros e 10% sobre o que passar de 1000. Cidadãos
//que recebem mais de 5000 dinheiros pagam 5% de imposto sobre 1000 dinheiros, 10% de imposto sobre
//4000 dinheiros e 20% sobre o que passar de 5000. Projete uma função que calcule o imposto que um
//cidadão deve pagar dada a sua renda.
pub fn calcular_imposto(renda: Float) -> Float {
  case renda <=. 1000.0 {
    True -> renda *. 0.05
    False ->
      case renda <=. 5000.0 {
        True -> { 1000.0 *. 0.05 } +. { { renda -. 1000.0 } *. 0.1 }
        False ->
          { 1000.0 *. 0.05 }
          +. { 4000.0 *. 0.1 }
          +. { { renda -. 5000.0 } *. 0.2 }
      }
  }
}

pub fn calcular_imposto_examples() {
  check.eq(calcular_imposto(0.0), 0.0)
  check.eq(calcular_imposto(1000.0), 50.0)
  check.eq(calcular_imposto(2500.0), 200.0)
  check.eq(calcular_imposto(5000.0), 450.0)
  check.eq(calcular_imposto(7500.0), 950.0)
}

// Exercicio 26
//Um construtor precisa calcular a quantidade de azulejos necessários para azulejar uma determinada
//parede. Cada azulejo é quadrado e tem 20cm de lado. Ajude o construtor e defina uma função que
//receba como entrada o comprimento e a altura em metros de uma parede e calcule a quantidade de
//azulejos inteiros necessários para azulejar a parede. Considere que o construtor nunca perde um azulejo
//e que recortes de azulejos não são reaproveitados.
pub fn calcular_azulejos(largura: Float, altura: Float) -> Float {
  let azulejo = { largura *. altura } /. { 0.2 *. 0.2 }
  float.ceiling(azulejo)
}

pub fn calcular_azulejos_examples() {
  check.eq(calcular_azulejos(1.0, 1.0), 25.0)
  check.eq(calcular_azulejos(1.1, 1.1), 31.0)
  check.eq(calcular_azulejos(2.12, 4.113), 218.0)
}

// Exercicio 27
//Rotacionar uma string n posições à direita significa mover os últimos n caracteres da string para as
//primeiras n posições da string. Por exemplo, rotacionar a string "marcelio" 5 posições à direita
//produz a string "celiomar". Projete uma função que receba como entrada uma string e um número
//n e produza uma nova string rotacionando a string de entrada n posições à direita.
pub fn rotacionar_direita(texto: String, n: Int) -> String {
  let tamanho = string.length(texto)
  let n_corrigido = n % tamanho
  let corte = tamanho - n_corrigido
  let inicio = string.slice(texto, 0, corte)
  let fim = string.slice(texto, corte, tamanho)

  fim <> inicio
}

pub fn rotacionar_direita_examples() {
  check.eq(rotacionar_direita("Matheus", 1), "sMatheu")
  check.eq(rotacionar_direita("Matheus", 2), "usMathe")
  check.eq(rotacionar_direita("Matheus", 3), "eusMath")
  check.eq(rotacionar_direita("Matheus", 4), "heusMat")
  check.eq(rotacionar_direita("Matheus", 5), "theusMa")
  check.eq(rotacionar_direita("Matheus", 6), "atheusM")
  check.eq(rotacionar_direita("Matheus", 7), "Matheus")
}
