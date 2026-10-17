import P196.Agent101DigitSplit.Agent101NumericFibers

/-!
Agent 105：实际十进制宽度、有限数位与跨宽度前驱的支持接口。

宽度唯一性直接复用 Agent101 已发表的 decimalWidth_unique，
数位唯一性直接复用原始基础模块的 value_injective。
本模块仅给出这些既有结果与真实 step/carry 语义之间的组合接口。
-/

namespace Agent105WidthSupport9df76b

open DecimalDigits Lychrel196 FoldedDecimal

/-- 同一个正整数的规范十进制表示具有相同宽度。 -/
theorem canonical_width_unique {n L K : Nat} {d e : Nat → Nat}
    (hd : Canonical n d L) (he : Canonical n e K) : L = K := by
  exact Agent101.decimalWidth_unique n L K
    (Agent101.canonical_decimalWidth n d L hd)
    (Agent101.canonical_decimalWidth n e K he)

/-- 唯一性只断言实际宽度内的数位，不限制数位函数的无限尾部。 -/
theorem canonical_digits_unique {n L : Nat} {d e : Nat → Nat}
    (hd : Canonical n d L) (he : Canonical n e L) :
    ∀ i, i < L → d i = e i := by
  exact value_injective d e L hd.2.1 he.2.1
    (hd.2.2.2.trans he.2.2.2.symm)

theorem canonical_width_and_digits_unique {n L K : Nat} {d e : Nat → Nat}
    (hd : Canonical n d L) (he : Canonical n e K) :
    L = K ∧ ∀ i, i < L → d i = e i := by
  have hw := canonical_width_unique hd he
  subst K
  exact ⟨rfl, canonical_digits_unique hd he⟩

/-- 最末进位精确决定真实 step 的规范输出宽度。 -/
theorem canonical_step_width {n L W : Nat} {d s : Nat → Nat}
    (hn : Canonical n d L) (hs : Canonical (step n) s W) :
    W = L + carry (columnSum d L) L := by
  rcases actual_overflow_cases d L hn.2.1 with hc | hc
  · have hw := canonical_width_unique hs
      (canonical_next_no_overflow n d L hn hc)
    simpa only [hc, Nat.add_zero] using hw
  · have hw := canonical_width_unique hs
      (canonical_next_overflow n d L hn hc)
    simpa only [hc] using hw

/-- 真实输出宽度必为 L 或 L+1，并同时确定相应末进位。 -/
theorem step_width_cases {n L W : Nat} {d s : Nat → Nat}
    (hn : Canonical n d L) (hs : Canonical (step n) s W) :
    (W = L ∧ carry (columnSum d L) L = 0) ∨
      (W = L + 1 ∧ carry (columnSum d L) L = 1) := by
  have hw := canonical_step_width hn hs
  rcases actual_overflow_cases d L hn.2.1 with hc | hc
  · exact Or.inl ⟨by simpa only [hc, Nat.add_zero] using hw, hc⟩
  · exact Or.inr ⟨by simpa only [hc] using hw, hc⟩

/-- 保留真实数值语义的具体输出数位存在性。 -/
theorem canonical_step_exists {n L : Nat} {d : Nat → Nat}
    (hn : Canonical n d L) :
    ∃ s, Canonical (step n) s (L + carry (columnSum d L) L) := by
  rcases actual_overflow_cases d L hn.2.1 with hc | hc
  · refine ⟨output (columnSum d L), ?_⟩
    simpa only [hc, Nat.add_zero] using canonical_next_no_overflow n d L hn hc
  · refine ⟨extended (columnSum d L) L, ?_⟩
    simpa only [hc] using canonical_next_overflow n d L hn hc

/-- 两个不同宽度的正数若有同一输出，宽度恰差一位；
短输入必溢出，长输入必不溢出。 -/
theorem cross_width_carries {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m) :
    K = L + 1 ∧ carry (columnSum d L) L = 1 ∧
      carry (columnSum e K) K = 0 := by
  obtain ⟨s, hs⟩ := canonical_step_exists hn
  have hs' : Canonical (step m) s (L + carry (columnSum d L) L) := by
    simpa only [hstep] using hs
  have hw := canonical_step_width hm hs'
  have hd := carry_bounded (columnSum d L) L
    (columnSum_bounded d L hn.2.1) L (Nat.le_refl L)
  have he := carry_bounded (columnSum e K) K
    (columnSum_bounded e K hm.2.1) K (Nat.le_refl K)
  omega

#print axioms canonical_width_unique
#print axioms canonical_digits_unique
#print axioms canonical_width_and_digits_unique
#print axioms canonical_step_width
#print axioms step_width_cases
#print axioms canonical_step_exists
#print axioms cross_width_carries

end Agent105WidthSupport9df76b
