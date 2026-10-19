import P196.CrossWidthTargetRecurrence.Weights

/-!
# A cubic transfer identity on productive collision states

The existing productive catalogue is finite. Kernel reduction checks the
cubic identity for the terminal indicator directly through the existing
transfer operator, without a second state table or quotient graph.
-/

set_option autoImplicit false

namespace CrossWidthTargetRecurrence

open CrossWidthCollisionStates

private theorem transfer_cubic_checked :
    productive.all (fun s => decide (
      transfer (transfer (transfer terminalWeight)) s =
        2 * transfer (transfer terminalWeight) s +
          3 * transfer terminalWeight s + terminalWeight s)) = true := by
  decide +kernel

/-- Three transfer steps satisfy the cubic recurrence at every state in
the existing productive collision catalogue. -/
theorem transfer_cubic {s : State} (hs : s ∈ productive) :
    transfer (transfer (transfer terminalWeight)) s =
      2 * transfer (transfer terminalWeight) s +
        3 * transfer terminalWeight s + terminalWeight s := by
  exact of_decide_eq_true (List.all_eq_true.mp transfer_cubic_checked s hs)

end CrossWidthTargetRecurrence

#print axioms CrossWidthTargetRecurrence.transfer_cubic
