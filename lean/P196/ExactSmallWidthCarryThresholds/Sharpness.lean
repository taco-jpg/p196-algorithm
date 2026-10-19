import P196.ExactSmallWidthCarryThresholds.Definitions
import P196.ExactSmallWidthCarryThresholds.WidthWitnesses
import P196.CarryWidthThresholds.SmallWitnesses

/-!
One canonical counterexample at every exact initial width from one to eight.
The three earlier witnesses are imported, and the five additional instances
supply the remaining widths. Each witness loses reconstruction at one fewer
observation than the proposed exact-width threshold, simultaneously for an
active pair coefficient and for the next ordinary integer.
-/

namespace ExactSmallWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

private theorem small_observation_count :
    ∀ w : Fin 3,
      exactWidthThreshold (CarryWidthThresholds.SmallWitnesses.width w) - 1 =
        CarryWidthThresholds.SmallWitnesses.observations w := by
  decide +kernel

private theorem additional_observation_count :
    ∀ w : Fin 5,
      exactWidthThreshold (Witnesses.width w) - 1 = Witnesses.observations w := by
  decide +kernel

/-- At each width in the classified domain, one fewer complete observation
leaves an active initial pair coefficient and the next integer ambiguous. -/
theorem exact_width_counterexample (L : Nat) (hpos : 0 < L) (hsmall : L ≤ 8) :
    ∃ (n m : Nat) (d e : Nat → Nat),
      Canonical n d L ∧ Canonical m e L ∧
      (∀ t, t < exactWidthThreshold L - 1 →
        ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
          carry (iterPairs (columnSum d L) L t).2 i =
            carry (iterPairs (columnSum e L) L t).2 i) ∧
      (∃ i, i < L ∧ columnSum d L i ≠ columnSum e L i) ∧
      Lychrel196.step n ≠ Lychrel196.step m := by
  by_cases hthree : L ≤ 3
  · let w : Fin 3 := ⟨L - 1, by omega⟩
    have hw : CarryWidthThresholds.SmallWitnesses.width w = L := by
      dsimp [w, CarryWidthThresholds.SmallWitnesses.width]
      omega
    rw [← hw]
    refine ⟨CarryWidthThresholds.SmallWitnesses.seed w false,
      CarryWidthThresholds.SmallWitnesses.seed w true,
      CarryWidthThresholds.SmallWitnesses.digits w false,
      CarryWidthThresholds.SmallWitnesses.digits w true,
      CarryWidthThresholds.SmallWitnesses.canonical w false,
      CarryWidthThresholds.SmallWitnesses.canonical w true, ?_, ?_,
      CarryWidthThresholds.SmallWitnesses.next_integers_differ w⟩
    · intro t ht i hi
      exact CarryWidthThresholds.SmallWitnesses.complete_carries w t
        (by simpa only [small_observation_count] using ht) i hi
    · exact ⟨0, (CarryWidthThresholds.SmallWitnesses.initial_pair_difference_active w).1,
        (CarryWidthThresholds.SmallWitnesses.initial_pair_difference_active w).2⟩
  · let w : Fin 5 := ⟨L - 4, by omega⟩
    have hw : Witnesses.width w = L := by
      dsimp [w, Witnesses.width]
      omega
    rw [← hw]
    refine ⟨Witnesses.seed w false, Witnesses.seed w true,
      Witnesses.digits w false, Witnesses.digits w true,
      Witnesses.canonical w false, Witnesses.canonical w true, ?_, ?_,
      Witnesses.next_integers_differ w⟩
    · intro t ht i hi
      exact Witnesses.complete_carries w t
        (by simpa only [additional_observation_count] using ht) i hi
    · exact ⟨Witnesses.differenceIndex w,
        (Witnesses.initial_pair_difference_active w).1,
        (Witnesses.initial_pair_difference_active w).2⟩

#print axioms exact_width_counterexample

end ExactSmallWidthCarryThresholds
