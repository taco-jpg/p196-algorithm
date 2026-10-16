import Agent100ThirdGateBoundary

/-! Kernel-checked controls for the local third-gate boundary hypotheses.
The concrete words are least-significant-column first, with zero outside
their stated width.  These controls concern only one or two local steps. -/

namespace Agent100.ThirdGate.Controls

set_option maxHeartbeats 2000000
set_option maxRecDepth 10000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization

def neighborNineLow (i : Nat) : Nat := [7, 9, 0, 9, 7].getD i 0
def neighborNineHigh (i : Nat) : Nat := [7, 9, 10, 9, 7].getD i 0
def spacerTwo (i : Nat) : Nat := [16, 2, 18, 18, 2, 16].getD i 0
def shortestHigh (i : Nat) : Nat := [16, 16].getD i 0

theorem neighbor_nine_low_control :
    Admissible 5 neighborNineLow ∧
      neighborNineLow 0 = 7 ∧ neighborNineLow 1 = 9 ∧
      nextWidth neighborNineLow 5 = 5 ∧ nextColumns neighborNineLow 5 0 = 14 := by
  decide

theorem neighbor_nine_high_control :
    Admissible 5 neighborNineHigh ∧
      neighborNineHigh 0 = 7 ∧ neighborNineHigh 1 = 9 ∧
      nextWidth neighborNineHigh 5 = 5 ∧ nextColumns neighborNineHigh 5 0 = 15 := by
  decide

/-- The excluded second coefficient 9 does not determine the next outer
coefficient, even when width and outer coefficient agree. -/
theorem neighbor_nine_not_determined :
    ¬ ∀ q s : Nat → Nat,
      Admissible 5 q → Admissible 5 s →
      q 0 = 7 → s 0 = 7 → q 1 = 9 → s 1 = 9 →
      nextColumns q 5 0 = nextColumns s 5 0 := by
  intro h
  have hl := neighbor_nine_low_control
  have hh := neighbor_nine_high_control
  have he := h neighborNineLow neighborNineHigh hl.1 hh.1
    hl.2.1 hh.2.1 hl.2.2.1 hh.2.2.1
  rw [hl.2.2.2.2, hh.2.2.2.2] at he
  omega

theorem spacer_two_control :
    Admissible 6 spacerTwo ∧ spacerTwo 0 = 16 ∧ spacerTwo 1 = 2 ∧
      (iterPairs spacerTwo 6 2).1 = 7 ∧ (iterPairs spacerTwo 6 2).2 0 = 15 := by
  decide

/-- The low-neighbor theorem cannot replace z ≤ 1 by z ≤ 2. -/
theorem low_bound_two_false :
    ¬ ∀ (q : Nat → Nat) (L z : Nat),
      Admissible L q → 2 ≤ L → q 0 = 16 → q 1 = z → z ≤ 2 →
      (iterPairs q L 2).2 0 = 14 := by
  intro h
  have hc := spacer_two_control
  have he := h spacerTwo 6 2 hc.1 (by decide) hc.2.1 hc.2.2.1 (by decide)
  rw [hc.2.2.2.2] at he
  omega

/-- The smallest admitted width is attained by the high branch. -/
theorem shortest_high_control :
    Admissible 2 shortestHigh ∧ shortestHigh 0 = 16 ∧ shortestHigh 1 = 16 ∧
      nextWidth shortestHigh 2 = 3 ∧
      nextColumns shortestHigh 2 0 = 7 ∧ nextColumns shortestHigh 2 1 = 14 ∧
      (iterPairs shortestHigh 2 2).1 = 3 ∧ (iterPairs shortestHigh 2 2).2 0 = 15 := by
  decide

def digits97 (i : Nat) : Nat := [7, 9].getD i 0
def digits176 (i : Nat) : Nat := [6, 7, 1].getD i 0
def digits847 (i : Nat) : Nat := [7, 4, 8].getD i 0

/-- The width-two control is an ordinary decimal realization.  All pair
columns at both following times are checked within their actual widths. -/
theorem ordinary_97_control :
    Canonical 97 digits97 2 ∧ Canonical 176 digits176 3 ∧ Canonical 847 digits847 3 ∧
      orbit 97 1 = 176 ∧ orbit 97 2 = 847 ∧
      (∀ i, i < 2 → columnSum digits97 2 i = shortestHigh i) ∧
      (∀ i, i < 3 → nextColumns shortestHigh 2 i = columnSum digits176 3 i) ∧
      (∀ i, i < 3 → (iterPairs shortestHigh 2 2).2 i = columnSum digits847 3 i) := by
  decide

end Agent100.ThirdGate.Controls

#print axioms Agent100.ThirdGate.Controls.neighbor_nine_low_control
#print axioms Agent100.ThirdGate.Controls.neighbor_nine_high_control
#print axioms Agent100.ThirdGate.Controls.neighbor_nine_not_determined
#print axioms Agent100.ThirdGate.Controls.spacer_two_control
#print axioms Agent100.ThirdGate.Controls.low_bound_two_false
#print axioms Agent100.ThirdGate.Controls.shortest_high_control
#print axioms Agent100.ThirdGate.Controls.ordinary_97_control
