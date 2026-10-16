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
  simp only [Int.mul_left_comm (c : Int) 10 (D : Int),
    Int.mul_left_comm (k : Int) 10 (D : Int)]
  omega

theorem betaNum_outerNext_raw (c : Nat) (B : List Nat) :
    betaNum (outerNext { c := c, B := B }).c (outerNext { c := c, B := B }).B =
      9 * (lowValue (rawSucc c B) : Int) -
        ((2 * (c - 9 * (if 10 ≤ c then 1 else 0)) : Nat) : Int) *
          (10 : Int) ^ (B.length + 1) := by
  unfold betaNum
  change zValue (2 * (c - 9 * (if 10 ≤ c then 1 else 0)))
      (outerNext { c := c, B := B }).B -
      ((2 * (c - 9 * (if 10 ≤ c then 1 else 0)) : Nat) : Int) = _
  rw [(successor_observation c B).1]
  simp only [Int.mul_sub, Int.mul_one]
  omega

/-- Exact signed update, including the suffix stripping in the original map. -/
theorem betaNum_outerNext (c : Nat) (B : List Nat) :
    betaNum (outerNext { c := c, B := B }).c (outerNext { c := c, B := B }).B =
      betaNum c B + highContribution c B := by
  rw [betaNum_outerNext_raw, (rawSucc_values c B).1, betaNum_eq]
  unfold highContribution
  dsimp only
  have hk : 10 * (if 10 ≤ c then 1 else 0) ≤ c := by
    split <;> omega
  generalize (if 10 ≤ c then 1 else 0) = k at hk ⊢
  generalize B.length = n
  generalize lowValue B = V
  generalize highValue B = H
  rw [Int.pow_succ, Int.mul_comm ((10 : Int) ^ n) 10]
  have h := beta_arithmetic V (10 ^ n) c k
    (if (H + k) / 10 ^ n = 0 then revN n (H + k) + (c - 9 * k) * 10 ^ n
     else 1 + 10 * revN n (H + k)) hk
  simp only [Int.natCast_pow, Int.cast_ofNat_Int] at h
  rw [h]
  by_cases hg : (H + k) / 10 ^ n = 0
  · simp only [if_pos hg, Int.natCast_add, Int.natCast_mul, Int.natCast_pow, Int.cast_ofNat_Int,
      Int.mul_add, Int.mul_assoc]
    omega
  · simp only [if_neg hg, Int.natCast_add, Int.natCast_mul, Int.cast_ofNat_Int,
      Int.mul_add, Int.mul_assoc]
    omega

end Agent6.ExteriorCoordinates
