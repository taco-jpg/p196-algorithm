import P196.CrossWidthTargetRecurrence.Weights

/-!
# Weighted folds on the existing collision-prefix enumeration

Appending one productive successor transports the terminal weight by the
existing transfer operator. The terminal indicator counts precisely the
accepted prefix filter and hence the duplicate-free ordinary target list.
-/

set_option autoImplicit false

namespace CrossWidthTargetRecurrence

open CrossWidthCollisionStates FoldedCollisionPrefixes CrossWidthTargetCensus

private theorem transfer_accumulator (w : State → Nat) (s : State) (acc : Nat) :
    productive.foldr
        (fun t total => if Edge s t then w t + total else total) acc =
      transfer w s + acc := by
  have h := List.foldr_hom (fun total : Nat => total + acc)
    (g₁ := fun t total => if Edge s t then w t + total else total)
    (g₂ := fun t total => if Edge s t then w t + total else total)
    (l := productive) (init := 0) (by
      intro t total
      by_cases he : Edge s t <;> simp [he, Nat.add_assoc])
  simpa only [Nat.zero_add, transfer] using h

/-- Summing a weight after one additional enumerated edge is the same as
summing its transfer over the preceding walks. -/
theorem weightedWalks_succ (k : Nat) (w : State → Nat) :
    weightedWalks (k + 1) w = weightedWalks k (transfer w) := by
  unfold weightedWalks
  rw [walkPrefixes, List.foldr_filter, List.flatMap_def,
    List.foldr_flatten, List.foldr_map]
  simp only [List.foldr_map, prefixAt_append _ _ (Nat.le_refl k),
    prefixAt_append_last, decide_eq_true_eq, transfer_accumulator]

/-- The terminal indicator counts the existing even-target census exactly. -/
theorem weightedWalks_terminal (k : Nat) :
    weightedWalks k terminalWeight = (evenTargets k).length := by
  calc
    weightedWalks k terminalWeight =
        ((walkPrefixes k).filter
          (fun p => decide (EvenTerminal (prefixAt p k)))).foldr
            (fun _ total => total + 1) 0 := by
      rw [List.foldr_filter]
      unfold weightedWalks
      congr 1
      funext p total
      by_cases ht : EvenTerminal (prefixAt p k) <;>
        simp [terminalWeight, ht, Nat.add_comm]
    _ = ((walkPrefixes k).filter
        (fun p => decide (EvenTerminal (prefixAt p k)))).length := by
      simp only [List.foldr_add_const, Nat.one_mul, Nat.zero_add]
    _ = (evenTargets k).length := by
      simp only [evenTargets, evenPrefixes, List.length_map]

end CrossWidthTargetRecurrence

#print axioms CrossWidthTargetRecurrence.weightedWalks_succ
#print axioms CrossWidthTargetRecurrence.weightedWalks_terminal
