import P196.CarryWidthThresholds.Thresholds
import P196.CarryPrefixThresholds.Thresholds

/-!
The exact joint threshold for bounded initial widths and requested active
pair prefixes. The threshold is the minimum of the existing full-profile
width threshold and the existing arbitrary-width prefix threshold.

All lower witnesses and positive reconstruction theorems are imported.
The width bound applies to the common initial width; subsequent widths are
unrestricted. Carry words include their terminal carries, and ordinary
iteration continues after palindromes. Recovered indices must be active.
This result concerns cumulative width classes, not individual-width minima
or recovery of the original decimal digit splitting.
-/

namespace BoundedCarryPrefixThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual CarryWidthThresholds CarryPrefixThresholds

/-- Uniform recovery of the active initial pair coefficients below `J`
from `K` complete carry observations at every admissible width at most `W`. -/
def PrefixReconstructionUpTo (W J K : Nat) : Prop :=
  ∀ (q r : Nat → Nat) (L : Nat), Admissible L q → Admissible L r → L ≤ W →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) →
    ∀ i, i < J → i < L → q i = r i

private theorem small_witness_lower (w : Fin 3) (W J K : Nat)
    (h : PrefixReconstructionUpTo W J K)
    (hW : SmallWitnesses.width w ≤ W) (hJ : 0 < J) :
    SmallWitnesses.observations w < K := by
  by_cases hK : SmallWitnesses.observations w < K
  · exact hK
  · exfalso
    have he := h (SmallWitnesses.columns w false) (SmallWitnesses.columns w true)
      (SmallWitnesses.width w) (SmallWitnesses.admissible w false)
      (SmallWitnesses.admissible w true) hW
      (fun t ht i hi => SmallWitnesses.complete_carries w t (by omega) i hi)
      0 hJ (SmallWitnesses.initial_pair_difference_active w).1
    exact (SmallWitnesses.initial_pair_difference_active w).2 he

private theorem eight_le_of_second_pair (W J K : Nat)
    (h : PrefixReconstructionUpTo W J K) (hW : 9 ≤ W) (hJ : 2 ≤ J) :
    8 ≤ K := by
  by_cases hK : 8 ≤ K
  · exact hK
  · exfalso
    have he := h SevenCarryWitness.leftColumns SevenCarryWitness.rightColumns 9
      SevenCarryWitness.left_admissible SevenCarryWitness.right_admissible hW
      (fun t ht i hi => SevenCarryWitness.seven_complete_carries
        t (by omega) i hi) 1 (by omega) (by decide)
    exact SevenCarryWitness.initial_pair_difference_active.2 he

private theorem nine_le_of_fourth_pair (W J K : Nat)
    (h : PrefixReconstructionUpTo W J K) (hW : 17 ≤ W) (hJ : 4 ≤ J) :
    9 ≤ K := by
  by_cases hK : 9 ≤ K
  · exact hK
  · exfalso
    have hl := NormalizationBridge.canonical_admissible
      90000000560706169 Agent10EightCarryCounterexample.leftDigits 17
      Agent10EightCarryCounterexample.left_canonical
    have hr := NormalizationBridge.canonical_admissible
      90000000806235169 Agent10EightCarryCounterexample.rightDigits 17
      Agent10EightCarryCounterexample.right_canonical
    have he := h Agent10EightCarryCounterexample.leftColumns
      Agent10EightCarryCounterexample.rightColumns 17 hl hr hW
      (fun t ht i hi => Agent10EightCarryCounterexample.eight_complete_carries
        t (by omega) i hi) 3 (by omega) (by decide)
    exact Agent10EightCarryCounterexample.initial_pair_difference_active.2 he

