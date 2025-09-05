import gleam/int
import sgleam/check

pub type Tempo {
  Tempo(horas: Int, minutos: Int, segundos: Int)
}

pub fn conv(t: Tempo) -> String {
  case t {
    Tempo(a, b, c) ->
      int.to_string(t.horas)
      <> " hora(s)"
      <> int.to_string(t.minutos)
      <> " minutos(s)"
      <> int.to_string(t.segundos)
      <> " segunos(s)"
    Tempo(0, b, c) ->
      int.to_string(t.minutos)
      <> " minutos(s)"
      <> int.to_string(t.segundos)
      <> " segunos(s)"
    Tempo(a, 0, c) ->
      int.to_string(t.horas)
      <> " hora(s)"
      <> int.to_string(t.segundos)
      <> " segunos(s)"
    Tempo(a, b, 0) ->
      int.to_string(t.horas)
      <> " hora(s)"
      <> int.to_string(t.minutos)
      <> " minutos(s)"
    Tempo(0, b, 0) -> int.to_string(t.minutos) <> " minutos(s)"
    Tempo(0, 0, c) -> int.to_string(t.segundos) <> " segunos(s)"
    Tempo(a, 0, 0) -> int.to_string(t.horas) <> " hora(s)"
  }
}

pub fn conv_examples() {
  check.eq(conv(Tempo(12, 12, 12)), "12 hora(s)12 minutos(s)12 segunos(s)")
  check.eq(conv(Tempo(12, 0, 12)), "12 hora(s)0 minutos(s)12 segunos(s)")
  check.eq(conv(Tempo(12, 12, 0)), "12 hora(s)12 minutos(s)0 segunos(s)")
}

pub type Tipo {
  Crianca
  Jovem(estudante: Bool)
  Adulto(professor: Bool)
  Idoso
}

pub fn desc(t: Tipo) -> Bool {
  case t {
    Crianca -> True
    Jovem(e) ->
      case e {
        True -> True
        False -> False
      }
    Adulto(p) ->
      case p {
        True -> True
        False -> False
      }
    Idoso -> True
  }
}

pub fn desc_examples() {
  check.eq(desc(Crianca), True)
  check.eq(desc(Adulto(True)), True)
  check.eq(desc(Adulto(False)), False)
}

pub type Produto {
  Produto(codigo: Int, quantidade: Int)
}

pub fn comp(l: List(Produto)) -> Int {
  case l {
    [] -> 0
    [first, ..rest] ->
      case first.codigo {
        111 ->
          case first.quantidade > 0 {
            True -> { 15 * first.quantidade } + comp(rest)
            False -> comp(rest)
          }
        222 ->
          case first.quantidade > 0 {
            True -> { 15 * first.quantidade } + comp(rest)
            False -> comp(rest)
          }
        333 ->
          case first.quantidade > 0 {
            True -> { 15 * first.quantidade } + comp(rest)
            False -> comp(rest)
          }
        _ -> comp(rest)
      }
  }
}

pub fn comp_examples() {
  check.eq(comp([Produto(111, 10), Produto(222, 10), Produto(333, 10)]), 450)
  check.eq(comp([Produto(111, 10), Produto(223, 10), Produto(333, 10)]), 300)
  check.eq(comp([Produto(1311, 10), Produto(2212, 10), Produto(3323, 10)]), 0)
}
