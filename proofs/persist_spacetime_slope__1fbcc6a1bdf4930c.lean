import Std

/-!
The small integer linear-algebra part of the uniform-16 slope obstruction.
These hypotheses are exactly the five (respectively three) selected rows of
the checked transducer-potential certificates. This file does not formalize
the transducer-to-integer bridge and does not prove a Lychrel existence claim.
Rational certificates can be scaled to integer coefficients/weights.
-/
namespace CarryMemorySlope

theorem unit_scale_nonpositive
    (w122 w266 w464 w468 p1129 p1137 p1513 p1521 : Int)
    (h82 : p1137 - p1129 + w122 ≤ 0)
    (h182 : p1129 - p1137 + w266 ≤ 0)
    (h2052 : w468 - w464 ≤ 0)
    (h7061 : p1521 - p1513 - w122 + w468 ≤ 0)
    (h7205 : p1513 - p1521 - w266 + w464 ≤ 0) :
    w468 ≤ 0 := by omega

theorem half_scale_nonpositive (w456 w464 w468 : Int)
    (h237 : w456 ≤ 0)
    (h2044 : w464 - 2 * w456 ≤ 0)
    (h2052 : w468 - 2 * w464 ≤ 0) :
    w468 ≤ 0 := by omega

theorem repeated_slope_nonpositive (base slope : Int) (n : Nat)
    (hb : base ≤ 0) (hs : slope ≤ 0) :
    base + (n : Int) * slope ≤ 0 := by
  have hn : 0 ≤ (n : Int) := Int.ofNat_zero_le n
  have hp : (n : Int) * slope ≤ 0 := Int.mul_nonpos_of_nonneg_of_nonpos hn hs
  omega

#print axioms unit_scale_nonpositive
#print axioms half_scale_nonpositive
#print axioms repeated_slope_nonpositive
end CarryMemorySlope
