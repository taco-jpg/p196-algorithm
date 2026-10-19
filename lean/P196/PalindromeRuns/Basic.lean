import P196.Foundations.LychrelDigitSums

set_option autoImplicit false

/-!
Exact consecutive-palindrome classification for ordinary decimal reverse-and-add.

Iteration continues after a palindrome. A positive palindromic input has a
palindromic successor exactly when every digit is at most four. Such a step
doubles every digit without changing the canonical width. Consequently, all
states through time k are palindromes exactly when the starting state is a
palindrome and every starting digit remains a decimal digit after k doublings.

This result does not exclude an isolated palindrome, assert a first hit, or
settle palindrome avoidance for 196 or any other positive seed.
-/

namespace PalindromeRuns

open Lychrel196 DecimalDigits

/-- For a positive palindrome, another palindromic state follows precisely
when each input digit can be doubled without carrying. -/
theorem palindrome_step_iff_digits_le_four
    (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hp : Palindrome n) :
    Palindrome (step n) ↔ ∀ i, i < L → d i ≤ 4 := by
  have hpv : Palindrome (value d L) := by
    rw [hc.2.2.2]
    exact hp
  have hsym :=
    (palindrome_value_iff d L hc.2.1 (Or.inr hc.2.2.1)).mp hpv
  have hcolumns : ∀ i, i < L → columnSum d L i = 2 * d i := by
    intro i hi
    dsimp only [columnSum, reflected]
    have hs := hsym i hi
    omega
  have hcriterion := step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1
  rw [hc.2.2.2] at hcriterion
  constructor
  · intro hstep
    rcases hcriterion.mp hstep with hsmall | hspecial
    · intro i hi
      have hb := hsmall i hi
      rw [hcolumns i hi] at hb
      omega
    · have he := hcolumns 0 hc.1
      have hodd := hspecial.1
      omega
  · intro hsmall
    apply hcriterion.mpr
    left
    intro i hi
    rw [hcolumns i hi]
    have hb := hsmall i hi
    omega

/-- Two consecutive positive palindromes have the same canonical width,
with every digit of the second equal to twice the corresponding first digit. -/
theorem canonical_double_of_palindromes
    (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hp : Palindrome n)
    (hstep : Palindrome (step n)) :
    Canonical (step n) (fun i => 2 * d i) L := by
  have hsmall := (palindrome_step_iff_digits_le_four n d L hc hp).mp hstep
  refine ⟨hc.1, ?_, ?_, ?_⟩
  · intro i hi
    have hb := hsmall i hi
    change 2 * d i ≤ 9
    omega
  · change 0 < 2 * d (L - 1)
    exact Nat.mul_pos (by decide) hc.2.2.1
  · rw [AstraModular.value_scale, hc.2.2.2]
    change 2 * n = n + reverse10 n
    have hr : reverse10 n = n := hp
    omega

/-- Exact classification of a consecutive palindromic prefix, including
time zero. Canonicality makes the seed positive and fixes its decimal digits. -/
theorem palindrome_prefix_iff
    (n : Nat) (d : Nat → Nat) (L k : Nat)
    (hc : Canonical n d L) :
    (∀ t, t ≤ k → Palindrome (orbit n t)) ↔
      Palindrome n ∧ ∀ i, i < L → 2 ^ k * d i ≤ 9 := by
  induction k generalizing n d with
  | zero =>
      constructor
      · intro h
        refine ⟨h 0 (by omega), ?_⟩
        intro i hi
        simpa only [Nat.pow_zero, Nat.one_mul] using hc.2.1 i hi
      · intro h t ht
        have ht0 : t = 0 := by omega
        subst t
        exact h.1
  | succ k ih =>
      constructor
      · intro h
        have hp : Palindrome n := h 0 (by omega)
        have hstep : Palindrome (step n) := h 1 (by omega)
        have hcstep := canonical_double_of_palindromes n d L hc hp hstep
        have hsuffix : ∀ j, j ≤ k → Palindrome (orbit (step n) j) := by
          intro j hj
          rw [orbit_from_step]
          exact h (j + 1) (by omega)
        have hnext := (ih (step n) (fun i => 2 * d i) hcstep).mp hsuffix
        refine ⟨hp, ?_⟩
        intro i hi
        have hb := hnext.2 i hi
        simpa only [Nat.pow_succ, Nat.mul_assoc] using hb
      · rintro ⟨hp, hbound⟩
        have hpow : ∀ i, i < L → 2 ^ k * (2 * d i) ≤ 9 := by
          intro i hi
          simpa only [Nat.pow_succ, Nat.mul_assoc] using hbound i hi
        have hsmall : ∀ i, i < L → d i ≤ 4 := by
          intro i hi
          have hpositive : 0 < 2 ^ k := Nat.pow_pos (by decide)
          have hone : 1 ≤ 2 ^ k := by omega
          have hmul := Nat.mul_le_mul_right (2 * d i) hone
          have htwo : 2 * d i ≤ 2 ^ k * (2 * d i) := by
            simpa only [Nat.one_mul] using hmul
          have hb := hpow i hi
          omega
        have hstep := (palindrome_step_iff_digits_le_four n d L hc hp).mpr hsmall
        have hcstep := canonical_double_of_palindromes n d L hc hp hstep
        have hsuffix :=
          (ih (step n) (fun i => 2 * d i) hcstep).mpr ⟨hstep, hpow⟩
        intro t ht
        cases t with
        | zero => exact hp
        | succ j =>
            rw [← orbit_from_step]
            exact hsuffix j (by omega)

#print axioms palindrome_step_iff_digits_le_four
#print axioms canonical_double_of_palindromes
#print axioms palindrome_prefix_iff

end PalindromeRuns
