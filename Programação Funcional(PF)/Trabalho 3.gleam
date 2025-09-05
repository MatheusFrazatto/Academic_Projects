import gleam/list
import sgleam/check

//1
pub fn rept(lst: List(Int)) -> Int {
  case lst {
    [] -> 0
    [p, ..r] -> reptaux(r, 1, p)
  }
}

pub fn reptaux(lst: List(Int), a: Int, b: Int) -> Int {
  case lst {
    [] -> a
    [p, ..r] ->
      case p == b {
        True -> reptaux(r, a + 1, b)
        False -> a
      }
  }
}

pub fn rept_examples() {
  check.eq(rept([1, 1, 1, 2]), 3)
  check.eq(rept([1, 1, 2]), 2)
  check.eq(rept([1, 2]), 1)
  check.eq(rept([2, 1, 1, 1]), 1)
}

//2
pub fn ord(lsta: List(Int), lstb: List(Int)) -> List(Int) {
  case lsta, lstb {
    [], [] -> []
    [], [_, ..] -> lstb
    [_, ..], [] -> lsta
    [pa, ..ra], [pb, ..rb] ->
      case pa < pb {
        True -> [pa, ..ord(ra, [pb, ..rb])]
        False -> [pb, ..ord([pa, ..ra], rb)]
      }
  }
}

pub fn ord_examples() {
  check.eq(ord([1, 3, 5, 7], [2, 4, 6, 8]), [1, 2, 3, 4, 5, 6, 7, 8])
  check.eq(ord([1, 3, 7], [2, 4, 6, 8]), [1, 2, 3, 4, 6, 7, 8])
  check.eq(ord([7], [2, 4, 6, 8]), [2, 4, 6, 7, 8])
  check.eq(ord([1, 3, 5, 7], [2, 4]), [1, 2, 3, 4, 5, 7])
}

//3
pub fn filt(valores: List(Int)) -> List(Int) {
  list.filter(valores, fn(x) { x >= 0 && x % 5 != 0 })
}

pub fn filt_examples() {
  check.eq(filt([1, 5, -1, -2, 10]), [1])
  check.eq(filt([-1, 5, 10, 15, 2, 3, 5]), [2, 3])
  check.eq(filt([1, 2, 3, 4]), [1, 2, 3, 4])
  check.eq(filt([5]), [])
}
