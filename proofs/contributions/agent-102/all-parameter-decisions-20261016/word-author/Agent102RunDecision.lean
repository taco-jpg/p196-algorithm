import Agent102RunWord

/-!
Agent #102：任意参数处的压缩字面词比较。
实际计算只使用段长总和及区间双遍历，不展开任何重复数字块。
允许空表、零长度段和任意自然数数字；不使用尾部或正长度假设。
-/

namespace Agent102

/-- 比较总段长，并检查每对具有正长度交叠的区间数字。 -/
def compressedEqual (A B : List Run) : Bool :=
  let SA := spans A
  let SB := spans B
  decide ((A.map Run.count).sum = (B.map Run.count).sum) &&
    SA.all (fun s => SB.all (fun t =>
      decide (max s.lo t.lo < min s.hi t.hi → s.digit = t.digit)))

theorem compressedEqual_eq_true_iff (A B : List Run) :
    compressedEqual A B = true ↔ word A = word B := by
  simpa only [compressedEqual, Bool.and_eq_true_iff, List.all_eq_true,
    decide_eq_true_eq, Span.overlaps]
    using (word_eq_iff_count_sum_and_overlap_digits A B).symm

theorem compressedEqual_eq_false_iff (A B : List Run) :
    compressedEqual A B = false ↔ word A ≠ word B := by
  rw [Bool.eq_false_iff, compressedEqual_eq_true_iff]

/-- 先按实际参数求每段自然数长度，再进行压缩比较。 -/
def equalAt (A B : List RunSpec) (k : Nat) : Bool :=
  compressedEqual (runsAt A k) (runsAt B k)

theorem equalAt_eq_true_iff (A B : List RunSpec) (k : Nat) :
    equalAt A B k = true ↔ wordAt A k = wordAt B k := by
  simpa only [equalAt, wordAt]
    using compressedEqual_eq_true_iff (runsAt A k) (runsAt B k)

theorem equalAt_eq_false_iff (A B : List RunSpec) (k : Nat) :
    equalAt A B k = false ↔ wordAt A k ≠ wordAt B k := by
  simpa only [equalAt, wordAt]
    using compressedEqual_eq_false_iff (runsAt A k) (runsAt B k)

end Agent102

#print axioms Agent102.compressedEqual
#print axioms Agent102.compressedEqual_eq_true_iff
#print axioms Agent102.compressedEqual_eq_false_iff
#print axioms Agent102.equalAt
#print axioms Agent102.equalAt_eq_true_iff
#print axioms Agent102.equalAt_eq_false_iff
