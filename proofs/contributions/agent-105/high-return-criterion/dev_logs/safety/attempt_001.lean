import HighCarryReduction

/-! Exact finite safety criteria for the first two positive outputs of an
ordinary decimal reverse-and-add orbit starting in the high region. The
large-adjacency criterion already excludes the exceptional first-output
palindrome, so these equivalences do not need a high-return hypothesis.
This therefore covers every actual two-step high return. No assertion is
made about the starting integer, later outputs, or all-time safety. -/

namespace Agent105.ReturnSafety

open DecimalDigits FoldedDecimal OverflowCarryNormalization Lychrel196
  HighCarryReduction

/-- In the high region, the exceptional overflow predecessor class reduces
exactly to the constant pair word eleven. -/
theorem numeric_first_palindrome_iff_all_eleven
    (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighCarryWord q L) :
    Palindrome (step n) ↔ ∀ i, i < L → q i = 11 := by
  constructor
  · intro hp
    have hp' : Palindrome (step (value d L)) := by
      simpa only [hc.2.2.2] using hp
    rcases (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mp hp'
      with hsmall | ⟨_, hspecial⟩
    · have hs := hsmall 0 hc.1
      rw [hrep 0 hc.1] at hs
      have hh := hq.2
      omega
    · intro i hi
      have hs := hspecial i hi
      rw [hrep i hi] at hs
      have hh := (hq.1 i hi).1
      omega
  · intro hall
    have hp : Palindrome (step (value d L)) := by
      apply (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mpr
      apply Or.inr
      constructor
      · rw [hrep 0 hc.1]
        exact hall 0 hc.1
      · intro i hi
        exact Or.inr (by rw [hrep i hi]; exact hall i hi)
    simpa only [hc.2.2.2] using hp

/-- Negating the exact numeric second-output classification gives a finite
witness: one adjacent source pair sum is at least twenty-eight. -/
theorem numeric_second_safe_iff_large_adjacent
    (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighCarryWord q L) :
    (¬ Palindrome (orbit n 2)) ↔
      ∃ i, 0 < i ∧ i < L ∧ 28 ≤ q (i - 1) + q i := by
  classical
  constructor
  · intro hs
    by_contra hnone
    apply hs
    apply (numeric_second_palindrome_iff_adjacent n d q L hc hrep hq).mpr
    intro i hi hiL
    by_contra hsmall
    exact hnone ⟨i, hi, hiL, by omega⟩
  · rintro ⟨i, hi, hiL, hlarge⟩ hp
    have hs := (numeric_second_palindrome_iff_adjacent n d q L hc hrep hq).mp
      hp i hi hiL
    omega

/-- A large adjacent source sum also rules out the only possible
first-output palindrome in the high region. -/
theorem numeric_first_safe_of_large_adjacent
    (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighCarryWord q L)
    (hlarge : ∃ i, 0 < i ∧ i < L ∧ 28 ≤ q (i - 1) + q i) :
    ¬ Palindrome (step n) := by
  intro hp
  obtain ⟨i, hi, hiL, hsum⟩ := hlarge
  have hall := (numeric_first_palindrome_iff_all_eleven n d q L hc hrep hq).mp hp
  have ha := hall (i - 1) (by omega)
  have hb := hall i hiL
  omega

/-- Exact safety of the first and second positive outputs of the same
ordinary integer. This is a finite two-output statement. -/
theorem numeric_two_outputs_safe_iff_large_adjacent
    (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighCarryWord q L) :
    (¬ Palindrome (step n) ∧ ¬ Palindrome (orbit n 2)) ↔
      ∃ i, 0 < i ∧ i < L ∧ 28 ≤ q (i - 1) + q i := by
  constructor
  · intro hs
    exact (numeric_second_safe_iff_large_adjacent n d q L hc hrep hq).mp hs.2
  · intro hlarge
    exact ⟨numeric_first_safe_of_large_adjacent n d q L hc hrep hq hlarge,
      (numeric_second_safe_iff_large_adjacent n d q L hc hrep hq).mpr hlarge⟩

/-- The large-adjacency witness is equivalent to a coefficient of at least
ten in the actual next pair word, with its actual next width. -/
theorem large_adjacent_iff_next_pair_large
    (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighCarryWord q L)
    (hsym : ∀ i, i < L → q i = q (L - 1 - i)) :
    (∃ i, 0 < i ∧ i < L ∧ 28 ≤ q (i - 1) + q i) ↔
      ∃ i, i < nextWidth q L ∧ 10 ≤ nextColumns q L i := by
  classical
  constructor
  · rintro ⟨i, hi, hiL, hlarge⟩
    refine ⟨i, ?_, ?_⟩
    · rw [nextWidth_eq q L hL hq]
      omega
    · rw [nextColumns_internal q L i hq hsym hi hiL]
      omega
  · intro hlarge
    by_contra hnone
    have hadj : ∀ i, 0 < i → i < L → q (i - 1) + q i ≤ 27 := by
      intro i hi hiL
      by_contra hs
      exact hnone ⟨i, hi, hiL, by omega⟩
    have hlow := (nextColumns_low_iff_adjacent q L hL hq hsym).mpr hadj
    obtain ⟨i, hi, hbig⟩ := hlarge
    have hs := hlow i hi
    omega

/-- Equivalent finite safety test using the represented first successor
pair word, without replacing the original integer by a constructed one. -/
theorem numeric_two_outputs_safe_iff_next_pair_large
    (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighCarryWord q L) :
    (¬ Palindrome (step n) ∧ ¬ Palindrome (orbit n 2)) ↔
      ∃ i, i < nextWidth q L ∧ 10 ≤ nextColumns q L i := by
  have ha := NormalizationBridge.admissible_congr L (columnSum d L) q
    (NormalizationBridge.canonical_admissible n d L hc) hrep
  exact (numeric_two_outputs_safe_iff_large_adjacent n d q L hc hrep hq).trans
    (large_adjacent_iff_next_pair_large q L hc.1 hq ha.2.2.2.1)

#print axioms numeric_first_palindrome_iff_all_eleven
#print axioms numeric_second_safe_iff_large_adjacent
#print axioms numeric_first_safe_of_large_adjacent
#print axioms numeric_two_outputs_safe_iff_large_adjacent
#print axioms large_adjacent_iff_next_pair_large
#print axioms numeric_two_outputs_safe_iff_next_pair_large
end Agent105.ReturnSafety
