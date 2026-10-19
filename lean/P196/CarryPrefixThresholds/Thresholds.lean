import P196.CarryPrefixThresholds.ExteriorReconstruction
import P196.CarryPrefixThresholds.SevenCarryWitness
import P196.EightCarryThreePairSharp.Sharpness
import P196.Agent10CarryObservability.Agent10SixCarryCounterexample

/-!
Agent #10: the exact observation count for every uniform active pair prefix.

Seven complete carry words recover the exterior coefficient; eight recover
the first three; nine recover all active coefficients. The matching lower
bounds use canonical witnesses differing at indices zero, one, and three.
Only the middle witness and the seven-word upper bound are new in this result.
The initial width is arbitrary, terminal carries are included, and iteration
continues after palindromes.
-/

namespace CarryPrefixThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- Minimum complete observation count for a uniform prefix of length `J`. -/
def prefixThreshold (J : Nat) : Nat :=
  if J = 0 then 0 else if J = 1 then 7 else if J ≤ 3 then 8 else 9

/-- At every common admissible initial width, `K` complete carry observations
determine every active initial pair coefficient with index below `J`. -/
def PrefixReconstruction (J K : Nat) : Prop :=
  ∀ (q r : Nat → Nat) (L : Nat), Admissible L q → Admissible L r →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) →
    ∀ i, i < J → i < L → q i = r i

private theorem seven_le_of_nonempty_prefix (J K : Nat)
    (h : PrefixReconstruction J K) (hJ : 0 < J) : 7 ≤ K := by
  by_cases hK : 7 ≤ K
  · exact hK
  · exfalso
    have hl := NormalizationBridge.canonical_admissible
      80000571539 Agent10SixCarryCounterexample.leftDigits 11
      Agent10SixCarryCounterexample.left_canonical
    have hr := NormalizationBridge.canonical_admissible
      70000817069 Agent10SixCarryCounterexample.rightDigits 11
      Agent10SixCarryCounterexample.right_canonical
    have he := h Agent10SixCarryCounterexample.leftColumns
      Agent10SixCarryCounterexample.rightColumns 11 hl hr
      (fun t ht i hi => Agent10SixCarryCounterexample.six_complete_carries
        t (by omega) i hi) 0 hJ (by decide)
    rw [Agent10SixCarryCounterexample.initial_pair_sums_differ.1,
      Agent10SixCarryCounterexample.initial_pair_sums_differ.2] at he
    omega

private theorem eight_le_of_second_pair (J K : Nat)
    (h : PrefixReconstruction J K) (hJ : 2 ≤ J) : 8 ≤ K := by
  by_cases hK : 8 ≤ K
  · exact hK
  · exfalso
    have he := h SevenCarryWitness.leftColumns SevenCarryWitness.rightColumns 9
      SevenCarryWitness.left_admissible SevenCarryWitness.right_admissible
      (fun t ht i hi => SevenCarryWitness.seven_complete_carries
        t (by omega) i hi) 1 (by omega) (by decide)
    exact SevenCarryWitness.initial_pair_difference_active.2 he

private theorem nine_le_of_fourth_pair (J K : Nat)
    (h : PrefixReconstruction J K) (hJ : 4 ≤ J) : 9 ≤ K := by
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
      Agent10EightCarryCounterexample.rightColumns 17 hl hr
      (fun t ht i hi => Agent10EightCarryCounterexample.eight_complete_carries
        t (by omega) i hi) 3 (by omega) (by decide)
    exact Agent10EightCarryCounterexample.initial_pair_difference_active.2 he

/-- Exact thresholds for all uniform prefixes: zero observations for the
empty prefix, seven for one coefficient, eight for two or three, and nine
for every longer prefix. All quantified indices must be initially active. -/
theorem prefix_reconstruction_iff (J K : Nat) :
    PrefixReconstruction J K ↔ prefixThreshold J ≤ K := by
  constructor
  · intro h
    by_cases h0 : J = 0
    · simp [prefixThreshold, h0]
    by_cases h1 : J = 1
    · simpa [prefixThreshold, h0, h1] using
        seven_le_of_nonempty_prefix J K h (by omega)
    by_cases h3 : J ≤ 3
    · simpa [prefixThreshold, h0, h1, h3] using
        eight_le_of_second_pair J K h (by omega)
    · simpa [prefixThreshold, h0, h1, h3] using
        nine_le_of_fourth_pair J K h (by omega)
  · intro h q r L hq hr hc i hi hiL
    by_cases h0 : J = 0
    · omega
    by_cases h1 : J = 1
    · have hK : 7 ≤ K := by simpa [prefixThreshold, h0, h1] using h
      have hi0 : i = 0 := by omega
      subst i
      exact seven_carries_determine_exterior_pair q r L hq hr
        (fun t ht j hj => hc t (by omega) j hj)
    by_cases h3 : J ≤ 3
    · have hK : 8 ≤ K := by simpa [prefixThreshold, h0, h1, h3] using h
      exact EightCarryThreePairSharp.eight_carries_determine_first_three_active_pairs
        q r L hq hr (fun t ht j hj => hc t (by omega) j hj) i (by omega) hiL
    · have hK : 9 ≤ K := by simpa [prefixThreshold, h0, h1, h3] using h
      exact DifferenceObservability.nine_carry_words_determine_pair_sums
        q r L hq hr (fun t ht j hj => hc t (by omega) j hj) i hiL

#print axioms prefix_reconstruction_iff

end CarryPrefixThresholds
