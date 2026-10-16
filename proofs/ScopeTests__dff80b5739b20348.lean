import NoAlternatingReturn

/-! Independent review fixtures, not an extension of Agent #4's result.
These examples test the boundary of the abstract theorem's hypotheses.
Compilation status is recorded separately; source alone is not verification. -/
namespace Agent104.TemporalStripReview
open P196.Agent4.TemporalStrip

def emptyCut : Cut Empty where
  lowEven := Empty.elim
  lowOdd := Empty.elim
  highEven := Empty.elim
  highOdd := Empty.elim
  delayed := Empty.elim

-- Nonemptiness really matters: every cut predicate is vacuous on Empty.
theorem empty_index_predicates : Valid emptyCut ∧ Outside emptyCut ∧
    LeftAligned emptyCut ∧ RightAligned emptyCut := by
  exact ⟨(by intro j; cases j), (by intro j; cases j),
    (by intro j; cases j), (by intro j; cases j)⟩

def leftStationary : Cut Unit where
  lowEven := fun _ => 0
  lowOdd := fun _ => 1
  highEven := fun _ => 0
  highOdd := fun _ => 1
  delayed := fun _ => 3

def rightStationary : Cut Unit where
  lowEven := fun _ => 1
  lowOdd := fun _ => 0
  highEven := fun _ => 1
  highOdd := fun _ => 0
  delayed := fun _ => 6

-- Aligned interior columns exist: the contradiction depends on Outside.
theorem left_stationary_valid : Valid leftStationary := by
  intro j; simp [leftStationary]
theorem left_stationary_aligned : LeftAligned leftStationary := by
  intro j; simp [leftStationary]
theorem left_stationary_column : Column id leftStationary leftStationary
    (fun _ => 6) (fun _ => 12) := by
  intro j; simp [leftStationary]

theorem right_stationary_valid : Valid rightStationary := by
  intro j; simp [rightStationary]
theorem right_stationary_aligned : RightAligned rightStationary := by
  intro j; simp [rightStationary]
theorem right_stationary_column : Column id rightStationary rightStationary
    (fun _ => 12) (fun _ => 6) := by
  intro j; simp [rightStationary]

def exterior : Cut Unit where
  lowEven := fun _ => 0
  lowOdd := fun _ => 0
  highEven := fun _ => 0
  highOdd := fun _ => 1
  delayed := fun _ => 1

theorem exterior_valid : Valid exterior := by intro j; simp [exterior]
theorem exterior_outside : Outside exterior := by intro j; simp [exterior]
theorem exterior_not_aligned : ¬ (LeftAligned exterior ∨ RightAligned exterior) := by
  intro h
  rcases h with h | h
  · have hh := (h ()).2.2.2
    simp [exterior] at hh
  · have hh := (h ()).1
    simp [exterior] at hh

-- A missing predecessor in time permits the exceptional scalar branch at 0.
-- This refutes dropping `onto` from left_backward, not the full strip theorem.
def leftOpenSource : Cut Nat where
  lowEven := fun j => if j = 0 then 1 else 0
  lowOdd := fun _ => 0
  highEven := fun _ => 0
  highOdd := fun j => if j = 0 then 0 else 1
  delayed := fun j => if j = 0 then 3 else 4

def leftOpenTarget : Cut Nat where
  lowEven := fun _ => 0
  lowOdd := fun j => if j = 0 then 0 else 1
  highEven := fun _ => 0
  highOdd := fun _ => 1
  delayed := fun j => if j = 0 then 4 else 3

def leftOpenX (j : Nat) := if j = 0 then 1 else 6
def leftOpenY (j : Nat) := if j = 0 then 3 else 12

theorem left_open_source_valid : Valid leftOpenSource := by
  intro j
  by_cases h : j = 0 <;> simp [leftOpenSource, h]
theorem left_open_target_valid : Valid leftOpenTarget := by
  intro j
  by_cases h : j = 0 <;> simp [leftOpenTarget, h]
theorem left_open_target_aligned : LeftAligned leftOpenTarget := by
  intro j
  by_cases h : j = 0 <;> simp [leftOpenTarget, h]
theorem left_open_column : Column Nat.succ leftOpenSource leftOpenTarget leftOpenX leftOpenY := by
  intro j
  by_cases h : j = 0 <;>
    simp [leftOpenSource, leftOpenTarget, leftOpenX, leftOpenY, h]
theorem left_open_source_not_aligned : ¬ LeftAligned leftOpenSource := by
  intro h
  have hh := (h 0).1
  simp [leftOpenSource] at hh

-- The analogous exceptional branch is available in the opposite alignment.
def rightOpenSource : Cut Nat where
  lowEven := fun j => if j = 0 then 0 else 1
  lowOdd := fun _ => 0
  highEven := fun _ => 1
  highOdd := fun j => if j = 0 then 1 else 0
  delayed := fun j => if j = 0 then 7 else 6

def rightOpenTarget : Cut Nat where
  lowEven := fun _ => 1
  lowOdd := fun j => if j = 0 then 1 else 0
  highEven := fun _ => 1
  highOdd := fun _ => 0
  delayed := fun j => if j = 0 then 5 else 6

def rightOpenX (j : Nat) := if j = 0 then 17 else 12
def rightOpenY (j : Nat) := if j = 0 then 15 else 6

theorem right_open_source_valid : Valid rightOpenSource := by
  intro j
  by_cases h : j = 0 <;> simp [rightOpenSource, h]
theorem right_open_target_valid : Valid rightOpenTarget := by
  intro j
  by_cases h : j = 0 <;> simp [rightOpenTarget, h]
theorem right_open_target_aligned : RightAligned rightOpenTarget := by
  intro j
  by_cases h : j = 0 <;> simp [rightOpenTarget, h]
theorem right_open_column : Column Nat.succ rightOpenSource rightOpenTarget rightOpenX rightOpenY := by
  intro j
  by_cases h : j = 0 <;>
    simp [rightOpenSource, rightOpenTarget, rightOpenX, rightOpenY, h]
theorem right_open_source_not_aligned : ¬ RightAligned rightOpenSource := by
  intro h
  have hh := (h 0).1
  simp [rightOpenSource] at hh

end Agent104.TemporalStripReview
