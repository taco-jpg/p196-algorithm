import P196.Agent1PeriodicOuterCatalog.Agent1PeriodicOuterChoices
namespace Agent1.OuterChoicesAuthorChecks
open Agent1.Periodic
/-- Exhaustive finite q=1,...,18 and g=0,1 order check; no realizability claim. -/
theorem outerImages_strict_order :
    ∀ q : Fin 18, ∀ g : Fin 2,
      (outerImages (q.val + 1) g.val).Pairwise (fun a b => a < b) := by decide
/-- Literal image table including deduplication, checked by kernel reduction. -/
theorem outerImages_table :
    (List.range 18).map (fun q => [outerImages (q+1) 0, outerImages (q+1) 1]) =
[[[2, 3], []], [[4, 5], []], [[6, 7], []], [[8, 9], []], [[10, 11], []], [[12, 13], []], [[14, 15], []], [[16, 17], []], [[18], [10]], [[], [1]], [[], [2]], [[], [3]], [[], [4]], [[], [5]], [[], [6]], [[], [7]], [[], [8]], [[], [9]]] := by decide
end Agent1.OuterChoicesAuthorChecks
#print axioms Agent1.OuterChoicesAuthorChecks.outerImages_strict_order
#print axioms Agent1.OuterChoicesAuthorChecks.outerImages_table
