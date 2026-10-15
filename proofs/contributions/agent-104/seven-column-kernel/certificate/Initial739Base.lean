import PrefixCertificate

namespace SevenColumn.Certificate739

def initialWord (i : Nat) : List Nat :=
  [7, 3, 9, i / 1000, (i / 100) % 10, (i / 10) % 10, i % 10]

theorem initialWord_digits {a b c d : Nat}
    (ha : a < 10) (hb : b < 10) (hc : c < 10) (hd : d < 10) :
    initialWord (1000 * a + 100 * b + 10 * c + d) = [7, 3, 9, a, b, c, d] := by
  simp only [initialWord, List.cons.injEq]
  simp only [true_and, and_true]
  exact ⟨by omega, by omega, by omega, by omega⟩

theorem initialWord_index_lt {a b c d : Nat}
    (ha : a < 10) (hb : b < 10) (hc : c < 10) (hd : d < 10) :
    1000 * a + 100 * b + 10 * c + d < 10000 := by omega

end SevenColumn.Certificate739
