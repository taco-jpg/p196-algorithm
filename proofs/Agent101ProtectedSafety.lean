import Agent101ProtectedMultiplicity
import Agent101NormalizationValue
import FiniteHorizonTheorem

/-!
Agent 101 ordinary-integer safety for every original decimal digit split
in Agent 3's protected coefficient family. The first-step normalization
uses the compatibility module; all future safety is inherited from the
unchanged `inputWord_normalized_safe` theorem. The horizon may vary with k.
-/

namespace Agent101.Protected

open P196.Agent3.OverflowHorizon

theorem digitValue_eq_natValue (ds : List Nat) : digitValue ds = natValue ds := rfl

/-- The first ordinary step is exactly the existing normalized coefficient value. -/
theorem inputFiber_first_value (xs : List Bool) (k n : Nat)
    (hn : n ∈ numericFiber (inputHalf xs k) none) :
    Lychrel196.step n = digitValue (Agent8.normalize (inputWord xs k) 0) := by
  simpa only [coefficientWord_inputHalf, digitValue_eq_natValue] using
    numericFiber_first_step (inputHalf xs k) none n hn

/-- The second value depends only on the bit-word length and the horizon. -/
theorem inputFiber_second_value (xs : List Bool) (k : Nat) (hk : 0 < k)
    (n : Nat) (hn : n ∈ numericFiber (inputHalf xs k) none) :
    Lychrel196.step (Lychrel196.step n) = natValue (target xs.length k) := by
  rw [inputFiber_first_value xs k n hn]
  exact inputWord_common_next_value xs k hk

/-- All positive times through k+1 are safe for every original digit split. -/
theorem inputFiber_safe_positive_times (xs : List Bool) (k : Nat) (hk : 0 < k)
    (n : Nat) (hn : n ∈ numericFiber (inputHalf xs k) none) :
    ∀ t, 1 ≤ t → t ≤ k + 1 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  intro t ht htk
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (show t ≠ 0 by omega)
  rw [← Lychrel196.orbit_from_step n j, inputFiber_first_value xs k n hn]
  exact (inputWord_normalized_safe xs k hk).2 j (by omega)

theorem protectedSeeds_first_value (m k n : Nat)
    (hn : n ∈ protectedSeeds m k) :
    ∃ xs : List Bool, xs.length = m ∧
      Lychrel196.step n = digitValue (Agent8.normalize (inputWord xs k) 0) := by
  obtain ⟨xs, hlen, hx⟩ := (mem_protectedSeeds m k n).mp hn
  exact ⟨xs, hlen, inputFiber_first_value xs k n hx⟩

theorem protectedSeeds_second_value (m k : Nat) (hk : 0 < k)
    (n : Nat) (hn : n ∈ protectedSeeds m k) :
    Lychrel196.step (Lychrel196.step n) = natValue (target m k) := by
  obtain ⟨xs, hlen, hx⟩ := (mem_protectedSeeds m k n).mp hn
  simpa only [hlen] using inputFiber_second_value xs k hk n hx

theorem protectedSeeds_common_second_value (m k : Nat) (hk : 0 < k)
    (n p : Nat) (hn : n ∈ protectedSeeds m k) (hp : p ∈ protectedSeeds m k) :
    Lychrel196.step (Lychrel196.step n) = Lychrel196.step (Lychrel196.step p) :=
  (protectedSeeds_second_value m k hk n hn).trans
    (protectedSeeds_second_value m k hk p hp).symm

theorem protectedSeeds_safe_positive_times (m k : Nat) (hk : 0 < k)
    (n : Nat) (hn : n ∈ protectedSeeds m k) :
    ∀ t, 1 ≤ t → t ≤ k + 1 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  obtain ⟨xs, _, hx⟩ := (mem_protectedSeeds m k n).mp hn
  exact inputFiber_safe_positive_times xs k hk n hx

/-- Once an initial palindrome has been excluded, the same seed is safe
at every time from zero through k+1. -/
theorem protectedSeeds_safe_all_times_of_nonpalindrome (m k : Nat) (hk : 0 < k)
    (n : Nat) (hn : n ∈ protectedSeeds m k) (hp : ¬ Lychrel196.Palindrome n) :
    ∀ t, t ≤ k + 1 → ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  intro t ht
  cases t with
  | zero => exact hp
  | succ t =>
    exact protectedSeeds_safe_positive_times m k hk n hn (t + 1) (by omega) ht

/-- Exact family cardinality and complete positive-time safety. This theorem
does not assert that every seed is nonpalindromic at time zero. -/
theorem protectedSeeds_exact_safe_positive_times (m k : Nat) (hk : 0 < k) :
    (protectedSeeds m k).length = 5 * 11 ^ m ∧
      (protectedSeeds m k).Nodup ∧
      ∀ n ∈ protectedSeeds m k,
        0 < n ∧ decimalWidth n (2 * (m + k + 1)) ∧
        Lychrel196.step (Lychrel196.step n) = natValue (target m k) ∧
        ∀ t, 1 ≤ t → t ≤ k + 1 →
          ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  refine ⟨length_protectedSeeds m k, protectedSeeds_nodup m k, ?_⟩
  intro n hn
  exact ⟨mem_protectedSeeds_positive m k n hn, mem_protectedSeeds_width m k n hn,
    protectedSeeds_second_value m k hk n hn,
    protectedSeeds_safe_positive_times m k hk n hn⟩

#print axioms digitValue_eq_natValue
#print axioms inputFiber_first_value
#print axioms inputFiber_second_value
#print axioms inputFiber_safe_positive_times
#print axioms protectedSeeds_first_value
#print axioms protectedSeeds_second_value
#print axioms protectedSeeds_common_second_value
#print axioms protectedSeeds_safe_positive_times
#print axioms protectedSeeds_safe_all_times_of_nonpalindrome
#print axioms protectedSeeds_exact_safe_positive_times

end Agent101.Protected
