import P196.Agent6CoordinateThreshold.ExteriorFactorizationProof

/-!
Agent #5: executable coordinate digit streams for the existing exterior map.

The low stream represents an integer numerator divided by 9 in the 10-adic
direction. The high stream is ordinary decimal long division. Both definitions
are total; their intended digit bounds and exterior-map correspondence are
proved in the adjoining modules, with the original state definitions unchanged.
-/

namespace Agent5.ExactDigitStreams

/-- First `n` low digits of the 10-adic quotient `a / 9`. -/
def adicNumeratorDigits : Nat → Int → List Nat
  | 0, _ => []
  | n + 1, a =>
      let d := ((-a) % 10).toNat
      d :: adicNumeratorDigits n ((a - 9 * (d : Int)) / 10)

/-- First `n` decimal fractional digits of `r / D`, by long division. -/
def fractionDigits : Nat → Nat → Nat → List Nat
  | 0, _, _ => []
  | n + 1, r, D =>
      (10 * r) / D :: fractionDigits n ((10 * r) % D) D

@[simp] theorem adicNumeratorDigits_length (n : Nat) (a : Int) :
    (adicNumeratorDigits n a).length = n := by
  induction n generalizing a with
  | zero => rfl
  | succ n ih => simp [adicNumeratorDigits, ih]

@[simp] theorem fractionDigits_length (n r D : Nat) :
    (fractionDigits n r D).length = n := by
  induction n generalizing r with
  | zero => rfl
  | succ n ih => simp [fractionDigits, ih]

end Agent5.ExactDigitStreams
