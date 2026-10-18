import P196.Drafts.Agent106CongruenceCarryBudget.Agent106CongruenceObstruction

/-!
Agent #106：CONGRUENCE_PATHS.md 中人工入口边的实际模 99、增长和十进制位宽。
本模块仅认证这些必要控制条件；真实进位预算的严格障碍由导入模块提供。

Claim: coordination commit 2d9f553521404c98c119ed92e4c0538dce17aea4.
Written source: Git blob fc8bef244f236095de36b9319f07147f23d41d1a.
-/

namespace Agent106.CongruenceBudget

open DecimalQuantitativeMass

theorem familyIndex_ge_four (R : Nat) (hR : 2 ≤ R) :
    4 ≤ familyIndex R := by
  unfold familyIndex
  omega

theorem familyWidth_ge_six (R : Nat) (hR : 2 ≤ R) :
    6 ≤ familyWidth R := by
  have hk := familyIndex_ge_four R hR
  unfold familyWidth
  omega

private theorem entry_tail_bound_shift (j : Nat) :
    990 * (j + 5) + 989 < 10 ^ (j + 4) := by
  induction j with
  | zero => decide
  | succ j ih =>
    have he : j + 1 + 4 = (j + 4) + 1 := by omega
    rw [he, Nat.pow_succ]
    omega

/-- 全参数尾界，足以核查原文的入口增长条件。 -/
theorem sparse_entry_tail_bound (a : Nat) (ha : 5 ≤ a) :
    990 * a + 989 < 10 ^ (a - 1) := by
  have h := entry_tail_bound_shift (a - 5)
  have he : a - 5 + 5 = a := by omega
  have hp : a - 5 + 4 = a - 1 := by omega
  simpa only [he, hp] using h

/-- 目标整数夹在其最高位与原文增长估计之间。 -/
theorem sparse_entry_bounds (a : Nat) (ha : 5 ≤ a) :
    10 ^ a ≤ sparse a ∧ sparse a < 11 * 10 ^ (a - 1) := by
  have ht := sparse_entry_tail_bound a ha
  have hr := rho_le a
  have hp : 10 ^ a = 10 ^ (a - 1) * 10 := by
    simpa only [Nat.succ_eq_add_one, show a - 1 + 1 = a by omega]
      using Nat.pow_succ 10 (a - 1)
  unfold sparse
  omega

private theorem controls_decimalLength_between_powers (a n : Nat)
    (hlo : 10 ^ a ≤ n) (hhi : n < 10 ^ (a + 1)) :
    decimalLength n = a + 1 := by
  induction a generalizing n with
  | zero =>
    have hn : n ≠ 0 := by simpa using Nat.ne_of_gt hlo
    have hb : n < 10 := by simpa using hhi
    have hq : n / 10 = 0 := by omega
    rw [decimalLength]
    simp only [hn, ↓reduceDIte, hq, decimalLength_zero]
  | succ a ih =>
    have hp : 0 < 10 ^ (a + 1) := Nat.pow_pos (by decide)
    have hn : n ≠ 0 := by omega
    have hlow : 10 ^ a ≤ n / 10 := by
      rw [Nat.pow_succ] at hlo
      omega
    have hhigh : n / 10 < 10 ^ (a + 1) := by
      rw [Nat.pow_succ] at hhi
      omega
    have hw := ih (n / 10) hlow hhigh
    rw [decimalLength]
    simp only [hn, ↓reduceDIte, hw]

/-- 使用原有除十递归定义计算目标的真实十进制位宽。 -/
theorem sparse_decimalLength (a : Nat) (ha : 5 ≤ a) :
    decimalLength (sparse a) = a + 1 := by
  have hb := sparse_entry_bounds a ha
  have hp : 10 ^ a = 10 ^ (a - 1) * 10 := by
    simpa only [Nat.succ_eq_add_one, show a - 1 + 1 = a by omega]
      using Nat.pow_succ 10 (a - 1)
  apply controls_decimalLength_between_powers a (sparse a) hb.1
  rw [Nat.pow_succ]
  omega

