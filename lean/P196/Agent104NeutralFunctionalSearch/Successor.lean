import P196.Agent104NeutralJointWidth.Edges

/-!
# A literal partial successor for normalized interface states

The candidate target is recovered directly from the original raw transitions.
Membership tests inspect widths and coefficients without enumerating the finite
state carrier. The original edge checker remains the acceptance test. In
particular, no target Hyp is imposed: it is checked only if that target is used
as the source of a subsequent edge.
-/

namespace Agent104.NeutralFunctionalSearch

open Agent120.Neutral Agent104.NeutralJointWidth

/-- A direct, linear-in-word-length test for membership in the finite carrier. -/
def stateOK (b M W : Nat) (s : State) : Bool :=
  decide (s.1.length = M) &&
    decide (s.2.length = W - 1 ∨ s.2.length = W) &&
    s.1.all (fun x => decide (x < 2 * b - 1)) &&
    s.2.all (fun x => decide (x < 2 * b - 1))

theorem stateOK_iff_mem (b M W : Nat) (s : State) :
    stateOK b M W s = true ↔ s ∈ states b M W := by
  cases s with
  | mk B C => simp [stateOK, mem_states, List.all_eq_true, and_assoc]

/-- The sole possible target, before applying membership and edge checks. -/
def rawTarget (b M W : Nat) (s : State) : State :=
  let v := if gam b s.1 s.2 = 1 ∧ s.2.length = W then 1 else 0
  let rawB := nextB b s.1 s.2
  let rawC := nextC b s.1 s.2
  (rawB.take M, (rawC.drop v).take (rawC.length - 2 * v))

/-- Compute one candidate and check it, without searching over possible targets. -/
def successor (b M W : Nat) (s : State) : Option State :=
  if stateOK b M W s then
    let t := rawTarget b M W s
    if stateOK b M W t && edgeOK b (edgeFrom b W s t) then some t else none
  else none

private theorem take_unpad {α : Type} (x : α) (v : Nat) (C : List α) :
    ((List.replicate v x ++ (C ++ List.replicate v x)).drop v).take
      ((List.replicate v x ++ (C ++ List.replicate v x)).length - 2 * v) = C := by
  have hl : (List.replicate v x ++ (C ++ List.replicate v x)).length - 2 * v =
      C.length := by
    simp only [List.length_append, List.length_replicate]
    omega
  rw [hl, List.drop_append_eq_append_drop]
  simp [List.take_append_eq_append_take]

private theorem rawTarget_eq_of_edgeOK {b M W : Nat} {s t : State}
    (ht : t ∈ states b M W) (he : edgeOK b (edgeFrom b W s t) = true) :
    rawTarget b M W s = t := by
  have hlen := ((mem_states b M W t.1 t.2).mp ht).1
  obtain ⟨_, hB, hC⟩ := edgeOK_sound he
  simp only [edgeFrom] at hB hC
  apply Prod.ext
  · change (nextB b s.1 s.2).take M = t.1
    rw [hB, ← hlen]
    simp [List.take_append_eq_append_take]
  · change ((nextC b s.1 s.2).drop
        (if gam b s.1 s.2 = 1 ∧ s.2.length = W then 1 else 0)).take
        ((nextC b s.1 s.2).length -
          2 * (if gam b s.1 s.2 = 1 ∧ s.2.length = W then 1 else 0)) = t.2
    rw [hC]
    exact take_unpad _ _ _

/-- Exact equivalence with the original edge checker inside the finite carrier.
No base, positive width, or target-Hyp assumptions are added. -/
theorem successor_eq_some_iff (b M W : Nat) (s t : State) :
    successor b M W s = some t ↔
      s ∈ states b M W ∧ t ∈ states b M W ∧
        edgeOK b (edgeFrom b W s t) = true := by
  constructor
  · intro h
    unfold successor at h
    split at h
    next hs =>
      dsimp only at h
      split at h
      next ht =>
        have heq : rawTarget b M W s = t := Option.some.inj h
        simp only [Bool.and_eq_true] at ht
        rw [heq] at ht
        exact ⟨(stateOK_iff_mem b M W s).mp hs,
          (stateOK_iff_mem b M W t).mp ht.1, ht.2⟩
      next => simp at h
    next => simp at h
  · rintro ⟨hs, ht, he⟩
    have hs' := (stateOK_iff_mem b M W s).mpr hs
    have ht' := (stateOK_iff_mem b M W t).mpr ht
    have hr := rawTarget_eq_of_edgeOK ht he
    simp [successor, hs', hr, ht', he]

theorem successor_source {b M W : Nat} {s t : State}
    (h : successor b M W s = some t) : s ∈ states b M W :=
  ((successor_eq_some_iff b M W s t).mp h).1

theorem successor_target {b M W : Nat} {s t : State}
    (h : successor b M W s = some t) : t ∈ states b M W :=
  ((successor_eq_some_iff b M W s t).mp h).2.1

theorem successor_edgeOK {b M W : Nat} {s t : State}
    (h : successor b M W s = some t) : edgeOK b (edgeFrom b W s t) = true :=
  ((successor_eq_some_iff b M W s t).mp h).2.2

theorem successor_normalized {b M W : Nat} {s t : State}
    (h : successor b M W s = some t) : NormalizedEdge b M W (edgeFrom b W s t) := by
  have hs := (mem_states b M W s.1 s.2).mp (successor_source h)
  exact ⟨hs.1, hs.2.1, rfl, rfl⟩

end Agent104.NeutralFunctionalSearch

#print axioms Agent104.NeutralFunctionalSearch.stateOK_iff_mem
#print axioms Agent104.NeutralFunctionalSearch.successor_eq_some_iff
#print axioms Agent104.NeutralFunctionalSearch.successor_source
#print axioms Agent104.NeutralFunctionalSearch.successor_target
#print axioms Agent104.NeutralFunctionalSearch.successor_edgeOK
#print axioms Agent104.NeutralFunctionalSearch.successor_normalized
