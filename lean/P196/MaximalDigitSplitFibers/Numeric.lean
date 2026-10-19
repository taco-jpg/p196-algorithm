import P196.MaximalDigitSplitFibers.Gap
import P196.Agent101DigitSplit.Agent101NumericFibers

/-!
Agent #7: exact maximum and sharp submaximum for complete ordinary-integer
digit-splitting fibers at a prescribed source width. The witnesses include
all predecessors of that width and have no repeated members.
-/

namespace Agent7.MaximalDigitSplitFibers

open Agent101

/-- A prescribed-profile numerical fiber reaches the uniform maximum
exactly when each outer, inner, and center factor does. -/
theorem numericFiber_max_iff (s : Nat) (h : List Nat) (c : Option Nat) :
    (numericFiber (s :: h) c).length = 9 * 10 ^ h.length ↔
      (s = 9 ∨ s = 10) ∧ (∀ t ∈ h, t = 9) ∧ centerCount c = 1 := by
  rw [length_numericFiber]
  exact profileCount_max_iff s h c

/-- No prescribed-profile numerical fiber with at least one inner pair
has a cardinality strictly between the sharp submaximum and maximum. -/
theorem numericFiber_gap (s : Nat) (h : List Nat) (c : Option Nat)
    (hlen : 0 < h.length)
    (hne : (numericFiber (s :: h) c).length ≠ 9 * 10 ^ h.length) :
    (numericFiber (s :: h) c).length ≤ 81 * 10 ^ (h.length - 1) := by
  rw [length_numericFiber] at hne ⊢
  exact profileCount_gap s h c hlen hne

/-- The no-inner-pair boundary has maximum nine and submaximum eight. -/
theorem numericFiber_gap_empty (s : Nat) (c : Option Nat)
    (hne : (numericFiber [s] c).length ≠ 9) :
    (numericFiber [s] c).length ≤ 8 := by
  rw [length_numericFiber] at hne ⊢
  exact profileCount_gap_empty s c hne

private theorem center_bounded_of_valid (c : Option Nat)
    (hc : centerCount c = 1) : ∀ t ∈ c.toList, t ≤ 18 := by
  cases c with
  | none => simp
  | some s =>
    have hs : s ≤ 18 := by
      by_cases hs : s ≤ 18
      · exact hs
      · simp [centerCount, hs] at hc
    simpa using hs
private theorem submax_word_bounded (k : Nat) (c : Option Nat)
    (hc : centerCount c = 1) :
    ∀ t ∈ coefficientWord (9 :: 8 :: List.replicate k 9) c, t ≤ 18 := by
  apply coefficientWord_bounded
  · intro t ht
    simp only [List.mem_cons] at ht
    rcases ht with rfl | rfl | ht
    · decide
    · decide
    · rw [List.eq_of_mem_replicate ht]
      decide
  · exact center_bounded_of_valid c hc

/-- An explicit complete, duplicate-free ordinary-integer fiber realizes
the submaximum for every positive inner length and every valid center.
The source width is given directly, including its parity through `c`. -/
theorem submax_complete_numeric_fiber (k : Nat) (c : Option Nat)
    (hc : centerCount c = 1) :
    ∃ target : Nat, ∃ xs : List Nat,
      xs.Nodup ∧
      (∀ n, n ∈ xs ↔
        decimalWidth n (2 * (k + 2) + c.toList.length) ∧
        Lychrel196.step n = target) ∧
      xs.length = 81 * 10 ^ k ∧ xs.length < 9 * 10 ^ (k + 1) := by
  refine ⟨natValue (coefficientWord (9 :: 8 :: List.replicate k 9) c),
    numericFiber (9 :: 8 :: List.replicate k 9) c,
    numericFiber_nodup _ _, ?_, ?_, ?_⟩
  · intro n
    have hm := mem_numericFiber (9 :: 8 :: List.replicate k 9) c n
      (submax_word_bounded k c hc)
    simpa only [length_coefficientWord, List.length_cons,
      List.length_replicate] using hm
  · rw [length_numericFiber]
    exact profileCount_submax_witness k c hc
  · rw [length_numericFiber]
    exact profileCount_submax_witness_lt k c hc

/-- The boundary submaximum is likewise realized by a complete numerical
fiber: width two with no center, or width three with a valid center. -/
theorem submax_complete_numeric_fiber_empty (c : Option Nat)
    (hc : centerCount c = 1) :
    ∃ target : Nat, ∃ xs : List Nat,
      xs.Nodup ∧
      (∀ n, n ∈ xs ↔ decimalWidth n (2 + c.toList.length) ∧
        Lychrel196.step n = target) ∧
      xs.length = 8 ∧ xs.length < 9 := by
  refine ⟨natValue (coefficientWord [8] c), numericFiber [8] c,
    numericFiber_nodup _ _, ?_, ?_, ?_⟩
  · intro n
    have hb := coefficientWord_bounded [8] c (by simp)
      (center_bounded_of_valid c hc)
    have hm := mem_numericFiber [8] c n hb
    simpa only [length_coefficientWord, List.length_cons,
      List.length_nil, Nat.reduceAdd, Nat.mul_one] using hm
  · rw [length_numericFiber]
    exact profileCount_submax_empty_witness c hc
  · rw [length_numericFiber]
    exact profileCount_submax_empty_witness_lt c hc
/-- The gap bound and an ordinary-integer attainer in one statement.
All profiles of the indexed half-width are covered by the upper bound. -/
theorem sharp_numeric_gap (k : Nat) (c : Option Nat)
    (hc : centerCount c = 1) :
    (∀ s h, h.length = k + 1 →
      (numericFiber (s :: h) c).length ≠ 9 * 10 ^ (k + 1) →
      (numericFiber (s :: h) c).length ≤ 81 * 10 ^ k) ∧
    ∃ target : Nat, ∃ xs : List Nat,
      xs.Nodup ∧
      (∀ n, n ∈ xs ↔
        decimalWidth n (2 * (k + 2) + c.toList.length) ∧
        Lychrel196.step n = target) ∧
      xs.length = 81 * 10 ^ k ∧ xs.length < 9 * 10 ^ (k + 1) := by
  refine ⟨?_, submax_complete_numeric_fiber k c hc⟩
  intro s h hh hne
  have hpos : 0 < h.length := by omega
  have hn : (numericFiber (s :: h) c).length ≠ 9 * 10 ^ h.length := by
    simpa only [hh] using hne
  have hg := numericFiber_gap s h c hpos hn
  simpa only [hh, Nat.add_sub_cancel] using hg

#print axioms numericFiber_max_iff
#print axioms numericFiber_gap
#print axioms numericFiber_gap_empty
#print axioms submax_complete_numeric_fiber
#print axioms submax_complete_numeric_fiber_empty
#print axioms sharp_numeric_gap

end Agent7.MaximalDigitSplitFibers
