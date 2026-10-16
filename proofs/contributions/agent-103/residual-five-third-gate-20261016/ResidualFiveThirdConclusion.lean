import ResidualFiveThirdDecoder
import ResidualFiveFourthOverflow

/-!
# Four consecutive terminal carries at an original 196 residual-five occurrence

The occurrence itself is a hypothesis. These exact local necessities neither
bound the depth of all residual-five inverse trees nor prove 196 avoidance.
All digit functions below are representations in the original Canonical sense.
-/

set_option autoImplicit false

namespace Agent103.ResidualFiveThirdConclusion

open Lychrel196 DecimalDigits FoldedDecimal
open Agent119.EightFamilies Agent103.ResidualFive
open Agent103.ResidualFiveFibers Agent103.ResidualFiveThirdWidth
open Agent103.ResidualFiveThirdDecoder Agent103.ResidualFiveFourthOverflow

/-- The third predecessor's source pair begins with one and six and has no
terminal overflow. Transport uses only the actual finite canonical width. -/
theorem occurrence_third_source (t r : Nat) (h : orbit 196 t = fam 5 r) :
    (V (t - 3)).1 = 2 * r + 4 ∧
    carry (V (t - 3)).2 (V (t - 3)).1 = 0 ∧
    (V (t - 3)).2 0 = 1 ∧ (V (t - 3)).2 1 = 6 := by
  have ht := occurrence_at_least105 t r h
  have hn := occurrence_predecessor_mem t r h
  obtain ⟨d, hd, hrep⟩ := V_rep (t - 3)
  have hs : step (orbit 196 (t - 3)) = orbit 196 (t - 2) := by
    change orbit 196 ((t - 3) + 1) = orbit 196 (t - 2)
    rw [show t - 3 + 1 = t - 2 by omega]
  obtain ⟨hw, hc, hq0, hq1⟩ := predecessor_width_and_source r
    (orbit 196 (t - 2)) (orbit 196 (t - 3)) (V (t - 3)).1 d hn hs hd
  have hcarry := carry_congr_upto (columnSum d (V (t - 3)).1)
    (V (t - 3)).2 (V (t - 3)).1 hrep (V (t - 3)).1 (Nat.le_refl _)
  exact ⟨hw, hcarry.symm.trans hc,
    (hrep 0 (by omega)).symm.trans hq0, (hrep 1 (by omega)).symm.trans hq1⟩

/-- The earlier actual addition overflows and starts at one digit less. -/
theorem occurrence_fourth_overflow (t r : Nat) (h : orbit 196 t = fam 5 r) :
    (V (t - 4)).1 = 2 * r + 3 ∧
    carry (V (t - 4)).2 (V (t - 4)).1 = 1 := by
  have ht := occurrence_at_least105 t r h
  have hn := occurrence_predecessor_mem t r h
  obtain ⟨d, hd, _⟩ := V_rep (t - 3)
  obtain ⟨e, he, hrep⟩ := V_rep (t - 4)
  have hzn : step (orbit 196 (t - 3)) = orbit 196 (t - 2) := by
    change orbit 196 ((t - 3) + 1) = orbit 196 (t - 2)
    rw [show t - 3 + 1 = t - 2 by omega]
  have hyz : step (orbit 196 (t - 4)) = orbit 196 (t - 3) := by
    change orbit 196 ((t - 4) + 1) = orbit 196 (t - 3)
    rw [show t - 4 + 1 = t - 3 by omega]
  obtain ⟨hw, hc⟩ := earlier_width_and_overflow r (orbit 196 (t - 2))
    (orbit 196 (t - 3)) (orbit 196 (t - 4))
    (V (t - 3)).1 (V (t - 4)).1 d e hn hzn hyz hd he
  have hcarry := carry_congr_upto (columnSum e (V (t - 4)).1)
    (V (t - 4)).2 (V (t - 4)).1 hrep (V (t - 4)).1 (Nat.le_refl _)
  exact ⟨by omega, hcarry.symm.trans hc⟩

/-- Every canonical target representation satisfies the full exterior and center
criterion; the positive predecessor is supplied by the original orbit. -/
theorem occurrence_digit_gate (t r : Nat) (h : orbit 196 t = fam 5 r)
    (e : Nat → Nat) (he : Canonical (orbit 196 (t - 2)) e (2 * r + 4)) :
    e 0 = 1 ∧ e (2 * r + 3) = 1 ∧ e 1 = 6 ∧ e (2 * r + 2) = 6 ∧
      (Agent105DecoderScan9df76b.scan (2 * r) (fun i => e (i + 2)) 0 0).isSome = true := by
  have ht := occurrence_at_least105 t r h
  apply (fiber_predecessor_iff r (orbit 196 (t - 2)) e
    (occurrence_predecessor_mem t r h) he).mp
  refine ⟨orbit 196 (t - 3), orbit_positive 196 (by decide) (t - 3), ?_⟩
  change orbit 196 ((t - 3) + 1) = orbit 196 (t - 2)
  rw [show t - 3 + 1 = t - 2 by omega]

/-- The complete finite necessary condition, in chronological order from t-4
through t. The carry sequence is exactly one, zero, zero, zero. -/
theorem occurrence_last_four (t r : Nat) (h : orbit 196 t = fam 5 r) :
    105 ≤ t ∧ 1 ≤ r ∧ t % 6 = 3 ∧
    (V (t - 4)).1 = 2 * r + 3 ∧
    (V (t - 3)).1 = 2 * r + 4 ∧ (V (t - 2)).1 = 2 * r + 4 ∧
    (V (t - 1)).1 = 2 * r + 4 ∧ (V t).1 = 2 * r + 4 ∧
    carry (V (t - 4)).2 (V (t - 4)).1 = 1 ∧
    carry (V (t - 3)).2 (V (t - 3)).1 = 0 ∧
    carry (V (t - 2)).2 (V (t - 2)).1 = 0 ∧
    carry (V (t - 1)).2 (V (t - 1)).1 = 0 ∧
    (V (t - 3)).2 0 = 1 ∧ (V (t - 3)).2 1 = 6 ∧
    (∀ e, Canonical (orbit 196 (t - 2)) e (2 * r + 4) →
      e 0 = 1 ∧ e (2 * r + 3) = 1 ∧ e 1 = 6 ∧ e (2 * r + 2) = 6 ∧
        (Agent105DecoderScan9df76b.scan (2 * r) (fun i => e (i + 2)) 0 0).isSome = true) := by
  obtain ⟨ht, hr, hm, hw1, hw2, hc1, hc2, _⟩ := occurrence_necessary_conditions t r h
  obtain ⟨hw3, hc3, hq0, hq1⟩ := occurrence_third_source t r h
  obtain ⟨hw4, hc4⟩ := occurrence_fourth_overflow t r h
  have hwt : (V t).1 = 2 * r + 4 := by
    have hs : (V ((t - 1) + 1)).1 = 2 * r + 4 := by
      rw [V_succ_fst]
      unfold nextWidth
      rw [if_pos hc1]
      exact hw1
    simpa only [show t - 1 + 1 = t by omega] using hs
  exact ⟨ht, hr, hm, hw4, hw3, hw2, hw1, hwt, hc4, hc3, hc2, hc1,
    hq0, hq1, fun e he => occurrence_digit_gate t r h e he⟩

#print axioms occurrence_third_source
#print axioms occurrence_fourth_overflow
#print axioms occurrence_digit_gate
#print axioms occurrence_last_four

end Agent103.ResidualFiveThirdConclusion