/-- 稠密源的实际整数值对模 99 恒为零。 -/
theorem denseOutput_mod99 (k : Nat) :
    (11 * (10 ^ k - 1)) % 99 = 0 := by
  induction k with
  | zero => decide
  | succ k ih =>
    have hp : 0 < 10 ^ k := Nat.pow_pos (by decide)
    have he : 11 * (10 ^ (k + 1) - 1) =
        10 * (11 * (10 ^ k - 1)) + 99 := by
      rw [Nat.pow_succ]
      omega
    rw [he, Nat.add_mod, Nat.mul_mod, ih]

/-- 原文的奇偶校正量使每一个目标整数都被 99 整除。 -/
theorem sparse_mod99 (a : Nat) : sparse a % 99 = 0 := by
  by_cases he : a % 2 = 0
  · have ho : a % 2 ≠ 1 := by omega
    simp [sparse, rho, Nat.add_mod, Nat.mul_mod, AstraModular.ten_pow_mod99, he, ho]
  · have ho : a % 2 = 1 := by omega
    simp [sparse, rho, Nat.add_mod, Nat.mul_mod, AstraModular.ten_pow_mod99, he, ho]

theorem familySource_mod99 (R : Nat) : familySource R % 99 = 0 := by
  exact denseOutput_mod99 (familyIndex R)

theorem familySource_decimalLength (R : Nat) (hR : 2 ≤ R) :
    decimalLength (familySource R) = familyWidth R := by
  have hk := familyIndex_ge_four R hR
  exact denseOutput_decimalLength (familyIndex R) (by omega)

/-- R≥2 时，人工入口边确实严格增长并满足小于十一倍源的上界。 -/
theorem sparse_family_entry_growth (R : Nat) (hR : 2 ≤ R) :
    familySource R < sparse (familyWidth R) ∧
      sparse (familyWidth R) < 11 * familySource R := by
  have hk := familyIndex_ge_four R hR
  have ha := familyWidth_ge_six R hR
  have hb := sparse_entry_bounds (familyWidth R) (by omega)
  have hp : 100 ≤ 10 ^ familyIndex R := by
    have h := Nat.pow_le_pow_right (show 0 < 10 by decide)
      (show 2 ≤ familyIndex R by omega)
    simpa using h
  have hpow1 : 10 ^ (familyIndex R + 1) = 10 ^ familyIndex R * 10 :=
    Nat.pow_succ 10 (familyIndex R)
  have hpow2 : 10 ^ (familyIndex R + 2) = 10 ^ familyIndex R * 100 := by
    rw [show familyIndex R + 2 = (familyIndex R + 1) + 1 by omega,
      Nat.pow_succ, Nat.pow_succ]
    omega
  have hpred : familyWidth R - 1 = familyIndex R + 1 := by
    unfold familyWidth
    omega
  have hlo : 10 ^ (familyIndex R + 2) ≤ sparse (familyWidth R) := hb.1
  have hhi : sparse (familyWidth R) < 11 * 10 ^ (familyIndex R + 1) := by
    simpa only [hpred] using hb.2
  rw [hpow2] at hlo
  rw [hpow1] at hhi
  unfold familySource
  omega

/-- 人工入口恰好增加一位，位宽来自真实十进制定义。 -/
theorem sparse_family_entry_width (R : Nat) (hR : 2 ≤ R) :
    decimalLength (sparse (familyWidth R)) =
      decimalLength (familySource R) + 1 := by
  have ha := familyWidth_ge_six R hR
  rw [sparse_decimalLength _ (by omega), familySource_decimalLength R hR]

/-- 模、增长和位宽条件的联合证书；与导入的真实步障碍同时成立。 -/
theorem congruence_sparse_entry_controls (R : Nat) (hR : 2 ≤ R) :
    familySource R % 99 = 0 ∧ sparse (familyWidth R) % 99 = 0 ∧
      familySource R < sparse (familyWidth R) ∧
      sparse (familyWidth R) < 11 * familySource R ∧
      decimalLength (sparse (familyWidth R)) =
        decimalLength (familySource R) + 1 := by
  have hg := sparse_family_entry_growth R hR
  exact ⟨familySource_mod99 R, sparse_mod99 (familyWidth R),
    hg.1, hg.2, sparse_family_entry_width R hR⟩

end Agent106.CongruenceBudget
