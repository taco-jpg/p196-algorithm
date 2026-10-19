import P196.CrossWidthTargetCensus.Census

/-!
# Terminal weights on the existing collision-walk census

The transfer operator sums a weight over productive successors. The
finite-walk aggregate sums the same weight at the last state of each
existing enumerated walk. No second walk or target list is introduced.
-/

set_option autoImplicit false

namespace CrossWidthTargetRecurrence

open CrossWidthCollisionStates FoldedCollisionPrefixes CrossWidthTargetCensus

/-- The indicator of the even terminal condition. -/
def terminalWeight (s : State) : Nat :=
  if EvenTerminal s then 1 else 0

/-- Sum a weight over all productive successors of a given state. -/
def transfer (w : State → Nat) (s : State) : Nat :=
  productive.foldr (fun t total => if Edge s t then w t + total else total) 0

/-- Sum terminal-state weights over the unchanged finite-walk enumeration. -/
def weightedWalks (k : Nat) (w : State → Nat) : Nat :=
  (walkPrefixes k).foldr (fun p total => w (prefixAt p k) + total) 0

/-- The zero-edge census consists of the forced initial state alone. -/
theorem weightedWalks_zero (w : State → Nat) :
    weightedWalks 0 w = w initial := rfl

end CrossWidthTargetRecurrence

#print axioms CrossWidthTargetRecurrence.terminalWeight
#print axioms CrossWidthTargetRecurrence.transfer
#print axioms CrossWidthTargetRecurrence.weightedWalks
#print axioms CrossWidthTargetRecurrence.weightedWalks_zero
