import LychrelDigitSums
import OverflowDigits

namespace P196.Agent51

/-- The ordinary positive integer realizing the explicit overflow family. -/
def witnessNumber (L k : Nat) : Nat :=
  DecimalDigits.value (inputDigit L k) L

theorem witness_canonical (L k : Nat) (hk : 0 < k) (hL : 2 * k ≤ L) :
    DecimalDigits.Canonical (witnessNumber L k) (inputDigit L k) L := by
  refine ⟨by omega, ?_, ?_, rfl⟩
  · intro i _
    exact inputDigit_bounded L k i
  · rw [inputDigit_last L k hk hL]
    omega

theorem witness_positive (L k : Nat) (hk : 0 < k) (hL : 2 * k ≤ L) :
    0 < witnessNumber L k := by
  apply DecimalDigits.value_positive
  · omega
  · rw [inputDigit_last L k hk hL]
    omega

theorem witness_columnSum (L k i : Nat) (hL : 2 * k ≤ L) (hi : i < L) :
    DecimalDigits.columnSum (inputDigit L k) L i = pairWord L k i := by
  exact inputDigit_pair L k i hL hi

theorem witness_not_palindrome (L k : Nat) (hk : 0 < k) (hL : 2 * k ≤ L) :
    ¬ Lychrel196.Palindrome (witnessNumber L k) := by
  intro hp
  have hd : ∀ i, i < L → inputDigit L k i ≤ 9 :=
    fun i _ => inputDigit_bounded L k i
  have hlead : 0 < inputDigit L k (L - 1) := by
    rw [inputDigit_last L k hk hL]
    omega
  have hs := (DecimalDigits.palindrome_value_iff (inputDigit L k) L hd
    (Or.inr hlead)).mp hp 0 (by omega)
  simp only [Nat.sub_zero] at hs
  rw [inputDigit_zero L k hk, inputDigit_last L k hk hL] at hs
  omega

theorem witness_overflow (L k : Nat) (hk : 0 < k) (hL : 2 * k ≤ L) :
    DecimalDigits.carry (DecimalDigits.columnSum (inputDigit L k) L) L = 1 := by
  have hd : ∀ i, i < L → inputDigit L k i ≤ 9 :=
    fun i _ => inputDigit_bounded L k i
  apply ((DecimalDigits.overflow_palindrome_iff (inputDigit L k) L (by omega) hd).mpr ?_).1
  constructor
  · rw [witness_columnSum L k 0 hL (by omega)]
    exact pairWord_zero L k hk
  · intro i hi
    rw [witness_columnSum L k i hL hi]
    exact pairWord_values L k i

theorem witness_step_palindrome (L k : Nat) (hk : 0 < k) (hL : 2 * k ≤ L) :
    Lychrel196.Palindrome (Lychrel196.step (witnessNumber L k)) := by
  have hd : ∀ i, i < L → inputDigit L k i ≤ 9 :=
    fun i _ => inputDigit_bounded L k i
  have hlead : 0 < inputDigit L k (L - 1) := by
    rw [inputDigit_last L k hk hL]
    omega
  apply (DecimalDigits.step_palindrome_iff_overflow (inputDigit L k) L
    (by omega) hd hlead (witness_overflow L k hk hL)).mpr
  constructor
  · rw [witness_columnSum L k 0 hL (by omega)]
    exact pairWord_zero L k hk
  · intro i hi
    rw [witness_columnSum L k i hL hi]
    exact pairWord_values L k i

theorem witness_step_canonical (L k : Nat) (hk : 0 < k) (hL : 2 * k ≤ L) :
    DecimalDigits.Canonical (Lychrel196.step (witnessNumber L k))
      (DecimalDigits.extended (DecimalDigits.columnSum (inputDigit L k) L) L) (L + 1) := by
  exact DecimalDynamics.canonical_next_overflow (witnessNumber L k) (inputDigit L k) L
    (witness_canonical L k hk hL) (witness_overflow L k hk hL)

#print axioms witness_canonical
#print axioms witness_positive
#print axioms witness_columnSum
#print axioms witness_not_palindrome
#print axioms witness_overflow
#print axioms witness_step_palindrome
#print axioms witness_step_canonical

end P196.Agent51
