import Agent102ParameterSetDecisions
import Lean
open Agent102 Agent102.ParameterSets Lean
set_option maxRecDepth 131072
def intervalJson (I : Interval) : Json :=
  Json.mkObj [("lo", Json.str (toString I.lo)), ("hi", match I.hi with | none => Json.null | some h => Json.str (toString h))]
def regionJson (R : Region) : Json := Json.arr (R.map intervalJson).toArray
def caseJson (s : String) (R : Region) : Json := Json.mkObj [("id", Json.str s), ("intervals", regionJson R)]
def left0 : List RunSpec := [⟨7, ⟨(1), (-2)⟩⟩, ⟨7, ⟨(-1), (2)⟩⟩]
def right0 : List RunSpec := [⟨7, ⟨(0), (1)⟩⟩]
def left1 : List RunSpec := [⟨4, ⟨(-1), (2)⟩⟩, ⟨4, ⟨(1), (-4)⟩⟩]
def right1 : List RunSpec := []
def left2 : List RunSpec := [⟨5, ⟨(1), (-2)⟩⟩, ⟨5, ⟨(1), (-6)⟩⟩]
def right2 : List RunSpec := [⟨5, ⟨(2), (-8)⟩⟩]
def left3 : List RunSpec := [⟨1, ⟨(0), (1)⟩⟩, ⟨7, ⟨(-1), (2)⟩⟩, ⟨1, ⟨(0), (1)⟩⟩]
def right3 : List RunSpec := [⟨1, ⟨(-1), (4)⟩⟩]
def left4 : List RunSpec := [⟨6, ⟨(1), (0)⟩⟩, ⟨6, ⟨(-1), (2)⟩⟩]
def right4 : List RunSpec := [⟨6, ⟨(0), (2)⟩⟩, ⟨6, ⟨(1), (-2)⟩⟩]
def left5 : List RunSpec := [⟨1, ⟨(1), (0)⟩⟩, ⟨2, ⟨(-1), (3)⟩⟩]
def right5 : List RunSpec := [⟨1, ⟨(1), (0)⟩⟩, ⟨1, ⟨(-1), (3)⟩⟩]
def left6 : List RunSpec := [⟨0, ⟨(0), (1)⟩⟩]
def right6 : List RunSpec := []
def left7 : List RunSpec := [⟨1, ⟨(-1), (3)⟩⟩, ⟨2, ⟨(0), (1)⟩⟩, ⟨1, ⟨(1), (-5)⟩⟩]
def left8 : List RunSpec := [⟨5, ⟨(1), (-10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)⟩⟩, ⟨5, ⟨(1), (-10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004)⟩⟩]
def right8 : List RunSpec := [⟨5, ⟨(2), (-20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004)⟩⟩]
def left9 : List RunSpec := [⟨1, ⟨(-1), (10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)⟩⟩, ⟨2, ⟨(0), (1)⟩⟩]
#eval IO.println ("A102_CANDIDATE_JSON:" ++ (Json.mkObj [("cases", Json.arr #[caseJson "two_isolated_points" (equalityRegions left0 right0),
  caseJson "bounded_empty_plateau" (equalityRegions left1 right1),
  caseJson "equality_with_middle_hole" (equalityRegions left2 right2),
  caseJson "zero_run_inside_positive_span" (equalityRegions left3 right3),
  caseJson "clipped_sums_identical" (equalityRegions left4 right4),
  caseJson "same_width_bad_digit_then_tail" (equalityRegions left5 right5),
  caseJson "literal_zero_is_not_empty" (equalityRegions left6 right6),
  caseJson "bounded_palindrome_interval" (palindromeRegions left7),
  caseJson "huge_equality_hole" (equalityRegions left8 right8),
  caseJson "huge_declining_palindrome" (palindromeRegions left9)])]).compress)
