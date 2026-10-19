import P196.CarryWidthThresholds.SmallWidths
import P196.CarryWidthThresholds.SmallWitnesses
import P196.SevenCarryMaximalWidth.Sharpness

/-!
The exact observation threshold for every cumulative initial-width class.
The two reconstruction predicates are imported from EightCarryMaximalWidth.
The new small-width upper bounds and canonical witnesses complete the existing
seven-, eight-, and nine-observation results without repeating their proofs.

The threshold is zero for the empty width class, four at width bound one,
five at two, seven from three through eight, eight from nine through sixteen,
and nine thereafter. These are uniform thresholds over all positive initial
widths up to the bound, not claims of optimality at each exact width. All
observations include the terminal carry; later widths and continued ordinary
iteration are unrestricted. No initial-digit injectivity or palindrome
avoidance is asserted.
-/

namespace CarryWidthThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual EightCarryMaximalWidth

/-- Exact number of complete carry observations required uniformly over all
positive admissible initial widths at most `W`. -/
def widthThreshold (W : Nat) : Nat :=
  if W = 0 then 0 else
  if W = 1 then 4 else
  if W = 2 then 5 else
  if W ≤ 8 then 7 else
  if W ≤ 16 then 8 else 9

/-- Uniform active-pair reconstruction implies uniform next-integer
reconstruction at the same width and observation bounds. -/
theorem next_integer_reconstruction_of_pair_reconstruction (W K : Nat)
    (h : PairReconstructionUpTo W K) : NextIntegerReconstructionUpTo W K := by
  intro n m d e L hn hm hL hc
  have he := h (columnSum d L) (columnSum e L) L
    (NormalizationBridge.canonical_admissible n d L hn)
    (NormalizationBridge.canonical_admissible m e L hm) hL hc
  calc
    Lychrel196.step n = value (columnSum d L) L :=
      step_eq_word_value n d (columnSum d L) L hn (by intro i hi; rfl)
    _ = value (columnSum e L) L := value_congr _ _ L he
    _ = Lychrel196.step m :=
      (step_eq_word_value m e (columnSum e L) L hm (by intro i hi; rfl)).symm

private theorem pair_more_observations (W K J : Nat)
    (h : PairReconstructionUpTo W K) (hK : K ≤ J) :
    PairReconstructionUpTo W J := by
  intro q r L hq hr hL hc
  exact h q r L hq hr hL (fun t ht i hi => hc t (by omega) i hi)

private theorem next_more_observations (W K J : Nat)
    (h : NextIntegerReconstructionUpTo W K) (hK : K ≤ J) :
    NextIntegerReconstructionUpTo W J := by
  intro n m d e L hn hm hL hc
  exact h n m d e L hn hm hL (fun t ht i hi => hc t (by omega) i hi)

private theorem small_pair_lower (w : Fin 3) (W K : Nat)
    (hW : SmallWitnesses.width w ≤ W) (h : PairReconstructionUpTo W K) :
    SmallWitnesses.observations w < K := by
  by_cases hK : SmallWitnesses.observations w < K
  · exact hK
  · exfalso
    have he := h (SmallWitnesses.columns w false) (SmallWitnesses.columns w true)
      (SmallWitnesses.width w) (SmallWitnesses.admissible w false)
      (SmallWitnesses.admissible w true) hW
      (fun t ht i hi => SmallWitnesses.complete_carries w t (by omega) i hi)
      0 (SmallWitnesses.initial_pair_difference_active w).1
    exact (SmallWitnesses.initial_pair_difference_active w).2 he

private theorem small_next_lower (w : Fin 3) (W K : Nat)
    (hW : SmallWitnesses.width w ≤ W) (h : NextIntegerReconstructionUpTo W K) :
    SmallWitnesses.observations w < K := by
  by_cases hK : SmallWitnesses.observations w < K
  · exact hK
  · exfalso
    apply SmallWitnesses.next_integers_differ w
    exact h (SmallWitnesses.seed w false) (SmallWitnesses.seed w true)
      (SmallWitnesses.digits w false) (SmallWitnesses.digits w true)
      (SmallWitnesses.width w) (SmallWitnesses.canonical w false)
      (SmallWitnesses.canonical w true) hW
      (fun t ht i hi => SmallWitnesses.complete_carries w t (by omega) i hi)

private theorem pair_threshold_sufficient (W K : Nat)
    (hK : widthThreshold W ≤ K) : PairReconstructionUpTo W K := by
  intro q r L hq hr hL hc
  by_cases h0 : W = 0
  · have hp := hq.1
    omega
  by_cases h1 : W = 1
  · have hL1 : L = 1 := by have hp := hq.1; omega
    subst L
    have hk : 4 ≤ K := by simpa [widthThreshold, h1] using hK
    exact four_carry_words_determine_pair_sums_of_width_one q r hq hr
      (fun t ht i hi => hc t (by omega) i hi)
  by_cases h2 : W = 2
  · have hk : 5 ≤ K := by simpa [widthThreshold, h2] using hK
    by_cases hL1 : L = 1
    · subst L
      exact four_carry_words_determine_pair_sums_of_width_one q r hq hr
        (fun t ht i hi => hc t (by omega) i hi)
    · have hL2 : L = 2 := by have hp := hq.1; omega
      subst L
      exact five_carry_words_determine_pair_sums_of_width_two q r hq hr
        (fun t ht i hi => hc t (by omega) i hi)
  by_cases h8 : W ≤ 8
  · have hk : 7 ≤ K := by simpa [widthThreshold, h0, h1, h2, h8] using hK
    exact SevenCarryMaximalWidth.seven_carry_words_determine_pair_sums_of_width_le_eight
      q r L hq hr (by omega) (fun t ht i hi => hc t (by omega) i hi)
  by_cases h16 : W ≤ 16
  · have hk : 8 ≤ K := by
      simpa [widthThreshold, h0, h1, h2, h8, h16] using hK
    exact eight_carry_words_determine_pair_sums_of_width_le_sixteen
      q r L hq hr (by omega) (fun t ht i hi => hc t (by omega) i hi)
  · have hk : 9 ≤ K := by
      simpa [widthThreshold, h0, h1, h2, h8, h16] using hK
    exact DifferenceObservability.nine_carry_words_determine_pair_sums
      q r L hq hr (fun t ht i hi => hc t (by omega) i hi)

