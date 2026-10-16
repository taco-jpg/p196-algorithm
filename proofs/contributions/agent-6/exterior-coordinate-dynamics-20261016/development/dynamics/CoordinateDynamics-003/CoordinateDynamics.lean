import ExteriorUpdateLaw

/-!
Agent #6: the signed finite-coordinate form of Agent #115's exterior update.
The existing exact update law is imported with its original identifiers.
All identities in this module describe the unchanged `outerNext` function.
They do not assert an exterior cycle or an infinite ordinary integer orbit.
-/

namespace Agent6.ExteriorCoordinates

open P196.Agent7.Finite Agent115.ExteriorFactorization

/-- Nine times the constant-tail 10-adic coordinate, as an ordinary integer. -/
def betaNum (c : Nat) (B : List Nat) : Int := zValue c B - (c : Int)

theorem betaNum_eq (c : Nat) (B : List Nat) :
    betaNum c B = 9 * (lowValue B : Int) - (c : Int) * (10 : Int) ^ B.length := by
  simp only [betaNum, zValue, Int.mul_sub, Int.mul_one]
  omega

/-- The signed high-side contribution in the exact finite update formula. -/
def highContribution (c : Nat) (B : List Nat) : Int :=
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let r := revN B.length (highValue B + k)
  if (highValue B + k) / 10 ^ B.length = 0 then
    9 * (r : Int) - (t : Int) * (10 : Int) ^ B.length
  else
    9 + 90 * (r : Int) - 10 * (t : Int) * (10 : Int) ^ B.length

private theorem beta_arithmetic (V D c k R : Nat) (hk : 10 * k ≤ c) :
    9 * ((V % D + (c + V / D - 10 * k) * D + R : Nat) : Int) -
        ((2 * (c - 9 * k) : Nat) : Int) * (10 * (D : Int)) =
      (9 * (V : Int) - (c : Int) * (D : Int)) +
        (9 * (R : Int) - 10 * ((c - 9 * k : Nat) : Int) * (D : Int)) := by
  have hk9 : 9 * k ≤ c := by omega
  have hku : 10 * k ≤ c + V / D := Nat.le_trans hk (Nat.le_add_right c (V / D))
  have hv : V % D + V / D * D = V := by
    simpa only [Nat.mul_comm] using Nat.mod_add_div V D
  have hv' : (V % D : Int) + (V / D : Int) * (D : Int) = (V : Int) := by
    exact_mod_cast hv
  rw [Int.natCast_add, Int.natCast_add, Int.natCast_mul,
    Int.ofNat_sub hku, Int.natCast_add, Int.natCast_mul,
    Int.natCast_mul, Int.ofNat_sub hk9, Int.natCast_mul]
  simp only [Int.add_mul, Int.sub_mul,
    Int.mul_add, Int.mul_sub, Int.mul_assoc]
  simp only [Int.mul_assoc, Int.mul_left_comm, Int.mul_comm] at hv' ⊢
  omega

end Agent6.ExteriorCoordinates
