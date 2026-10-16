import Agent101PalindromeFibers

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

/-- A computable test for whether this complete profile has an initial
palindrome. Positivity excludes impossible profiles and the empty numeral. -/
def palindromePossible (h : List Nat) (c : Option Nat) : Bool :=
  decide (0 < profileCount h c) &&
    (coefficientWord h c).all (fun s => decide (s % 2 = 0))

theorem palindromePossible_iff (h : List Nat) (c : Option Nat) :
    palindromePossible h c = true ↔
      0 < profileCount h c ∧ ∀ s ∈ coefficientWord h c, s % 2 = 0 := by
  simp [palindromePossible, List.all_eq_true]

def palindromeIndicator (h : List Nat) (c : Option Nat) : Nat :=
  if palindromePossible h c then 1 else 0

theorem list_eq_singleton_of_nodup_mem_iff {α : Type} (xs : List α) (a : α)
    (hn : xs.Nodup) (hm : ∀ x, x ∈ xs ↔ x = a) : xs = [a] := by
  cases xs with
  | nil =>
    have h := (hm a).mpr rfl
    simp at h
  | cons b bs =>
    have hb := (hm b).mp (by simp)
    subst b
    cases bs with
    | nil => rfl
    | cons b bs =>
      have hb := (hm b).mp (by simp)
      subst b
      have hnot := (List.nodup_cons.mp hn).1
      exact False.elim (hnot (by simp))

theorem list_eq_nil_of_forall_not_mem {α : Type} (xs : List α)
    (h : ∀ x, x ∉ xs) : xs = [] := by
  cases xs with
  | nil => rfl
  | cons a xs => exact False.elim (h a (by simp))

/-- The palindrome sublist is explicitly empty or the unique half-profile
numeral; no decision over an unbounded collection of integers is involved. -/
theorem palindromeNumericFiber_eq (h : List Nat) (c : Option Nat) :
    palindromeNumericFiber h c =
      if palindromePossible h c then
        [natValue ((coefficientWord h c).map (fun s => s / 2))]
      else [] := by
  by_cases hp : palindromePossible h c = true
  · rw [if_pos hp]
    apply list_eq_singleton_of_nodup_mem_iff _ _ (palindromeNumericFiber_nodup h c)
    intro n
    rw [mem_palindromeNumericFiber, palindrome_mem_numericFiber_iff]
    have hc := (palindromePossible_iff h c).mp hp
    exact ⟨fun hn => hn.2.2, fun heq => ⟨hc.1, hc.2, heq⟩⟩
  · rw [if_neg hp]
    apply list_eq_nil_of_forall_not_mem
    intro n hn
    have hi := (palindrome_mem_numericFiber_iff h c n).mp
      ((mem_palindromeNumericFiber h c n).mp hn)
    exact hp ((palindromePossible_iff h c).mpr ⟨hi.1, hi.2.1⟩)

theorem length_palindromeNumericFiber (h : List Nat) (c : Option Nat) :
    (palindromeNumericFiber h c).length = palindromeIndicator h c := by
  rw [palindromeNumericFiber_eq]
  cases hp : palindromePossible h c <;> simp [palindromeIndicator, hp]

/-- Exact number of distinct initially nonpalindromic ordinary integers
in the prescribed complete profile fiber. -/
theorem length_nonpalindromicNumericFiber (h : List Nat) (c : Option Nat) :
    (nonpalindromicNumericFiber h c).length =
      profileCount h c - palindromeIndicator h c := by
  have h := numericFiber_length_partition h c
  rw [length_palindromeNumericFiber] at h
  omega

theorem nonpalindromicNumericFiber_exact (h : List Nat) (c : Option Nat) :
    (nonpalindromicNumericFiber h c).Nodup ∧
    (nonpalindromicNumericFiber h c).length =
      profileCount h c - palindromeIndicator h c ∧
    ∀ n, n ∈ nonpalindromicNumericFiber h c ↔
      n ∈ numericFiber h c ∧ ¬ Lychrel196.Palindrome n := by
  exact ⟨nonpalindromicNumericFiber_nodup h c,
    length_nonpalindromicNumericFiber h c, mem_nonpalindromicNumericFiber h c⟩

#print axioms palindromeNumericFiber
#print axioms nonpalindromicNumericFiber
#print axioms mem_palindromeNumericFiber
#print axioms mem_nonpalindromicNumericFiber
#print axioms palindromeNumericFiber_nodup
#print axioms nonpalindromicNumericFiber_nodup
#print axioms length_filter_partition
#print axioms numericFiber_length_partition
#print axioms mem_nonpalindromicNumericFiber_numeric
#print axioms palindromePossible
#print axioms palindromePossible_iff
#print axioms palindromeIndicator
#print axioms list_eq_singleton_of_nodup_mem_iff
#print axioms list_eq_nil_of_forall_not_mem
#print axioms palindromeNumericFiber_eq
#print axioms length_palindromeNumericFiber
#print axioms length_nonpalindromicNumericFiber
#print axioms nonpalindromicNumericFiber_exact

end Agent101
