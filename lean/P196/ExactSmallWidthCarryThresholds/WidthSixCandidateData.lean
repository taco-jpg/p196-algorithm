import P196.SevenCarryMaximalWidth.CertificateTools

/-!
Literal covers for the two width-six difference profiles at six observations.
All history decisions use the imported encoded checker, with no new transition
or enumeration definition. Each certificate checks one-sided coverage: a
retained literal bypasses history evaluation, and every other start is rejected.
-/

namespace ExactSmallWidthCarryThresholds.WidthSixCandidates

open EightCarryMaximalWidth.PrefixHistory

abbrev Pair := EightCarryMaximalWidth.Candidates.Pair

/-- One bounded literal is retained or rejected by the six-observation checker. -/
abbrev Leaf (allowed : List Pair) (p : Pair) : Prop :=
  (allowed.contains p || !survivesEncoded 6 p.1 p.2) = true

/-- Actual survival transfers a coverage certificate to membership. -/
theorem leaf_mem (allowed : List Pair) (p : Pair) (h : Leaf allowed p)
    (hs : survivesEncoded 6 p.1 p.2 = true) : p ∈ allowed := by
  simpa only [Leaf, hs, Bool.not_true, Bool.or_false, List.contains_iff_mem] using h

/-- Common one-coefficient cover with difference (1). -/
def firstColumns : List Pair := [
  ([4], [3]),
  ([6], [5]),
  ([9], [8]),
  ([11], [10]),
  ([13], [12]),
  ([15], [14]),
  ([17], [16]),
  ([18], [17])
]

/-- Two-coefficient cover with difference (1,-2). -/
def secondA : List Pair := [
  ([11, 3], [10, 5]),
  ([11, 4], [10, 6]),
  ([11, 12], [10, 14]),
  ([11, 13], [10, 15]),
  ([13, 6], [12, 8]),
  ([13, 15], [12, 17]),
  ([15, 6], [14, 8]),
  ([15, 15], [14, 17]),
  ([15, 16], [14, 18]),
  ([17, 0], [16, 2]),
  ([17, 2], [16, 4]),
  ([17, 3], [16, 5]),
  ([17, 4], [16, 6]),
  ([17, 5], [16, 7]),
  ([17, 6], [16, 8]),
  ([17, 9], [16, 11]),
  ([17, 11], [16, 13]),
  ([17, 12], [16, 14]),
  ([17, 13], [16, 15]),
  ([17, 14], [16, 16]),
  ([17, 15], [16, 17]),
  ([17, 16], [16, 18])
]

/-- Three-coefficient cover with difference (1,-2,1). -/
def thirdA : List Pair := [
  ([17, 0, 1], [16, 2, 0]),
  ([17, 0, 5], [16, 2, 4]),
  ([17, 0, 8], [16, 2, 7]),
  ([17, 0, 14], [16, 2, 13]),
  ([17, 0, 17], [16, 2, 16]),
  ([17, 2, 9], [16, 4, 8]),
  ([17, 2, 18], [16, 4, 17]),
  ([17, 3, 2], [16, 5, 1]),
  ([17, 3, 4], [16, 5, 3]),
  ([17, 3, 11], [16, 5, 10]),
  ([17, 3, 13], [16, 5, 12]),
  ([17, 9, 10], [16, 11, 9]),
  ([17, 9, 14], [16, 11, 13]),
  ([17, 9, 17], [16, 11, 16]),
  ([17, 11, 18], [16, 13, 17]),
  ([17, 12, 2], [16, 14, 1]),
  ([17, 12, 4], [16, 14, 3]),
  ([17, 12, 11], [16, 14, 10]),
  ([17, 12, 13], [16, 14, 12]),
  ([17, 16, 3], [16, 18, 2]),
  ([17, 16, 8], [16, 18, 7]),
  ([17, 16, 12], [16, 18, 11]),
  ([17, 16, 17], [16, 18, 16])
]

/-- Two-coefficient cover with difference (1,-1). -/
def secondB : List Pair := [
  ([6, 13], [5, 14]),
  ([6, 17], [5, 18]),
  ([11, 3], [10, 4]),
  ([11, 4], [10, 5]),
  ([11, 12], [10, 13]),
  ([11, 13], [10, 14]),
  ([13, 6], [12, 7]),
  ([13, 15], [12, 16]),
  ([13, 17], [12, 18]),
  ([15, 17], [14, 18])
]

/-- Three-coefficient cover with difference (1,-1,0). -/
def thirdB : List Pair := [
  ([11, 13, 9], [10, 14, 9]),
  ([13, 17, 9], [12, 18, 9])
]

#print axioms leaf_mem

end ExactSmallWidthCarryThresholds.WidthSixCandidates
