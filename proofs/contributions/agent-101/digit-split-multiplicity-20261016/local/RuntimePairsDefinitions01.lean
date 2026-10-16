import Std

/-!
Finite choices for one ordered low/high decimal digit pair and for an
optional center column. These are ordinary finite lists; the high digit
of an outer pair must be nonzero.
-/

namespace Agent101

/-- Ordered `(low digit, high digit)` choices for a prescribed pair sum. -/
def pairChoices (outer : Bool) (s : Nat) : List (Nat × Nat) :=
  ((List.range 10).product (List.range 10)).filter fun p =>
    decide (p.1 + p.2 = s ∧ (outer = true → 0 < p.2))

/-- Exact number of choices for a bounded decimal digit pair. -/
def pairCount (outer : Bool) (s : Nat) : Nat :=
  if s ≤ 9 then (if outer then s else s + 1)
  else if s ≤ 18 then 19 - s else 0

/-- An absent center contributes no digits; an even center sum fixes one digit. -/
def centerWords (c : Option Nat) : List (List Nat) :=
  match c with
  | none => [[]]
  | some s => if s ≤ 18 ∧ s % 2 = 0 then [[s / 2]] else []

/-- The explicit zero-or-one count of optional-center realizations. -/
def centerCount (c : Option Nat) : Nat :=
  match c with
  | none => 1
  | some s => if s ≤ 18 ∧ s % 2 = 0 then 1 else 0

end Agent101
