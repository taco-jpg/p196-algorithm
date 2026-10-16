import ResidualFive
import ResidualFiveShape
import ResidualFiveWitness

set_option autoImplicit false

/-!
The complete necessary-condition endpoint for the residual digit-five family.
Every occurrence hypothesis below is an occurrence on the original orbit of
196. No first-hit hypothesis or external finite certificate is assumed.
-/

namespace Agent103.ResidualFive

open Lychrel196 DecimalDigits FoldedDecimal
open OverflowCarryNormalization NormalizationBridge CarryHistory
open Agent119.EightFamilies

/-- The phase restriction sharpens the checked initial exclusion. -/
theorem occurrence_at_least105 (t r : Nat) (h : orbit 196 t = fam 5 r) :
    105 ≤ t := by
  have ht := occurrence_after100 t r h
  have hm := occurrence_time_mod6 t r h
  omega

/-- Complete pair-sum shape at time `t-2`, and the actual integer at `t-1`. -/
theorem occurrence_two_step_shape (t r : Nat) (h : orbit 196 t = fam 5 r) :
    (V (t - 2)).1 = 2 * r + 4 ∧
    (∀ i, i < 2 * r + 4 → (V (t - 2)).2 i = fiveSourceDigit r i) ∧
    orbit 196 (t - 1) = 33 * 10 ^ (2 * r + 2) + 22 := by
  have ht := occurrence_after100 t r h
  have he : t - 2 + 1 = t - 1 := by omega
  obtain ⟨hw, hq⟩ := occurrence_penultimate_pairs t r h
  obtain ⟨hc1, hc2⟩ := occurrence_final_carries t r h
  have hw' : (V ((t - 2) + 1)).1 = 2 * r + 4 := by
    simpa only [he] using hw
  have hq' : ∀ i, i < 2 * r + 4 →
      (V ((t - 2) + 1)).2 i = famDigit 5 r i := by
    simpa only [he] using hq
  obtain ⟨hp, hm⟩ := middle_no_overflow_five (t - 2) r hw' hq' hc2
  have hwidth : (V ((t - 2) + 1)).1 = (V (t - 2)).1 := by
    rw [V_succ_fst]
    simp [nextWidth, hc2]
  refine ⟨hwidth.symm.trans hw', hp, ?_⟩
  simpa only [he] using hm

/-- All internal carries in the earlier of the final two additions. -/
theorem occurrence_internal_carries (t r : Nat) (h : orbit 196 t = fam 5 r)
    (i : Nat) (hi : i ≤ 2 * r + 4) :
    carry (V (t - 2)).2 i = if 2 ≤ i ∧ i ≤ 2 * r + 3 then 1 else 0 := by
  exact five_source_carry (V (t - 2)).2 r
    (occurrence_two_step_shape t r h).2.1 i hi

/-- A single endpoint with every original-orbit occurrence obligation explicit.
The digit function is constrained only inside the actual canonical width. -/
theorem occurrence_necessary_conditions (t r : Nat)
    (h : orbit 196 t = fam 5 r) :
    105 ≤ t ∧ 1 ≤ r ∧ t % 6 = 3 ∧
    (V (t - 1)).1 = 2 * r + 4 ∧ (V (t - 2)).1 = 2 * r + 4 ∧
    carry (V (t - 1)).2 (V (t - 1)).1 = 0 ∧
    carry (V (t - 2)).2 (V (t - 2)).1 = 0 ∧
    orbit 196 (t - 1) = 33 * 10 ^ (2 * r + 2) + 22 ∧
    (∀ i, i < 2 * r + 4 → (V (t - 2)).2 i = fiveSourceDigit r i) ∧
    (∀ i, i ≤ 2 * r + 4 →
      carry (V (t - 2)).2 i = if 2 ≤ i ∧ i ≤ 2 * r + 3 then 1 else 0) := by
  obtain ⟨_, hr⟩ := early_or_short 5 r t (by decide) (by decide) h
  obtain ⟨hc1, hc2⟩ := occurrence_final_carries t r h
  obtain ⟨hw2, hq, hm⟩ := occurrence_two_step_shape t r h
  exact ⟨occurrence_at_least105 t r h, hr, occurrence_time_mod6 t r h,
    (occurrence_penultimate_pairs t r h).1, hw2, hc1, hc2, hm, hq,
    occurrence_internal_carries t r h⟩

/-- The same endpoint written with the explicit original integer family. -/
theorem occurrence_necessary_conditions_unfolded (t r : Nat)
    (h : orbit 196 t = 55 * (10 ^ (2 * r + 2) + 1)) :
    105 ≤ t ∧ 1 ≤ r ∧ t % 6 = 3 ∧
    orbit 196 (t - 1) = 33 * 10 ^ (2 * r + 2) + 22 ∧
    (V (t - 2)).1 = 2 * r + 4 ∧
    (∀ i, i < 2 * r + 4 → (V (t - 2)).2 i = fiveSourceDigit r i) := by
  have hf : orbit 196 t = fam 5 r := by simpa only [fam] using h
  have hn := occurrence_necessary_conditions t r hf
  exact ⟨hn.1, hn.2.1, hn.2.2.1, hn.2.2.2.2.2.2.2.1,
    hn.2.2.2.2.1, hn.2.2.2.2.2.2.2.2.1⟩

#print axioms occurrence_at_least105
#print axioms occurrence_two_step_shape
#print axioms occurrence_internal_carries
#print axioms occurrence_necessary_conditions
#print axioms occurrence_necessary_conditions_unfolded

end Agent103.ResidualFive
