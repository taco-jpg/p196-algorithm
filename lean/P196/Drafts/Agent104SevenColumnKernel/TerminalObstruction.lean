import P196.Agent104P620Witness.ActualPrefix

/-!
The terminal prefix (1,9,6) in the 739 inverse certificate has no actual
predecessor, at any source width. These are pair-column sums, not the
digits of the integer 196. The theorem does not settle the 196 conjecture.
-/
namespace SevenColumnKernel.TerminalObstruction

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open SevenColumnProjection

/-- The local terminal obstruction, including sources shorter than three. -/
theorem next_prefix_196_impossible (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hw : 3 ≤ nextWidth q L) :
    ¬ (nextColumns q L 0 = 1 ∧ nextColumns q L 1 = 9 ∧
      nextColumns q L 2 = 6) := by
  intro hp
  by_cases hL : 3 ≤ L
  · have hm := actual_mem_prefixPredecessors q L 3 ha (by decide) hL
    have he : wordPrefix (nextColumns q L) 3 = [1, 9, 6] := by
      simp [wordPrefix, segment, hp.1, hp.2.1, hp.2.2]
    rw [he, SevenColumn.prefix_196_has_no_predecessors] at hm
    exact List.not_mem_nil hm
  · have hu : nextWidth q L ≤ L + 1 := by
      unfold nextWidth
      split <;> omega
    have he : nextWidth q L = 3 := by omega
    have hn := NormalizationBridge.admissible_next q L ha
    have hs := hn.2.2.2.1 0 (by omega)
    simp only [he, Nat.sub_zero] at hs
    rw [hp.1, hp.2.2] at hs
    omega

/-- Every positive-time actual pair-word state avoids the terminal prefix. -/
theorem positive_time_no_196_pair_prefix (q : Nat → Nat) (L t : Nat)
    (ha : Admissible L q) (hw : 3 ≤ (iterPairs q L (t + 1)).1) :
    ¬ ((iterPairs q L (t + 1)).2 0 = 1 ∧
      (iterPairs q L (t + 1)).2 1 = 9 ∧
      (iterPairs q L (t + 1)).2 2 = 6) := by
  exact next_prefix_196_impossible (iterPairs q L t).2
    (iterPairs q L t).1 (iterPairs_admissible q L t ha) hw

#print axioms next_prefix_196_impossible
#print axioms positive_time_no_196_pair_prefix

end SevenColumnKernel.TerminalObstruction
