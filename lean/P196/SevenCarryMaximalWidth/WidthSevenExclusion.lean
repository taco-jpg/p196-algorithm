import P196.EightCarryMaximalWidth.PrefixExclusion
import P196.SevenCarryMaximalWidth.BaseCertificate
import P196.SevenCarryMaximalWidth.MinusThreeCertificate
import P196.SevenCarryMaximalWidth.MinusTwoCertificate
import P196.SevenCarryMaximalWidth.CenterFourCertificate
import P196.SevenCarryMaximalWidth.CenterTwoCertificate
import P196.SevenCarryMaximalWidth.ReflectionCertificate

/-!
The two possible nonzero width-seven profiles cannot occur in an actual
history of seven equal complete carry observations. Center parity narrows
the fourth coefficient, and symmetry supplies the fifth coefficient.
All finite exclusions use the imported encoded prefix checker. Its actual
history theorem is instantiated separately at each required prefix length.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SevenCarryMaximalWidth

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual SevenColumnProjection
open EightCarryMaximalWidth (prefix_succ)
open EightCarryMaximalWidth.PrefixHistory
open SevenCarryMaximalWidth.Candidates

/-- Neither oriented symmetric width-seven profile can have seven matching
complete carry words. Admissibility supplies the remaining reflected entries. -/
theorem seven_carries_exclude_width_seven_profiles
    (q r : Nat → Nat) (hq : Admissible 7 q) (hr : Admissible 7 r)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q 7 t).1 →
      carry (iterPairs q 7 t).2 i = carry (iterPairs r 7 t).2 i)
    (h0 : q 0 = r 0) (h1 : q 1 = r 1 + 1)
    (hcases : (r 2 = q 2 + 3 ∧ q 3 = r 3 + 4) ∨
      (r 2 = q 2 + 2 ∧ q 3 = r 3 + 2)) : False := by
  have hs : ∀ k, 0 < k → k ≤ 7 →
      survivesEncoded 7 (wordPrefix q k) (wordPrefix r k) = true := by
    intro k hk0 hk
    exact actual_history_survives_encoded q r 7 k 7 hq hr hk0 hk hc
  have hm2 : (wordPrefix q 2, wordPrefix r 2) ∈ pairs := by
    have hp : q 0 - 1 < 18 := by
      have := hq.2.2.1 0 (by decide)
      omega
    have ha : r 1 < 18 := by
      have := hq.2.2.1 1 (by decide)
      omega
    have hp0 : q 0 - 1 + 1 = q 0 := by have := hq.2.1; omega
    have hleaf := cover_pairs ⟨q 0 - 1, hp⟩ ⟨r 1, ha⟩
    have hleaf' : Leaf pairs (wordPrefix q 2, wordPrefix r 2) := by
      change Leaf pairs ([q 0, q 1], [r 0, r 1])
      simpa only [Fin.val_mk, hp0, ← h0, h1] using hleaf
    exact leaf_mem _ _ hleaf' (hs 2 (by decide) (by decide))
  obtain ⟨i2, hi2⟩ := List.mem_iff_get.mp hm2
  have heven : r 3 % 2 = 0 := hr.2.2.2.2 3 (by decide) (by decide)
  have hhalf : 2 * (r 3 / 2) = r 3 := by omega
  rcases hcases with ⟨h2, h3⟩ | ⟨h2, h3⟩
  · have ha : q 2 < 16 := by have := hr.2.2.1 2 (by decide); omega
    have hleaf3 := cover_minus_three i2 ⟨q 2, ha⟩
    have hleaf3' : Leaf minusThreeTriples (wordPrefix q 3, wordPrefix r 3) := by
      simpa only [hi2, Fin.val_mk, prefix_succ, h2] using hleaf3
    have hm3 := leaf_mem _ _ hleaf3' (hs 3 (by decide) (by decide))
    obtain ⟨i3, hi3⟩ := List.mem_iff_get.mp hm3
    have ha3 : r 3 / 2 < 8 := by have := hq.2.2.1 3 (by decide); omega
    have hleaf4 := exclude_center_four i3 ⟨r 3 / 2, ha3⟩
    have hleaf4' : Leaf [] (wordPrefix q 4, wordPrefix r 4) := by
      simpa only [hi3, Fin.val_mk, hhalf, prefix_succ, h3] using hleaf4
    exact List.not_mem_nil (leaf_mem _ _ hleaf4' (hs 4 (by decide) (by decide)))
  · have ha : q 2 < 17 := by have := hr.2.2.1 2 (by decide); omega
    have hleaf3 := cover_minus_two i2 ⟨q 2, ha⟩
    have hleaf3' : Leaf minusTwoTriples (wordPrefix q 3, wordPrefix r 3) := by
      simpa only [hi2, Fin.val_mk, prefix_succ, h2] using hleaf3
    have hm3 := leaf_mem _ _ hleaf3' (hs 3 (by decide) (by decide))
    obtain ⟨i3, hi3⟩ := List.mem_iff_get.mp hm3
    have ha3 : r 3 / 2 < 9 := by have := hq.2.2.1 3 (by decide); omega
    have hleaf4 := cover_center_two i3 ⟨r 3 / 2, ha3⟩
    have hleaf4' : Leaf centerTwoQuadruples (wordPrefix q 4, wordPrefix r 4) := by
      simpa only [hi3, Fin.val_mk, hhalf, prefix_succ, h3] using hleaf4
    have hm4 := leaf_mem _ _ hleaf4' (hs 4 (by decide) (by decide))
    obtain ⟨i4, hi4⟩ := List.mem_iff_get.mp hm4
    have hq4 : q 4 = q 2 := hq.2.2.2.1 4 (by decide)
    have hr4 : r 4 = r 2 := hr.2.2.2.1 4 (by decide)
    have hleaf5 := exclude_reflected_fifth i4
    have hleaf5' : Leaf [] (wordPrefix q 5, wordPrefix r 5) := by
      simpa only [hi4, prefix_getD q 4 2 (by decide),
        prefix_getD r 4 2 (by decide), prefix_succ, hq4, hr4] using hleaf5
    exact List.not_mem_nil (leaf_mem _ _ hleaf5' (hs 5 (by decide) (by decide)))

#print axioms seven_carries_exclude_width_seven_profiles

end SevenCarryMaximalWidth
