import P196.Drafts.Agent7RunPopulationRenewal.HighCarryReduction

/-! Local high-region return conditions for the actual decimal carry recursion.
The reflection is at the unchanged physical width, as ensured by no overflow.
No disjointness assumption is made about the reflected columns. -/

namespace Agent105.LocalHigh

open DecimalDigits FoldedDecimal

/-- Sum of the two incoming carries at a pair of actual reflected positions. -/
def actualCarrySum (p : Nat → Nat) (M i : Nat) : Nat :=
  carry p i + carry p (M - 1 - i)

/-- The complete local criterion for an emitted pair coefficient in `9..18`. -/
def LocalAllowed (a u : Nat) : Prop :=
  ((4 ≤ a ∧ a ≤ 9) ∨ (14 ≤ a ∧ a ≤ 18)) ∧
    ((a = 4 ∨ a = 14) → 1 ≤ u) ∧ (a = 9 → u ≤ 1)

theorem actualCarrySum_le_two (p : Nat → Nat) (M i : Nat)
    (hb : ∀ j, j < M → p j ≤ 18) (hi : i < M) :
    actualCarrySum p M i ≤ 2 := by
  have ha := carry_bounded p M hb i (by omega)
  have hb' := carry_bounded p M hb (M - 1 - i) (by omega)
  unfold actualCarrySum
  omega

/-- Exact no-overflow pair update. At a high coefficient the subtraction
`2 * p i - 20` is nontruncated because that branch has `10 ≤ p i`. -/
theorem nextColumns_formula (p : Nat → Nat) (M i : Nat)
    (hb : ∀ j, j < M → p j ≤ 18)
    (hs : ∀ j, j < M → p j = p (M - 1 - j))
    (hi : i < M) (hc : carry p M = 0) :
    nextColumns p M i =
      if p i < 9 then 2 * p i + actualCarrySum p M i
      else if p i = 9 then 18 - 9 * actualCarrySum p M i
      else 2 * p i - 20 + actualCarrySum p M i := by
  have ha := carry_bounded p M hb i (by omega)
  have hb' := carry_bounded p M hb (M - 1 - i) (by omega)
  have hp := hb i hi
  rw [folded_emission_no_overflow p M i hi hs hc]
  unfold actualCarrySum
  by_cases hlo : p i < 9
  · simp only [if_pos hlo]
    omega
  · simp only [if_neg hlo]
    by_cases hnine : p i = 9
    · simp only [if_pos hnine]
      omega
    · simp only [if_neg hnine]
      omega

/-- A local high coefficient is equivalent to the carry-aware allowed set,
using the carries determined by the input word itself. -/
theorem nextColumns_high_iff (p : Nat → Nat) (M i : Nat)
    (hb : ∀ j, j < M → p j ≤ 18)
    (hs : ∀ j, j < M → p j = p (M - 1 - j))
    (hi : i < M) (hc : carry p M = 0) :
    (9 ≤ nextColumns p M i ∧ nextColumns p M i ≤ 18) ↔
      LocalAllowed (p i) (actualCarrySum p M i) := by
  have hu := actualCarrySum_le_two p M i hb hi
  have hp := hb i hi
  rw [nextColumns_formula p M i hb hs hi hc]
  unfold LocalAllowed
  by_cases hlo : p i < 9
  · simp only [if_pos hlo]
    omega
  · simp only [if_neg hlo]
    by_cases hnine : p i = 9
    · simp only [if_pos hnine]
      omega
    · simp only [if_neg hnine]
      omega

end Agent105.LocalHigh
