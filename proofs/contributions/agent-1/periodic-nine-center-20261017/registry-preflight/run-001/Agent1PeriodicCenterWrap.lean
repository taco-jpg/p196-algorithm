import Agent1PeriodicCenterStrip

/-!
One exact mirrored wrapper is removed by the existing center-strip loop.
Input-length fuel after that removal exceeds the middle word's own fuel;
the private lemma equates those sufficient-fuel executions. No recursion,
empty-period convention, validity predicate or global rewrite is changed.
-/

namespace Agent1.Periodic
open Agent8

private theorem centerAux_extraFuel (w H : Word) (fuel extra : Nat)
    (hw : w ≠ []) (hfuel : H.length ≤ fuel) :
    stripPeriodCenterAux w (fuel + extra) H = stripPeriodCenterAux w fuel H := by
  induction fuel generalizing H with
  | zero =>
      have hH : H = [] := List.length_eq_zero_iff.mp (by omega)
      subst H
      have hp : 0 < w.length := List.length_pos_iff.mpr hw
      have htest : ¬ ([] : Word) = w ++ stripPeriodMiddle w [] ++ w.reverse := by
        intro heq
        have hl := congrArg List.length heq
        simp only [List.length_nil, List.length_append, List.length_reverse] at hl
        omega
      cases extra with
      | zero => rfl
      | succ extra => simp only [Nat.zero_add, stripPeriodCenterAux, if_neg htest]
  | succ fuel ih =>
      rw [Nat.succ_add]
      by_cases htest : H = w ++ stripPeriodMiddle w H ++ w.reverse
      · simp only [stripPeriodCenterAux, if_pos htest]
        rw [ih (stripPeriodMiddle w H) (by
          have := stripPeriodMiddle_length_lt w H hw htest
          omega)]
      · simp only [stripPeriodCenterAux, if_neg htest]

/-- Adding one complete period on both sides leaves the exact stripped
middle unchanged and increments the count by one. The middle may be empty,
already wrapped, or asymmetric; only the period is required to be nonempty. -/
theorem stripPeriodCenter_wrap (w K : Word) (hw : w ≠ []) :
    stripPeriodCenter w (w ++ K ++ w.reverse) =
      ((stripPeriodCenter w K).1, (stripPeriodCenter w K).2 + 1) := by
  have hp : 0 < w.length := List.length_pos_iff.mpr hw
  have hlen : (w ++ K ++ w.reverse).length =
      (K.length + (2*w.length-1)) + 1 := by
    simp only [List.length_append, List.length_reverse]
    omega
  simp only [stripPeriodCenter, if_neg hw]
  rw [hlen, stripPeriodCenterAux, stripPeriodMiddle_wrap]
  rw [if_pos rfl, centerAux_extraFuel w K K.length (2*w.length-1) hw (Nat.le_refl _)]

end Agent1.Periodic
#print axioms Agent1.Periodic.stripPeriodCenter_wrap
