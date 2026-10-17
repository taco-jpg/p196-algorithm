import P196.Agent104P620Witness.PrefixCertificate
import P196.Agent104P620Witness.PrefixInverse

namespace SevenColumn.Certificate

/-- Long transitions are used only at the fixed prefix width.  Short complete
words require the separate exact short-boundary exclusion theorem. -/
def longPred (width : Nat) (p : Word) : List Word :=
  if p.length = width then prefixPredecessors p else []

def LongEdge (width : Nat) (p q : Word) : Prop :=
  p.length = width ∧ LongCompatible p q

theorem longPred_complete {width : Nat} {p q : Word}
    (h : LongEdge width p q) : q ∈ longPred width p := by
  simp only [longPred, h.1, ↓reduceIte]
  exact longCompatible_mem_prefixPredecessors h.2

theorem checked_long_path_bound {tree : RankTree} {width bound n : Nat}
    (checked : CheckedRows tree (longPred width)) {p q : Word}
    (path : BackPath (LongEdge width) n p q)
    (initial : checkInitial tree bound p = true) : n ≤ bound :=
  initial_backPath_length_le checked (fun _ _ h => longPred_complete h) path initial

#print axioms checked_long_path_bound

end SevenColumn.Certificate
