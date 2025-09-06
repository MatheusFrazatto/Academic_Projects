import gleam/float
import gleam/string
import sgleam/check

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

pub fn calcular_azulejos(largura: Float, altura: Float) -> Float {
  let azulejo = { largura *. altura } /. { 0.2 *. 0.2 }
  float.ceiling(azulejo)
}

pub fn calcular_azulejos_examples() {
  check.eq(calcular_azulejos(1.0, 1.0), 25.0)
  check.eq(calcular_azulejos(1.1, 1.1), 31.0)
  check.eq(calcular_azulejos(2.12, 4.113), 218.0)
}

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

