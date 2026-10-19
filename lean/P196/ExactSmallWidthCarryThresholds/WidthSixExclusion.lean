import P196.EightCarryMaximalWidth.PrefixExclusion
import P196.ExactSmallWidthCarryThresholds.WidthSixBaseCertificate
import P196.ExactSmallWidthCarryThresholds.WidthSixAMinusTwoCertificate
import P196.ExactSmallWidthCarryThresholds.WidthSixAPlusOneCertificate
import P196.ExactSmallWidthCarryThresholds.WidthSixAReflectionCertificate
import P196.ExactSmallWidthCarryThresholds.WidthSixBMinusOneCertificate
import P196.ExactSmallWidthCarryThresholds.WidthSixBEqualCertificate
import P196.ExactSmallWidthCarryThresholds.WidthSixBReflectionCertificate

/-!
The two oriented width-six profiles cannot share six complete carry words.
Finite covers restrict their first three coefficients. Actual symmetry then
repeats the third coefficient in position three, and both reflected covers
are empty. Every required prefix separately uses the imported theorem for
actual histories, retaining all six observations.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual SevenColumnProjection
open EightCarryMaximalWidth (prefix_succ)
open EightCarryMaximalWidth.PrefixHistory
open WidthSixCandidates

/-- Neither oriented residual profile at exact width six admits six matching
complete carry observations. Admissibility supplies the reflected coefficients. -/
theorem six_carries_exclude_width_six_profiles
    (q r : Nat → Nat) (hq : Admissible 6 q) (hr : Admissible 6 r)
    (hc : ∀ t, t < 6 → ∀ i, i ≤ (iterPairs q 6 t).1 →
      carry (iterPairs q 6 t).2 i = carry (iterPairs r 6 t).2 i)
    (h0 : q 0 = r 0 + 1)
    (hcases : (r 1 = q 1 + 2 ∧ q 2 = r 2 + 1) ∨
      (r 1 = q 1 + 1 ∧ q 2 = r 2)) : False := by
  have hs : ∀ k, 0 < k → k ≤ 6 →
      survivesEncoded 6 (wordPrefix q k) (wordPrefix r k) = true := by
    intro k hk0 hk
    exact actual_history_survives_encoded q r 6 k 6 hq hr hk0 hk hc
  have hm1 : (wordPrefix q 1, wordPrefix r 1) ∈ firstColumns := by
    have hp : r 0 - 1 < 17 := by
      have := hq.2.2.1 0 (by decide)
      have := hr.2.1
      omega
    have hq0 : r 0 - 1 + 2 = q 0 := by have := hr.2.1; omega
    have hr0 : r 0 - 1 + 1 = r 0 := by have := hr.2.1; omega
    have hleaf := cover_first_columns ⟨r 0 - 1, hp⟩
    have hleaf' : Leaf firstColumns (wordPrefix q 1, wordPrefix r 1) := by
      change Leaf firstColumns ([q 0], [r 0])
      simpa only [Fin.val_mk, hq0, hr0] using hleaf
    exact leaf_mem _ _ hleaf' (hs 1 (by decide) (by decide))
  obtain ⟨i1, hi1⟩ := List.mem_iff_get.mp hm1
  have hq3 : q 3 = q 2 := hq.2.2.2.1 3 (by decide)
  have hr3 : r 3 = r 2 := hr.2.2.2.1 3 (by decide)
  rcases hcases with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · have ha1 : q 1 < 17 := by have := hr.2.2.1 1 (by decide); omega
    have hleaf2 := cover_a_minus_two i1 ⟨q 1, ha1⟩
    have hleaf2' : Leaf secondA (wordPrefix q 2, wordPrefix r 2) := by
      simpa only [hi1, Fin.val_mk, prefix_succ, h1] using hleaf2
    have hm2 := leaf_mem _ _ hleaf2' (hs 2 (by decide) (by decide))
    obtain ⟨i2, hi2⟩ := List.mem_iff_get.mp hm2
    have ha2 : r 2 < 18 := by have := hq.2.2.1 2 (by decide); omega
    have hleaf3 := cover_a_plus_one i2 ⟨r 2, ha2⟩
    have hleaf3' : Leaf thirdA (wordPrefix q 3, wordPrefix r 3) := by
      simpa only [hi2, Fin.val_mk, prefix_succ, h2] using hleaf3
    have hm3 := leaf_mem _ _ hleaf3' (hs 3 (by decide) (by decide))
    obtain ⟨i3, hi3⟩ := List.mem_iff_get.mp hm3
    have hleaf4 := exclude_a_reflected_fourth i3
    have hleaf4' : Leaf [] (wordPrefix q 4, wordPrefix r 4) := by
      simpa only [hi3, prefix_getD q 3 2 (by decide),
        prefix_getD r 3 2 (by decide), prefix_succ, hq3, hr3] using hleaf4
    exact List.not_mem_nil (leaf_mem _ _ hleaf4' (hs 4 (by decide) (by decide)))
  · have ha1 : q 1 < 18 := by have := hr.2.2.1 1 (by decide); omega
    have hleaf2 := cover_b_minus_one i1 ⟨q 1, ha1⟩
    have hleaf2' : Leaf secondB (wordPrefix q 2, wordPrefix r 2) := by
      simpa only [hi1, Fin.val_mk, prefix_succ, h1] using hleaf2
    have hm2 := leaf_mem _ _ hleaf2' (hs 2 (by decide) (by decide))
    obtain ⟨i2, hi2⟩ := List.mem_iff_get.mp hm2
    have ha2 : r 2 < 19 := by have := hr.2.2.1 2 (by decide); omega
    have hleaf3 := cover_b_equal i2 ⟨r 2, ha2⟩
    have hleaf3' : Leaf thirdB (wordPrefix q 3, wordPrefix r 3) := by
      simpa only [hi2, Fin.val_mk, prefix_succ, h2] using hleaf3
    have hm3 := leaf_mem _ _ hleaf3' (hs 3 (by decide) (by decide))
    obtain ⟨i3, hi3⟩ := List.mem_iff_get.mp hm3
    have hleaf4 := exclude_b_reflected_fourth i3
    have hleaf4' : Leaf [] (wordPrefix q 4, wordPrefix r 4) := by
      simpa only [hi3, prefix_getD q 3 2 (by decide),
        prefix_getD r 3 2 (by decide), prefix_succ, hq3, hr3] using hleaf4
    exact List.not_mem_nil (leaf_mem _ _ hleaf4' (hs 4 (by decide) (by decide)))

#print axioms six_carries_exclude_width_six_profiles

end ExactSmallWidthCarryThresholds