/-- Complete classification of active-pair reconstruction for every width
bound and every number of complete carry observations. -/
theorem pair_reconstruction_iff (W K : Nat) :
    PairReconstructionUpTo W K ↔ widthThreshold W ≤ K := by
  constructor
  · intro h
    by_cases h0 : W = 0
    · simp [widthThreshold, h0]
    by_cases h1 : W = 1
    · have hs := small_pair_lower (0 : Fin 3) W K
        (by simpa [SmallWitnesses.width, h1]) h
      have hk : 3 < K := by simpa [SmallWitnesses.observations] using hs
      simpa [widthThreshold, h1] using (show 4 ≤ K by omega)
    by_cases h2 : W = 2
    · have hs := small_pair_lower (1 : Fin 3) W K
        (by simpa [SmallWitnesses.width, h2]) h
      have hk : 4 < K := by simpa [SmallWitnesses.observations] using hs
      simpa [widthThreshold, h2] using (show 5 ≤ K by omega)
    by_cases h8 : W ≤ 8
    · have hw : SmallWitnesses.width (2 : Fin 3) ≤ W := by
        change 3 ≤ W
        omega
      have hs := small_pair_lower (2 : Fin 3) W K hw h
      have hk : 6 < K := by simpa [SmallWitnesses.observations] using hs
      simpa [widthThreshold, h0, h1, h2, h8] using (show 7 ≤ K by omega)
    by_cases h16 : W ≤ 16
    · have hk : 8 ≤ K := by
        by_cases hk : 8 ≤ K
        · exact hk
        · have hw := (SevenCarryMaximalWidth.seven_pair_reconstruction_iff_width_le_eight W).mp
            (pair_more_observations W K 7 h (by omega))
          omega
      simpa [widthThreshold, h0, h1, h2, h8, h16] using hk
    · have hk : 9 ≤ K := by
        by_cases hk : 9 ≤ K
        · exact hk
        · have hw := (eight_pair_reconstruction_iff_width_le_sixteen W).mp
            (pair_more_observations W K 8 h (by omega))
          omega
      simpa [widthThreshold, h0, h1, h2, h8, h16] using hk
  · exact pair_threshold_sufficient W K

/-- The same exact threshold classifies reconstruction of the next ordinary
integer from shared-width canonical decimal inputs. -/
theorem next_integer_reconstruction_iff (W K : Nat) :
    NextIntegerReconstructionUpTo W K ↔ widthThreshold W ≤ K := by
  constructor
  · intro h
    by_cases h0 : W = 0
    · simp [widthThreshold, h0]
    by_cases h1 : W = 1
    · have hs := small_next_lower (0 : Fin 3) W K
        (by simpa [SmallWitnesses.width, h1]) h
      have hk : 3 < K := by simpa [SmallWitnesses.observations] using hs
      simpa [widthThreshold, h1] using (show 4 ≤ K by omega)
    by_cases h2 : W = 2
    · have hs := small_next_lower (1 : Fin 3) W K
        (by simpa [SmallWitnesses.width, h2]) h
      have hk : 4 < K := by simpa [SmallWitnesses.observations] using hs
      simpa [widthThreshold, h2] using (show 5 ≤ K by omega)
    by_cases h8 : W ≤ 8
    · have hw : SmallWitnesses.width (2 : Fin 3) ≤ W := by
        change 3 ≤ W
        omega
      have hs := small_next_lower (2 : Fin 3) W K hw h
      have hk : 6 < K := by simpa [SmallWitnesses.observations] using hs
      simpa [widthThreshold, h0, h1, h2, h8] using (show 7 ≤ K by omega)
    by_cases h16 : W ≤ 16
    · have hk : 8 ≤ K := by
        by_cases hk : 8 ≤ K
        · exact hk
        · have hw :=
            (SevenCarryMaximalWidth.seven_next_integer_reconstruction_iff_width_le_eight W).mp
            (next_more_observations W K 7 h (by omega))
          omega
      simpa [widthThreshold, h0, h1, h2, h8, h16] using hk
    · have hk : 9 ≤ K := by
        by_cases hk : 9 ≤ K
        · exact hk
        · have hw := (eight_next_integer_reconstruction_iff_width_le_sixteen W).mp
            (next_more_observations W K 8 h (by omega))
          omega
      simpa [widthThreshold, h0, h1, h2, h8, h16] using hk
  · intro hK
    exact next_integer_reconstruction_of_pair_reconstruction W K
      (pair_reconstruction_iff W K |>.mpr hK)

#print axioms next_integer_reconstruction_of_pair_reconstruction
#print axioms pair_reconstruction_iff
#print axioms next_integer_reconstruction_iff

end CarryWidthThresholds
