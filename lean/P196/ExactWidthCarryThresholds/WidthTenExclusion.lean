import P196.EightCarryMaximalWidth.PrefixExclusion
import P196.SevenCarryMaximalWidth.BaseCertificate
import P196.SevenCarryMaximalWidth.MinusTwoCertificate
import P196.SevenCarryMaximalWidth.CenterTwoCertificate
import P196.ExactWidthCarryThresholds.OddFourthCertificate
import P196.ExactWidthCarryThresholds.FifthCertificate
import P196.ExactWidthCarryThresholds.ReflectionCertificate

/-!
The oriented residual width-ten profile is incompatible with seven equal
complete carry observations. The imported covers handle the first three
coefficients and the even fourth coefficient. The new odd cover completes
the fourth coefficient, and the fifth cover followed by exact width-ten
reflection excludes the remaining prefixes. All covers are one-sided.

The actual history theorem for the imported encoded checker is instantiated
separately at each required prefix length, always with seven observations.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual SevenColumnProjection
open EightCarryMaximalWidth (prefix_succ)
open EightCarryMaximalWidth.PrefixHistory
open SevenCarryMaximalWidth.Candidates
open WidthTenCandidates

/-- The positively oriented width-ten residual profile cannot occur in an
admissible history of seven matching complete carry words. -/
theorem seven_carries_exclude_width_ten_profile
    (q r : Nat → Nat) (hq : Admissible 10 q) (hr : Admissible 10 r)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q 10 t).1 →
      carry (iterPairs q 10 t).2 i = carry (iterPairs r 10 t).2 i)
    (h0 : q 0 = r 0) (h1 : q 1 = r 1 + 1)
    (h2 : r 2 = q 2 + 2) (h3 : q 3 = r 3 + 2)
    (h4 : r 4 = q 4 + 1) : False := by
  have hs : ∀ k, 0 < k → k ≤ 10 →
      survivesEncoded 7 (wordPrefix q k) (wordPrefix r k) = true := by
    intro k hk0 hk
    exact actual_history_survives_encoded q r 10 k 7 hq hr hk0 hk hc
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
  have ha2 : q 2 < 17 := by have := hr.2.2.1 2 (by decide); omega
  have hleaf3 := cover_minus_two i2 ⟨q 2, ha2⟩
  have hleaf3' : Leaf minusTwoTriples (wordPrefix q 3, wordPrefix r 3) := by
    simpa only [hi2, Fin.val_mk, prefix_succ, h2] using hleaf3
  have hm3 := leaf_mem _ _ hleaf3' (hs 3 (by decide) (by decide))
  obtain ⟨i3, hi3⟩ := List.mem_iff_get.mp hm3
  have hm4 : (wordPrefix q 4, wordPrefix r 4) ∈ quadruples := by
    change (wordPrefix q 4, wordPrefix r 4) ∈
      centerTwoQuadruples ++ oddFourthQuadruples
    by_cases heven : r 3 % 2 = 0
    · have hhalf : 2 * (r 3 / 2) = r 3 := by omega
      have ha3 : r 3 / 2 < 9 := by have := hq.2.2.1 3 (by decide); omega
      have hleaf4 := cover_center_two i3 ⟨r 3 / 2, ha3⟩
      have hleaf4' : Leaf centerTwoQuadruples
          (wordPrefix q 4, wordPrefix r 4) := by
        simpa only [hi3, Fin.val_mk, hhalf, prefix_succ, h3] using hleaf4
      exact List.mem_append.mpr
        (Or.inl (leaf_mem _ _ hleaf4' (hs 4 (by decide) (by decide))))
    · have hodd : r 3 % 2 = 1 := by
        have := Nat.mod_lt (r 3) (by decide : 0 < 2)
        omega
      have hhalf : 2 * (r 3 / 2) + 1 = r 3 := by omega
      have ha3 : r 3 / 2 < 8 := by have := hq.2.2.1 3 (by decide); omega
      have hq3 : 2 * (r 3 / 2) + 3 = q 3 := by omega
      have hleaf4 := cover_odd_fourth i3 ⟨r 3 / 2, ha3⟩
      have hleaf4' : Leaf oddFourthQuadruples
          (wordPrefix q 4, wordPrefix r 4) := by
        simpa only [hi3, Fin.val_mk, hhalf, hq3, prefix_succ] using hleaf4
      exact List.mem_append.mpr
        (Or.inr (leaf_mem _ _ hleaf4' (hs 4 (by decide) (by decide))))
  obtain ⟨i4, hi4⟩ := List.mem_iff_get.mp hm4
  have ha4 : q 4 < 18 := by have := hr.2.2.1 4 (by decide); omega
  have hleaf5 := cover_fifth i4 ⟨q 4, ha4⟩
  have hleaf5' : Leaf quintuples (wordPrefix q 5, wordPrefix r 5) := by
    simpa only [hi4, Fin.val_mk, prefix_succ, h4] using hleaf5
  have hm5 := leaf_mem _ _ hleaf5' (hs 5 (by decide) (by decide))
  obtain ⟨i5, hi5⟩ := List.mem_iff_get.mp hm5
  have hq5 : q 5 = q 4 := hq.2.2.2.1 5 (by decide)
  have hr5 : r 5 = r 4 := hr.2.2.2.1 5 (by decide)
  have hleaf6 := exclude_reflected_sixth i5
  have hleaf6' : Leaf [] (wordPrefix q 6, wordPrefix r 6) := by
    simpa only [hi5, prefix_getD q 5 4 (by decide),
      prefix_getD r 5 4 (by decide), prefix_succ, hq5, hr5] using hleaf6
  exact List.not_mem_nil (leaf_mem _ _ hleaf6' (hs 6 (by decide) (by decide)))

#print axioms seven_carries_exclude_width_ten_profile

end ExactWidthCarryThresholds
