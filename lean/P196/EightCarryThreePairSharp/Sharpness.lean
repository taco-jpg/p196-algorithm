import P196.EightCarryThreePairSharp.Reconstruction
import P196.Agent10NineCarrySharp.Agent10EightCarryCounterexample

/-!
Agent #10: three is the largest uniform active-prefix length determined by
eight complete carry observations across arbitrary admissible initial widths.

The upper bound imports the first-three-pair reconstruction theorem. The
failure at every larger prefix length reuses the existing canonical width-
seventeen counterexample, whose first differing pair has index three. No
ordinary integer witness or carry-history computation is repeated here.
-/

namespace EightCarryThreePairSharp

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- Uniform reconstruction of the first `J` active initial pair coefficients
from eight complete carry observations, at every common admissible width. -/
def EightCarryPrefixReconstruction (J : Nat) : Prop :=
  ∀ (q r : Nat → Nat) (L : Nat), Admissible L q → Admissible L r →
    (∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) →
    ∀ i, i < J → i < L → q i = r i

/-- Exactly the prefix lengths at most three admit uniform reconstruction
from eight complete observations when the initial width is unrestricted. -/
theorem eight_carry_prefix_reconstruction_iff (J : Nat) :
    EightCarryPrefixReconstruction J ↔ J ≤ 3 := by
  constructor
  · intro h
    by_cases hJ : J ≤ 3
    · exact hJ
    · exfalso
      have hl := NormalizationBridge.canonical_admissible
        90000000560706169 Agent10EightCarryCounterexample.leftDigits 17
        Agent10EightCarryCounterexample.left_canonical
      have hr := NormalizationBridge.canonical_admissible
        90000000806235169 Agent10EightCarryCounterexample.rightDigits 17
        Agent10EightCarryCounterexample.right_canonical
      have he := h Agent10EightCarryCounterexample.leftColumns
        Agent10EightCarryCounterexample.rightColumns 17 hl hr
        Agent10EightCarryCounterexample.eight_complete_carries 3 (by omega) (by decide)
      exact Agent10EightCarryCounterexample.initial_pair_difference_active.2 he
  · intro hJ q r L hq hr hc i hi hiL
    exact eight_carries_determine_first_three_active_pairs q r L hq hr hc
      i (by omega) hiL

#print axioms eight_carry_prefix_reconstruction_iff

end EightCarryThreePairSharp
