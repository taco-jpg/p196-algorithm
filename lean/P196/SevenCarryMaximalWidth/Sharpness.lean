import P196.SevenCarryMaximalWidth.Reconstruction
import P196.CarryPrefixThresholds.SevenCarryWitness
import P196.EightCarryMaximalWidth.Sharpness

/-!
Eight is the largest uniform initial-width bound for complete reconstruction
from seven carry observations. Both the predicates and the canonical
width-nine obstruction are imported unchanged. This result does not classify
the minimum observation count within each smaller width class.
-/

namespace SevenCarryMaximalWidth

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual EightCarryMaximalWidth
open CarryPrefixThresholds

/-- Exactly the initial-width bounds at most eight permit uniform recovery
of all active pairs from seven complete carry observations. -/
theorem seven_pair_reconstruction_iff_width_le_eight (W : Nat) :
    PairReconstructionUpTo W 7 ↔ W ≤ 8 := by
  constructor
  · intro h
    by_cases hW : W ≤ 8
    · exact hW
    · exfalso
      have he := h SevenCarryWitness.leftColumns SevenCarryWitness.rightColumns 9
        SevenCarryWitness.left_admissible SevenCarryWitness.right_admissible
        (by omega) SevenCarryWitness.seven_complete_carries 1 (by decide)
      exact SevenCarryWitness.initial_pair_difference_active.2 he
  · intro hW q r L hq hr hL hc
    exact seven_carry_words_determine_pair_sums_of_width_le_eight
      q r L hq hr (Nat.le_trans hL hW) hc

/-- The same exact width threshold holds for reconstruction of the next
ordinary integer from shared-width canonical inputs. -/
theorem seven_next_integer_reconstruction_iff_width_le_eight (W : Nat) :
    NextIntegerReconstructionUpTo W 7 ↔ W ≤ 8 := by
  constructor
  · intro h
    by_cases hW : W ≤ 8
    · exact hW
    · exfalso
      apply SevenCarryWitness.next_integers_differ
      exact h 490039199 480047399 SevenCarryWitness.leftDigits
        SevenCarryWitness.rightDigits 9 SevenCarryWitness.left_canonical
        SevenCarryWitness.right_canonical (by omega)
        SevenCarryWitness.seven_complete_carries
  · intro hW n m d e L hn hm hL hc
    exact seven_carry_words_determine_next_integer_of_width_le_eight
      n m d e L hn hm (Nat.le_trans hL hW) hc

#print axioms seven_pair_reconstruction_iff_width_le_eight
#print axioms seven_next_integer_reconstruction_iff_width_le_eight

end SevenCarryMaximalWidth
