import Agent102PiecewiseCounts

namespace Agent102.ParameterSets.PiecewiseReviewer

set_option maxRecDepth 8192

def zeroAtom : CountExpr := .atom ⟨0, 0⟩

def zeroSum : CountExpr := .add zeroAtom (.add zeroAtom zeroAtom)

theorem empty_sign_cases_pruned :
    zeroAtom.pieces.length = 1 ∧ zeroSum.pieces.length = 1 := by
  decide

def wedge : CountExpr := .add (.atom ⟨1, -3⟩) (.atom ⟨-1, 3⟩)

theorem opposite_clips_have_three_pieces : wedge.pieces.length = 3 := by
  decide

theorem opposite_clips_zero_only_at_three :
    eqRegion wedge .zero = [⟨3, some 4⟩] := by
  decide

def H : Nat :=
  10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def hugeRamp : CountExpr := .atom ⟨1, -(H : Int)⟩

theorem huge_zero_boundary :
    test (eqRegion hugeRamp .zero) H = true ∧
    test (eqRegion hugeRamp .zero) (H + 1) = false ∧
    inhabited (ltRegion hugeRamp .zero) = false := by
  decide

#print axioms empty_sign_cases_pruned
#print axioms opposite_clips_have_three_pieces
#print axioms opposite_clips_zero_only_at_three
#print axioms huge_zero_boundary

end Agent102.ParameterSets.PiecewiseReviewer
