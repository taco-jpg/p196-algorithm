import P196.EightCarryMaximalWidth.PrefixExclusion
import P196.EightCarryThreePairSharp.ExtensionCertificate

/-!
Actual eight-observation histories exclude the remaining possible positive
third-pair difference. The shared five-column cover is imported directly;
only the minus-seven and plus-eight extensions are new here.
-/

namespace EightCarryThreePairSharp

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual SevenColumnProjection
open EightCarryMaximalWidth EightCarryMaximalWidth.PrefixHistory
open EightCarryMaximalWidth.Candidates Candidates

/-- The remaining bounded fourth-smoothing prefix cannot occur in an actual
history of eight equal complete carry observations. -/
theorem eight_carries_exclude_minus_seven_prefix
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (h7 : 7 ≤ L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (h0 : q 0 = r 0) (h1 : q 1 = r 1) (h2 : q 2 = r 2 + 1)
    (h3 : r 3 = q 3 + 3) (h4 : q 4 = r 4 + 5)
    (h5 : r 5 = q 5 + 7) (h6 : q 6 = r 6 + 8) : False := by
  have hm5 := eight_carries_force_short_core_five_prefix q r L hq hr
    (by omega) hc h0 h1 h2 h3 h4
  have hs : ∀ k, 0 < k → k ≤ 7 →
      accepted (wordPrefix q k, wordPrefix r k) = true := by
    intro k hk0 hk
    exact actual_history_survives_encoded q r L k 8 hq hr hk0 (by omega) hc
  have hm6 : (wordPrefix q 6, wordPrefix r 6) ∈ minusSevenSextuples := by
    have he := extensions_mem 0 7 12 quintuples _ _ hm5 (q 5)
      (by have := hr.2.2.1 5 (by omega); omega)
    have he' : (wordPrefix q 6, wordPrefix r 6) ∈
        extensions 0 7 12 quintuples := by
      simpa only [prefix_succ, h5, Nat.add_zero] using he
    exact covered_mem _ _ cover_minus_seven _ he' (hs 6 (by decide) (by decide))
  have he := extensions_mem 8 0 11 minusSevenSextuples _ _ hm6 (r 6)
    (by have := hq.2.2.1 6 (by omega); omega)
  have he' : (wordPrefix q 7, wordPrefix r 7) ∈
      extensions 8 0 11 minusSevenSextuples := by
    simpa only [prefix_succ, h6, Nat.add_zero] using he
  have hm := covered_mem _ _ cover_plus_eight _ he'
    (hs 7 (by decide) (by decide))
  exact List.not_mem_nil hm

#print axioms eight_carries_exclude_minus_seven_prefix

end EightCarryThreePairSharp
