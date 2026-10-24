import P196.Core.AlternatingScalarBoundary

/-!
Agent #218: an exact period-three counterexample to extending the scalar
two-predecessor erasure argument to the six-phase constant-band trace.

These are traces in the existing local spatial relation. No ordinary integer
orbit, full outside-to-band path, or accepted return certificate is asserted.
-/

namespace Agent218.SixPhaseCounterexample

open Agent9.AlternatingScalarBoundary

local instance (s : Slot) : Decidable (Valid s) := by
  unfold Valid
  infer_instance

/-- The cut in the bulk whose even phases are 2, 8, 14. -/
def S (j : Nat) : Slot :=
  match j % 3 with
  | 0 => ⟨0, 0, 0, 4⟩
  | 1 => ⟨0, 1, 0, 6⟩
  | _ => ⟨1, 1, 1, 0⟩

/-- A predecessor differing from the bulk trace at every temporal phase. -/
def X (j : Nat) : Slot :=
  match j % 3 with
  | 0 => ⟨0, 1, 0, 3⟩
  | 1 => ⟨0, 0, 0, 7⟩
  | _ => ⟨1, 0, 1, 1⟩

/-- A second predecessor: the exceptional first predecessor is viable. -/
def Y (j : Nat) : Slot :=
  match j % 3 with
  | 0 => ⟨1, 0, 0, -1⟩
  | 1 => ⟨1, 0, 0, 3⟩
  | _ => ⟨0, 0, 1, 5⟩

def qXS (j : Nat) : Int :=
  match j % 3 with | 0 => 2 | 1 => 8 | _ => 14

def rXS (j : Nat) : Int :=
  match j % 3 with | 0 => 4 | 1 => 16 | _ => 10

def eXS (j : Nat) : Int :=
  match j % 3 with | 0 => 0 | _ => 1

def qYX (j : Nat) : Int :=
  match j % 3 with | 0 => 6 | 1 => 3 | _ => 10

def rYX (j : Nat) : Int :=
  match j % 3 with | 0 => 13 | 1 => 7 | _ => 1

def eYX (j : Nat) : Int :=
  match j % 3 with | 0 => 1 | _ => 0

theorem tile_XS (j : Nat) :
    Tile (X j) (S j) (qXS j) (rXS j) (eXS j) (qXS (j + 1)) := by
  have hj : j % 3 = 0 ∨ j % 3 = 1 ∨ j % 3 = 2 := by omega
  have hn : (j + 1) % 3 = (j % 3 + 1) % 3 := by omega
  rcases hj with hj | hj | hj <;>
    simp only [X, S, qXS, rXS, eXS, hn, hj] <;>
    constructor <;> decide

theorem tile_YX (j : Nat) :
    Tile (Y j) (X j) (qYX j) (rYX j) (eYX j) (qYX (j + 1)) := by
  have hj : j % 3 = 0 ∨ j % 3 = 1 ∨ j % 3 = 2 := by omega
  have hn : (j + 1) % 3 = (j % 3 + 1) % 3 := by omega
  rcases hj with hj | hj | hj <;>
    simp only [Y, X, qYX, rYX, eYX, hn, hj] <;>
    constructor <;> decide

/-- Every exact tile field holds at every time, including the temporal seam. -/
theorem step_XS : Step X S :=
  ⟨qXS, rXS, eXS, tile_XS⟩

theorem step_YX : Step Y X :=
  ⟨qYX, rYX, eYX, tile_YX⟩

theorem everywhere_ne (j : Nat) : X j ≠ S j := by
  have hj : j % 3 = 0 ∨ j % 3 = 1 ∨ j % 3 = 2 := by omega
  rcases hj with hj | hj | hj <;> simp only [X, S, hj] <;> decide

/-- No one-shift erasure statement of this form can hold for this bulk. -/
theorem shifted_erasure_false :
    ¬ (∀ p x : Trace, Step p x → Step x S → ∀ j, x (j + 1) = S (j + 1)) := by
  intro h
  exact everywhere_ne 1 (h Y X step_YX step_XS 0)

end Agent218.SixPhaseCounterexample

#print axioms Agent218.SixPhaseCounterexample.step_XS
#print axioms Agent218.SixPhaseCounterexample.step_YX
#print axioms Agent218.SixPhaseCounterexample.everywhere_ne
#print axioms Agent218.SixPhaseCounterexample.shifted_erasure_false
