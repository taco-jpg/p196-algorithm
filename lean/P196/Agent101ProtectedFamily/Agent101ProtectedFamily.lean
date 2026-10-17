import P196.Agent101ProtectedFamily.Agent101ProtectedNonpalindromic
import P196.Agent101ProtectedFamily.Agent101ProtectedSafety

/-!
Agent #101. Complete ordinary-integer family with exact digit-split count,
a common second iterate, and initial-through-finite-horizon nonpalindromicity.
The transition and horizon theorem are Agent #3's unchanged protected-family
results. This module combines them with the new complete integer enumeration.
The horizon parameter is finite and may change with the chosen family.
-/

namespace Agent101.Protected

open P196.Agent3.OverflowHorizon

theorem protectedNonpalSeeds_second_value (m k : Nat) (hk : 0 < k)
    (n : Nat) (hn : n ∈ protectedNonpalSeeds m k) :
    Lychrel196.step (Lychrel196.step n) = natValue (target m k) :=
  protectedSeeds_second_value m k hk n
    ((mem_protectedNonpalSeeds m k n).mp hn).1

theorem protectedNonpalSeeds_common_second_value (m k : Nat) (hk : 0 < k)
    (n p : Nat) (hn : n ∈ protectedNonpalSeeds m k)
    (hp : p ∈ protectedNonpalSeeds m k) :
    Lychrel196.step (Lychrel196.step n) =
      Lychrel196.step (Lychrel196.step p) :=
  (protectedNonpalSeeds_second_value m k hk n hn).trans
    (protectedNonpalSeeds_second_value m k hk p hp).symm

theorem protectedNonpalSeeds_safe (m k : Nat) (hk : 0 < k)
    (n : Nat) (hn : n ∈ protectedNonpalSeeds m k) :
    ∀ t, t ≤ k + 1 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  have hs := (mem_protectedNonpalSeeds m k n).mp hn
  exact protectedSeeds_safe_all_times_of_nonpalindrome m k hk n hs.1 hs.2

/-- Exact distinct ordinary integers, all positive and of the stated width,
all sharing the explicit second iterate, all nonpalindromic through k+1.
The list is complete for the specified profiles after initial-palindrome
removal; this is not a claim about every second preimage of the target. -/
theorem protectedNonpalFamily_exact (m k : Nat) (hk : 0 < k) :
    (protectedNonpalSeeds m k).length = 5 * 11 ^ m - 1 ∧
    (protectedNonpalSeeds m k).Nodup ∧
    (∃ n, n ∈ protectedNonpalSeeds m k) ∧
    ∀ n ∈ protectedNonpalSeeds m k,
      0 < n ∧ decimalWidth n (2 * (m + k + 1)) ∧
      Lychrel196.step (Lychrel196.step n) = natValue (target m k) ∧
      ∀ t, t ≤ k + 1 →
        ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  refine ⟨length_protectedNonpalSeeds m k, protectedNonpalSeeds_nodup m k,
    protectedNonpalSeeds_nonempty m k, ?_⟩
  intro n hn
  exact ⟨mem_protectedNonpalSeeds_positive m k n hn,
    mem_protectedNonpalSeeds_width m k n hn,
    protectedNonpalSeeds_second_value m k hk n hn,
    protectedNonpalSeeds_safe m k hk n hn⟩

#print axioms protectedNonpalSeeds_second_value
#print axioms protectedNonpalSeeds_common_second_value
#print axioms protectedNonpalSeeds_safe
#print axioms protectedNonpalFamily_exact

end Agent101.Protected
