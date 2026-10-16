import Agent102AffineAllParameters
import Agent102AffineBoundary

/-!
Agent #102 的作者控制证书：区分有限前缀与稳定尾部，并保留字面词语义。
闭布尔命题由 `decide` 产生证明项；全称与存在结论另经规格定理取得。
巨大系数仅送入任意单参数的压缩检查器，不枚举巨大 cutoff 的前缀。
-/

namespace Agent102.AllParameterControls

/-- 一个或更多前置的 1 与末尾的 2 不构成回文。 -/
theorem replicate_one_two_palindrome_iff (n : Nat) :
    List.replicate n 1 ++ [2] = (List.replicate n 1 ++ [2]).reverse ↔ n = 0 := by
  cases n with
  | zero => decide
  | succ n => simp [List.replicate_succ, List.reverse_append]

theorem moving_fixed3_only_eq (k : Nat) :
    wordAt AffineBoundary.moving k = wordAt (AffineBoundary.fixed 3) k ↔ k = 3 :=
  AffineBoundary.moving_fixed_eq_iff k 3

theorem moving_fixed3_controls :
    allEqual AffineBoundary.moving (AffineBoundary.fixed 3) = false ∧
    someEqual AffineBoundary.moving (AffineBoundary.fixed 3) = true ∧
    allUnequal AffineBoundary.moving (AffineBoundary.fixed 3) = false ∧
    someUnequal AffineBoundary.moving (AffineBoundary.fixed 3) = true := by
  decide

theorem moving_fixed3_semantics :
    (∃ k : Nat, wordAt AffineBoundary.moving k = wordAt (AffineBoundary.fixed 3) k) ∧
    (∃ k : Nat, wordAt AffineBoundary.moving k ≠ wordAt (AffineBoundary.fixed 3) k) :=
  ⟨(someEqual_spec _ _).mp moving_fixed3_controls.2.1,
    (someUnequal_spec _ _).mp moving_fixed3_controls.2.2.2⟩

/-- 尾部从不相等，唯一的相等参数位于被枚举的有限前缀。 -/
theorem moving_fixed3_prefix_witness :
    3 < equalityCutoff AffineBoundary.moving (AffineBoundary.fixed 3) ∧
    equalAt AffineBoundary.moving (AffineBoundary.fixed 3) 3 = true ∧
    fastEqualOnTail AffineBoundary.moving (AffineBoundary.fixed 3) = false := by
  decide

def growing : List RunSpec := [⟨1, ⟨1, 0⟩⟩, ⟨2, ⟨0, 1⟩⟩]

theorem growing_word (k : Nat) :
    wordAt growing k = List.replicate k 1 ++ [2] := by
  simp [growing, wordAt, runsAt, word, Affine.eval]

theorem growing_palindrome_iff (k : Nat) :
    wordAt growing k = (wordAt growing k).reverse ↔ k = 0 := by
  rw [growing_word]
  exact replicate_one_two_palindrome_iff k

theorem growing_controls :
    allPalindromic growing = false ∧ somePalindromic growing = true ∧
    allNonpalindromic growing = false ∧ someNonpalindromic growing = true := by
  decide

theorem growing_semantics :
    (∃ k : Nat, wordAt growing k = (wordAt growing k).reverse) ∧
    (∃ k : Nat, wordAt growing k ≠ (wordAt growing k).reverse) :=
  ⟨(somePalindromic_spec _).mp growing_controls.2.1,
    (someNonpalindromic_spec _).mp growing_controls.2.2.2⟩

theorem growing_prefix_witness :
    fastPalindromicOnTail growing = false ∧ somePalindromic growing = true ∧
    equalAt growing growing.reverse 0 = true := by
  decide

def declining : List RunSpec := [⟨1, ⟨-1, 3⟩⟩, ⟨2, ⟨0, 1⟩⟩]

theorem declining_word (k : Nat) :
    wordAt declining k = List.replicate ((-(k : Int) + 3).toNat) 1 ++ [2] := by
  simp [declining, wordAt, runsAt, word, Affine.eval]

/-- 负斜率在 k=3 起裁成零长度，之前的三个参数均不回文。 -/
theorem declining_palindrome_iff (k : Nat) :
    wordAt declining k = (wordAt declining k).reverse ↔ 3 ≤ k := by
  rw [declining_word, replicate_one_two_palindrome_iff]
  omega

theorem declining_controls :
    allPalindromic declining = false ∧ somePalindromic declining = true ∧
    allNonpalindromic declining = false ∧ someNonpalindromic declining = true := by
  decide

theorem declining_semantics :
    (∃ k : Nat, wordAt declining k = (wordAt declining k).reverse) ∧
    (∃ k : Nat, wordAt declining k ≠ (wordAt declining k).reverse) :=
  ⟨(somePalindromic_spec _).mp declining_controls.2.1,
    (someNonpalindromic_spec _).mp declining_controls.2.2.2⟩

/-- 尾部全部回文不能代替全部自然参数均回文。 -/
theorem declining_prefix_obstruction :
    fastPalindromicOnTail declining = true ∧ allPalindromic declining = false ∧
    equalAt declining declining.reverse 0 = false := by
  decide

def alwaysDifferent : List RunSpec := [⟨1, ⟨1, 1⟩⟩, ⟨2, ⟨1, 1⟩⟩]

theorem alwaysDifferent_controls :
    allPalindromic alwaysDifferent = false ∧ somePalindromic alwaysDifferent = false ∧
    allNonpalindromic alwaysDifferent = true ∧ someNonpalindromic alwaysDifferent = true := by
  decide

