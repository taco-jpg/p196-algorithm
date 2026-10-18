import P196.Drafts.Agent7OddNooverflowFibers.OddCanonical

/- Independent interpretation checks for the complete canonical odd-word domain. -/
namespace P196.Agent7.ReviewCanonical

open P196.Agent9.InverseFibers P196.Agent7.OddFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

/-- All ten target-center digits, including the empty outer half. -/
theorem width_one_complete : ∀ v : Fin 10,
    fullOddPreimages [] v =
      if v.val % 2 = 0 ∧ 0 < v.val then [[v.val]] else [] := by
  decide

/-- Odd exterior coefficients are allowed; it is the true center that is even. -/
theorem odd_head_even_center_accepted : CanonicalOddFiber [2] 2 [1,2,1] := by
  simp [CanonicalOddFiber, scan, Agent8.stepWord, Agent8.normalize,
    Agent8.pair, Agent8.zipAdd, oddMirror]

/-- An even exterior does not excuse an odd coefficient at the literal center. -/
theorem even_head_odd_center_rejected : ¬ CanonicalOddFiber [4] 1 [2,1,2] := by
  simp [CanonicalOddFiber]

theorem width_three_complete : fullOddPreimages [2] 2 = [[1,2,1]] := by
  decide

theorem empty_full_word_rejected (ss : List Symbol) (v : Fin 10) :
    ¬ CanonicalOddFiber ss v [] := by
  simp [CanonicalOddFiber]

#print axioms width_one_complete
#print axioms odd_head_even_center_accepted
#print axioms even_head_odd_center_rejected
#print axioms width_three_complete
#print axioms empty_full_word_rejected

end P196.Agent7.ReviewCanonical
