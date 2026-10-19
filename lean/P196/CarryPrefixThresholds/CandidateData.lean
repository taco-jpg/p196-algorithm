import P196.EightCarryMaximalWidth.CandidateData

/-!
Candidate covers for seven complete carry observations with a positive
exterior difference. The checker is the existing observation-count
parameterized encoded prefix checker. The generic bounded extension
enumeration is also reused unchanged.
-/

namespace CarryPrefixThresholds.Candidates
open EightCarryMaximalWidth.PrefixHistory
open EightCarryMaximalWidth.Candidates (extensions)

abbrev Pair := EightCarryMaximalWidth.Candidates.Pair

def accepted (p : Pair) : Bool := survivesEncoded 7 p.1 p.2

/-- Every strictly ordered pair of positive exterior coefficients at most 18. -/
def positiveOuterStarts : List Pair :=
  (List.range 18).flatMap fun a =>
    (List.range a).map fun b => ([a + 1], [b + 1])

/-- A cover of the one-column starts surviving seven observations. -/
def outerCover : List Pair :=
  [([9], [8]), ([13], [12]), ([15], [14]), ([18], [17])]

/-- The fourth-smoothing bound forces the second difference into [-6,-2]. -/
def secondStarts : List Pair :=
  (List.range 5).flatMap fun d =>
    extensions 0 (d + 2) (17 - d) outerCover

def secondCover : List Pair := [([15, 16], [14, 18])]

/-- For the retained pair, the third difference must lie in [0,4]. -/
def thirdStarts : List Pair :=
  (List.range 5).flatMap fun d =>
    extensions d 0 (19 - d) secondCover

end CarryPrefixThresholds.Candidates
