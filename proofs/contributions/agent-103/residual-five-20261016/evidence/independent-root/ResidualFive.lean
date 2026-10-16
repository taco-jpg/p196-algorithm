import EightFamilies
import TemporalResidues

set_option autoImplicit false

/-!
# Agent #103: necessary conditions for the residual digit-five family

This module applies Agent #119's unchanged ordinary-decimal interfaces and
Agent #423's unchanged modulo-99 table to the still-open family
`fam 5 r = 55 * (10^(2*r+2) + 1)`.
An occurrence is assumed only to derive necessary conditions. No occurrence,
infinite palindrome avoidance, or resolution of the 196 problem is asserted.
-/

namespace Agent103.ResidualFive

open Lychrel196 DecimalDigits FoldedDecimal
open OverflowCarryNormalization NormalizationBridge CarryHistory
open Agent119.EightFamilies Agent423.TemporalResidues

/-- The original family has residue 11 modulo 99 at every parameter. -/
theorem five_family_mod99 (r : Nat) : fam 5 r % 99 = 11 := by
  have hp := AstraModular.ten_pow_mod99 (2 * r + 2)
  have he : (2 * r + 2) % 2 = 0 := by omega
  simp only [he, if_true] at hp
  change (55 * (10 ^ (2 * r + 2) + 1)) % 99 = 11
  rw [Nat.mul_mod, Nat.add_mod, hp]

/-- Existing checked initial exclusion removes every time through 100. -/
theorem occurrence_after100 (t r : Nat) (h : orbit 196 t = fam 5 r) :
    100 < t := by
  by_cases ht : t ≤ 100
  · have hp : Palindrome (orbit 196 t) := by
      rw [h]
      exact fam_palindrome 5 r (by decide) (by decide)
    exact (no_palindrome_through_100 t ht hp).elim
  · omega

/-- A residual-family occurrence must be in phase three of the actual orbit. -/
theorem occurrence_time_mod6 (t r : Nat) (h : orbit 196 t = fam 5 r) :
    t % 6 = 3 := by
  have ht := occurrence_after100 t r h
  have he : 6 + (t - 6) = t := by omega
  have hphase := orbit196_mod99_table (t - 6)
  rw [he, h, five_family_mod99] at hphase
  have hm : (t - 6) % 6 = t % 6 := by omega
  simp only [phase196, hm] at hphase
  split at hphase
  · omega
  · split at hphase
    · omega
    · split at hphase
      · omega
      · split at hphase
        · assumption
        · split at hphase <;> omega

/-- The final two additions do not increase the canonical digit width.
The earlier addition may have internal carries. -/
theorem occurrence_final_carries (t r : Nat) (h : orbit 196 t = fam 5 r) :
    carry (V (t - 1)).2 (V (t - 1)).1 = 0 ∧
    carry (V (t - 2)).2 (V (t - 2)).1 = 0 := by
  obtain ⟨ht, hr⟩ := early_or_short 5 r t (by decide) (by decide) h
  have hlast : orbit 196 ((t - 1) + 1) = fam 5 r := by
    simpa only [show t - 1 + 1 = t by omega] using h
  have hcLast : carry (V (t - 1)).2 (V (t - 1)).1 = 0 := by
    have hb := V_carry_le (t - 1)
    by_cases hz : carry (V (t - 1)).2 (V (t - 1)).1 = 0
    · exact hz
    · have hc1 : carry (V (t - 1)).2 (V (t - 1)).1 = 1 := by omega
      have hf := (last_step_overflow (t - 1) 5 r (by decide) (by decide)
        hr hlast hc1).1
      omega
  refine ⟨hcLast, ?_⟩
  obtain ⟨hw, hq⟩ := last_step_no_overflow (t - 1) 5 r
    (by decide) (by decide) hlast hcLast
  have hb := V_carry_le (t - 2)
  by_cases hz : carry (V (t - 2)).2 (V (t - 2)).1 = 0
  · exact hz
  · have hc1 : carry (V (t - 2)).2 (V (t - 2)).1 = 1 := by omega
    have he : t - 2 + 1 = t - 1 := by omega
    have hw' : (V ((t - 2) + 1)).1 = 2 * r + 4 := by simpa only [he] using hw
    have hq' : ∀ i, i < 2 * r + 4 →
        (V ((t - 2) + 1)).2 i = famDigit 5 r i := by simpa only [he] using hq
    have hf := (middle_overflow (t - 2) 5 r (by decide) (by decide) hr
      (by omega) hw' hq' hc1).1
    omega

/-- The penultimate pair sums are the exact digits of the final palindrome. -/
theorem occurrence_penultimate_pairs (t r : Nat) (h : orbit 196 t = fam 5 r) :
    (V (t - 1)).1 = 2 * r + 4 ∧
    ∀ i, i < 2 * r + 4 → (V (t - 1)).2 i = famDigit 5 r i := by
  have ht := occurrence_after100 t r h
  have he : t - 1 + 1 = t := by omega
  apply last_step_no_overflow (t - 1) 5 r (by decide) (by decide)
  · simpa only [he] using h
  · exact (occurrence_final_carries t r h).1

#print axioms five_family_mod99
#print axioms occurrence_after100
#print axioms occurrence_time_mod6
#print axioms occurrence_final_carries
#print axioms occurrence_penultimate_pairs

end Agent103.ResidualFive
