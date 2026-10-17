import ResidualFiveFibers
import ResidualFiveConclusion

set_option autoImplicit false

namespace Agent103.ResidualFiveFibers

open Lychrel196 DecimalDigits FoldedDecimal
open Agent119.EightFamilies Agent103.ResidualFive
open SevenColumnKernel.PalindromeBridge

/-- The actual intermediate integer has canonical leading digit three. -/
theorem middle_canonical (r : Nat) :
    Canonical (middle r) (fiveOutputDigit r) (2 * r + 4) := by
  refine ⟨by omega, ?_, ?_, ?_⟩
  · intro i hi
    unfold fiveOutputDigit
    split <;> (try split) <;> omega
  · have hi : 2 * r + 4 - 1 = 2 * r + 3 := by omega
    simp only [hi, fiveOutputDigit_hi0]
    decide
  · rw [value_sparse (fiveOutputDigit r) r
      (fun i h1 h2 => fiveOutputDigit_mid r i h1 h2)]
    rw [fiveOutputDigit_zero, fiveOutputDigit_one,
      fiveOutputDigit_hi1, fiveOutputDigit_hi0]
    unfold middle
    omega

/-- Reuse the original leading-digit theorem to remove any source-width guess. -/
theorem predecessor_width_and_no_overflow (r n L : Nat) (d : Nat → Nat)
    (hc : Canonical n d L) (hs : step n = middle r) :
    L = 2 * r + 4 ∧ carry (columnSum d L) L = 0 := by
  have hlead : 1 < fiveOutputDigit r (2 * r + 4 - 1) := by
    rw [show 2 * r + 4 - 1 = 2 * r + 3 by omega, fiveOutputDigit_hi0]
    decide
  have hcarry := no_overflow_of_target_leading_gt_one hc (middle_canonical r) hs hlead
  have hn : Canonical (middle r) (output (columnSum d L)) L := by
    simpa only [hs] using canonical_next_no_overflow n d L hc hcarry
  exact ⟨(canonical_unique hn (middle_canonical r)).1, hcarry⟩

/-- Every ordinary predecessor is positive and has the prescribed width. -/
theorem predecessor_decimal_width (r n : Nat) (hs : step n = middle r) :
    Agent101.decimalWidth n (2 * r + 4) := by
  have hn : 0 < n := by
    by_cases hz : n = 0
    · rw [hz, show step 0 = 0 by decide] at hs
      unfold middle at hs
      omega
    · omega
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hw := (predecessor_width_and_no_overflow r n L d hc hs).1
  simpa only [hw] using Agent101.canonical_decimalWidth n d L hc

/-- A complete fiber over all ordinary natural numbers, with no width premise. -/
theorem fiber_mem_iff (r n : Nat) : n ∈ fiber r ↔ step n = middle r := by
  rw [fiber_mem_fixed_width]
  constructor
  · exact fun h => h.2
  · exact fun hs => ⟨predecessor_decimal_width r n hs, hs⟩

/-- The hypothetical 196 predecessor belongs to the complete concrete list. -/
theorem occurrence_predecessor_mem (t r : Nat)
    (h : orbit 196 t = fam 5 r) : orbit 196 (t - 2) ∈ fiber r := by
  apply (fiber_mem_iff r _).mpr
  have ht := occurrence_after100 t r h
  change orbit 196 ((t - 2) + 1) = middle r
  have he : t - 2 + 1 = t - 1 := by omega
  simpa only [he, middle] using (occurrence_two_step_shape t r h).2.2

/-- The actual phase selects residue 77 among the complete predecessors. -/
theorem occurrence_predecessor_mod99 (t r : Nat)
    (h : orbit 196 t = fam 5 r) : orbit 196 (t - 2) % 99 = 77 := by
  have ht := occurrence_after100 t r h
  have hm := occurrence_time_mod6 t r h
  have he : 6 + (t - 8) = t - 2 := by omega
  have hp : (t - 8) % 6 = 1 := by omega
  have htab := Agent423.TemporalResidues.orbit196_mod99_table (t - 8)
  rw [he] at htab
  simpa only [Agent423.TemporalResidues.phase196, hp] using htab

/-- Exact finite enumeration and size, including the short case `r=0`. -/
theorem complete_predecessor_fiber (r : Nat) :
    (fiber r).Nodup ∧ (fiber r).length = 14 * 10 ^ r ∧
    (∀ n, n ∈ fiber r ↔ step n = 33 * 10 ^ (2 * r + 2) + 22) := by
  exact ⟨fiber_nodup r, fiber_length r, fiber_mem_iff r⟩

#print axioms middle_canonical
#print axioms predecessor_width_and_no_overflow
#print axioms predecessor_decimal_width
#print axioms fiber_mem_iff
#print axioms occurrence_predecessor_mem
#print axioms occurrence_predecessor_mod99
#print axioms complete_predecessor_fiber

end Agent103.ResidualFiveFibers
