import Agent1PeriodicGuard

/-!
Remove complete copies of a period from both ends of a center word.
The public operation is total, including an explicit empty-period convention.
For nonempty periods, input-length fuel suffices for maximal stripping.
These are finite list identities, with no validity or safety assertion.
-/

namespace Agent1.Periodic
open Agent8 Agent1.RepeatedBlock

/-- The candidate middle after deleting one period from each end. -/
def stripPeriodMiddle (w H : Word) : Word :=
  (H.drop w.length).take (H.length - 2 * w.length)

theorem stripPeriodMiddle_wrap (w K : Word) :
    stripPeriodMiddle w (w ++ K ++ w.reverse) = K := by
  unfold stripPeriodMiddle
  have hlen : (w ++ K ++ w.reverse).length - 2 * w.length = K.length := by
    simp only [List.length_append, List.length_reverse]
    omega
  rw [hlen, List.append_assoc, List.drop_left, List.take_left]

/-- Structural fuel recursion; each successful test removes two complete
periods and increments the number removed on each side. -/
def stripPeriodCenterAux (w : Word) : Nat → Word → Word × Nat
  | 0, H => (H, 0)
  | fuel + 1, H =>
      if H = w ++ stripPeriodMiddle w H ++ w.reverse then
        let r := stripPeriodCenterAux w fuel (stripPeriodMiddle w H)
        (r.1, r.2 + 1)
      else (H, 0)

/-- Empty periods remove nothing. Nonempty periods use the original input
length as fuel; the adequacy theorem below establishes maximal stopping. -/
def stripPeriodCenter (w H : Word) : Word × Nat :=
  if w = [] then (H, 0) else stripPeriodCenterAux w H.length H

theorem stripPeriodCenter_empty (H : Word) : stripPeriodCenter [] H = (H, 0) := by
  simp [stripPeriodCenter]

/-- Decomposition is exact at every fuel value, even before maximality. -/
theorem stripPeriodCenterAux_decomposition (w H : Word) (fuel : Nat) :
    H = pow w (stripPeriodCenterAux w fuel H).2 ++
      (stripPeriodCenterAux w fuel H).1 ++
      pow w.reverse (stripPeriodCenterAux w fuel H).2 := by
  induction fuel generalizing H with
  | zero => simp [stripPeriodCenterAux, pow]
  | succ fuel ih =>
      by_cases h : H = w ++ stripPeriodMiddle w H ++ w.reverse
      · simp only [stripPeriodCenterAux, if_pos h]
        calc
          H = w ++ stripPeriodMiddle w H ++ w.reverse := h
          _ = w ++ (pow w (stripPeriodCenterAux w fuel (stripPeriodMiddle w H)).2 ++
              (stripPeriodCenterAux w fuel (stripPeriodMiddle w H)).1 ++
              pow w.reverse (stripPeriodCenterAux w fuel (stripPeriodMiddle w H)).2) ++
              w.reverse := by rw [← ih (stripPeriodMiddle w H)]
          _ = _ := by rw [pow, pow_succ_right]; simp only [List.append_assoc]
      · simp [stripPeriodCenterAux, h, pow]

/-- A successful removal strictly decreases input length for a nonempty period. -/
theorem stripPeriodMiddle_length_lt (w H : Word) (hw : w ≠ [])
    (h : H = w ++ stripPeriodMiddle w H ++ w.reverse) :
    (stripPeriodMiddle w H).length < H.length := by
  have hp : 0 < w.length := List.length_pos.mpr hw
  have hl := congrArg List.length h
  simp only [List.length_append, List.length_reverse] at hl
  omega

/-- Input-length fuel is sufficient: the remaining center has no complete
period at both ends. The zero-fuel case is justified by the length premise. -/
theorem stripPeriodCenterAux_maximal (w H : Word) (fuel : Nat)
    (hw : w ≠ []) (hfuel : H.length ≤ fuel) :
    ¬ ∃ K, (stripPeriodCenterAux w fuel H).1 = w ++ K ++ w.reverse := by
  induction fuel generalizing H with
  | zero =>
      have hH : H = [] := List.length_eq_zero_iff.mp (by omega)
      have hp : 0 < w.length := List.length_pos.mpr hw
      simp only [stripPeriodCenterAux, hH]
      rintro ⟨K, hK⟩
      have hl := congrArg List.length hK
      simp only [List.length_nil, List.length_append, List.length_reverse] at hl
      omega
  | succ fuel ih =>
      by_cases h : H = w ++ stripPeriodMiddle w H ++ w.reverse
      · simp only [stripPeriodCenterAux, if_pos h]
        apply ih (stripPeriodMiddle w H)
        have hlt := stripPeriodMiddle_length_lt w H hw h
        omega
      · simp only [stripPeriodCenterAux, if_neg h]
        rintro ⟨K, hK⟩
        apply h
        rw [hK, stripPeriodMiddle_wrap]

/-- Every input is recovered by reinserting exactly the removed periods. -/
theorem stripPeriodCenter_decomposition (w H : Word) :
    H = pow w (stripPeriodCenter w H).2 ++ (stripPeriodCenter w H).1 ++
      pow w.reverse (stripPeriodCenter w H).2 := by
  by_cases hw : w = []
  · subst w
    simp [stripPeriodCenter, pow]
  · simpa only [stripPeriodCenter, if_neg hw] using
      stripPeriodCenterAux_decomposition w H H.length

theorem stripPeriodCenter_maximal (w H : Word) (hw : w ≠ []) :
    ¬ ∃ K, (stripPeriodCenter w H).1 = w ++ K ++ w.reverse := by
  simpa only [stripPeriodCenter, if_neg hw] using
    stripPeriodCenterAux_maximal w H H.length hw (Nat.le_refl _)

/-- Exact length accounting counts one removed copy on each side. -/
theorem stripPeriodCenter_length (w H : Word) :
    H.length = 2 * ((stripPeriodCenter w H).2 * w.length) +
      (stripPeriodCenter w H).1.length := by
  have h := congrArg List.length (stripPeriodCenter_decomposition w H)
  simp only [List.length_append, pow_length, List.length_reverse] at h
  omega

theorem stripPeriodCenter_length_le (w H : Word) :
    (stripPeriodCenter w H).1.length ≤ H.length := by
  have h := stripPeriodCenter_length w H
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.stripPeriodMiddle
#print axioms Agent1.Periodic.stripPeriodMiddle_wrap
#print axioms Agent1.Periodic.stripPeriodCenterAux
#print axioms Agent1.Periodic.stripPeriodCenter
#print axioms Agent1.Periodic.stripPeriodCenter_empty
#print axioms Agent1.Periodic.stripPeriodCenterAux_decomposition
#print axioms Agent1.Periodic.stripPeriodMiddle_length_lt
#print axioms Agent1.Periodic.stripPeriodCenterAux_maximal
#print axioms Agent1.Periodic.stripPeriodCenter_decomposition
#print axioms Agent1.Periodic.stripPeriodCenter_maximal
#print axioms Agent1.Periodic.stripPeriodCenter_length
#print axioms Agent1.Periodic.stripPeriodCenter_length_le
