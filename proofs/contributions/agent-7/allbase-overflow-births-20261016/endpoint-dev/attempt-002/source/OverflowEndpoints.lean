import OverflowDigits

/-!
The two endpoints of the actual overflowing paired word.
The unchanged normalization appends the computed terminal one, so each
endpoint is one plus the first ordinary remainder. Coefficient bounds are
needed only to identify the old coefficient in the binary maximum case.

This module proves the all-base endpoint classification. The existing
`IntrinsicReverseAdd.binary_safety_boundary` remains the provenance for the
previously formalized binary 110 -> 1001 example; no new example claim is made.
-/

namespace P196.Agent7.AllBaseOverflow

open ResetNormalization PhysicalWidth ReverseAdd

/-- Adding the actual terminal one makes an endpoint positive in every
base at least two, even if the old coefficient has no bounds. -/
theorem endpoint_residue_positive (b q : Int) (hb : 2 ≤ b) :
    0 < 1 + q % b := by
  have hmod := Int.emod_nonneg q (show b ≠ 0 by omega)
  omega

/-- In bases at least three, an endpoint cannot reach the maximal paired
coefficient. This conclusion also needs no bounds on the old coefficient. -/
theorem endpoint_residue_below_max (b q : Int) (hb : 3 ≤ b) :
    1 + q % b < 2 * b - 2 := by
  have hmod := Int.emod_lt_of_pos q (show 0 < b by omega)
  omega

/-- The bounded coefficient itself is determined in the exceptional binary
case; without this bound, only its odd remainder would be determined. -/
theorem endpoint_residue_max_iff (b q : Int) (hb : 2 ≤ b)
    (hq : 0 ≤ q ∧ q ≤ 2 * b - 2) :
    1 + q % b = 2 * b - 2 ↔ b = 2 ∧ q = 1 := by
  have hmod := Int.emod_lt_of_pos q (show 0 < b by omega)
  constructor
  · intro heq
    have hb2 : b = 2 := by omega
    have hq1 : q = 1 := by
      subst b
      omega
    exact ⟨hb2, hq1⟩
  · rintro ⟨rfl, rfl⟩
    decide

/-- A computed terminal one excludes an empty source. Thus the coefficient
returned by getD at zero is a real source element, and inherits its bound. -/
theorem overflow_head_coefficient_bound (b : Int) (xs : List (Int × Bool))
    (hbound : Bounded b xs) (ho : terminal b 0 (ordinaryTags xs) = 1) :
    0 ≤ (xs.getD 0 (0, false)).1 ∧
      (xs.getD 0 (0, false)).1 ≤ 2 * b - 2 := by
  have hx0 := overflow_length_pos b xs ho
  have hq := hbound (xs[0]'hx0) (List.getElem_mem hx0)
  simpa only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hx0,
    Option.getD_some] using hq

/-- Both actual output endpoints are strictly positive. No symmetry or
coefficient bound is required. -/
theorem actual_overflow_endpoints_pos (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (ho : terminal b 0 (ordinaryTags xs) = 1) :
    0 < (pairs (actualDigits b xs)).getD 0 0 ∧
      0 < (pairs (actualDigits b xs)).getD xs.length 0 := by
  rcases actual_overflow_endpoints b xs ho with ⟨hfirst, hlast⟩
  rw [hfirst, hlast]
  exact ⟨endpoint_residue_positive b _ hb, endpoint_residue_positive b _ hb⟩

/-- In particular, neither actual endpoint is a zero paired coefficient. -/
theorem actual_overflow_endpoints_nonzero (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (ho : terminal b 0 (ordinaryTags xs) = 1) :
    (pairs (actualDigits b xs)).getD 0 0 ≠ 0 ∧
      (pairs (actualDigits b xs)).getD xs.length 0 ≠ 0 := by
  have hpos := actual_overflow_endpoints_pos b xs hb ho
  constructor <;> omega

/-- Each actual endpoint is maximal exactly in base two when the bounded
old endpoint coefficient is one. The two equivalences are stated separately. -/
theorem actual_overflow_endpoints_max_iff (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hbound : Bounded b xs)
    (ho : terminal b 0 (ordinaryTags xs) = 1) :
    ((pairs (actualDigits b xs)).getD 0 0 = 2 * b - 2 ↔
      b = 2 ∧ (xs.getD 0 (0, false)).1 = 1) ∧
    ((pairs (actualDigits b xs)).getD xs.length 0 = 2 * b - 2 ↔
      b = 2 ∧ (xs.getD 0 (0, false)).1 = 1) := by
  rcases actual_overflow_endpoints b xs ho with ⟨hfirst, hlast⟩
  rw [hfirst, hlast]
  have hq := overflow_head_coefficient_bound b xs hbound ho
  exact ⟨endpoint_residue_max_iff b _ hb hq, endpoint_residue_max_iff b _ hb hq⟩

/-- In every base at least three, both endpoints avoid both extreme paired
coefficients. Coefficient bounds and source symmetry are unnecessary here. -/
theorem actual_overflow_endpoints_nonextreme (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (ho : terminal b 0 (ordinaryTags xs) = 1) :
    ((pairs (actualDigits b xs)).getD 0 0 ≠ 0 ∧
      (pairs (actualDigits b xs)).getD 0 0 ≠ 2 * b - 2) ∧
    ((pairs (actualDigits b xs)).getD xs.length 0 ≠ 0 ∧
      (pairs (actualDigits b xs)).getD xs.length 0 ≠ 2 * b - 2) := by
  have hn := actual_overflow_endpoints_nonzero b xs (by omega) ho
  rcases actual_overflow_endpoints b xs ho with ⟨hfirst, hlast⟩
  have hlt := endpoint_residue_below_max b (xs.getD 0 (0, false)).1 hb
  constructor
  · exact ⟨hn.1, by rw [hfirst]; omega⟩
  · exact ⟨hn.2, by rw [hlast]; omega⟩

#print axioms endpoint_residue_positive
#print axioms endpoint_residue_below_max
#print axioms endpoint_residue_max_iff
#print axioms overflow_head_coefficient_bound
#print axioms actual_overflow_endpoints_pos
#print axioms actual_overflow_endpoints_nonzero
#print axioms actual_overflow_endpoints_max_iff
#print axioms actual_overflow_endpoints_nonextreme

end P196.Agent7.AllBaseOverflow
