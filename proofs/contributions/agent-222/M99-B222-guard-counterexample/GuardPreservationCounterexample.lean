import SevenStepOrbit

/-!
Agent #222 / Manager #99 assignment M99-B222.

Kernel-checkable formalization of Agent #12's ordinary-decimal witness
against the repository's actual pair-word semantics. The theorem refutes
only unconditional preservation of SevenGuards after a guarded seven-step
return; it makes no claim about the P196 orbit.

Witness pair word:
  (4,4,0,1,3,16,3,1,0,4,4)

The corresponding ordinary decimal seed is 44013800000.
-/

namespace Agent222M99B222

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary Lychrel196 SevenStepOrbit

def witnessQ : Nat → Nat
  | 0 => 4
  | 1 => 4
  | 2 => 0
  | 3 => 1
  | 4 => 3
  | 5 => 16
  | 6 => 3
  | 7 => 1
  | 8 => 0
  | 9 => 4
  | 10 => 4
  | _ => 0

theorem witness_admissible : Admissible 11 witnessQ := by
  unfold Admissible
  constructor
  · omega
  constructor
  · rfl
  constructor
  · intro i hi
    interval_cases i <;> decide
  constructor
  · intro i hi
    interval_cases i <;> decide
  · intro i hi hcenter
    interval_cases i <;> decide

theorem witness_initial_boundary : boundary witnessQ = initial := by
  rfl

theorem witness_first_guard : SevenGuards witnessQ 11 := by
  decide

theorem witness_returned_guard_fails :
    ¬ SevenGuards
      (fun i => (iterPairs witnessQ 11 7).2 i)
      (iterPairs witnessQ 11 7).1 := by
  decide

theorem guard_preservation_counterexample :
    ¬ (∀ (q : Nat → Nat) (L : Nat),
      6 ≤ L →
      Admissible L q →
      boundary q = initial →
      SevenGuards q L →
      SevenGuards
        (fun i => (iterPairs q L 7).2 i)
        (iterPairs q L 7).1) := by
  intro h
  have hreturned :=
    h witnessQ 11 (by omega) witness_admissible witness_initial_boundary
      witness_first_guard
  exact witness_returned_guard_fails hreturned

#print axioms witness_admissible
#print axioms witness_first_guard
#print axioms witness_returned_guard_fails
#print axioms guard_preservation_counterexample

end Agent222M99B222
