import Std

namespace P196.Agent51

/-- Least-significant-first ordinary input digits: k twos, zeros, k nines. -/
def inputDigit (L k i : Nat) : Nat :=
  if i < k then 2 else if L - k ≤ i ∧ i < L then 9 else 0

/-- The exact proposed mirrored coefficient word, including exterior zero extension. -/
def pairWord (L k i : Nat) : Nat :=
  if i < k ∨ (L - k ≤ i ∧ i < L) then 11 else 0

theorem inputDigit_bounded (L k i : Nat) : inputDigit L k i ≤ 9 := by
  unfold inputDigit
  split <;> (try split) <;> omega

theorem inputDigit_zero (L k : Nat) (hk : 0 < k) :
    inputDigit L k 0 = 2 := by
  simp [inputDigit, hk]

theorem inputDigit_last (L k : Nat) (hk : 0 < k) (hL : 2 * k ≤ L) :
    inputDigit L k (L - 1) = 9 := by
  have hfirst : ¬ L - 1 < k := by omega
  have hlast : L - k ≤ L - 1 ∧ L - 1 < L := by omega
  simp [inputDigit, hfirst, hlast]

theorem inputDigit_pair (L k i : Nat) (hL : 2 * k ≤ L) (hi : i < L) :
    inputDigit L k i + inputDigit L k (L - 1 - i) = pairWord L k i := by
  unfold inputDigit pairWord
  split <;> (try split) <;> (try split) <;> (try split) <;> (try split) <;> omega

theorem pairWord_values (L k i : Nat) :
    pairWord L k i = 0 ∨ pairWord L k i = 11 := by
  unfold pairWord
  split <;> simp_all

theorem pairWord_zero (L k : Nat) (hk : 0 < k) :
    pairWord L k 0 = 11 := by
  simp [pairWord, hk]

end P196.Agent51