theorem alwaysDifferent_semantics :
    ∀ k : Nat, wordAt alwaysDifferent k ≠ (wordAt alwaysDifferent k).reverse :=
  (allNonpalindromic_spec _).mp alwaysDifferent_controls.2.2.1

def symmetric : List RunSpec := [⟨1, ⟨1, 0⟩⟩, ⟨2, ⟨0, 1⟩⟩, ⟨1, ⟨1, 0⟩⟩]

theorem symmetric_controls :
    allPalindromic symmetric = true ∧ somePalindromic symmetric = true ∧
    allNonpalindromic symmetric = false ∧ someNonpalindromic symmetric = false := by
  decide

theorem symmetric_semantics :
    ∀ k : Nat, wordAt symmetric k = (wordAt symmetric k).reverse :=
  (allPalindromic_spec _).mp symmetric_controls.1

/-- 一个显式零段和一个始终裁成零的非正长度段。 -/
def erased : List RunSpec := [⟨7, ⟨0, 0⟩⟩, ⟨8, ⟨-1, 0⟩⟩]

theorem empty_zero_controls :
    allEqual erased [] = true ∧ allPalindromic erased = true ∧
    allPalindromic [] = true ∧ someNonpalindromic [] = false := by
  decide

theorem zero_runs_semantics : ∀ k : Nat, wordAt erased k = [] := by
  intro k
  simpa only [wordAt_nil] using (allEqual_spec _ _).mp empty_zero_controls.1 k

theorem empty_palindrome : ∀ k : Nat, wordAt [] k = (wordAt [] k).reverse :=
  (allPalindromic_spec _).mp empty_zero_controls.2.2.1

def leadingZero : List RunSpec := [⟨0, ⟨0, 1⟩⟩, ⟨1, ⟨0, 1⟩⟩]

theorem leading_zero_word (k : Nat) : wordAt leadingZero k = [0, 1] := by
  simp [leadingZero, wordAt, runsAt, word, Affine.eval]

/-- 字面词 [0,1] 保留前导零，既不等于 [1]，也不回文。 -/
theorem leading_zero_controls :
    allUnequal leadingZero (AffineBoundary.fixed 1) = true ∧
    allNonpalindromic leadingZero = true := by
  decide

theorem leading_zero_unequal :
    ∀ k : Nat, wordAt leadingZero k ≠ wordAt (AffineBoundary.fixed 1) k :=
  (allUnequal_spec _ _).mp leading_zero_controls.1

theorem leading_zero_nonpalindrome :
    ∀ k : Nat, wordAt leadingZero k ≠ (wordAt leadingZero k).reverse :=
  (allNonpalindromic_spec _).mp leading_zero_controls.2

/-- 10^100，直接写成字面量；以下定义不送入全参数前缀扫描。 -/
def huge : Nat :=
  10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def hugeOne : List RunSpec := [⟨1, ⟨(huge : Int), (huge : Int)⟩⟩]

def hugeSplit : List RunSpec :=
  [⟨1, ⟨(huge : Int), (huge : Int)⟩⟩, ⟨7, ⟨0, 0⟩⟩,
    ⟨1, ⟨(huge : Int), (huge : Int)⟩⟩]

def hugeMerged : List RunSpec := [⟨1, ⟨2 * (huge : Int), 2 * (huge : Int)⟩⟩]

def hugeWidthChanged : List RunSpec := [⟨1, ⟨(huge : Int), (huge : Int) + 1⟩⟩]

def hugeNegative : List RunSpec :=
  [⟨5, ⟨-(huge : Int), (huge : Int)⟩⟩, ⟨1, ⟨(huge : Int), (huge : Int)⟩⟩]

theorem huge_split_at : equalAt hugeSplit hugeMerged huge = true := by decide

theorem huge_split_semantics : wordAt hugeSplit huge = wordAt hugeMerged huge :=
  (equalAt_eq_true_iff _ _ _).mp huge_split_at

theorem huge_width_at : equalAt hugeOne hugeWidthChanged huge = false := by decide

theorem huge_width_semantics : wordAt hugeOne huge ≠ wordAt hugeWidthChanged huge :=
  (equalAt_eq_false_iff _ _ _).mp huge_width_at

theorem huge_negative_at : equalAt hugeNegative hugeOne huge = true := by decide

theorem huge_negative_semantics : wordAt hugeNegative huge = wordAt hugeOne huge :=
  (equalAt_eq_true_iff _ _ _).mp huge_negative_at

#print axioms replicate_one_two_palindrome_iff
#print axioms moving_fixed3_only_eq
#print axioms moving_fixed3_controls
#print axioms moving_fixed3_semantics
#print axioms moving_fixed3_prefix_witness
#print axioms growing_word
#print axioms growing_palindrome_iff
#print axioms growing_controls
#print axioms growing_semantics
#print axioms growing_prefix_witness
#print axioms declining_word
#print axioms declining_palindrome_iff
#print axioms declining_controls
#print axioms declining_semantics
#print axioms declining_prefix_obstruction
#print axioms alwaysDifferent_controls
#print axioms alwaysDifferent_semantics
#print axioms symmetric_controls
#print axioms symmetric_semantics
#print axioms empty_zero_controls
#print axioms zero_runs_semantics
#print axioms empty_palindrome
#print axioms leading_zero_word
#print axioms leading_zero_controls
#print axioms leading_zero_unequal
#print axioms leading_zero_nonpalindrome
#print axioms huge_split_at
#print axioms huge_split_semantics
#print axioms huge_width_at
#print axioms huge_width_semantics
#print axioms huge_negative_at
#print axioms huge_negative_semantics

end Agent102.AllParameterControls
