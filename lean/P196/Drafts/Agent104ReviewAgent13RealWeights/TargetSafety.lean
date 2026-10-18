import P196.Drafts.Agent104ReviewAgent13RealWeights.Family

namespace Agent13SafeFamily
open DecimalDigits Lychrel196

def targetDigit (k : Nat) : Nat → Nat := extended (familyColumn k) (2*k+2)

theorem targetDigit_leading (k : Nat) : targetDigit k (2*k+3-1) = 1 := by
  simp [targetDigit, extended, familyColumn_carry, show ¬ 2*k+2 ≤ k by omega]

theorem targetDigit_units (k : Nat) (hk : 0 < k) : targetDigit k 0 = 9 := by
  simp [targetDigit, extended, output, carry, familyColumn,
    show 0 < 2*k+2 by omega, show 0 ≠ k by omega]

theorem target_canonical (k : Nat) : Canonical (target k) (targetDigit k) (2*k+3) := by
  refine ⟨by omega, ?_, ?_, ?_⟩
  · intro i hi
    unfold targetDigit extended
    split
    · exact output_bounded _ _
    · rw [familyColumn_carry]
      split <;> omega
  · rw [targetDigit_leading]; decide
  · change value (extended (familyColumn k) (2*k+2)) ((2*k+2)+1) = target k
    rw [value_extended, value_output, familyColumn_value]

theorem target_not_palindrome (k : Nat) (hk : 0 < k) : ¬ Palindrome (target k) := by
  intro hp
  have hc := target_canonical k
  rw [← hc.2.2.2] at hp
  have hs := (palindrome_value_iff _ _ hc.2.1 (Or.inr hc.2.2.1)).mp hp
  have hz := hs 0 (by omega)
  simp only [Nat.sub_zero, targetDigit_units k hk, targetDigit_leading] at hz
  omega

theorem target_outer_column (k : Nat) (hk : 0 < k) :
    columnSum (targetDigit k) (2*k+3) 0 = 10 := by
  simp only [columnSum, reflected, Nat.sub_zero,
    targetDigit_units k hk, targetDigit_leading]

theorem target_step_not_palindrome (k : Nat) (hk : 0 < k) :
    ¬ Palindrome (step (target k)) := by
  intro hp
  have hc := target_canonical k
  rw [← hc.2.2.2] at hp
  have hb := (step_palindrome_iff _ _ hc.1 hc.2.1 hc.2.2.1).mp hp
  have ho := target_outer_column k hk
  rcases hb with hs | hs
  · have h := hs 0 (by omega); omega
  · omega

theorem target_gt_pow (k : Nat) : 10^(2*k+2) < target k := by
  have hp : 0 < 10^k := Nat.pow_pos (by decide)
  unfold target
  omega

theorem target_safe (k : Nat) (hk : 0 < k) : Safe (target k) := by
  refine ⟨?_, target_not_palindrome k hk, target_step_not_palindrome k hk⟩
  exact Nat.lt_trans (Nat.pow_pos (by decide)) (target_gt_pow k)

theorem value_lt_pow (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9) : value d L < 10^L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    have hb := ih (fun i hi => hd i (by omega))
    have hm := Nat.mul_le_mul_right (10^L) (hd L (by omega))
    simp only [value, Nat.pow_succ]
    omega

theorem family_bounds (a : Nat → Nat) (k : Nat) (hk : 0 < k)
    (ha : ∀ i, i < k → a i ≤ 9) (hlead : 0 < a (k-1)) :
    0 < family a k ∧ family a k < 10^(2*k+2) ∧ 10^(2*k+2) < target k := by
  have hc := family_canonical a k hk ha hlead
  exact ⟨value_positive _ _ hc.1 hc.2.2.1,
    value_lt_pow _ _ hc.2.1, target_gt_pow k⟩

theorem family_safe (a : Nat → Nat) (k : Nat) (hk : 0 < k)
    (ha : ∀ i, i < k → a i ≤ 9) (hlead : 0 < a (k-1)) : Safe (family a k) := by
  refine ⟨(family_bounds a k hk ha hlead).1, family_not_palindrome a k hk ha hlead, ?_⟩
  rw [family_step a k hk ha hlead]
  exact target_not_palindrome k hk

/-- Full original all-word safety and arithmetic claim, before counting. -/
theorem family_safe_predecessor (a : Nat → Nat) (k : Nat) (hk : 0 < k)
    (ha : ∀ i, i < k → a i ≤ 9) (hlead : 0 < a (k-1)) :
    Safe (family a k) ∧ Safe (target k) ∧ step (family a k) = target k ∧
      family a k < 10^(2*k+2) ∧ 10^(2*k+2) < target k := by
  exact ⟨family_safe a k hk ha hlead, target_safe k hk, family_step a k hk ha hlead,
    (family_bounds a k hk ha hlead).2⟩

end Agent13SafeFamily
