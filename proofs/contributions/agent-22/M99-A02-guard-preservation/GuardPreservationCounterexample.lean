import SevenStepOrbit

/-!
Agent #22 / Manager #99 M99-A02.

Independent formalization of the concrete guard-preservation counterexample
identified on Agent #12's M99-A02 branch.  The proposed unconditional
preservation theorem is false, so this module proves the precise negation
for one ordinary decimal realization rather than weakening the target.

Source witness: q = (4,4,0,1,3,16,3,1,0,4,4), realized by
44013800000 with low-to-high digits (0,0,0,0,0,8,3,1,0,4,4).
No placeholder, custom axiom, or native_decide is used.
-/

namespace Agent22M99A02

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary Lychrel196 SevenStepOrbit

def witnessDigits : Nat → Nat
  | 0 => 0
  | 1 => 0
  | 2 => 0
  | 3 => 0
  | 4 => 0
  | 5 => 8
  | 6 => 3
  | 7 => 1
  | 8 => 0
  | 9 => 4
  | 10 => 4
  | _ => 0

def witnessQ : Nat → Nat := columnSum witnessDigits 11

def witnessSeed : Nat := 44013800000

theorem witness_digits_canonical :
    Canonical witnessSeed witnessDigits 11 := by
  constructor
  · decide
  constructor
  · intro i hi
    interval_cases i <;> simp [witnessDigits]
  constructor
  · decide
  · decide

theorem witness_q_admissible :
    Admissible 11 witnessQ := by
  refine ⟨by decide, ?_, ?_, ?_, ?_⟩
  · decide [witnessQ, columnSum, reflected, witnessDigits]
  · exact columnSum_bounded witnessDigits 11 (by
      intro i hi
      interval_cases i <;> simp [witnessDigits])
  · intro i hi
    exact columnSum_symmetric witnessDigits 11 hi
  · intro i hi hcenter
    subst hcenter
    decide [witnessQ, columnSum, reflected, witnessDigits]

theorem witness_initial_boundary :
    boundary witnessQ = initial := by
  decide [witnessQ, boundary, initial, columnSum, reflected, witnessDigits]

theorem witness_first_guard :
    SevenGuards witnessQ 11 := by
  decide [SevenGuards, controlAt, actualControl, innerCarryAt,
    iterPairs, witnessQ, columnSum, reflected, witnessDigits, carry]

theorem witness_returned_middle :
    (iterPairs witnessQ 11 7).2 =
      fun i =>
        match i with
        | 0 => 3
        | 1 => 5
        | 2 => 9
        | 3 => 15
        | 4 => 15
        | 5 => 9
        | 6 => 5
        | 7 => 3
        | _ => 0 := by
  funext i
  interval_cases i <;>
    decide [iterPairs, witnessQ, columnSum, reflected, witnessDigits,
      carry, nextWidth, nextColumns, output, extended]

theorem witness_next_guard_fails :
    ¬ SevenGuards
      (fun i => (iterPairs witnessQ 11 7).2 i)
      (iterPairs witnessQ 11 7).1 := by
  decide [SevenGuards, controlAt, actualControl, innerCarryAt,
    iterPairs, witnessQ, columnSum, reflected, witnessDigits, carry,
    nextWidth, nextColumns, output, extended]

theorem guard_preservation_counterexample :
    ∃ (q : Nat → Nat) (L : Nat),
      6 ≤ L ∧ Admissible L q ∧ boundary q = initial ∧
      SevenGuards q L ∧
      ¬ SevenGuards
        (fun i => (iterPairs q L 7).2 i)
        (iterPairs q L 7).1 := by
  exact ⟨witnessQ, 11, by decide, witness_q_admissible,
    witness_initial_boundary, witness_first_guard, witness_next_guard_fails⟩

#print axioms witness_digits_canonical
#print axioms witness_q_admissible
#print axioms witness_first_guard
#print axioms witness_returned_middle
#print axioms witness_next_guard_fails
#print axioms guard_preservation_counterexample

end Agent22M99A02
