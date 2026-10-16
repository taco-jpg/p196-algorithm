import ActualWordBridge

/-!
# 实际列表返回的时间与位宽界

Agent #105：补充 VARIABLE_RETURN_THEOREMS.md §1 的统一时间界。
这里只使用原 Agent8 列表动力学；没有定义替代的进位、迭代或势函数。
所有返回等式、首项相等、位宽关系与正时间前提都显式列出。

精确源依赖（SOURCE_MAP.json 中的原模块名）：
* PeriodObstructions.lean，SHA-256
  83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a
* ActualWordBridge.lean，SHA-256
  3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6

CanonicalPair 是原 Agent8 的列表条件。它不单独保证整数可实现性；
用于实际正整数时，应另接原 Agent109.Endpoints.pairWord_canonical
与 Agent109.Compat.pairWord_orbit。这里不声称任何返回实例存在，
也不声称返回段避开回文。
-/

namespace Agent105.ReturnTimeBound

/-- 保留两端势函数的实际迭代不等式。 -/
theorem orbit_width_potential_bound (w : Agent8.Word) (t : Nat)
    (hw : Agent8.CanonicalPair w) :
    (t : Int) + Agent8.lowerPotential ((Agent8.orbit w t).headD 0) +
        4 * (w.length : Int) ≤
      Agent8.lowerPotential (w.headD 0) + 4 * ((Agent8.orbit w t).length : Int) := by
  have hp := (Agent8.path_potential_bounds (Agent8.actualExterior w)
    (Agent8.actualInput w) t
    (fun i _ => Agent8.actual_path_valid w hw i)
    (fun i _ => Agent8.actual_path_evolves w hw i)).2
  change (t : Int) ≤ 4 * Agent8.actualOverflows w t +
    Agent8.lowerPotential (w.headD 0) -
      Agent8.lowerPotential ((Agent8.orbit w t).headD 0) at hp
  have hwidth := Agent8.actual_width w hw t
  omega

/-- 返回等式可直接代入的两端势函数形式。 -/
theorem return_width_potential_bound (w v : Agent8.Word) (t : Nat)
    (hw : Agent8.CanonicalPair w) (hreturn : Agent8.orbit w t = v) :
    (t : Int) + Agent8.lowerPotential (v.headD 0) + 4 * (w.length : Int) ≤
      Agent8.lowerPotential (w.headD 0) + 4 * (v.length : Int) := by
  simpa only [hreturn] using orbit_width_potential_bound w t hw

/-- 首项相等时两端势相消，真实宽度增量同时给出两侧时间界。 -/
theorem return_time_bounds_of_width_gain (w v : Agent8.Word) (t gain : Nat)
    (hw : Agent8.CanonicalPair w) (hreturn : Agent8.orbit w t = v)
    (hhead : v.headD 0 = w.headD 0) (hwidth : v.length = w.length + gain) :
    2 * gain ≤ t ∧ t ≤ 4 * gain := by
  have hclosed : Agent8.actualExterior w t = Agent8.actualExterior w 0 := by
    change (Agent8.orbit w t).headD 0 = w.headD 0
    rw [hreturn]
    exact hhead
  have hb := Agent8.actual_return_bounds w hw t hclosed
  have hl := Agent8.actual_width w hw t
  rw [hreturn, hwidth] at hl
  omega

/-- 正时间前提显式保留；没有从返回等式自动推断正时间。 -/
theorem positive_return_time_bound_of_width_gain (w v : Agent8.Word) (t gain : Nat)
    (hw : Agent8.CanonicalPair w) (hreturn : Agent8.orbit w t = v)
    (hhead : v.headD 0 = w.headD 0) (hwidth : v.length = w.length + gain)
    (ht : 0 < t) : 1 ≤ t ∧ t ≤ 4 * gain := by
  have hb := return_time_bounds_of_width_gain w v t gain hw hreturn hhead hwidth
  omega

/-- 一般端点长度上界允许不同截距，并保留未相消的首项势。 -/
theorem return_time_bound_with_offset (w v : Agent8.Word)
    (t gain sourceOffset targetOffset : Nat)
    (hw : Agent8.CanonicalPair w) (hreturn : Agent8.orbit w t = v)
    (hwidth : v.length + sourceOffset ≤ w.length + gain + targetOffset) :
    (t : Int) + 4 * (sourceOffset : Int) + Agent8.lowerPotential (v.headD 0) ≤
      4 * (gain : Int) + 4 * (targetOffset : Int) +
        Agent8.lowerPotential (w.headD 0) := by
  have hp := return_width_potential_bound w v t hw hreturn
  omega

