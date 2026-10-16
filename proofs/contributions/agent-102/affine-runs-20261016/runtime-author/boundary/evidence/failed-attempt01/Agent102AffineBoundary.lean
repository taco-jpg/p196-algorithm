import Agent102RunWord
import Agent102AffineArithmetic

/-!
Agent #102：仿射段词的显式边界见证。
这些证明不使用待完成的整体尾部稳定定理；只展开字面段词。
-/

namespace Agent102.AffineBoundary

def movingLength : Affine := ⟨1, 0⟩

def fixedLength (N : Nat) : Affine := ⟨0, (N : Int)⟩

def moving : List RunSpec := [⟨1, movingLength⟩]

def fixed (N : Nat) : List RunSpec := [⟨1, fixedLength N⟩]

@[simp] theorem wordAt_moving (k : Nat) :
    wordAt moving k = List.replicate k 1 := by
  simp [wordAt, runsAt, word, moving, movingLength, Affine.eval]

@[simp] theorem wordAt_fixed (N k : Nat) :
    wordAt (fixed N) k = List.replicate N 1 := by
  simp [wordAt, runsAt, word, fixed, fixedLength, Affine.eval]

/-- 包括 k=0 和 N=0；相等恰好发生一次。 -/
theorem moving_fixed_eq_iff (k N : Nat) :
    wordAt moving k = wordAt (fixed N) k ↔ k = N := by
  rw [wordAt_moving, wordAt_fixed]
  constructor
  · intro h
    have hl := congrArg List.length h
    simpa only [List.length_replicate] using hl
  · intro h
    subst k
    rfl

/-- 此例中，通用标量比较界正好等于固定长度截距再加一。 -/
theorem compareCutoff_moving_fixed (N : Nat) :
    Affine.compareCutoff movingLength (fixedLength N) = N + 1 := by
  simp [Affine.compareCutoff, movingLength, fixedLength]

/-- 对这一对模板，尾部判定恒定的精确必要充分条件为 K>N。 -/
theorem moving_fixed_stable_iff (N K : Nat) :
    (∀ k : Nat, K ≤ k →
      (wordAt moving k = wordAt (fixed N) k ↔
        wordAt moving K = wordAt (fixed N) K)) ↔ N < K := by
  simp only [moving_fixed_eq_iff]
  constructor
  · intro h
    by_cases hlt : N < K
    · exact hlt
    · have hKN : K ≤ N := by omega
      have he : K = N := (h N hKN).mp rfl
      have hn : N + 1 = N := (h (N + 1) (by omega)).mpr he
      omega
  · intro h k hk
    constructor <;> intro he <;> omega

/-- 任意预先指定的界之后，都有相等真假在相邻参数处变化的模板对。 -/
theorem equality_changes_arbitrarily_late :
    ∀ K : Nat, ∃ A B : List RunSpec, ∃ k : Nat,
      K ≤ k ∧ wordAt A k = wordAt B k ∧
        wordAt A (k + 1) ≠ wordAt B (k + 1) := by
  intro K
  refine ⟨moving, fixed K, K, Nat.le_refl K,
    (moving_fixed_eq_iff K K).mpr rfl, ?_⟩
  intro h
  have he := (moving_fixed_eq_iff (K + 1) K).mp h
  omega

/-- 截距依赖不可被删去：没有同时适用于全部模板对的常数界。 -/
theorem no_uniform_wordAt_cutoff :
    ¬ ∃ K : Nat, ∀ A B : List RunSpec, ∀ k : Nat, K ≤ k →
      (wordAt A k = wordAt B k ↔ wordAt A K = wordAt B K) := by
  rintro ⟨K, hK⟩
  obtain ⟨A, B, k, hk, he, hn⟩ := equality_changes_arbitrarily_late K
  have heK : wordAt A K = wordAt B K := (hK A B k hk).mp he
  exact hn ((hK A B (k + 1) (by omega)).mpr heK)

def splitRuns : List Run := [⟨1, 1⟩, ⟨1, 1⟩]

def shortRuns : List Run := [⟨1, 1⟩]

def longRuns : List Run := [⟨1, 2⟩]

/-- 两个非空正长度段与一个段的结构不同，但展开词完全相同。 -/
theorem run_structure_counterexample :
    splitRuns ≠ longRuns ∧ word splitRuns = word longRuns := by
  decide

/-- 所有实际交叠段的数字一致，且确有交叠，仍不能替代总宽度条件。 -/
theorem overlap_digits_without_width :
    (∀ s ∈ spans shortRuns, ∀ t ∈ spans longRuns,
      s.overlaps t → s.digit = t.digit) ∧
    (∃ s ∈ spans shortRuns, ∃ t ∈ spans longRuns, s.overlaps t) ∧
    (word shortRuns).length ≠ (word longRuns).length ∧
    word shortRuns ≠ word longRuns := by
  constructor
  · simp [spans, spansFrom, shortRuns, longRuns]
  · refine ⟨?_, ?_⟩
    · exact ⟨⟨1, 0, 1⟩, by decide, ⟨1, 0, 2⟩, by decide, by decide⟩
    · decide

def emptySpan : Span := ⟨7, 1, 1⟩

def coveringSpan : Span := ⟨9, 0, 2⟩

def withZeroRuns : List Run := [⟨9, 1⟩, ⟨7, 0⟩, ⟨9, 1⟩]

def withoutZeroRuns : List Run := [⟨9, 2⟩]

/-- [1,1) 为零长度段；两条交叉严格不等式都真，但实际交叠为假。 -/
theorem zero_span_cross_inequalities :
    emptySpan.lo = emptySpan.hi ∧
    emptySpan.lo < coveringSpan.hi ∧ coveringSpan.lo < emptySpan.hi ∧
    ¬ emptySpan.overlaps coveringSpan ∧ emptySpan.digit ≠ coveringSpan.digit := by
  decide

/-- 上述零段确实出现在真实段表中，插入它不改变字面展开词。 -/
theorem zero_span_realized :
    emptySpan ∈ spans withZeroRuns ∧ coveringSpan ∈ spans withoutZeroRuns ∧
    word withZeroRuns = word withoutZeroRuns := by
  decide

/-- 仅用交叉不等式代替正长度交叠，会错误地拒绝这一对相同词。 -/
theorem cross_inequalities_false_negative :
    word withZeroRuns = word withoutZeroRuns ∧
    ¬ (∀ s ∈ spans withZeroRuns, ∀ t ∈ spans withoutZeroRuns,
      s.lo < t.hi → t.lo < s.hi → s.digit = t.digit) := by
  refine ⟨zero_span_realized.2.2, ?_⟩
  intro h
  have he := h emptySpan zero_span_realized.1 coveringSpan zero_span_realized.2.1
    zero_span_cross_inequalities.2.1 zero_span_cross_inequalities.2.2.1
  exact zero_span_cross_inequalities.2.2.2.2 he

#print axioms wordAt_moving
#print axioms wordAt_fixed
#print axioms moving_fixed_eq_iff
#print axioms compareCutoff_moving_fixed
#print axioms moving_fixed_stable_iff
#print axioms equality_changes_arbitrarily_late
#print axioms no_uniform_wordAt_cutoff
#print axioms run_structure_counterexample
#print axioms overlap_digits_without_width
#print axioms zero_span_cross_inequalities
#print axioms zero_span_realized
#print axioms cross_inequalities_false_negative

end Agent102.AffineBoundary
