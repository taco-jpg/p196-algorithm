import P196.Agent6CoordinateDynamics.CoordinateDynamics
import P196.Agent6CoordinateThreshold.CoordinateThreshold

/-!
Agent #6: nonvanishing and sign controls for the signed exterior increment.

These statements concern the imported literal finite exterior map.  The main
nonvanishing result needs only a positive phase, with no coefficient, width,
canonical-head, or trimming premise.  The exact canonical examples show that
both signs occur within each of the zero and one overflow classes.
-/

namespace Agent6.ExteriorCoordinates

open P196.Agent7.Finite Agent115.ExteriorFactorization

/-- Fixed-width decimal reversal is strictly below the corresponding power. -/
theorem revN_lt_power (n v : Nat) : revN n v < 10 ^ n := by
  induction n generalizing v with
  | zero => simp [revN, digitsOf, highValue]
  | succ n ih =>
    rw [revN, digitsOf, highValue_cons, digitsOf_length, Nat.pow_succ]
    have hd : v % 10 ≤ 9 := by
      have := Nat.mod_lt v (by decide : 0 < 10)
      omega
    have hr := ih (v / 10)
    change highValue (digitsOf n (v / 10)) < 10 ^ n at hr
    have hm := Nat.mul_le_mul_right (10 ^ n) hd
    omega

private theorem ten_power_mod_nine (n : Nat) : 10 ^ n % 9 = 1 := by
  induction n with
  | zero => decide
  | succ n ih => simp [Nat.pow_succ, Nat.mul_mod, ih]

private theorem reversal_difference_ne_zero (n r t : Nat)
    (hr : r < 10 ^ n) (ht : 0 < t) :
    9 * (r : Int) - (t : Int) * (10 : Int) ^ n ≠ 0 := by
  intro hz
  have he' : 9 * (r : Int) = (t : Int) * (10 : Int) ^ n := by omega
  have he : 9 * r = t * 10 ^ n := by exact_mod_cast he'
  have hmod := congrArg (fun a : Nat => a % 9) he
  have htmod : t % 9 = 0 := by
    simpa [Nat.mul_mod, ten_power_mod_nine] using hmod.symm
  have ht9 : 9 ≤ t := by omega
  have hmul : 9 * 10 ^ n ≤ t * 10 ^ n := Nat.mul_le_mul_right _ ht9
  have hstrict : 9 * r < 9 * 10 ^ n :=
    Nat.mul_lt_mul_of_pos_left hr (by decide)
  omega

/-- A nonzero overflow gives residue nine modulo ten, without phase bounds. -/
theorem highContribution_emod_ten_of_overflow_ne_zero (c : Nat) (B : List Nat)
    (hg : overflow c B ≠ 0) : highContribution c B % 10 = 9 := by
  rw [overflow_eq_highValue] at hg
  unfold phaseCarry at hg
  simp only [highContribution, if_neg hg]
  simp [Int.sub_emod, Int.add_emod, Int.mul_emod]

/-- Every positive phase has a nonzero signed increment, for every finite word. -/
theorem highContribution_ne_zero_of_pos (c : Nat) (B : List Nat) (hc : 0 < c) :
    highContribution c B ≠ 0 := by
  by_cases hg : overflow c B = 0
  · have h := hg
    rw [overflow_eq_highValue] at h
    unfold phaseCarry at h
    simp only [highContribution, if_pos h]
    exact reversal_difference_ne_zero B.length
      (revN B.length (highValue B + phaseCarry c)) (phaseDigit c)
      (revN_lt_power _ _) (phaseDigit_pos c hc)
  · intro hz
    have hm := highContribution_emod_ten_of_overflow_ne_zero c B hg
    rw [hz] at hm
    contradiction

/-- The permitted nonneutral phases inherit the unrestricted positive-phase result. -/
theorem highContribution_ne_zero_of_nonneutral (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) : highContribution c B ≠ 0 := by
  apply highContribution_ne_zero_of_pos c B
  simp only [nonneutralPhase, List.mem_cons, List.mem_nil_iff, or_false] at hc
  omega

/-- Positive phase is essential: the empty zero-phase state has zero increment. -/
theorem zero_phase_empty_control : highContribution 0 [] = 0 := by decide

/-- A canonical zero-overflow example with a negative signed increment. -/
theorem zero_overflow_negative_control :
    nonneutralPhase 2 ∧ validOuter ⟨2, [1]⟩ = true ∧
    overflow 2 [1] = 0 ∧ highContribution 2 [1] = -11 := by
  unfold nonneutralPhase
  decide

/-- A canonical zero-overflow example with a positive signed increment. -/
theorem zero_overflow_positive_control :
    nonneutralPhase 2 ∧ validOuter ⟨2, [3]⟩ = true ∧
    overflow 2 [3] = 0 ∧ highContribution 2 [3] = 7 := by
  unfold nonneutralPhase
  decide

/-- A canonical one-overflow example with a negative signed increment. -/
theorem one_overflow_negative_control :
    nonneutralPhase 2 ∧ validOuter ⟨2, [10]⟩ = true ∧
    overflow 2 [10] = 1 ∧ highContribution 2 [10] = -191 := by
  unfold nonneutralPhase
  decide

/-- A canonical one-overflow example with a positive signed increment. -/
theorem one_overflow_positive_control :
    nonneutralPhase 2 ∧ validOuter ⟨2, [13]⟩ = true ∧
    overflow 2 [13] = 1 ∧ highContribution 2 [13] = 79 := by
  unfold nonneutralPhase
  decide

/-- At the same permitted phase, zero overflow is compatible with both signs. -/
theorem both_signs_at_zero_overflow :
    ∃ Bneg Bpos : List Nat,
      nonneutralPhase 2 ∧ validOuter ⟨2, Bneg⟩ = true ∧
      validOuter ⟨2, Bpos⟩ = true ∧ overflow 2 Bneg = 0 ∧
      overflow 2 Bpos = 0 ∧ highContribution 2 Bneg < 0 ∧
      0 < highContribution 2 Bpos := by
  refine ⟨[1], [3], ?_⟩
  unfold nonneutralPhase
  decide

/-- At the same permitted phase, one overflow is compatible with both signs. -/
theorem both_signs_at_one_overflow :
    ∃ Bneg Bpos : List Nat,
      nonneutralPhase 2 ∧ validOuter ⟨2, Bneg⟩ = true ∧
      validOuter ⟨2, Bpos⟩ = true ∧ overflow 2 Bneg = 1 ∧
      overflow 2 Bpos = 1 ∧ highContribution 2 Bneg < 0 ∧
      0 < highContribution 2 Bpos := by
  refine ⟨[10], [13], ?_⟩
  unfold nonneutralPhase
  decide

end Agent6.ExteriorCoordinates
