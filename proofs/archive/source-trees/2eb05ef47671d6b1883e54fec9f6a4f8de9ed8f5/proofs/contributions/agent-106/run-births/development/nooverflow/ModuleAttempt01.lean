import LychrelDigitSums

/-!
# Exact births of 0 and 18 at a no-overflow step

This module formalizes the two unrestricted one-column equivalences in
ABSORBING_CORE.md, section 4, for the actual `FoldedDecimal.nextColumns`.
All word-level statements retain `Admissible L q`, the physical index
`i < L`, and the actual final carry `carry q L = 0`.

The two incoming carry bits are `carry q i` and
`carry q (L - 1 - i)`, corresponding to a_i and beta_(i+1).
Their bit bounds are derived from admissibility, not assumed as a model.
The fresh-birth statements additionally require the old coefficient to
differ from the target. No run-ancestry or infinite-orbit claim is made.
-/

namespace Agent106.NoOverflowBirths

open DecimalDigits FoldedDecimal

/-- Exact local residue classification for output coefficient 18. -/
theorem residues_eighteen_iff (x a b : Nat)
    (hx : x ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    (x + a) % 10 + (x + b) % 10 = 18 ↔
      ((x = 8 ∨ x = 18) ∧ a + b = 2) ∨ (x = 9 ∧ a + b = 0) := by
  omega

/-- Exact local residue classification for output coefficient 0. -/
theorem residues_zero_iff (x a b : Nat)
    (hx : x ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    (x + a) % 10 + (x + b) % 10 = 0 ↔
      ((x = 0 ∨ x = 10) ∧ a + b = 0) ∨ (x = 9 ∧ a + b = 2) := by
  omega

/-- The section-4 equivalence for 18, using the actual incoming carry sum. -/
theorem next_eighteen_iff_sum (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0) :
    nextColumns q L i = 18 ↔
      ((q i = 8 ∨ q i = 18) ∧
        carry q i + carry q (L - 1 - i) = 2) ∨
      (q i = 9 ∧ carry q i + carry q (L - 1 - i) = 0) := by
  rw [folded_emission_no_overflow q L i hi ha.2.2.2.1 hc]
  exact residues_eighteen_iff (q i) (carry q i) (carry q (L - 1 - i))
    (ha.2.2.1 i hi) (carry_bounded q L ha.2.2.1 i (by omega))
    (carry_bounded q L ha.2.2.1 (L - 1 - i) (by omega))

/-- The section-4 equivalence for 0, using the actual incoming carry sum. -/
theorem next_zero_iff_sum (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0) :
    nextColumns q L i = 0 ↔
      ((q i = 0 ∨ q i = 10) ∧
        carry q i + carry q (L - 1 - i) = 0) ∨
      (q i = 9 ∧ carry q i + carry q (L - 1 - i) = 2) := by
  rw [folded_emission_no_overflow q L i hi ha.2.2.2.1 hc]
  exact residues_zero_iff (q i) (carry q i) (carry q (L - 1 - i))
    (ha.2.2.1 i hi) (carry_bounded q L ha.2.2.1 i (by omega))
    (carry_bounded q L ha.2.2.1 (L - 1 - i) (by omega))

/-- Carry-bit form: old 8/18 with two ones, or old 9 with two zeroes. -/
theorem next_eighteen_iff_bits (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0) :
    nextColumns q L i = 18 ↔
      ((q i = 8 ∨ q i = 18) ∧
        carry q i = 1 ∧ carry q (L - 1 - i) = 1) ∨
      (q i = 9 ∧ carry q i = 0 ∧ carry q (L - 1 - i) = 0) := by
  have haBit := carry_bounded q L ha.2.2.1 i (by omega)
  have hbBit := carry_bounded q L ha.2.2.1 (L - 1 - i) (by omega)
  rw [next_eighteen_iff_sum q L i ha hi hc]
  omega

/-- Carry-bit form: old 0/10 with two zeroes, or old 9 with two ones. -/
theorem next_zero_iff_bits (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0) :
    nextColumns q L i = 0 ↔
      ((q i = 0 ∨ q i = 10) ∧
        carry q i = 0 ∧ carry q (L - 1 - i) = 0) ∨
      (q i = 9 ∧ carry q i = 1 ∧ carry q (L - 1 - i) = 1) := by
  have haBit := carry_bounded q L ha.2.2.1 i (by omega)
  have hbBit := carry_bounded q L ha.2.2.1 (L - 1 - i) (by omega)
  rw [next_zero_iff_sum q L i ha hi hc]
  omega

/-- An actually new 18 has exactly two possible old coefficients: 8 or 9. -/
theorem fresh_eighteen_iff (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0) :
    (nextColumns q L i = 18 ∧ q i ≠ 18) ↔
      (q i = 8 ∧ carry q i = 1 ∧ carry q (L - 1 - i) = 1) ∨
      (q i = 9 ∧ carry q i = 0 ∧ carry q (L - 1 - i) = 0) := by
  rw [next_eighteen_iff_bits q L i ha hi hc]
  omega

/-- An actually new 0 has exactly two possible old coefficients: 10 or 9. -/
theorem fresh_zero_iff (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0) :
    (nextColumns q L i = 0 ∧ q i ≠ 0) ↔
      (q i = 10 ∧ carry q i = 0 ∧ carry q (L - 1 - i) = 0) ∨
      (q i = 9 ∧ carry q i = 1 ∧ carry q (L - 1 - i) = 1) := by
  rw [next_zero_iff_bits q L i ha hi hc]
  omega

/-- At an old 9, two zeroes create 18, mixed bits give 9, and two ones create 0. -/
theorem nine_emission_classification (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0)
    (hqi : q i = 9) :
    (nextColumns q L i = 18 ↔ carry q i + carry q (L - 1 - i) = 0) ∧
    (nextColumns q L i = 9 ↔ carry q i + carry q (L - 1 - i) = 1) ∧
    (nextColumns q L i = 0 ↔ carry q i + carry q (L - 1 - i) = 2) := by
  have he := folded_emission_no_overflow q L i hi ha.2.2.2.1 hc
  have haBit := carry_bounded q L ha.2.2.1 i (by omega)
  have hbBit := carry_bounded q L ha.2.2.1 (L - 1 - i) (by omega)
  rw [hqi] at he
  omega

/-- At an old 8 or 18, the emitted coefficient is 16 plus the carry sum. -/
theorem eight_or_eighteen_emission (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0)
    (hqi : q i = 8 ∨ q i = 18) :
    nextColumns q L i = 16 + carry q i + carry q (L - 1 - i) := by
  have he := folded_emission_no_overflow q L i hi ha.2.2.2.1 hc
  have haBit := carry_bounded q L ha.2.2.1 i (by omega)
  have hbBit := carry_bounded q L ha.2.2.1 (L - 1 - i) (by omega)
  omega

/-- At an old 0 or 10, the emitted coefficient is the carry sum. -/
theorem zero_or_ten_emission (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0)
    (hqi : q i = 0 ∨ q i = 10) :
    nextColumns q L i = carry q i + carry q (L - 1 - i) := by
  have he := folded_emission_no_overflow q L i hi ha.2.2.2.1 hc
  have haBit := carry_bounded q L ha.2.2.1 i (by omega)
  have hbBit := carry_bounded q L ha.2.2.1 (L - 1 - i) (by omega)
  omega

/-- A new 18 at a self-reflected center must come from 8 and carry 1.
The old-9 branch is excluded by the actual center parity condition. -/
theorem fresh_eighteen_center_iff (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0)
    (hcenter : i = L - 1 - i) :
    (nextColumns q L i = 18 ∧ q i ≠ 18) ↔
      q i = 8 ∧ carry q i = 1 := by
  have hparity := ha.2.2.2.2 i hi hcenter
  rw [fresh_eighteen_iff q L i ha hi hc, ← hcenter]
  omega

/-- A new 0 at a self-reflected center must come from 10 and carry 0. -/
theorem fresh_zero_center_iff (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0)
    (hcenter : i = L - 1 - i) :
    (nextColumns q L i = 0 ∧ q i ≠ 0) ↔
      q i = 10 ∧ carry q i = 0 := by
  have hparity := ha.2.2.2.2 i hi hcenter
  rw [fresh_zero_iff q L i ha hi hc, ← hcenter]
  omega

#print axioms residues_eighteen_iff
#print axioms residues_zero_iff
#print axioms next_eighteen_iff_sum
#print axioms next_zero_iff_sum
#print axioms next_eighteen_iff_bits
#print axioms next_zero_iff_bits
#print axioms fresh_eighteen_iff
#print axioms fresh_zero_iff
#print axioms nine_emission_classification
#print axioms eight_or_eighteen_emission
#print axioms zero_or_ten_emission
#print axioms fresh_eighteen_center_iff
#print axioms fresh_zero_center_iff

end Agent106.NoOverflowBirths
