import P196.Agent101NonpalindromicFibers.Agent101NonpalindromicFibers
import P196.Agent101ProtectedFamily.Agent101ProtectedPalindrome

/-!
Agent #101. Remove the exactly one initially palindromic integer from the
complete digit-split realization of Agent #3's protected profile family.
The exact count includes m = 0 and k = 0. Positive-time safety is supplied
separately from the original Agent #3 finite-horizon theorem when 0 < k.
-/

namespace Agent101.Protected

open P196.Agent3.OverflowHorizon

def protectedNonpalSeeds (m k : Nat) : List Nat :=
  (protectedSeeds m k).filter (fun n => !decide (Lychrel196.Palindrome n))

theorem mem_protectedNonpalSeeds (m k n : Nat) :
    n ∈ protectedNonpalSeeds m k ↔
      n ∈ protectedSeeds m k ∧ ¬ Lychrel196.Palindrome n := by
  simp [protectedNonpalSeeds]

theorem protectedNonpalSeeds_nodup (m k : Nat) :
    (protectedNonpalSeeds m k).Nodup :=
  (protectedSeeds_nodup m k).filter _

theorem protectedSeeds_palindrome_filter (m k : Nat) :
    (protectedSeeds m k).filter (fun n => decide (Lychrel196.Palindrome n)) =
      [palindromeSeed m k] := by
  apply list_eq_singleton_of_nodup_mem_iff _ _
    ((protectedSeeds_nodup m k).filter _)
  intro n
  simpa using protectedSeeds_palindrome_iff m k n

/-- The exact number of distinct ordinary integer seeds in this specified
family after excluding the single initial palindrome. -/
theorem length_protectedNonpalSeeds (m k : Nat) :
    (protectedNonpalSeeds m k).length = 5 * 11 ^ m - 1 := by
  have h := length_filter_partition (protectedSeeds m k)
    (fun n => decide (Lychrel196.Palindrome n))
  rw [protectedSeeds_palindrome_filter, List.length_singleton,
    length_protectedSeeds] at h
  change 1 + (protectedNonpalSeeds m k).length = 5 * 11 ^ m at h
  omega

theorem mem_protectedNonpalSeeds_positive (m k n : Nat)
    (hn : n ∈ protectedNonpalSeeds m k) : 0 < n :=
  mem_protectedSeeds_positive m k n ((mem_protectedNonpalSeeds m k n).mp hn).1

theorem mem_protectedNonpalSeeds_width (m k n : Nat)
    (hn : n ∈ protectedNonpalSeeds m k) :
    decimalWidth n (2 * (m + k + 1)) :=
  mem_protectedSeeds_width m k n ((mem_protectedNonpalSeeds m k n).mp hn).1

theorem mem_protectedNonpalSeeds_numeric (m k n : Nat) :
    n ∈ protectedNonpalSeeds m k ↔
      decimalWidth n (2 * (m + k + 1)) ∧
      ¬ Lychrel196.Palindrome n ∧
      ∃ xs : List Bool, xs.length = m ∧
        Lychrel196.step n = natValue (inputWord xs k) := by
  rw [mem_protectedNonpalSeeds, mem_protectedSeeds_numeric]
  constructor
  · rintro ⟨⟨hw, hx⟩, hp⟩
    exact ⟨hw, hp, hx⟩
  · rintro ⟨hw, hp, hx⟩
    exact ⟨⟨hw, hx⟩, hp⟩

/-- The count is genuinely positive, including the smallest m = k = 0
case. No empty-family premise can hide the subsequent safety assertion. -/
theorem protectedNonpalSeeds_nonempty (m k : Nat) :
    ∃ n, n ∈ protectedNonpalSeeds m k := by
  have hc := length_protectedNonpalSeeds m k
  have hp : 0 < 11 ^ m := Nat.pow_pos (by decide)
  cases hs : protectedNonpalSeeds m k with
  | nil => simp only [hs, List.length_nil] at hc; omega
  | cons n ns => exact ⟨n, by simp [hs]⟩

theorem protectedNonpalSeeds_exact (m k : Nat) :
    (protectedNonpalSeeds m k).length = 5 * 11 ^ m - 1 ∧
    (protectedNonpalSeeds m k).Nodup ∧
    (∃ n, n ∈ protectedNonpalSeeds m k) ∧
    ∀ n ∈ protectedNonpalSeeds m k,
      0 < n ∧ decimalWidth n (2 * (m + k + 1)) ∧
      ¬ Lychrel196.Palindrome n := by
  refine ⟨length_protectedNonpalSeeds m k, protectedNonpalSeeds_nodup m k,
    protectedNonpalSeeds_nonempty m k, ?_⟩
  intro n hn
  exact ⟨mem_protectedNonpalSeeds_positive m k n hn,
    mem_protectedNonpalSeeds_width m k n hn,
    ((mem_protectedNonpalSeeds m k n).mp hn).2⟩

#print axioms protectedNonpalSeeds
#print axioms mem_protectedNonpalSeeds
#print axioms protectedNonpalSeeds_nodup
#print axioms protectedSeeds_palindrome_filter
#print axioms length_protectedNonpalSeeds
#print axioms mem_protectedNonpalSeeds_positive
#print axioms mem_protectedNonpalSeeds_width
#print axioms mem_protectedNonpalSeeds_numeric
#print axioms protectedNonpalSeeds_nonempty
#print axioms protectedNonpalSeeds_exact

end Agent101.Protected
