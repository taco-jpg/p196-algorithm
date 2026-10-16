import Agent105AffineBasics
import Agent105AffineNormalize
import Agent105AffineZip

/-!
# 实际仿射游程字的平移、反转与固定步数轨道闭包

Agent #105 / lean_runtime，session 8f1107db019a。
沿用原 Agent102.RunSpec、Affine.eval、runsAt、wordAt 与原 Agent8 操作。
整数仿射长度仍由原定义 `.toNat` 截断；下面的平移恒等式对所有自然数
参数成立，不预设长度为正，也不把有限样本拟合当作表示证明。

规范化采用 Agent105.AffineNormalize.hasAffineRuns_normalize 的已证明
无条件接口；逐项相加采用 zipAdd_wordAt_eventually 的已证明无条件接口。
由此直接证明原 Agent8.pair、stepWord 与每个固定 t 的 orbit 闭包。
这里没有把规范化或逐项相加闭包设作额外假设。表示阈值可依赖固定 t，
不声称存在对所有轨道时间同时通用的参数阈值。
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

/-- 对两个实际尾部字族使用已证明的逐项相加闭包。
不要求输入长度相等；与原 zipAdd 的截断语义一致。 -/
theorem hasAffineRuns_zipAdd (w v : Nat → List Nat) (M N : Nat)
    (hw : HasAffineRuns w M) (hv : HasAffineRuns v N) :
    HasAffineRuns (fun k => Agent8.zipAdd (w k) (v k)) (M + N) := by
  obtain ⟨rs, hrs, K₁, hword⟩ := hw
  obtain ⟨ss, hss, K₂, hother⟩ := hv
  obtain ⟨ts, hts, K₃, hzip⟩ := zipAdd_wordAt_eventually rs ss M N hrs hss
  refine ⟨ts, hts, max K₁ (max K₂ K₃), ?_⟩
  intro k hk
  have hk₁ : K₁ ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
  have hk₂ : K₂ ≤ k := Nat.le_trans
    (Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)) hk
  have hk₃ : K₃ ≤ k := Nat.le_trans
    (Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)) hk
  change Agent8.zipAdd (w k) (v k) = wordAt ts k
  rw [hword k hk₁, hother k hk₂]
  exact hzip k hk₃

/-- 真实十进制数字字与其反转配对后，得到符号不超过 18 的仿射游程字。 -/
theorem hasAffineRuns_pair (w : Nat → List Nat) (hw : HasAffineRuns w 9) :
    HasAffineRuns (fun k => Agent8.pair (w k)) 18 := by
  exact hasAffineRuns_zipAdd w (fun k => (w k).reverse) 9 9 hw
    (hasAffineRuns_reverse w 9 hw)

/-- 原 Agent8.stepWord 的实际一步闭包，包含真实终端进位及变化后的宽度。 -/
theorem hasAffineRuns_stepWord (w : Nat → List Nat) (hw : HasAffineRuns w 18) :
    HasAffineRuns (fun k => Agent8.stepWord (w k)) 18 := by
  exact hasAffineRuns_pair (fun k => Agent8.normalize (w k) 0)
    (Agent105.AffineNormalize.hasAffineRuns_normalize w hw 0 (by decide))

/-- 每个固定的真实迭代步数都有尾部仿射游程表示。 -/
theorem hasAffineRuns_orbit (w : Nat → List Nat) (hw : HasAffineRuns w 18)
    (t : Nat) : HasAffineRuns (fun k => Agent8.orbit (w k) t) 18 := by
  induction t with
  | zero => exact hw
  | succ t ih =>
      exact hasAffineRuns_stepWord (fun k => Agent8.orbit (w k) t) ih

/-- 固定轨道时间处的实际规范化输出也有数字界为 9 的尾部表示。 -/
theorem hasAffineRuns_normalized_orbit (w : Nat → List Nat)
    (hw : HasAffineRuns w 18) (t e : Nat) (he : e ≤ 1) :
    HasAffineRuns (fun k => Agent8.normalize (Agent8.orbit (w k) t) e) 9 := by
  exact Agent105.AffineNormalize.hasAffineRuns_normalize
    (fun k => Agent8.orbit (w k) t) (hasAffineRuns_orbit w hw t) e he

/-- 固定游程表的一步实际输出；没有额外的标量或闭包前提。 -/
theorem stepWord_wordAt_eventually (rs : List RunSpec) (hrs : SpecBound rs 18) :
    ∃ ts : List RunSpec, SpecBound ts 18 ∧
      ∃ K : Nat, ∀ k, K ≤ k → Agent8.stepWord (wordAt rs k) = wordAt ts k := by
  exact hasAffineRuns_stepWord (wordAt rs) (hasAffineRuns_wordAt rs 18 hrs)

/-- 对每个给定 t，原实际列表轨道本身最终等于一个固定仿射游程展开字。 -/
theorem orbit_wordAt_eventually (rs : List RunSpec) (hrs : SpecBound rs 18)
    (t : Nat) :
    ∃ ts : List RunSpec, SpecBound ts 18 ∧
      ∃ K : Nat, ∀ k, K ≤ k → Agent8.orbit (wordAt rs k) t = wordAt ts k := by
  exact hasAffineRuns_orbit (wordAt rs) (hasAffineRuns_wordAt rs 18 hrs) t

/-- 固定迭代后的真实规范化数字字，供后续回文等式稳定性使用。 -/
theorem normalized_orbit_wordAt_eventually (rs : List RunSpec)
    (hrs : SpecBound rs 18) (t e : Nat) (he : e ≤ 1) :
    ∃ ts : List RunSpec, SpecBound ts 9 ∧
      ∃ K : Nat, ∀ k, K ≤ k →
        Agent8.normalize (Agent8.orbit (wordAt rs k) t) e = wordAt ts k := by
  exact hasAffineRuns_normalized_orbit (wordAt rs) (hasAffineRuns_wordAt rs 18 hrs) t e he

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
#print axioms Agent105.AffineDynamics.hasAffineRuns_zipAdd
#print axioms Agent105.AffineDynamics.hasAffineRuns_pair
#print axioms Agent105.AffineDynamics.hasAffineRuns_stepWord
#print axioms Agent105.AffineDynamics.hasAffineRuns_orbit
#print axioms Agent105.AffineDynamics.hasAffineRuns_normalized_orbit
#print axioms Agent105.AffineDynamics.stepWord_wordAt_eventually
#print axioms Agent105.AffineDynamics.orbit_wordAt_eventually
#print axioms Agent105.AffineDynamics.normalized_orbit_wordAt_eventually
