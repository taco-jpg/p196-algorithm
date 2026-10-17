import P196.Agent10EightCarry.Agent10SevenStepCount
import P196.Agent10EightCarry.Agent10SmoothingBridge

/-!
Agent #10: discharge the nonoverflow-count premise in eight-word reconstruction.

The seven-step count is proved for all admissible widths in Agent10SevenStepCount.
The imported smoothing bridge retains the original integer-sequence definitions.
Eight full carry words suffice when the initial pair difference is bounded by five;
in particular this bound follows from an initial nonoverflow addition.

The numeric conclusion identifies the next ordinary reverse-and-add integer, not
the original digit splitting. No universal eight-word bound or avoidance theorem
is asserted here.
-/

set_option maxHeartbeats 10000000

namespace Agent10EightCarry
open DifferenceObservability CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- The count hypothesis in the inherited small-difference theorem is discharged
for every admissible positive width, including the singleton case. -/
theorem eight_carry_words_determine_pair_sums_of_small_difference
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (hd : ∀ i, -5 ≤ cappedDiff q r L i ∧ cappedDiff q r L i ≤ 5) :
    ∀ i, i < L → q i = r i := by
  by_cases hN : 4 ≤ orbitCount q L 7
  · apply iterPairs_endpoint_carry_history_injective q r L 7 hq hr
    · intro t ht i hi
      exact hc t (by omega) i hi
    · exact hN
  · have hlo := Agent10SevenStepCount.actual_seven_step_count_all_widths q L hq
    have hn : orbitCount q L 7 = 3 := by omega
    exact Agent10SmoothingBridge.eight_carries_small_difference q r L hq hr hc hn hd

/-- Eight complete observations recover the initial pair sums whenever the first
actual addition does not overflow. The nonoverflow count is not a premise. -/
theorem eight_carry_words_determine_pair_sums_of_initial_nonoverflow
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (ho : carry q L = 0) :
    ∀ i, i < L → q i = r i := by
  apply eight_carry_words_determine_pair_sums_of_small_difference q r L hq hr hc
  have hd := Agent10SmoothingBridge.initial_nonoverflow_difference_bound q r L hq hr
    (fun t ht => hc t (by omega)) ho
  intro i
  have hdi := hd i
  omega

/-- Exact ordinary-decimal consequence at a shared canonical initial width. -/
theorem eight_carry_words_determine_next_integer_of_initial_nonoverflow
    (n m : Nat) (d e : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m e L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i)
    (ho : carry (columnSum d L) L = 0) :
    Lychrel196.step n = Lychrel196.step m := by
  have hq := NormalizationBridge.canonical_admissible n d L hn
  have hr := NormalizationBridge.canonical_admissible m e L hm
  have he := eight_carry_words_determine_pair_sums_of_initial_nonoverflow
    (columnSum d L) (columnSum e L) L hq hr hc ho
  calc
    Lychrel196.step n = value (columnSum d L) L :=
      step_eq_word_value n d (columnSum d L) L hn (by intro i hi; rfl)
    _ = value (columnSum e L) L := value_congr _ _ L he
    _ = Lychrel196.step m :=
      (step_eq_word_value m e (columnSum e L) L hm (by intro i hi; rfl)).symm

#print axioms eight_carry_words_determine_pair_sums_of_small_difference
#print axioms eight_carry_words_determine_pair_sums_of_initial_nonoverflow
#print axioms eight_carry_words_determine_next_integer_of_initial_nonoverflow

end Agent10EightCarry
