import P196.Agent105AllPredecessors.Agent105WordFiber9df76b

/-!
Agent #2: digit-split multiplicities for the decoded residual-five words.
The weights are the lengths of Agent #101's existing raw digit enumeration.
All half and center identities apply to arbitrary finite coefficient lists,
including empty lists and lists of odd length. No orbit statement is made.
-/

namespace P196.ResidualFivePredecessorMass

open Agent101 Agent105WordFiber9df76b

/-- The number of bounded digit splits, allowing a zero high digit. -/
def rawWeight (qs : List Nat) : Nat :=
  (Agent101.rawWords (Agent105WordFiber9df76b.half qs)
    (Agent105WordFiber9df76b.center qs)).length

/-- Adding a matching exterior pair adds one entry to the low half. -/
theorem half_wrap (q : Nat) (qs : List Nat) :
    half (wrapDigits q q qs) = q :: half qs := by
  have hdiv : (qs.length + 2) / 2 = qs.length / 2 + 1 := by omega
  unfold half
  rw [length_wrapDigits, hdiv]
  change (q :: (qs ++ [q])).take (qs.length / 2 + 1) =
    q :: qs.take (qs.length / 2)
  rw [List.take_succ_cons, List.take_append_of_le_length (by omega)]

/-- Adding an exterior pair preserves the optional middle coefficient. -/
theorem center_wrap (q : Nat) (qs : List Nat) :
    center (wrapDigits q q qs) = center qs := by
  have hdiv : (qs.length + 2) / 2 = qs.length / 2 + 1 := by omega
  have hmod : (qs.length + 2) % 2 = qs.length % 2 := by omega
  unfold center
  simp only [length_wrapDigits, hdiv, hmod]
  by_cases heven : qs.length % 2 = 0
  · simp only [if_pos heven]
  · simp only [if_neg heven, wrapDigits, List.getElem?_cons_succ]
    exact List.getElem?_append_left (by omega)

/-- There is exactly one split of an empty coefficient list. -/
theorem rawWeight_nil : rawWeight [] = 1 := by
  rfl

/-- An exterior coefficient contributes its existing digit-pair count. -/
theorem rawWeight_wrap (q : Nat) (qs : List Nat) :
    rawWeight (wrapDigits q q qs) = pairCount false q * rawWeight qs := by
  simp only [rawWeight, half_wrap, center_wrap, length_rawWords,
    List.map_cons, natProduct]
  exact Nat.mul_left_comm _ _ _

/-- The decoded exterior coefficients one and six contribute seven splits. -/
theorem wordFiber_wrap_one_six_length (qs : List Nat) :
    (wordFiber (wrapDigits 1 1 (wrapDigits 6 6 qs))).length =
      7 * rawWeight qs := by
  simp only [wordFiber, half_wrap, center_wrap, length_numericFiber_cons,
    List.map_cons, natProduct, rawWeight, length_rawWords]
  have hone : pairCount true 1 = 1 := by decide
  have hsix : pairCount false 6 = 7 := by decide
  rw [hone, hsix, Nat.one_mul]
  exact Nat.mul_left_comm _ _ _

#print axioms half_wrap
#print axioms center_wrap
#print axioms rawWeight_nil
#print axioms rawWeight_wrap
#print axioms wordFiber_wrap_one_six_length

end P196.ResidualFivePredecessorMass
