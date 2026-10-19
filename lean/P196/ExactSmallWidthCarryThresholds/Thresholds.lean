import P196.ExactSmallWidthCarryThresholds.Reconstruction
import P196.ExactSmallWidthCarryThresholds.Sharpness
import P196.CarryWidthThresholds.SmallWidths
import P196.SevenCarryMaximalWidth.Reconstruction

/-!
The exact complete-carry observation minima at initial widths one through
eight are 4, 5, 7, 6, 7, 6, 7, and 7. Width is fixed separately in each
input class; the resulting thresholds need not increase with width.

The new six-word reconstruction at widths four and six is combined with
imported positive results at the remaining widths. The canonical witnesses
in Sharpness rule out every smaller observation count for both pair recovery
and next-integer recovery. All observations include terminal carries, later
widths remain unrestricted, and iteration continues after palindromes.
-/

namespace ExactSmallWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

private theorem pair_threshold_sufficient (L K : Nat) (hsmall : L ≤ 8)
    (hK : exactWidthThreshold L ≤ K) : PairReconstructionAtWidth L K := by
  intro q r hq hr hc
  by_cases h1 : L = 1
  · subst L
    have hk : 4 ≤ K := by simpa [exactWidthThreshold] using hK
    exact CarryWidthThresholds.four_carry_words_determine_pair_sums_of_width_one
      q r hq hr (fun t ht i hi => hc t (by omega) i hi)
  by_cases h2 : L = 2
  · subst L
    have hk : 5 ≤ K := by simpa [exactWidthThreshold] using hK
    exact CarryWidthThresholds.five_carry_words_determine_pair_sums_of_width_two
      q r hq hr (fun t ht i hi => hc t (by omega) i hi)
  by_cases h4 : L = 4
  · subst L
    have hk : 6 ≤ K := by simpa [exactWidthThreshold] using hK
    exact six_carry_words_determine_pair_sums_of_width_four
      q r hq hr (fun t ht i hi => hc t (by omega) i hi)
  by_cases h6 : L = 6
  · subst L
    have hk : 6 ≤ K := by simpa [exactWidthThreshold] using hK
    exact six_carry_words_determine_pair_sums_of_width_six
      q r hq hr (fun t ht i hi => hc t (by omega) i hi)
  have hk : 7 ≤ K := by simpa [exactWidthThreshold, h1, h2, h4, h6] using hK
  exact SevenCarryMaximalWidth.seven_carry_words_determine_pair_sums_of_width_le_eight
    q r L hq hr hsmall (fun t ht i hi => hc t (by omega) i hi)

/-- Complete classification of active-pair reconstruction at every exact
initial width from one through eight, for all observation counts. -/
theorem pair_reconstruction_iff (L K : Nat)
    (hpos : 0 < L) (hsmall : L ≤ 8) :
    PairReconstructionAtWidth L K ↔ exactWidthThreshold L ≤ K := by
  constructor
  · intro h
    by_cases hk : exactWidthThreshold L ≤ K
    · exact hk
    · exfalso
      rcases exact_width_counterexample L hpos hsmall with
        ⟨n, m, d, e, hn, hm, hc, ⟨i, hi, hne⟩, _⟩
      apply hne
      exact h (columnSum d L) (columnSum e L)
        (NormalizationBridge.canonical_admissible n d L hn)
        (NormalizationBridge.canonical_admissible m e L hm)
        (fun t ht j hj => hc t (by omega) j hj) i hi
  · exact pair_threshold_sufficient L K hsmall

/-- The same exact-width thresholds recover the next ordinary integer from
shared-width canonical inputs, without identifying their initial digit split. -/
theorem next_integer_reconstruction_iff (L K : Nat)
    (hpos : 0 < L) (hsmall : L ≤ 8) :
    NextIntegerReconstructionAtWidth L K ↔ exactWidthThreshold L ≤ K := by
  constructor
  · intro h
    by_cases hk : exactWidthThreshold L ≤ K
    · exact hk
    · exfalso
      rcases exact_width_counterexample L hpos hsmall with
        ⟨n, m, d, e, hn, hm, hc, _, hne⟩
      apply hne
      exact h n m d e hn hm (fun t ht i hi => hc t (by omega) i hi)
  · intro hK
    exact next_integer_reconstruction_of_pair_reconstruction L K
      ((pair_reconstruction_iff L K hpos hsmall).mpr hK)

#print axioms pair_reconstruction_iff
#print axioms next_integer_reconstruction_iff

end ExactSmallWidthCarryThresholds
