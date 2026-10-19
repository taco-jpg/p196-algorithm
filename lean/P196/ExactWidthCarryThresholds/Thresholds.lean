import P196.ExactWidthCarryThresholds.Reconstruction
import P196.ExactWidthCarryThresholds.Sharpness
import P196.ExactSmallWidthCarryThresholds.Thresholds
import P196.EightCarryMaximalWidth.Reconstruction
import P196.Agent10EightCarry.DifferenceObservability

/-!
The exact complete-carry observation minima at initial widths one through
seventeen are 4, 5, 7, 6, 7, 6, 7, 7, 8, 7, 8, 8, 8, 8, 8, 8, and 9.
The predicates for active-pair recovery and next-integer recovery are the
unchanged fixed-width predicates of ExactSmallWidthCarryThresholds.

The new seven-word reconstruction at width ten is combined with the imported
small-width classification, eight-word reconstruction through width sixteen,
and universal nine-word reconstruction. Canonical counterexamples rule out
every smaller observation count. All words include terminal carries, later
widths remain unrestricted, and ordinary iteration continues after palindromes.
No exact-width classification outside the positive range through seventeen
is asserted, nor is reconstruction of the original digit split asserted.
-/

namespace ExactWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual
open ExactSmallWidthCarryThresholds
  (PairReconstructionAtWidth NextIntegerReconstructionAtWidth)

private theorem pair_threshold_sufficient (L K : Nat) (hpos : 0 < L)
    (hK : exactWidthThreshold L ≤ K) : PairReconstructionAtWidth L K := by
  by_cases hsmall : L ≤ 8
  · exact (ExactSmallWidthCarryThresholds.pair_reconstruction_iff L K hpos hsmall).mpr
      (by simpa only [exactWidthThreshold, if_pos hsmall] using hK)
  intro q r hq hr hc
  by_cases h10 : L = 10
  · subst L
    have hk : 7 ≤ K := by simpa [exactWidthThreshold] using hK
    exact seven_carry_words_determine_pair_sums_of_width_ten
      q r hq hr (fun t ht i hi => hc t (by omega) i hi)
  by_cases h16 : L ≤ 16
  · have hk : 8 ≤ K := by
      simpa only [exactWidthThreshold, if_neg hsmall, if_neg h10, if_pos h16] using hK
    exact EightCarryMaximalWidth.eight_carry_words_determine_pair_sums_of_width_le_sixteen
      q r L hq hr h16 (fun t ht i hi => hc t (by omega) i hi)
  have hk : 9 ≤ K := by
    simpa only [exactWidthThreshold, if_neg hsmall, if_neg h10, if_neg h16] using hK
  exact DifferenceObservability.nine_carry_words_determine_pair_sums
    q r L hq hr (fun t ht i hi => hc t (by omega) i hi)

/-- The minimum number of complete observations for active-pair reconstruction
at each positive exact initial width through seventeen. -/
theorem pair_reconstruction_iff (L K : Nat)
    (hpos : 0 < L) (hwidth : L ≤ 17) :
    PairReconstructionAtWidth L K ↔ exactWidthThreshold L ≤ K := by
  constructor
  · intro h
    by_cases hk : exactWidthThreshold L ≤ K
    · exact hk
    · exfalso
      rcases exact_width_counterexample L hpos hwidth with
        ⟨n, m, d, e, hn, hm, hc, ⟨i, hi, hne⟩, _⟩
      apply hne
      exact h (columnSum d L) (columnSum e L)
        (NormalizationBridge.canonical_admissible n d L hn)
        (NormalizationBridge.canonical_admissible m e L hm)
        (fun t ht j hj => hc t (by omega) j hj) i hi
  · exact pair_threshold_sufficient L K hpos

/-- The same exact thresholds recover the next ordinary integer from canonical
inputs at the specified initial width, for every observation count. -/
theorem next_integer_reconstruction_iff (L K : Nat)
    (hpos : 0 < L) (hwidth : L ≤ 17) :
    NextIntegerReconstructionAtWidth L K ↔ exactWidthThreshold L ≤ K := by
  constructor
  · intro h
    by_cases hk : exactWidthThreshold L ≤ K
    · exact hk
    · exfalso
      rcases exact_width_counterexample L hpos hwidth with
        ⟨n, m, d, e, hn, hm, hc, _, hne⟩
      apply hne
      exact h n m d e hn hm (fun t ht i hi => hc t (by omega) i hi)
  · intro hK
    exact ExactSmallWidthCarryThresholds.next_integer_reconstruction_of_pair_reconstruction L K
      ((pair_reconstruction_iff L K hpos hwidth).mpr hK)

#print axioms pair_reconstruction_iff
#print axioms next_integer_reconstruction_iff

end ExactWidthCarryThresholds
