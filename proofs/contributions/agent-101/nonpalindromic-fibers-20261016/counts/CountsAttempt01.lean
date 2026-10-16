import Agent101NumericFibers

/-!
Agent #101. Complete sublists of the exact numeric fiber, separated by the
initial palindrome predicate. The common output is not assumed nonpalindromic.
This module therefore excludes time zero only; later safety statements must
supply their additional hypotheses explicitly.
-/

namespace Agent101

def palindromeNumericFiber (h : List Nat) (c : Option Nat) : List Nat :=
  (numericFiber h c).filter (fun n => decide (Lychrel196.Palindrome n))

def nonpalindromicNumericFiber (h : List Nat) (c : Option Nat) : List Nat :=
  (numericFiber h c).filter (fun n => !decide (Lychrel196.Palindrome n))

theorem mem_palindromeNumericFiber (h : List Nat) (c : Option Nat) (n : Nat) :
    n ∈ palindromeNumericFiber h c ↔
      n ∈ numericFiber h c ∧ Lychrel196.Palindrome n := by
  simp [palindromeNumericFiber]

theorem mem_nonpalindromicNumericFiber (h : List Nat) (c : Option Nat) (n : Nat) :
    n ∈ nonpalindromicNumericFiber h c ↔
      n ∈ numericFiber h c ∧ ¬ Lychrel196.Palindrome n := by
  simp [nonpalindromicNumericFiber]

theorem palindromeNumericFiber_nodup (h : List Nat) (c : Option Nat) :
    (palindromeNumericFiber h c).Nodup := by
  exact (numericFiber_nodup h c).filter _

theorem nonpalindromicNumericFiber_nodup (h : List Nat) (c : Option Nat) :
    (nonpalindromicNumericFiber h c).Nodup := by
  exact (numericFiber_nodup h c).filter _

theorem length_filter_partition {α : Type} (xs : List α) (p : α → Bool) :
    (xs.filter p).length + (xs.filter (fun x => !p x)).length = xs.length := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
    cases hp : p a <;> simp [List.filter_cons, hp] <;> omega

theorem numericFiber_length_partition (h : List Nat) (c : Option Nat) :
    (palindromeNumericFiber h c).length +
      (nonpalindromicNumericFiber h c).length = profileCount h c := by
  rw [palindromeNumericFiber, nonpalindromicNumericFiber,
    length_filter_partition, length_numericFiber]

theorem mem_nonpalindromicNumericFiber_numeric
    (h : List Nat) (c : Option Nat) (n : Nat)
    (hq : ∀ s ∈ coefficientWord h c, s ≤ 18) :
    n ∈ nonpalindromicNumericFiber h c ↔
      decimalWidth n (coefficientWord h c).length ∧
      Lychrel196.step n = natValue (coefficientWord h c) ∧
      ¬ Lychrel196.Palindrome n := by
  rw [mem_nonpalindromicNumericFiber, mem_numericFiber h c n hq]
  exact and_assoc

#print axioms palindromeNumericFiber
#print axioms nonpalindromicNumericFiber
#print axioms mem_palindromeNumericFiber
#print axioms mem_nonpalindromicNumericFiber
#print axioms palindromeNumericFiber_nodup
#print axioms nonpalindromicNumericFiber_nodup
#print axioms length_filter_partition
#print axioms numericFiber_length_partition
#print axioms mem_nonpalindromicNumericFiber_numeric

end Agent101