/-- The exact observation threshold under simultaneous initial-width and
active-prefix bounds is the minimum of the two separate thresholds. -/
theorem reconstruction_iff (W J K : Nat) :
    PrefixReconstructionUpTo W J K ↔
      min (CarryWidthThresholds.widthThreshold W)
        (CarryPrefixThresholds.prefixThreshold J) ≤ K := by
  constructor
  · intro h
    by_cases hW0 : W = 0
    · simp [widthThreshold, hW0]
    by_cases hJ0 : J = 0
    · simp [prefixThreshold, hJ0]
    have hJpos : 0 < J := by omega
    by_cases hW1 : W = 1
    · have hs := small_witness_lower (0 : Fin 3) W J K h
        (by simp [SmallWitnesses.width, hW1]) hJpos
      have hk : 4 ≤ K := by
        have hh : 3 < K := by simpa [SmallWitnesses.observations] using hs
        omega
      simpa [widthThreshold, hW1] using
        (show min 4 (prefixThreshold J) ≤ K by omega)
    by_cases hW2 : W = 2
    · have hs := small_witness_lower (1 : Fin 3) W J K h
        (by simp [SmallWitnesses.width, hW2]) hJpos
      have hk : 5 ≤ K := by
        have hh : 4 < K := by simpa [SmallWitnesses.observations] using hs
        omega
      simpa [widthThreshold, hW2] using
        (show min 5 (prefixThreshold J) ≤ K by omega)
    have h7 : 7 ≤ K := by
      have hs := small_witness_lower (2 : Fin 3) W J K h
        (by change 3 ≤ W; omega) hJpos
      have hh : 6 < K := by simpa [SmallWitnesses.observations] using hs
      omega
    by_cases hJ1 : J = 1
    · simpa [prefixThreshold, hJ1] using
        (show min (widthThreshold W) 7 ≤ K by omega)
    by_cases hW8 : W ≤ 8
    · simpa [widthThreshold, hW0, hW1, hW2, hW8] using
        (show min 7 (prefixThreshold J) ≤ K by omega)
    have h8 := eight_le_of_second_pair W J K h (by omega) (by omega)
    by_cases hJ3 : J ≤ 3
    · simpa [prefixThreshold, hJ0, hJ1, hJ3] using
        (show min (widthThreshold W) 8 ≤ K by omega)
    by_cases hW16 : W ≤ 16
    · simpa [widthThreshold, hW0, hW1, hW2, hW8, hW16] using
        (show min 8 (prefixThreshold J) ≤ K by omega)
    have h9 := nine_le_of_fourth_pair W J K h (by omega) (by omega)
    simpa [widthThreshold, prefixThreshold, hW0, hW1, hW2, hW8, hW16,
      hJ0, hJ1, hJ3] using h9
  · intro h q r L hq hr hL hc i hi hiL
    have hroute : widthThreshold W ≤ K ∨ prefixThreshold J ≤ K := by omega
    rcases hroute with hw | hj
    · exact (CarryWidthThresholds.pair_reconstruction_iff W K).mpr hw
        q r L hq hr hL hc i hiL
    · exact (CarryPrefixThresholds.prefix_reconstruction_iff J K).mpr hj
        q r L hq hr hc i hi hiL

/-- The joint reconstruction property holds exactly when either the full
bounded-width theorem or the arbitrary-width prefix theorem applies. -/
theorem reconstruction_iff_either (W J K : Nat) :
    PrefixReconstructionUpTo W J K ↔
      EightCarryMaximalWidth.PairReconstructionUpTo W K ∨
        CarryPrefixThresholds.PrefixReconstruction J K := by
  rw [reconstruction_iff, CarryWidthThresholds.pair_reconstruction_iff,
    CarryPrefixThresholds.prefix_reconstruction_iff]
  omega

/-- Requesting indices beyond the width bound adds no active coefficients. -/
theorem prefix_cutoff_reduction (W J K : Nat) :
    PrefixReconstructionUpTo W J K ↔
      PrefixReconstructionUpTo W (min J W) K := by
  constructor
  · intro h q r L hq hr hL hc i hi hiL
    exact h q r L hq hr hL hc i (by omega) hiL
  · intro h q r L hq hr hL hc i hi hiL
    exact h q r L hq hr hL hc i (by omega) hiL

#print axioms reconstruction_iff
#print axioms reconstruction_iff_either
#print axioms prefix_cutoff_reduction

end BoundedCarryPrefixThresholds