/-- 同首项端点的自然数截距形式，不使用截断减法表示宽度差。 -/
theorem same_head_return_time_bound_with_offset (w v : Agent8.Word)
    (t gain sourceOffset targetOffset : Nat)
    (hw : Agent8.CanonicalPair w) (hreturn : Agent8.orbit w t = v)
    (hhead : v.headD 0 = w.headD 0)
    (hwidth : v.length + sourceOffset ≤ w.length + gain + targetOffset) :
    t + 4 * sourceOffset ≤ 4 * gain + 4 * targetOffset := by
  have hp := return_time_bound_with_offset w v t gain sourceOffset targetOffset
    hw hreturn hwidth
  rw [hhead] at hp
  omega

/-- 参数化字族的正返回时间界；正斜率与正平移作为应用前提保留。 -/
theorem word_family_return_time_bound (Q : Nat → Agent8.Word) (k s A t : Nat)
    (hA : 0 < A) (hs : 0 < s) (ht : 0 < t)
    (hcanonical : Agent8.CanonicalPair (Q k))
    (hreturn : Agent8.orbit (Q k) t = Q (k + s))
    (hhead : (Q (k + s)).headD 0 = (Q k).headD 0)
    (hwidth : (Q (k + s)).length = (Q k).length + A * s) :
    0 < 4 * A * s ∧ 1 ≤ t ∧ t ≤ 4 * A * s := by
  have hgain : 0 < A * s := Nat.mul_pos hA hs
  have hb := positive_return_time_bound_of_width_gain (Q k) (Q (k + s)) t
    (A * s) hcanonical hreturn hhead hwidth ht
  rw [Nat.mul_assoc]
  omega

/-- 只要求两个返回端点的仿射长度公式，无需假定其他参数处的公式。 -/
theorem affine_endpoint_return_time_bound (Q : Nat → Agent8.Word)
    (k s A B t : Nat) (hA : 0 < A) (hs : 0 < s) (ht : 0 < t)
    (hcanonical : Agent8.CanonicalPair (Q k))
    (hreturn : Agent8.orbit (Q k) t = Q (k + s))
    (hhead : (Q (k + s)).headD 0 = (Q k).headD 0)
    (hsource : (Q k).length = A * k + B)
    (htarget : (Q (k + s)).length = A * (k + s) + B) :
    0 < 4 * A * s ∧ 1 ≤ t ∧ t ≤ 4 * A * s := by
  have hwidth : (Q (k + s)).length = (Q k).length + A * s := by
    rw [hsource, htarget, Nat.mul_add]
    omega
  exact word_family_return_time_bound Q k s A t hA hs ht
    hcanonical hreturn hhead hwidth

/-- 两个端点的截距可不同；结论显式保留截距代价及正时间。 -/
theorem affine_endpoint_return_time_bound_with_offset (Q : Nat → Agent8.Word)
    (k s A sourceOffset targetOffset t : Nat)
    (hA : 0 < A) (hs : 0 < s) (ht : 0 < t)
    (hcanonical : Agent8.CanonicalPair (Q k))
    (hreturn : Agent8.orbit (Q k) t = Q (k + s))
    (hhead : (Q (k + s)).headD 0 = (Q k).headD 0)
    (hsource : (Q k).length = A * k + sourceOffset)
    (htarget : (Q (k + s)).length = A * (k + s) + targetOffset) :
    0 < 4 * A * s ∧ 1 ≤ t ∧
      t + 4 * sourceOffset ≤ 4 * A * s + 4 * targetOffset := by
  have hgain : 0 < A * s := Nat.mul_pos hA hs
  have hwidth : (Q (k + s)).length + sourceOffset ≤
      (Q k).length + A * s + targetOffset := by
    rw [hsource, htarget, Nat.mul_add]
    omega
  have hb := same_head_return_time_bound_with_offset (Q k) (Q (k + s)) t
    (A * s) sourceOffset targetOffset hcanonical hreturn hhead hwidth
  rw [Nat.mul_assoc]
  omega

end Agent105.ReturnTimeBound

#print axioms Agent105.ReturnTimeBound.orbit_width_potential_bound
#print axioms Agent105.ReturnTimeBound.return_width_potential_bound
#print axioms Agent105.ReturnTimeBound.return_time_bounds_of_width_gain
#print axioms Agent105.ReturnTimeBound.positive_return_time_bound_of_width_gain
#print axioms Agent105.ReturnTimeBound.return_time_bound_with_offset
#print axioms Agent105.ReturnTimeBound.same_head_return_time_bound_with_offset
#print axioms Agent105.ReturnTimeBound.word_family_return_time_bound
#print axioms Agent105.ReturnTimeBound.affine_endpoint_return_time_bound
#print axioms Agent105.ReturnTimeBound.affine_endpoint_return_time_bound_with_offset
