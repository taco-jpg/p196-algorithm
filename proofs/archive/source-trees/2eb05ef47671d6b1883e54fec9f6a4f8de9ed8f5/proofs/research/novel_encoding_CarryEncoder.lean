import Std

/-!
Exact local carry encoders from bases 2 and 4 into base 10.
These lemmas do not assert a decimal Lychrel number exists.
The source carry into a column is `c`; each theorem assumes it is 0 or 1.
-/
namespace AffineCarryEncoder

theorem centered_binary_carry (d e c : Nat)
    (hd : d ≤ 1) (he : e ≤ 1) (hc : c ≤ 1) :
    ((d + 4) + (e + 4) + c) / 10 = (d + e + c) / 2 := by
  omega

theorem centered_binary_output (d e c : Nat)
    (hd : d ≤ 1) (he : e ≤ 1) (hc : c ≤ 1) :
    ((d + 4) + (e + 4) + c) % 10 =
      (d + e + c) % 2 + 8 * (1 - (d + e + c) / 2) := by
  omega

theorem centered_quaternary_carry (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    ((d + 3) + (e + 3) + c) / 10 = (d + e + c) / 4 := by
  omega

theorem centered_quaternary_output (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    ((d + 3) + (e + 3) + c) % 10 =
      (d + e + c) % 4 + 6 * (1 - (d + e + c) / 4) := by
  omega

theorem dilated_binary_carry (d e c : Nat)
    (hd : d ≤ 1) (he : e ≤ 1) (hc : c ≤ 1) :
    (9 * d + 9 * e + c) / 10 = (d + e + c) / 2 := by
  omega

theorem dilated_binary_output (d e c : Nat)
    (hd : d ≤ 1) (he : e ≤ 1) (hc : c ≤ 1) :
    (((9 * d + 9 * e + c) % 10 : Nat) : Int) =
      9 * (((d + e + c) % 2 : Nat) : Int) +
      8 * ((((d + e + c) / 2 : Nat) : Int) - (c : Int)) := by
  omega

theorem dilated_quaternary_carry (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    (3 * d + 3 * e + c) / 10 = (d + e + c) / 4 := by
  omega

theorem dilated_quaternary_output (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    (((3 * d + 3 * e + c) % 10 : Nat) : Int) =
      3 * (((d + e + c) % 4 : Nat) : Int) +
      2 * ((((d + e + c) / 4 : Nat) : Int) - (c : Int)) := by
  omega

#print axioms centered_binary_output
#print axioms centered_quaternary_output
#print axioms dilated_binary_output
#print axioms dilated_quaternary_output
end AffineCarryEncoder

namespace AffineCarryEncoder

theorem reversed_centered_quaternary_carry (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    ((6 - d) + (6 - e) + (1 - c)) / 10 =
      1 - (d + e + c) / 4 := by
  omega

theorem reversed_centered_quaternary_output (d e c : Nat)
    (hd : d ≤ 3) (he : e ≤ 3) (hc : c ≤ 1) :
    ((6 - d) + (6 - e) + (1 - c)) % 10 =
      3 - (d + e + c) % 4 + 6 * ((d + e + c) / 4) := by
  omega

#print axioms reversed_centered_quaternary_output
end AffineCarryEncoder
