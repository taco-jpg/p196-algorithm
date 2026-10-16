import SharpnessClass

/-! Agent #4: universal-base sharpness data and every schoolbook certificate row. -/
namespace P196.Agent4.GeneralBase

def sharpFirst (b r : Nat) : Nat → Nat
  | 0 => b - 1 | 1 => b - 1 | 2 => 2 * r | 3 => 0 | 4 => 0 | 5 => 1 | _ => 0

def sharpSecond (b r : Nat) : Nat → Nat
  | 0 => 0 | 1 => 0 | 2 => 2 * r + 1 | 3 => 2 * r
  | 4 => b - 1 | 5 => 0 | 6 => 1 | _ => 0

def sharpThird (b r : Nat) : Nat → Nat
  | 0 => 1 | 1 => 0 | 2 => 2 * r | 3 => (4 * r + 1) % b
  | 4 => 2 * r + (4 * r + 1) / b | 5 => 1 | 6 => 1 | _ => 0

def sharpFourth : Nat → Nat
  | 0 => 2 | 1 => 1 | 2 => 0 | 3 => 2 | 4 => 0 | 5 => 1 | 6 => 2 | _ => 0

def sharpSeed (b : Nat) : Nat → Nat
  | 0 => 0 | 1 => 0 | 2 => b / 2 | 3 => b - 1 | 4 => b - 1 | _ => 0

def sharpSecondCarry : Nat → Nat
  | 0 => 0 | 1 => 1 | 2 => 1 | 3 => 0 | 4 => 0 | 5 => 0 | 6 => 1 | _ => 0

def sharpThirdCarry (b r : Nat) : Nat → Nat
  | 0 => 0 | 1 => 0 | 2 => 0 | 3 => 1
  | 4 => (4 * r + 1) / b | 5 => 1 | 6 => 0 | 7 => 0 | _ => 0

theorem sharp_quotient_bit (b r : Nat) (hb : 10 ≤ b) (hr : r < b / 2) :
    (4 * r + 1) / b ≤ 1 := by
  have h : (4 * r + 1) / b < 2 := by
    apply (Nat.div_lt_iff_lt_mul (by omega : 0 < b)).2
    omega
  omega

theorem sharp_first_canonical (b r : Nat) (hb : 10 ≤ b) (hr : r < b / 2) :
    CanonicalDigits b 6 (sharpFirst b r) := by
  refine ⟨by decide, ?_, by simp [sharpFirst]⟩
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl <;> simp [sharpFirst] <;> omega

theorem sharp_second_canonical (b r : Nat) (hb : 10 ≤ b) (hr : r < b / 2) :
    CanonicalDigits b 7 (sharpSecond b r) := by
  refine ⟨by decide, ?_, by simp [sharpSecond]⟩
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [sharpSecond] <;> omega

theorem sharp_third_canonical (b r : Nat) (hb : 10 ≤ b) (hr : r < b / 2) :
    CanonicalDigits b 7 (sharpThird b r) := by
  have hq := sharp_quotient_bit b r hb hr
  have hm := Nat.mod_lt (4 * r + 1) (by omega : 0 < b)
  refine ⟨by decide, ?_, by simp [sharpThird]⟩
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [sharpThird] <;> omega

theorem sharp_fourth_canonical (b : Nat) (hb : 10 ≤ b) :
    CanonicalDigits b 7 sharpFourth := by
  refine ⟨by decide, ?_, by simp [sharpFourth]⟩
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [sharpFourth] <;> omega

theorem sharp_seed_canonical (b : Nat) (hb : 10 ≤ b) :
    CanonicalDigits b 5 (sharpSeed b) := by
  refine ⟨by decide, ?_, ?_⟩
  · intro i hi
    have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
    rcases h with rfl | rfl | rfl | rfl | rfl <;> simp [sharpSeed] <;> omega
  · simp [sharpSeed]
    omega

theorem sharp_seed_pairs (b : Nat) (hbe : b % 2 = 0) (i : Nat) (hi : i < 5) :
    pairCoeff 5 (sharpSeed b) i = sharpPair b 0 i := by
  have heven := Nat.mod_add_div b 2
  rw [hbe] at heven
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl <;>
    simp [pairCoeff, sharpSeed, sharpPair] <;> omega

theorem sharp_first_rows (b r : Nat) (hb : 10 ≤ b) (i : Nat) (hi : i < 5) :
    sharpPair b r i + sharpCarry i = sharpFirst b r i + b * sharpCarry (i + 1) := by
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl <;>
    simp [sharpPair, sharpCarry, sharpFirst] <;> omega

theorem sharp_second_rows (b r : Nat) (hb : 10 ≤ b) (i : Nat) (hi : i < 6) :
    pairCoeff 6 (sharpFirst b r) i + sharpSecondCarry i =
      sharpSecond b r i + b * sharpSecondCarry (i + 1) := by
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [pairCoeff, sharpFirst, sharpSecond, sharpSecondCarry] <;> omega

theorem sharp_third_rows (b r : Nat) (hb : 10 ≤ b) (i : Nat) (hi : i < 7) :
    pairCoeff 7 (sharpSecond b r) i + sharpThirdCarry b r i =
      sharpThird b r i + b * sharpThirdCarry b r (i + 1) := by
  have hm := Nat.mod_add_div (4 * r + 1) b
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [pairCoeff, sharpSecond, sharpThird, sharpThirdCarry] <;> omega

theorem sharp_fourth_symmetric : Symmetric 7 sharpFourth := by
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> rfl

end P196.Agent4.GeneralBase

#print axioms P196.Agent4.GeneralBase.sharp_quotient_bit
#print axioms P196.Agent4.GeneralBase.sharp_first_canonical
#print axioms P196.Agent4.GeneralBase.sharp_second_canonical
#print axioms P196.Agent4.GeneralBase.sharp_third_canonical
#print axioms P196.Agent4.GeneralBase.sharp_fourth_canonical
#print axioms P196.Agent4.GeneralBase.sharp_seed_canonical
#print axioms P196.Agent4.GeneralBase.sharp_seed_pairs
#print axioms P196.Agent4.GeneralBase.sharp_first_rows
#print axioms P196.Agent4.GeneralBase.sharp_second_rows
#print axioms P196.Agent4.GeneralBase.sharp_third_rows
#print axioms P196.Agent4.GeneralBase.sharp_fourth_symmetric
