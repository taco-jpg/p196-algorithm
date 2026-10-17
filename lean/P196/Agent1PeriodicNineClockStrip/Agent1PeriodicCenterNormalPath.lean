import P196.Foundations.Agent1PeriodicWidthPath

/-!
Retraction of the unchanged maximal center-strip algorithm, and normalization
of every center on a positive exact quotient path whose center and period
return. Neither initial normalization nor original validity is assumed.
-/

namespace Agent1.Periodic
open Agent8

/-- A center with no mirrored complete-period wrapper is unchanged by the
original stripping algorithm, with exactly zero removals. -/
theorem stripPeriodCenter_of_maximal (w H : Word)
    (hmax : ¬ ∃ K, H = w ++ K ++ w.reverse) :
    stripPeriodCenter w H = (H, 0) := by
  by_cases hw : w = []
  · subst w
    exact stripPeriodCenter_empty H
  · have htest : H ≠ w ++ stripPeriodMiddle w H ++ w.reverse := by
      intro h
      exact hmax ⟨stripPeriodMiddle w H, h⟩
    unfold stripPeriodCenter
    rw [if_neg hw]
    cases hlen : H.length with
    | zero => simp only [hlen, stripPeriodCenterAux]
    | succ n => simp only [hlen, stripPeriodCenterAux, if_neg htest]

/-- Every center on a positive exact quotient path with returned center and
period is already normalized. Positive indices inherit actual quotient
maximality; the returned endpoint supplies normalization at index zero. -/
theorem quotient_path_return_centers_normal (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hN : 0 < N)
    (hHreturn : H N = H 0) (hwreturn : w N = w 0) :
    ∀ i, i ≤ N → stripPeriodCenter (w i) (H i) = (H i, 0) := by
  have hpositive : ∀ i, 0 < i → i ≤ N →
      stripPeriodCenter (w i) (H i) = (H i, 0) := by
    intro i hi hle
    cases i with
    | zero => omega
    | succ j =>
        obtain ⟨hB, hH, hw, hlen, _, hnextH, hnextw⟩ := hp j (by omega)
        rw [hnextH, hnextw]
        exact stripPeriodCenter_of_maximal _ _
          (quotient_irreducible (B j) (H j) (w j) hB hH hw hlen).2
  intro i hi
  cases i with
  | zero =>
      have hlast := hpositive N hN (Nat.le_refl N)
      simpa only [hHreturn, hwreturn] using hlast
  | succ i => exact hpositive (i+1) (by omega) hi

end Agent1.Periodic

#print axioms Agent1.Periodic.stripPeriodCenter_of_maximal
#print axioms Agent1.Periodic.quotient_path_return_centers_normal
