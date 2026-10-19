import P196.PrefixTruncation.CycleObstructions

/-!
# A cyclic coarse prefix with a dead refinement

The one-column coefficient word `[1]` lies on a nine-edge backward cycle.
Its refinement `[1, 9, 6]` has no predecessors and fits in a checked rank tree
with rank zero.  Thus a coarse-prefix cycle does not prevent a finer prefix
from admitting a rank certificate.

The lists here are coefficient words, not ordinary decimal integers.  In
particular the control is not a statement about the orbit of integer 196.
-/

namespace PrefixTruncation

open SevenColumn SevenColumn.Certificate

/-- A small cycle evaluated only at one-column inverse relations. -/
theorem coarse_cycle :
    BackPath (fun p s => s ∈ prefixPredecessors p) 9 [1] [1] := by
  apply BackPath.step (q := [10])
  · decide
  apply BackPath.step (q := [5])
  · decide
  apply BackPath.step (q := [14])
  · decide
  apply BackPath.step (q := [7])
  · decide
  apply BackPath.step (q := [16])
  · decide
  apply BackPath.step (q := [8])
  · decide
  apply BackPath.step (q := [4])
  · decide
  apply BackPath.step (q := [2])
  · decide
  apply BackPath.step (q := [1])
  · decide
  exact BackPath.refl _

/-- Every checked rank tree omits the cyclic coarse word. -/
theorem coarse_lookup_none (tree : RankTree)
    (checked : CheckedRows tree prefixPredecessors) : lookup tree [1] = none := by
  simpa using lookup_none_of_projected_cycle checked
    (BackPath.refl [1]) coarse_cycle (by decide) (k := 1) (by decide)

/-- A single-node rank-zero tree for the dead refinement. -/
def refinementTree : RankTree :=
  .node (wordCode [1, 9, 6]) [1, 9, 6] 0 .empty .empty

theorem refinementTree_checked : CheckedRows refinementTree prefixPredecessors := by
  simp [CheckedRows, RankTree.All, refinementTree, checkRow,
    prefix_196_has_no_predecessors]

theorem refinementTree_lookup : lookup refinementTree [1, 9, 6] = some 0 := by
  decide

/-- A concrete failure of any converse that would propagate a coarse cycle
to every longer refinement. -/
theorem coarse_cycle_dead_refinement :
    [1, 9, 6].take 1 = [1] ∧
    prefixPredecessors [1, 9, 6] = [] ∧
    (∀ tree, CheckedRows tree prefixPredecessors → lookup tree [1] = none) ∧
    ∃ tree, CheckedRows tree prefixPredecessors ∧
      lookup tree [1, 9, 6] = some 0 := by
  exact ⟨rfl, prefix_196_has_no_predecessors, coarse_lookup_none,
    refinementTree, refinementTree_checked, refinementTree_lookup⟩

#print axioms coarse_cycle
#print axioms coarse_lookup_none
#print axioms refinementTree_checked
#print axioms refinementTree_lookup
#print axioms coarse_cycle_dead_refinement

end PrefixTruncation
