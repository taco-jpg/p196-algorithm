import Lychrel196Research

/-!
Agent #222 / M99-B222 continuation.

Exact ordinary-decimal bridge for the same witness used in the
guard-preservation counterexample. This connects the finite pair-word
witness to the actual decimal seed 44013800000 and checks its first
seven reverse-and-add iterates without using an external oracle.
-/

namespace Agent222M99B222

open Lychrel196

/-- Exact first seven ordinary reverse-and-add iterates of the witness. -/
set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem witness_orbit_values :
    orbit 44013800000 0 = 44013800000 ∧
    orbit 44013800000 1 = 44014631044 ∧
    orbit 44013800000 2 = 88028272088 ∧
    orbit 44013800000 3 = 176055554176 ∧
    orbit 44013800000 4 = 847511104847 ∧
    orbit 44013800000 5 = 1595912220595 ∧
    orbit 44013800000 6 = 7546134416546 ∧
    orbit 44013800000 7 = 14002278733003 := by
  decide

/-- None of the seed or its first seven iterates is a palindrome. -/
set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem witness_orbit_safe_through_seven :
    (∀ k, k ≤ 7 → ¬ Palindrome (orbit 44013800000 k)) := by
  intro k hk
  interval_cases k <;> decide

#print axioms witness_orbit_values
#print axioms witness_orbit_safe_through_seven

end Agent222M99B222
