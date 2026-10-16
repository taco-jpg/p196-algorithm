import NumericStrip

/-!
Agent #14 / M99-A04: source-level regression fixtures.

UNEXECUTED in the authoring session. These fixtures are not new research
results or a replacement for the Agent #112 bridge. They must be compiled
against the exact eight-module closure in Agent14M99A04Manifest.json.
The earlier BridgeContract.lean on withdrawn PR #55 is not imported.
-/
namespace Agent14.M99A04Review

open DecimalDigits Lychrel196
open Agent9.AlternatingScalarBoundary

/-- Reject the two incompatible tails used by the withdrawn draft. -/
theorem distinct_tails : six ≠ twelve := by decide

/-- The actual arithmetic outside cut is not the special 8/17 root. -/
theorem physical_outside_not_special_root :
    Agent112.TwoPhase.physicalOutside ≠ root := by decide

/-- Regression diagnosis only: no path hypothesis is needed to refute the
withdrawn draft's simultaneous-tail assumptions. -/
theorem rejected_dual_tail (t : Trace)
    (hs : t = constant six) (ht : t = constant twelve) : False := by
  have h : six = twelve := congrFun (hs.symm.trans ht) 0
  exact distinct_tails h

/-- Exact original numeric endpoint type. In particular, both phases use
their own canonical width, the interior cut is fixed, the overflow schedule
is an explicit hypothesis, and the orientation is one global disjunction. -/
def NumericObstructionSignature : Prop :=
  ∀ (n : Nat) (D : Nat → Nat → Nat) (W : Nat → Nat),
    (∀ t, Canonical (orbit n t) (D t) (W t)) →
    ∀ (width : Nat), 0 < width →
    (∀ j, width < W (2*j) ∧ width < W (2*j+1)) →
    (∀ j,
      carry (columnSum (D (2*j)) (W (2*j))) (W (2*j)) = 0 ∧
      carry (columnSum (D (2*j+1)) (W (2*j+1))) (W (2*j+1)) = 1) →
    ((∀ j,
        columnSum (D (2*j)) (W (2*j)) (width-1) = 6 ∧
        columnSum (D (2*j)) (W (2*j)) width = 6 ∧
        columnSum (D (2*j+1)) (W (2*j+1)) (width-1) = 12 ∧
        columnSum (D (2*j+1)) (W (2*j+1)) width = 12) ∨
     (∀ j,
        columnSum (D (2*j)) (W (2*j)) (width-1) = 12 ∧
        columnSum (D (2*j)) (W (2*j)) width = 12 ∧
        columnSum (D (2*j+1)) (W (2*j+1)) (width-1) = 6 ∧
        columnSum (D (2*j+1)) (W (2*j+1)) width = 6)) → False

/-- A type regression, not an independent proof of the imported theorem. -/
theorem numeric_endpoint_matches : NumericObstructionSignature :=
  Agent112.TwoPhase.Numeric.no_numeric_persistent_alternating_band

/-- The finite cyclic bridge must discharge the original recorded contract,
including the final-to-first prefix seam, not a weakened replacement. -/
theorem finite_contract_matches :
    Agent104.TemporalStripObligations.ActualPrefixTransportObligation :=
  Agent112.TwoPhase.actual_prefix_transport

/-- The tail bridge must discharge the original recorded common-cut contract. -/
theorem tail_contract_matches :
    Agent104.TemporalStripObligations.UniformBandTailObligation :=
  Agent112.TwoPhase.uniform_band_tail

#check Agent9.AlternatingScalarBoundary.no_finite_path
#check Agent112.TwoPhase.actual_tile
#check Agent112.TwoPhase.actual_spatial_step
#check Agent112.TwoPhase.actual_outside
#check Agent112.TwoPhase.Numeric.numeric_representation
#check Agent112.TwoPhase.Numeric.finite_scope_control
#check Agent112.TwoPhase.Numeric.phase_alone_not_overflow_alternation

#print axioms distinct_tails
#print axioms physical_outside_not_special_root
#print axioms rejected_dual_tail
#print axioms numeric_endpoint_matches
#print axioms finite_contract_matches
#print axioms tail_contract_matches

end Agent14.M99A04Review
