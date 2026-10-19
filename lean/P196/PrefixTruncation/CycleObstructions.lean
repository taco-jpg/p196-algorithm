import P196.PrefixTruncation.Truncation
import P196.Agent117RemainingCycles.PrefixCycle

/-!
# Rank obstructions at smaller prefix widths

A reachable positive backward cycle remains such a cycle after any positive
prefix truncation.  The existing rank soundness theorem therefore excludes
its projected starting word from every fully checked rank tree.

This does not extend a cycle to a longer coefficient word.  It also does not
give a backward cycle of ordinary integers or an assertion about 196.
-/

namespace PrefixTruncation

open SevenColumn SevenColumn.Certificate

/-- A reachable positive cycle excludes every projected starting word from
every rank tree checked against the complete executable inverse. -/
theorem lookup_none_of_projected_cycle {tree : RankTree}
    (checked : CheckedRows tree prefixPredecessors)
    {m n k : Nat} {p z : Word}
    (entry : BackPath (fun p s => s ∈ prefixPredecessors p) m p z)
    (cycle : BackPath (fun p s => s ∈ prefixPredecessors p) n z z)
    (hn : 0 < n) (hk : 0 < k) :
    lookup tree (p.take k) = none := by
  exact Agent117.lookup_none_of_cycle checked
    (backPath_take entry hk) (backPath_take cycle hk) hn

/-- No proposed initial bound can succeed at a positive projected width. -/
theorem checkInitial_false_of_projected_cycle {tree : RankTree}
    (checked : CheckedRows tree prefixPredecessors)
    {m n k : Nat} {p z : Word}
    (entry : BackPath (fun p s => s ∈ prefixPredecessors p) m p z)
    (cycle : BackPath (fun p s => s ∈ prefixPredecessors p) n z z)
    (hn : 0 < n) (hk : 0 < k) (bound : Nat) :
    checkInitial tree bound (p.take k) = false := by
  unfold checkInitial
  rw [lookup_none_of_projected_cycle checked entry cycle hn hk]

#print axioms lookup_none_of_projected_cycle
#print axioms checkInitial_false_of_projected_cycle

end PrefixTruncation
