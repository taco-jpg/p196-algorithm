import P196.Agent5ExactDigitStreams.CoordinateStreams
import P196.Agent6CoordinateThreshold.CoordinateThreshold

/-!
Agent #5: coordinate-only corollaries of the literal digit-stream identities.

The outgoing carry is replaced using Agent #6's published CoordinateThreshold
interface. The threshold and quotient facts are reused without reproving their
arithmetic. All finite exterior words, including the empty word, are included.
-/

namespace Agent5.ExactDigitStreams

open P196.Agent7.Finite Agent115.ExteriorFactorization

/-- The existing eight-phase predicate supplies Agent #6's phase hypotheses. -/
theorem nonneutralPhase_coordinate_bounds (c : Nat) (hc : nonneutralPhase c) :
    c ≤ 17 ∧ c ≠ 9 := by
  simp only [nonneutralPhase, List.mem_cons, List.not_mem_nil, or_false] at hc
  omega

/-- Agent #6's exact threshold selects the actual outgoing carry. -/
theorem overflow_eq_coordinate_selector (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 =
      if 9 * 10 ^ B.length ≤ rhoNum c B then 1 else 0 := by
  have hphase := nonneutralPhase_coordinate_bounds c hc
  change Agent6.ExteriorCoordinates.overflow c B = _
  split
  · exact (Agent6.ExteriorCoordinates.overflow_eq_one_iff
      c B hphase.1 hphase.2 hB).mpr ‹_›
  · exact (Agent6.ExteriorCoordinates.overflow_eq_zero_iff
      c B hphase.1 hphase.2).mpr (by omega)

/-- Every sufficient cutoff reconstructs the original exterior successor using
only the phase, length, and two coordinates; the high scale uses the threshold. -/
theorem outerNext_from_coordinates (c : Nat) (B : List Nat) (cut : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : B.length + 1 ≤ cut) :
    outerNext { c := c, B := B } =
      { c := bulkPhase c,
        B := stripSuffix (bulkPhase c)
          (List.zipWith (fun x y => x + y)
            (adicNumeratorDigits cut (zValue c B - (c : Int)))
            (fractionDigits cut (rhoNum c B)
              (9 * 10 ^ B.length *
                10 ^ (if 9 * 10 ^ B.length ≤ rhoNum c B then 1 else 0)))) } := by
  simpa only [overflow_eq_coordinate_selector c B hc hB] using
    outerNext_from_streams_of_cutoff c B cut hc hB hcut

/-- The same coordinate reconstruction with Agent #6's exact quotient for the
high scale. This reuses the published quotient theorem directly. -/
theorem outerNext_from_coordinates_quotient (c : Nat) (B : List Nat) (cut : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : B.length + 1 ≤ cut) :
    outerNext { c := c, B := B } =
      { c := bulkPhase c,
        B := stripSuffix (bulkPhase c)
          (List.zipWith (fun x y => x + y)
            (adicNumeratorDigits cut (zValue c B - (c : Int)))
            (fractionDigits cut (rhoNum c B)
              (9 * 10 ^ B.length *
                10 ^ (rhoNum c B / (9 * 10 ^ B.length))))) } := by
  have hphase := nonneutralPhase_coordinate_bounds c hc
  have hcarry : (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 =
      rhoNum c B / (9 * 10 ^ B.length) :=
    Agent6.ExteriorCoordinates.overflow_eq_rho_quotient c B hphase.1 hphase.2
  simpa only [hcarry] using outerNext_from_streams_of_cutoff c B cut hc hB hcut

/-- Every prefix of the high stream selected by the coordinate threshold
consists of decimal digits, with no lower bound on its requested length. -/
theorem fractionDigits_coordinates_digits_lt_ten (c : Nat) (B : List Nat) (n : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    ∀ x ∈ fractionDigits n (rhoNum c B)
      (9 * 10 ^ B.length *
        10 ^ (if 9 * 10 ^ B.length ≤ rhoNum c B then 1 else 0)), x < 10 := by
  simpa only [overflow_eq_coordinate_selector c B hc hB] using
    fractionDigits_exterior_digits_lt_ten c B n hc hB

end Agent5.ExactDigitStreams
