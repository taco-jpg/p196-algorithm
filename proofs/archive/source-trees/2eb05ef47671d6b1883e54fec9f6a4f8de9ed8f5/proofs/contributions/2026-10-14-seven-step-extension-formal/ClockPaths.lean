import SevenStepOrbit

/-! Finite path consequences of actual seven-step returns. -/

namespace ClockPaths

open DecimalDigits FoldedDecimal OverflowCarryNormalization
  BoundaryTransducer ActualBoundary SevenStepOrbit

theorem rank_path_bound (r : Nat → Nat) (N : Nat)
    (h : ∀ t, t < N → r (t + 1) < r t) : N ≤ r 0 := by
  have hp : ∀ t, t ≤ N → t + r t ≤ r 0 := by
    intro t
    induction t with
    | zero => intro _; omega
    | succ t ih =>
      intro ht
      have hi := ih (by omega)
      have hs := h t (by omega)
      omega
  have := hp N (Nat.le_refl _)
  omega

theorem no_infinite_strict_rank (r : Nat → Nat) :
    ¬ (∀ t, r (t + 1) < r t) := by
  intro h
  have hb := rank_path_bound r (r 0 + 1) (fun t _ => h t)
  omega

theorem segment_trace_of_endpoints (q : Nat → Nat) (L a : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hstart : boundaryAt q L a = initial)
    (hend : boundaryAt q L (a + 7) = initial) :
    actualTrace q L a 7 =
      [⟨4, 4, 0⟩, ⟨8, 8, 0⟩, ⟨16, 16, 0⟩, ⟨7, 14, 7⟩,
       ⟨15, 8, 15⟩, ⟨6, 14, 14⟩, ⟨13, 9, 9⟩, ⟨4, 4, 0⟩] := by
  have hr := run_actual q L a 7 hL ha
  change run (boundaryAt q L a)
    [controlAt q L a, controlAt q L (a+1), controlAt q L (a+2),
      controlAt q L (a+3), controlAt q L (a+4), controlAt q L (a+5),
      controlAt q L (a+6)] = boundaryAt q L (a+7) at hr
  rw [hstart, hend] at hr
  have ht := trace_actual q L a 7 hL ha
  change trace (boundaryAt q L a)
    [controlAt q L a, controlAt q L (a+1), controlAt q L (a+2),
      controlAt q L (a+3), controlAt q L (a+4), controlAt q L (a+5),
      controlAt q L (a+6)] = actualTrace q L a 7 at ht
  rw [hstart] at ht
  rw [← ht]
  exact BoundaryTransducer.seven_trace_of_return _ _ _ _ _ _ _ hr

theorem segment_overflows_of_endpoints (q : Nat → Nat) (L a : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hstart : boundaryAt q L a = initial)
    (hend : boundaryAt q L (a + 7) = initial) :
    actualOverflows q L a 7 = [0, 0, 1, 0, 1, 0, 1] := by
  have hr := run_actual q L a 7 hL ha
  change run (boundaryAt q L a)
    [controlAt q L a, controlAt q L (a+1), controlAt q L (a+2),
      controlAt q L (a+3), controlAt q L (a+4), controlAt q L (a+5),
      controlAt q L (a+6)] = boundaryAt q L (a+7) at hr
  rw [hstart, hend] at hr
  have ht := overflows_actual q L a 7 hL ha
  change overflows (boundaryAt q L a)
    [controlAt q L a, controlAt q L (a+1), controlAt q L (a+2),
      controlAt q L (a+3), controlAt q L (a+4), controlAt q L (a+5),
      controlAt q L (a+6)] = actualOverflows q L a 7 at ht
  rw [hstart] at ht
  rw [← ht]
  exact BoundaryTransducer.seven_overflows_of_return _ _ _ _ _ _ _ hr

theorem actualTrace_get (q : Nat → Nat) (L a n i : Nat) (hi : i ≤ n) :
    (actualTrace q L a n)[i]? = some (boundaryAt q L (a+i)) := by
  induction n generalizing a i with
  | zero =>
    have hz : i = 0 := by omega
    subst i
    rfl
  | succ n ih =>
    cases i with
    | zero => rfl
    | succ i =>
      have hh := ih (a+1) i (by omega)
      simpa only [actualTrace, List.getElem?_cons_succ, Nat.add_assoc,
        Nat.add_comm 1 i] using hh

theorem actualOverflows_get (q : Nat → Nat) (L a n i : Nat) (hi : i < n) :
    (actualOverflows q L a n)[i]? = some (overflowAt q L (a+i)) := by
  induction n generalizing a i with
  | zero => omega
  | succ n ih =>
    cases i with
    | zero => rfl
    | succ i =>
      have hh := ih (a+1) i (by omega)
      simpa only [actualOverflows, List.getElem?_cons_succ, Nat.add_assoc,
        Nat.add_comm 1 i] using hh

end ClockPaths
