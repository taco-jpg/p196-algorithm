import P196.Foundations.LychrelDigitSums

/-!
Finite digit-mass bounds for the low-digit-sum termination argument.
The coefficients are arbitrary natural numbers; no canonical digit or
reverse-and-add hypothesis is required for these inequalities.
-/

namespace LowDigitSumTermination

open DecimalDigits DecimalMass

/-- An active coefficient contributes no more than the whole word sum. -/
theorem wordSum_single_le (d : Nat → Nat) (L i : Nat) (hi : i < L) :
    d i ≤ wordSum d L := by
  have h := DecimalZeroGap.wordSum_mono_length d (i + 1) L (by omega)
  change wordSum d i + d i ≤ wordSum d L at h
  omega

/-- Two distinct active coefficients are counted separately in the word sum. -/
theorem wordSum_pair_le (d : Nat → Nat) (L i j : Nat)
    (hi : i < L) (hj : j < L) (hij : i ≠ j) :
    d i + d j ≤ wordSum d L := by
  induction L generalizing i j with
  | zero => omega
  | succ L ih =>
      by_cases hiL : i = L
      · subst i
        have h := wordSum_single_le d L j (by omega)
        change d L + d j ≤ wordSum d L + d L
        omega
      · by_cases hjL : j = L
        · subst j
          have h := wordSum_single_le d L i (by omega)
          change d i + d L ≤ wordSum d L + d L
          omega
        · have h := ih i j (by omega) (by omega) hij
          change d i + d j ≤ wordSum d L + d L
          omega

/-- Three pairwise distinct active coefficients fit within the word sum. -/
theorem wordSum_triple_le (d : Nat → Nat) (L i j k : Nat)
    (hi : i < L) (hj : j < L) (hk : k < L)
    (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k) :
    d i + d j + d k ≤ wordSum d L := by
  induction L generalizing i j k with
  | zero => omega
  | succ L ih =>
      by_cases hiL : i = L
      · subst i
        have h := wordSum_pair_le d L j k (by omega) (by omega) hjk
        change d L + d j + d k ≤ wordSum d L + d L
        omega
      · by_cases hjL : j = L
        · subst j
          have h := wordSum_pair_le d L i k (by omega) (by omega) hik
          change d i + d L + d k ≤ wordSum d L + d L
          omega
        · by_cases hkL : k = L
          · subst k
            have h := wordSum_pair_le d L i j (by omega) (by omega) hij
            change d i + d j + d L ≤ wordSum d L + d L
            omega
          · have h := ih i j k (by omega) (by omega) (by omega) hij hik hjk
            change d i + d j + d k ≤ wordSum d L + d L
            omega

/-- A noncentral column of an odd-width word uses two distinct digits. -/
theorem noncentral_column_le_mass (d : Nat → Nat) (m i : Nat)
    (hi : i < 2 * m + 1) (hne : i ≠ m) :
    columnSum d (2 * m + 1) i ≤ wordSum d (2 * m + 1) := by
  have hr : 2 * m + 1 - 1 - i < 2 * m + 1 := by omega
  have hd : i ≠ 2 * m + 1 - 1 - i := by omega
  simpa only [columnSum, reflected] using
    wordSum_pair_le d (2 * m + 1) i (2 * m + 1 - 1 - i) hi hr hd

/-- The middle digit remains available after counting any noncentral pair. -/
theorem noncentral_column_add_middle_le_mass (d : Nat → Nat) (m i : Nat)
    (hi : i < 2 * m + 1) (hne : i ≠ m) :
    columnSum d (2 * m + 1) i + d m ≤ wordSum d (2 * m + 1) := by
  have hr : 2 * m + 1 - 1 - i < 2 * m + 1 := by omega
  have hm : m < 2 * m + 1 := by omega
  have hd : i ≠ 2 * m + 1 - 1 - i := by omega
  have hrm : 2 * m + 1 - 1 - i ≠ m := by omega
  simpa only [columnSum, reflected] using
    wordSum_triple_le d (2 * m + 1) i (2 * m + 1 - 1 - i) m
      hi hr hm hd hne hrm

#print axioms wordSum_single_le
#print axioms wordSum_pair_le
#print axioms wordSum_triple_le
#print axioms noncentral_column_le_mass
#print axioms noncentral_column_add_middle_le_mass

end LowDigitSumTermination
