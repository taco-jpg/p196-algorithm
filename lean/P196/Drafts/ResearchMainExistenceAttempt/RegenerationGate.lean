import P196.Drafts.D20261015ExternalIntrinsicReviewSources.IntrinsicSeam

/-!
A concrete all-gap safe neutral-band regeneration gate.

For every g>=0, the canonical pair word B,9^g,H,9^g,reverse(B), with
B=(1,9,12,3,14,14) and H=(4,4,15,10,15,4,4), updates without overflow
to C,9^(g+4),J,9^(g+4),reverse(C), where C=(3,9,4,8), J=(11,2,11).
This is one exact safe expansion, not recurrent closure or a Lychrel proof.
All indices are least-significant first.
-/

namespace RegenerationGate

open DecimalDigits FoldedDecimal IntrinsicSeam

def width (g : Nat) : Nat := 2 * g + 19

/-- Explicit source coefficients, including both possibly empty 9-bands. -/
def source (g i : Nat) : Nat :=
  if i = 0 ∨ i = 2 * g + 18 then 1
  else if i = 1 ∨ i = 2 * g + 17 ∨
      (6 ≤ i ∧ i < g + 6) ∨ (g + 13 ≤ i ∧ i < 2 * g + 13) then 9
  else if i = 2 ∨ i = 2 * g + 16 then 12
  else if i = 3 ∨ i = 2 * g + 15 then 3
  else if i = 4 ∨ i = 5 ∨ i = 2 * g + 13 ∨ i = 2 * g + 14 then 14
  else if i = g + 6 ∨ i = g + 7 ∨ i = g + 11 ∨ i = g + 12 then 4
  else if i = g + 8 ∨ i = g + 10 then 15
  else if i = g + 9 then 10 else 0

/-- The actual normalized digits: DB,0^g,DH,9^g,DR. -/
def normalized (g i : Nat) : Nat :=
  if i = 1 ∨ (g + 13 ≤ i ∧ i < 2 * g + 13) then 9
  else if i = g + 10 then 6
  else if i = 5 ∨ i = g + 6 ∨ i = g + 8 ∨ i = g + 11 ∨ i = 2 * g + 14 then 5
  else if i = 3 ∨ i = 4 ∨ i = g + 7 ∨ i = g + 12 ∨
      i = 2 * g + 13 ∨ i = 2 * g + 15 then 4
  else if i = 2 ∨ i = 2 * g + 16 ∨ i = 2 * g + 18 then 2
  else if i = 0 ∨ i = g + 9 then 1 else 0

/-- The exact incoming carry at every column, including the terminal one. -/
def incoming (g i : Nat) : Nat :=
  if i = 3 ∨ (5 ≤ i ∧ i ≤ g + 6) ∨ (g + 9 ≤ i ∧ i ≤ g + 11) ∨
      (2 * g + 14 ≤ i ∧ i ≤ 2 * g + 15) ∨
      (2 * g + 17 ≤ i ∧ i ≤ 2 * g + 18) then 1 else 0

/-- Target coefficients: C,9^(g+4),J,9^(g+4),reverse(C). -/
def target (g i : Nat) : Nat :=
  if i = 0 ∨ i = 2 * g + 18 then 3
  else if i = 1 ∨ i = 2 * g + 17 ∨
      (4 ≤ i ∧ i < g + 8) ∨ (g + 11 ≤ i ∧ i < 2 * g + 15) then 9
  else if i = 2 ∨ i = 2 * g + 16 then 4
  else if i = 3 ∨ i = 2 * g + 15 then 8
  else if i = g + 8 ∨ i = g + 10 then 11
  else if i = g + 9 then 2 else 0

theorem source_bounded (g i : Nat) : source g i ≤ 18 := by
  unfold source
  repeat first | omega | split

theorem normalized_bounded (g i : Nat) : normalized g i ≤ 9 := by
  unfold normalized
  repeat first | omega | split

theorem incoming_zero (g : Nat) : incoming g 0 = 0 := by
  unfold incoming
  split <;> omega

theorem incoming_terminal (g : Nat) : incoming g (width g) = 0 := by
  unfold incoming width
  split <;> omega

set_option maxHeartbeats 1000000 in
theorem exact_column_equation (g i : Nat) :
    normalized g i + 10 * incoming g (i + 1) = source g i + incoming g i := by
  have hcases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨
      (6 ≤ i ∧ i < g + 6) ∨ i = g + 6 ∨ i = g + 7 ∨ i = g + 8 ∨
      i = g + 9 ∨ i = g + 10 ∨ i = g + 11 ∨ i = g + 12 ∨
      (g + 13 ≤ i ∧ i < 2 * g + 13) ∨ i = 2 * g + 13 ∨ i = 2 * g + 14 ∨
      i = 2 * g + 15 ∨ i = 2 * g + 16 ∨ i = 2 * g + 17 ∨ i = 2 * g + 18 ∨
      2 * g + 19 ≤ i := by omega
  rcases hcases with h | h | h | h | h | h | h | h | h | h | h | h |
    h | h | h | h | h | h | h | h | h | h
  all_goals (try subst i)
  all_goals simp (disch := omega) [normalized, incoming, source]
  all_goals (repeat first | omega | split)

end RegenerationGate
