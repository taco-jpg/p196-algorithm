import Agent105AffineBasics

/-!
# 实际仿射游程字的参数平移和反转

Agent #105 / lean_runtime，session 8f1107db019a。
沿用原 Agent102.RunSpec、Affine.eval、runsAt、wordAt 与原 Agent8 操作。
整数仿射长度仍由原定义 `.toNat` 截断；下面的平移恒等式对所有自然数
参数成立，不预设长度为正，也不把有限样本拟合当作表示证明。

本阶段提供实际参数平移、反转及有界表示保持；真实规范化和逐项相加的
无条件接口完成后再连接一步与固定步数轨道闭包。
-/

namespace Agent105.AffineDynamics

open Agent102

/-- 将仿射长度的参数替换为 `k + s`。 -/
def shiftAffine (f : Affine) (s : Nat) : Affine :=
  ⟨f.slope, f.slope * (s : Int) + f.intercept⟩

/-- 参数平移保持一个游程的字面符号。 -/
def shiftRun (r : RunSpec) (s : Nat) : RunSpec :=
  ⟨r.digit, shiftAffine r.length s⟩

/-- 对固定有限游程表逐项进行参数平移。 -/
def shiftSpecs (rs : List RunSpec) (s : Nat) : List RunSpec :=
  rs.map (fun r => shiftRun r s)

@[simp] theorem shiftAffine_eval (f : Affine) (s k : Nat) :
    (shiftAffine f s).eval k = f.eval (k + s) := by
  simp [shiftAffine, Affine.eval, Int.natCast_add, Int.mul_add, Int.add_assoc]

@[simp] theorem shiftRun_digit (r : RunSpec) (s : Nat) :
    (shiftRun r s).digit = r.digit := rfl

/-- 平移后的具体游程数值与原游程在平移参数处完全相同。 -/
theorem runsAt_shift (rs : List RunSpec) (s k : Nat) :
    runsAt (shiftSpecs rs s) k = runsAt rs (k + s) := by
  simp [runsAt, shiftSpecs, List.map_map, Function.comp_def, shiftRun]

/-- 实际展开字的精确参数平移，不仅是长度或符号表的相等。 -/
@[simp] theorem wordAt_shift (rs : List RunSpec) (s k : Nat) :
    wordAt (shiftSpecs rs s) k = wordAt rs (k + s) := by
  exact congrArg word (runsAt_shift rs s k)

theorem specBound_shift (rs : List RunSpec) (b s : Nat) (h : SpecBound rs b) :
    SpecBound (shiftSpecs rs s) b := by
  intro r hr
  obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hr
  exact h q hq

@[simp] theorem shiftSpecs_append (rs ss : List RunSpec) (s : Nat) :
    shiftSpecs (rs ++ ss) s = shiftSpecs rs s ++ shiftSpecs ss s := by
  simp [shiftSpecs]

@[simp] theorem shiftSpecs_reverse (rs : List RunSpec) (s : Nat) :
    shiftSpecs rs.reverse s = (shiftSpecs rs s).reverse := by
  simp [shiftSpecs]

/-- 反转真实字族保持同一字面符号界和尾部仿射表示。 -/
theorem hasAffineRuns_reverse (w : Nat → List Nat) (b : Nat)
    (hw : HasAffineRuns w b) : HasAffineRuns (fun k => (w k).reverse) b := by
  obtain ⟨rs, hb, K, hword⟩ := hw
  refine ⟨rs.reverse, specBound_reverse hb, K, ?_⟩
  intro k hk
  change (w k).reverse = wordAt rs.reverse k
  rw [hword k hk, wordAt_reverse]

/-- 平移真实字族的自然数参数保持有界尾部仿射表示。 -/
theorem hasAffineRuns_shift (w : Nat → List Nat) (b s : Nat)
    (hw : HasAffineRuns w b) : HasAffineRuns (fun k => w (k + s)) b := by
  obtain ⟨rs, hb, K, hword⟩ := hw
  refine ⟨shiftSpecs rs s, specBound_shift rs b s hb, K, ?_⟩
  intro k hk
  rw [wordAt_shift]
  exact hword (k + s) (by omega)

/-- 参数平移与字反转可组合，且不会改变符号界。 -/
theorem hasAffineRuns_shift_reverse (w : Nat → List Nat) (b s : Nat)
    (hw : HasAffineRuns w b) :
    HasAffineRuns (fun k => (w (k + s)).reverse) b := by
  exact hasAffineRuns_reverse (fun k => w (k + s)) b (hasAffineRuns_shift w b s hw)

end Agent105.AffineDynamics

#print axioms Agent105.AffineDynamics.shiftAffine_eval
#print axioms Agent105.AffineDynamics.shiftRun_digit
#print axioms Agent105.AffineDynamics.runsAt_shift
#print axioms Agent105.AffineDynamics.wordAt_shift
#print axioms Agent105.AffineDynamics.specBound_shift
#print axioms Agent105.AffineDynamics.shiftSpecs_append
#print axioms Agent105.AffineDynamics.shiftSpecs_reverse
#print axioms Agent105.AffineDynamics.hasAffineRuns_reverse
#print axioms Agent105.AffineDynamics.hasAffineRuns_shift
#print axioms Agent105.AffineDynamics.hasAffineRuns_shift_reverse
