import P196.Drafts.Agent418Agent418.Agent418SaturatedInputAudit

namespace Agent418.SaturatedInputAudit

/-- At odd indices the incoming carry bit is independently chosen.
    This definition is not a claim about realizable ordinary-integer carries. -/
def freeControl (a : Nat → Fin 2) (i : Nat) : Nat :=
  match i % 8 with
  | 0 => 1
  | 2 => 0
  | 4 => 0
  | 6 => 1
  | _ => (a i).val

def localControl (e : Fin 2) (r : Nat) : Nat :=
  match r with
  | 0 => 1
  | 2 => 0
  | 4 => 0
  | 6 => 1
  | _ => e.val

theorem local_free_edge : ∀ r : Fin 8, ∀ e : Fin 2,
    advance (cycleState r.val) (localControl e r.val) =
      (cycleState (r.val + 1), r.val % 2) := by decide

theorem cycleState_mod (i : Nat) : cycleState (i % 8) = cycleState i := by
  simp [cycleState, Nat.mod_mod]

theorem cycleState_succ_mod (i : Nat) :
    cycleState (i % 8 + 1) = cycleState (i + 1) := by
  have h : (i % 8 + 1) % 8 = (i + 1) % 8 := by omega
  unfold cycleState
  rw [h]

theorem freeControl_bit (a : Nat → Fin 2) (i : Nat) : freeControl a i ≤ 1 := by
  have he := (a i).isLt
  unfold freeControl
  split <;> omega

theorem arbitrary_time_edge (a : Nat → Fin 2) (i : Nat) :
    advance (cycleState i) (freeControl a i) =
      (cycleState (i + 1), i % 2) := by
  have h := local_free_edge ⟨i % 8, Nat.mod_lt _ (by decide)⟩ (a i)
  have hm : (i % 8) % 2 = i % 2 := by omega
  simpa only [cycleState_mod, cycleState_succ_mod, hm, localControl,
    freeControl] using h

/-- The actual recursively evaluated trajectory in the abstract relation. -/
def controlledRun (a : Nat → Fin 2) : Nat → Prefix
  | 0 => cycleState 0
  | n+1 => (advance (controlledRun a n) (freeControl a n)).1

theorem controlledRun_eq (a : Nat → Fin 2) (n : Nat) :
    controlledRun a n = cycleState n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [controlledRun, ih, arbitrary_time_edge]

def runOverflow (a : Nat → Fin 2) (i : Nat) : Nat :=
  (advance (controlledRun a i) (freeControl a i)).2

theorem runOverflow_eq (a : Nat → Fin 2) (i : Nat) :
    runOverflow a i = i % 2 := by
  simp only [runOverflow, controlledRun_eq, arbitrary_time_edge]

theorem parity_total (n : Nat) : total (fun i => i % 2) n = n / 2 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [total, ih]
    omega

theorem arbitrary_time_overflow_total (a : Nat → Fin 2) (n : Nat) :
    total (runOverflow a) n = n / 2 := by
  have hf : runOverflow a = fun i => i % 2 := by
    funext i
    exact runOverflow_eq a i
  rw [hf, parity_total]

theorem every_eight_block_saturated (a : Nat → Fin 2) (k : Nat) :
    2 * total (runOverflow a) (8*k) = 8*k := by
  rw [arbitrary_time_overflow_total]
  omega

#print axioms local_free_edge
#print axioms freeControl_bit
#print axioms arbitrary_time_edge
#print axioms controlledRun_eq
#print axioms runOverflow_eq
#print axioms parity_total
#print axioms arbitrary_time_overflow_total
#print axioms every_eight_block_saturated

end Agent418.SaturatedInputAudit
