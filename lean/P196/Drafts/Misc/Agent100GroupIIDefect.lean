import P196.Drafts.Agent100GroupIIOverlap.Agent100GroupIIDynamics

/-! Mechanism of the Group II delayed overlap repair.  The redundant overlap
is used only as a comparison word: it is not an admissible pair word.
Its normalized difference from the actual middle word is antisymmetric,
so the next reflected column sum cancels the difference exactly.
The final theorem records failure of renewal within the same four-core shape. -/

namespace Agent100.GroupII

set_option maxHeartbeats 4000000
set_option maxRecDepth 10000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open DelayedOverlapGate

def redundantCarry (r i : Nat) : Nat :=
  if i = r + 3 ∨ i = r + 4 ∨ i = r + 5 then 2
  else if i = r + 2 ∨ i = r + 6 then 1 else 0

def coefficientDefect (r i : Nat) : Int :=
  if i = r + 1 ∨ i = r + 5 then 1
  else if i = r + 2 ∨ i = r + 4 then -19
  else if i = r + 3 then -18 else 0

def digitDefect (r i : Nat) : Int :=
  if i = r + 1 ∨ i = r + 2 then 1
  else if i = r + 4 ∨ i = r + 5 then -1 else 0

/-- The exact signed coefficient error has central values (1,-19,-18,-19,1). -/
theorem coefficient_defect_exact (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, (middle r p u v i : Int) - (redundant r p u v i : Int) =
      coefficientDefect r i := by
  intro i
  unfold Domain at h
  simp only [middle, redundant, initial, fiveWord, coefficientDefect]
  repeat (first | omega | split)

theorem redundant_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (redundant r p u v) i = redundantCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold redundantCarry; repeat (first | omega | split))
  intro i hi
  simp only [redundant, initial, fiveWord, redundantCarry]
  repeat (first | omega | split)

theorem redundant_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (redundant r p u v) (2 * r + 7) = 0 := by
  rw [redundant_carry r p u v h _ (Nat.le_refl _)]
  unfold redundantCarry
  repeat (first | omega | split)

/-- Normalization turns the coefficient error into (1,1,0,-1,-1). -/
theorem normalized_digit_defect_exact (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 7 →
      (output (middle r p u v) i : Int) - (output (redundant r p u v) i : Int) =
        digitDefect r i := by
  intro i hi
  simp only [output]
  rw [middle_carry r p u v h i (by omega), redundant_carry r p u v h i (by omega)]
  unfold Domain at h
  simp only [middle, redundant, initial, fiveWord, middleCarry, redundantCarry, digitDefect]
  repeat (first | omega | split)

theorem digitDefect_antisymmetric (r : Nat) :
    ∀ i, i < 2 * r + 7 →
      digitDefect r i = -digitDefect r (2 * r + 7 - 1 - i) := by
  intro i hi
  simp only [digitDefect]
  repeat (first | omega | split)

/-- The antisymmetric normalized error cancels in the next reflected sum. -/
theorem seam_cancels_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 7 →
      nextColumns (middle r p u v) (2 * r + 7) i =
        nextColumns (redundant r p u v) (2 * r + 7) i := by
  intro i hi
  simp only [nextColumns, middle_no_overflow r p u v h,
    redundant_no_overflow r p u v h, if_true]
  apply columnSum_eq_of_antisymmetric_difference _ _ _ _ i hi
  intro j hj
  rw [normalized_digit_defect_exact r p u v h j hj,
    normalized_digit_defect_exact r p u v h (2 * r + 7 - 1 - j) (by omega)]
  exact digitDefect_antisymmetric r j hj

theorem redundant_not_admissible (r p u v : Nat) (h : Domain r p u v) :
    ¬ Admissible (2 * r + 7) (redundant r p u v) := by
  intro ha
  have hb := ha.2.2.1 (r + 3) (by omega)
  simp only [redundant, initial, fiveWord_center r p u (u + v) (2 * v) h.1] at hb
  unfold Domain at h
  omega

/-- The six-column return cannot close the original four-column component
family at the same spacer and width.  The new coefficient at r is 1. -/
theorem returnedComponent_not_same_shape (r p u v : Nat) (hr : 1 ≤ r) :
    ¬ ∃ p' u' v', ∀ i, i < 2 * r + 6 →
      returnedComponent r p u v i = component r p' u' v' i := by
  rintro ⟨p', u', v', he⟩
  have hx := he r (by omega)
  rw [(returnedComponent_core_table r p u v hr).1] at hx
  simp only [component] at hx
  repeat (first | omega | split at hx)

end Agent100.GroupII

#print axioms Agent100.GroupII.coefficient_defect_exact
#print axioms Agent100.GroupII.redundant_carry
#print axioms Agent100.GroupII.redundant_no_overflow
#print axioms Agent100.GroupII.normalized_digit_defect_exact
#print axioms Agent100.GroupII.digitDefect_antisymmetric
#print axioms Agent100.GroupII.seam_cancels_next
#print axioms Agent100.GroupII.redundant_not_admissible
#print axioms Agent100.GroupII.returnedComponent_not_same_shape
