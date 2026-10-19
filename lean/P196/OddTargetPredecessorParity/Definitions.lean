import P196.CompleteFiberParity.Integration

/-!
# Arithmetic candidates for odd-target predecessor parity

Agent #6: the target's two boundary digits select the only source width
that can contribute odd multiplicity. A shifted half-target supplies
the corresponding palindrome candidate.
-/

set_option autoImplicit false

namespace OddTargetPredecessorParity

/-- The source width selected by the target's leading and units digits. -/
def selectedWidth (e : Nat → Nat) (W : Nat) : Nat :=
  if e (W - 1) = 1 ∧ e 0 = 9 then W - 1 else W

/-- The half-target after adding one in both outer coefficient positions. -/
def shiftedHalf (Y L : Nat) : Nat :=
  (Y + 10 ^ (L - 1) + 1) / 2

/-- A palindrome of the required width with leading digit at most five. -/
def candidateAccepts (Y L : Nat) : Prop :=
  2 ≤ L ∧
  10 ^ (L - 1) ≤ shiftedHalf Y L ∧
  shiftedHalf Y L < 6 * 10 ^ (L - 1) ∧
  Lychrel196.Palindrome (shiftedHalf Y L)

/-- The candidate test is decidable by ordinary integer arithmetic. -/
instance candidateAcceptsDecidable (Y L : Nat) : Decidable (candidateAccepts Y L) := by
  unfold candidateAccepts
  infer_instance

#print axioms selectedWidth
#print axioms shiftedHalf
#print axioms candidateAccepts
#print axioms candidateAcceptsDecidable

end OddTargetPredecessorParity
