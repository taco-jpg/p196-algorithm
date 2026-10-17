import P196.Agent102AffineParameterIntervals.Agent102ParameterIntervalDefs

/-!
Agent #102：所有自然参数上的精确整数仿射不等式区间。
端点仅使用整数四则运算和正除数的 Euclidean 除法，不枚举区间中的点。
-/

namespace Agent102.ParameterSets

/-- 严格不等式的完整参数集合，以一个左闭右开区间表示。 -/
def ltInterval (f g : Affine) : Interval :=
  let a := f.slope - g.slope
  let b := g.intercept - f.intercept
  if 0 < a then
    ⟨0, some (((b - 1) / a + 1).toNat)⟩
  else if a < 0 then
    ⟨((-b / -a + 1).toNat), none⟩
  else if 0 < b then Interval.univ else Interval.empty

theorem contains_ltInterval (f g : Affine) (k : Nat) :
    (ltInterval f g).Contains k ↔ f.eval k < g.eval k := by
  let a := f.slope - g.slope
  let b := g.intercept - f.intercept
  have hreduce : f.eval k < g.eval k ↔ a * (k : Int) < b := by
    dsimp [a, b, Affine.eval]
    rw [Int.sub_mul]
    omega
  change (if 0 < a then
      (⟨0, some (((b - 1) / a + 1).toNat)⟩ : Interval)
    else if a < 0 then
      (⟨((-b / -a + 1).toNat), none⟩ : Interval)
    else if 0 < b then Interval.univ else Interval.empty).Contains k ↔ _
  rw [hreduce]
  by_cases hp : 0 < a
  · simp only [if_pos hp, Interval.Contains]
    have hdiv := Int.le_ediv_iff_mul_le (a := (k : Int)) (b := b - 1) (c := a) hp
    rw [Int.mul_comm] at hdiv
    omega
  · by_cases hn : a < 0
    · simp only [if_neg hp, if_pos hn, Interval.Contains]
      have hm : 0 < -a := by omega
      have hdiv := Int.ediv_lt_iff_lt_mul (a := -b) (b := (k : Int)) (c := -a) hm
      rw [Int.mul_comm, Int.neg_mul, Int.neg_lt_neg_iff] at hdiv
      simpa only [and_true, Int.toNat_le, Int.add_one_le_iff] using hdiv
    · have ha : a = 0 := by omega
      by_cases hb : 0 < b
      · simp [hp, hn, hb, ha, Interval.univ, Interval.Contains]
      · simp [hp, hn, hb, ha, Interval.empty, Interval.Contains]

/-- 整数非严格比较等价于把右侧截距增加一后的严格比较。 -/
def leInterval (f g : Affine) : Interval :=
  ltInterval f ⟨g.slope, g.intercept + 1⟩

theorem contains_leInterval (f g : Affine) (k : Nat) :
    (leInterval f g).Contains k ↔ f.eval k ≤ g.eval k := by
  rw [leInterval, contains_ltInterval]
  simp only [Affine.eval]
  omega

#print axioms ltInterval
#print axioms contains_ltInterval
#print axioms leInterval
#print axioms contains_leInterval

end Agent102.ParameterSets
