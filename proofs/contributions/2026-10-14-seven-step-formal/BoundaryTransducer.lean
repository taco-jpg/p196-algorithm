import Std

/-!
# Exact three-coordinate boundary transducer

This file concerns a finite transducer only.  Its input control is the carry
entering the upper three columns from the unrepresented middle.  Connecting
the transducer to a complete reverse-add word requires a separate bridge.
The finite return classification does not assert that an actual trajectory
supplies the required controls, or that a return repeats indefinitely.
-/

namespace BoundaryTransducer

structure Prefix where
  a : Nat
  b : Nat
  c : Nat
  deriving DecidableEq, Repr

/-- Three lower columns, three upper columns, and the final overflow. -/
def step (p : Prefix) (control : Bool) : Prefix × Nat :=
  let l0 := p.a % 10
  let carrylo1 := p.a / 10
  let l1 := (p.b + carrylo1) % 10
  let carrylo2 := (p.b + carrylo1) / 10
  let l2 := (p.c + carrylo2) % 10
  let h0 := (p.c + control.toNat) % 10
  let k1 := (p.c + control.toNat) / 10
  let h1 := (p.b + k1) % 10
  let k2 := (p.b + k1) / 10
  let h2 := (p.a + k2) % 10
  let e := (p.a + k2) / 10
  let q := if e = 0 then
    Prefix.mk (l0 + h2) (l1 + h1) (l2 + h0)
  else
    Prefix.mk (l0 + 1) (l1 + h2) (l2 + h1)
  (q, e)

def initial : Prefix := ⟨4, 4, 0⟩

/-- The final prefix after consuming every control. -/
def run (p : Prefix) : List Bool → Prefix
  | [] => p
  | control :: controls => run (step p control).1 controls

/-- Prefix states, including the initial state and the final state. -/
def trace (p : Prefix) : List Bool → List Prefix
  | [] => [p]
  | control :: controls => p :: trace (step p control).1 controls

/-- One final-column overflow for each consumed control. -/
def overflows (p : Prefix) : List Bool → List Nat
  | [] => []
  | control :: controls =>
      (step p control).2 :: overflows (step p control).1 controls

def sevenReturn (c0 c1 c2 c3 c4 c5 c6 : Bool) : Prop :=
  run initial [c0, c1, c2, c3, c4, c5, c6] = initial

/-- Exact classification of all 128 seven-control words. -/
theorem seven_return_iff (c0 c1 c2 c3 c4 c5 c6 : Bool) :
    sevenReturn c0 c1 c2 c3 c4 c5 c6 ↔
      c0 = false ∧ c1 = false ∧ c3 = false ∧ c5 = false ∧ c6 = true := by
  unfold sevenReturn
  cases c0 <;> cases c1 <;> cases c2 <;> cases c3 <;>
    cases c4 <;> cases c5 <;> cases c6 <;> decide

/-- The two free controls do not change any prefix along a return. -/
theorem seven_trace (c2 c4 : Bool) :
    trace initial [false, false, c2, false, c4, false, true] =
      [⟨4, 4, 0⟩, ⟨8, 8, 0⟩, ⟨16, 16, 0⟩, ⟨7, 14, 7⟩,
       ⟨15, 8, 15⟩, ⟨6, 14, 14⟩, ⟨13, 9, 9⟩, ⟨4, 4, 0⟩] := by
  cases c2 <;> cases c4 <;> decide

theorem seven_overflows (c2 c4 : Bool) :
    overflows initial [false, false, c2, false, c4, false, true] =
      [0, 0, 1, 0, 1, 0, 1] := by
  cases c2 <;> cases c4 <;> decide

theorem seven_trace_of_controls (c0 c1 c2 c3 c4 c5 c6 : Bool)
    (h : c0 = false ∧ c1 = false ∧ c3 = false ∧ c5 = false ∧ c6 = true) :
    trace initial [c0, c1, c2, c3, c4, c5, c6] =
      [⟨4, 4, 0⟩, ⟨8, 8, 0⟩, ⟨16, 16, 0⟩, ⟨7, 14, 7⟩,
       ⟨15, 8, 15⟩, ⟨6, 14, 14⟩, ⟨13, 9, 9⟩, ⟨4, 4, 0⟩] := by
  rcases h with ⟨rfl, rfl, rfl, rfl, rfl⟩
  exact seven_trace c2 c4

theorem seven_overflows_of_controls (c0 c1 c2 c3 c4 c5 c6 : Bool)
    (h : c0 = false ∧ c1 = false ∧ c3 = false ∧ c5 = false ∧ c6 = true) :
    overflows initial [c0, c1, c2, c3, c4, c5, c6] =
      [0, 0, 1, 0, 1, 0, 1] := by
  rcases h with ⟨rfl, rfl, rfl, rfl, rfl⟩
  exact seven_overflows c2 c4

theorem seven_trace_of_return (c0 c1 c2 c3 c4 c5 c6 : Bool)
    (h : sevenReturn c0 c1 c2 c3 c4 c5 c6) :
    trace initial [c0, c1, c2, c3, c4, c5, c6] =
      [⟨4, 4, 0⟩, ⟨8, 8, 0⟩, ⟨16, 16, 0⟩, ⟨7, 14, 7⟩,
       ⟨15, 8, 15⟩, ⟨6, 14, 14⟩, ⟨13, 9, 9⟩, ⟨4, 4, 0⟩] :=
  seven_trace_of_controls c0 c1 c2 c3 c4 c5 c6
    ((seven_return_iff c0 c1 c2 c3 c4 c5 c6).mp h)

theorem seven_overflows_of_return (c0 c1 c2 c3 c4 c5 c6 : Bool)
    (h : sevenReturn c0 c1 c2 c3 c4 c5 c6) :
    overflows initial [c0, c1, c2, c3, c4, c5, c6] =
      [0, 0, 1, 0, 1, 0, 1] :=
  seven_overflows_of_controls c0 c1 c2 c3 c4 c5 c6
    ((seven_return_iff c0 c1 c2 c3 c4 c5 c6).mp h)

#print axioms seven_return_iff
#print axioms seven_trace
#print axioms seven_overflows
#print axioms seven_trace_of_controls
#print axioms seven_overflows_of_controls
#print axioms seven_trace_of_return
#print axioms seven_overflows_of_return

end BoundaryTransducer
