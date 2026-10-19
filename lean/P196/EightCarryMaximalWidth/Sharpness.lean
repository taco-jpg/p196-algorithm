import P196.EightCarryMaximalWidth.Reconstruction
import P196.Agent10NineCarrySharp.Agent10EightCarryCounterexample
import P196.EightCarryWidthBound.Sharpness

/-!
Agent #10: sixteen is the largest uniform initial-width bound for reconstruction
from eight complete carry observations. At that width bound, eight is the
smallest uniform observation count. Both statements concern active initial
pair coefficients and the next ordinary integer.

The upper bounds use this result's actual reconstruction theorems. Width
maximality reuses the existing canonical width-seventeen counterexample.
Observation minimality restricts to the already established width-fourteen
class, whose lower bound is the existing canonical width-thirteen witness.
No witness computation or transition certificate is repeated here.

Only the common initial width is bounded. Every carry, including terminal
overflow, is observed; later widths are unrestricted, and ordinary iteration
continues after palindromes. The observation threshold is uniform over the
whole class, with no separate optimality claim at every individual width and
no initial-integer injectivity or palindrome-avoidance conclusion.
-/

namespace EightCarryMaximalWidth
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- Uniform reconstruction of active initial pair coefficients from `K`
complete observations at a common admissible initial width at most `W`. -/
def PairReconstructionUpTo (W K : Nat) : Prop :=
  ∀ (q r : Nat → Nat) (L : Nat), Admissible L q → Admissible L r → L ≤ W →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) →
    ∀ i, i < L → q i = r i

/-- Uniform reconstruction of the next ordinary integer from `K` complete
observations at a common canonical initial width at most `W`. -/
def NextIntegerReconstructionUpTo (W K : Nat) : Prop :=
  ∀ (n m : Nat) (d e : Nat → Nat) (L : Nat),
    Canonical n d L → Canonical m e L → L ≤ W →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) →
    Lychrel196.step n = Lychrel196.step m

/-- Sixteen is the exact largest initial-width bound for uniform active-pair
reconstruction from eight complete carry observations. -/
theorem eight_pair_reconstruction_iff_width_le_sixteen (W : Nat) :
    PairReconstructionUpTo W 8 ↔ W ≤ 16 := by
  constructor
  · intro h
    by_cases hW : W ≤ 16
    · exact hW
    · exfalso
      have hl := NormalizationBridge.canonical_admissible
        90000000560706169 Agent10EightCarryCounterexample.leftDigits 17
        Agent10EightCarryCounterexample.left_canonical
      have hr := NormalizationBridge.canonical_admissible
        90000000806235169 Agent10EightCarryCounterexample.rightDigits 17
        Agent10EightCarryCounterexample.right_canonical
      have he := h Agent10EightCarryCounterexample.leftColumns
        Agent10EightCarryCounterexample.rightColumns 17 hl hr (by omega)
        Agent10EightCarryCounterexample.eight_complete_carries
      exact Agent10EightCarryCounterexample.initial_pair_difference_active.2
        (he 3 (by decide))
  · intro hW q r L hq hr hL hc
    exact eight_carry_words_determine_pair_sums_of_width_le_sixteen
      q r L hq hr (Nat.le_trans hL hW) hc

/-- Sixteen is the exact largest initial-width bound for uniform next-integer
reconstruction from eight complete carry observations. -/
theorem eight_next_integer_reconstruction_iff_width_le_sixteen (W : Nat) :
    NextIntegerReconstructionUpTo W 8 ↔ W ≤ 16 := by
  constructor
  · intro h
    by_cases hW : W ≤ 16
    · exact hW
    · exfalso
      apply Agent10EightCarryCounterexample.next_integers_differ
      exact h 90000000560706169 90000000806235169
        Agent10EightCarryCounterexample.leftDigits
        Agent10EightCarryCounterexample.rightDigits 17
        Agent10EightCarryCounterexample.left_canonical
        Agent10EightCarryCounterexample.right_canonical (by omega)
        Agent10EightCarryCounterexample.eight_complete_carries
  · intro hW n m d e L hn hm hL hc
    exact eight_carry_words_determine_next_integer_of_width_le_sixteen
      n m d e L hn hm (Nat.le_trans hL hW) hc

/-- Eight is the exact uniform observation threshold for active-pair
reconstruction over all admissible initial widths at most sixteen. -/
theorem pair_reconstruction_up_to_sixteen_iff (K : Nat) :
    PairReconstructionUpTo 16 K ↔ 8 ≤ K := by
  constructor
  · intro h
    apply (EightCarryWidthBound.pair_reconstruction_up_to_fourteen_iff K).mp
    intro q r L hq hr hL hc
    exact h q r L hq hr (by omega) hc
  · intro hK q r L hq hr hL hc
    exact eight_carry_words_determine_pair_sums_of_width_le_sixteen
      q r L hq hr hL (fun t ht i hi => hc t (by omega) i hi)

/-- Eight is the exact uniform observation threshold for next-integer
reconstruction over all canonical initial widths at most sixteen. -/
theorem next_integer_reconstruction_up_to_sixteen_iff (K : Nat) :
    NextIntegerReconstructionUpTo 16 K ↔ 8 ≤ K := by
  constructor
  · intro h
    apply (EightCarryWidthBound.next_integer_reconstruction_up_to_fourteen_iff K).mp
    intro n m d e L hn hm hL hc
    exact h n m d e L hn hm (by omega) hc
  · intro hK n m d e L hn hm hL hc
    exact eight_carry_words_determine_next_integer_of_width_le_sixteen
      n m d e L hn hm hL (fun t ht i hi => hc t (by omega) i hi)

#print axioms eight_pair_reconstruction_iff_width_le_sixteen
#print axioms eight_next_integer_reconstruction_iff_width_le_sixteen
#print axioms pair_reconstruction_up_to_sixteen_iff
#print axioms next_integer_reconstruction_up_to_sixteen_iff

end EightCarryMaximalWidth
