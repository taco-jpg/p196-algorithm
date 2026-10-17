import P196.Agent1PeriodicReturnClock.Agent1PeriodicReturnClock

/-!
Repeat one supplied finite exact quotient path whose three endpoint blocks
return. The wrap uses the complete endpoint equalities, not a projected graph
return. This module constructs no cycle and makes no exponent, safety, or
ordinary-orbit assertion. Original validity is reused from ReturnClock.
-/

namespace Agent1.Periodic
open Agent8

/-- Repeat the given finite state list by its original indices modulo N. -/
def repeatWordState (x : Nat → Word) (N t : Nat) : Word := x (t % N)

theorem repeatWordState_zero (x : Nat → Word) (N : Nat) :
    repeatWordState x N 0 = x 0 := by simp [repeatWordState]

/-- The wrapped successor is the original successor at the current residue.
The only boundary identification needed is the supplied endpoint equality. -/
theorem repeatWordState_succ (x : Nat → Word) (N : Nat) (hN : 0 < N)
    (hx : x N = x 0) (t : Nat) :
    repeatWordState x N (t+1) = x (t%N+1) := by
  have hr : t % N < N := Nat.mod_lt t hN
  have hm : (t+1) % N = (t%N+1) % N := by
    simp only [Nat.add_mod, Nat.mod_mod]
  unfold repeatWordState
  rw [hm]
  by_cases hlt : t%N+1 < N
  · rw [Nat.mod_eq_of_lt hlt]
  · have heq : t%N+1 = N := by omega
    rw [heq, Nat.mod_self]
    exact hx.symm

/-- Repeating a complete returned quotient tuple gives an exact quotient
path at every finite horizon, including the wrap and an empty horizon. -/
theorem quotient_path_repeat (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) (M : Nat) :
    QuotientPath (repeatWordState B N) (repeatWordState H N)
      (repeatWordState w N) M := by
  intro i _
  obtain ⟨hB, hH, hw, hlen, hnextB, hnextH, hnextw⟩ := hp (i%N) (Nat.mod_lt i hN)
  refine ⟨hB, hH, hw, hlen, ?_, ?_, ?_⟩
  · rw [repeatWordState_succ B N hN hreturn.1 i]
    exact hnextB
  · rw [repeatWordState_succ H N hN hreturn.2.1 i]
    exact hnextH
  · rw [repeatWordState_succ w N hN hreturn.2.2 i]
    exact hnextw

/-- Every repeated state has original validity. Pointwise repetition uses
only validity of the original finite path; endpoint closure is unnecessary. -/
theorem quotient_path_repeat_valid (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hN : 0 < N) (t : Nat) :
    ValidPeriodic (repeatWordState B N t) (repeatWordState H N t)
      (repeatWordState w N t) :=
  quotient_path_valid B H w N hp hv (t%N) (Nat.le_of_lt (Nat.mod_lt t hN))

end Agent1.Periodic

#print axioms Agent1.Periodic.repeatWordState
#print axioms Agent1.Periodic.repeatWordState_zero
#print axioms Agent1.Periodic.repeatWordState_succ
#print axioms Agent1.Periodic.quotient_path_repeat
#print axioms Agent1.Periodic.quotient_path_repeat_valid
