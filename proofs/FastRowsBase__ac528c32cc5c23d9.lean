import LongRowsBase
import FastInverse

namespace SevenColumn.Certificate

def fastLongPred (width : Nat) (p : Word) : List Word :=
  if p.length = width then fastPrefixPredecessors p else []

theorem longPred_mem_fastLongPred {width : Nat} {p q : Word}
    (h : q ∈ longPred width p) : q ∈ fastLongPred width p := by
  unfold longPred at h
  unfold fastLongPred
  split at h
  · rename_i hp
    rw [if_pos hp]
    exact fastPrefixPredecessors_mem_iff.mpr h
  · contradiction

theorem checkedRows_fast_to_long {tree : RankTree} {width : Nat}
    (checked : CheckedRows tree (fastLongPred width)) :
    CheckedRows tree (longPred width) :=
  checkedRows_of_complete_enumeration checked (fun _ _ h => longPred_mem_fastLongPred h)

#print axioms checkedRows_fast_to_long

end SevenColumn.Certificate
