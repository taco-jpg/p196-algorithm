import P196.Agent101ProtectedFamily.FamilyDefinitions
import P196.Agent1Pr104Repair.DecimalSafeRuns

/-!
The finite-horizon target is interpreted through the repository's original
decimal column-sum semantics. The central run of `2 * k - 1` eighteens
supplies safety at positive times `1, ..., k` by `DecimalSafeRuns`.
Its odd outer column also rules out a palindrome at time zero.
-/

namespace P196.Agent3.OverflowHorizon

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
open DecimalSafeRuns

/-- The list target, with irrelevant out-of-range columns set to zero. -/
def targetColumn (m k i : Nat) : Nat := ((target m k)[i]?).getD 0

theorem target_length_for_safety (m k : Nat) (hk : 0 < k) :
    (target m k).length = 2 * m + 2 * k + 3 := by
  simp only [target, List.length_append, List.length_singleton, List.length_replicate]
  omega

theorem target_reverse_for_safety (m k : Nat) :
    (target m k).reverse = target m k := by
  simp [target, List.reverse_append, List.append_assoc]

theorem targetColumn_zero (m k : Nat) : targetColumn m k 0 = 5 := by
  simp [targetColumn, target]

theorem targetColumn_bound (m k i : Nat) (hi : i < (target m k).length) :
    targetColumn m k i ≤ 18 := by
  have hm : targetColumn m k i ∈ target m k := by
    simp only [targetColumn, List.getElem?_eq_getElem hi, Option.getD_some]
    exact List.getElem_mem hi
  simp [target, List.mem_replicate] at hm
  omega

theorem targetColumn_reflection (m k i : Nat) (hi : i < (target m k).length) :
    targetColumn m k i = targetColumn m k ((target m k).length - 1 - i) := by
  unfold targetColumn
  rw [← List.getElem?_reverse hi, target_reverse_for_safety]

theorem targetColumn_central (m k i : Nat)
    (hlo : m + 2 ≤ i) (hhi : i < m + 2 + (2 * k - 1)) :
    targetColumn m k i = 18 := by
  have h0 : ¬ i < 1 := by omega
  have h1 : ¬ i - 1 < m := by omega
  have h2 : ¬ i - 1 - m < 1 := by omega
  have h3 : i - 1 - m - 1 < 2 * k - 1 := by omega
  simp only [targetColumn, target, List.append_assoc, List.getElem?_append,
    List.length_singleton, List.length_replicate, List.getElem?_replicate,
    h0, h1, h2, h3, if_false, if_true, Option.getD_some]

/-- The target is a realizable finite decimal column-sum word. -/
theorem target_admissible (m k : Nat) (hk : 0 < k) :
    Admissible (target m k).length (targetColumn m k) := by
  have hlen := target_length_for_safety m k hk
  refine ⟨by omega, ?_, targetColumn_bound m k, targetColumn_reflection m k, ?_⟩
  · rw [targetColumn_zero]
    decide
  · intro i hi heq
    have hlo : m + 2 ≤ i := by omega
    have hhi : i < m + 2 + (2 * k - 1) := by omega
    rw [targetColumn_central m k i hlo hhi]

/-- The full explicit central run used by the existing persistence theorem. -/
theorem target_hasRun18 (m k : Nat) (hk : 0 < k) :
    HasRun18 (targetColumn m k) (target m k).length (2 * k - 1) := by
  refine ⟨m + 2, ?_, ?_⟩
  · rw [target_length_for_safety m k hk]
    omega
  · intro i hlo hhi
    exact targetColumn_central m k i hlo hhi

/-- Every decimal realization of the shared target avoids palindromes at
each of its next `k` positive iterates. -/
theorem target_numeric_safe_prefix (m k : Nat) (hk : 0 < k)
    (n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (target m k).length)
    (hrep : ∀ i, i < (target m k).length →
      columnSum d (target m k).length i = targetColumn m k i) :
    ∀ t, t < k → ¬ Palindrome (orbit n (t + 1)) := by
  intro t ht
  apply iter_not_palindrome_of_run n d (targetColumn m k)
    (target m k).length t hc hrep (target_admissible m k hk)
  obtain ⟨a, ha, hrun⟩ := target_hasRun18 m k hk
  refine ⟨a, by omega, ?_⟩
  intro i hlo hhi
  exact hrun i hlo (by omega)

/-- The odd outer sum rules out a palindrome in any realization of the
target itself, independently of the central-run argument. -/
theorem target_realization_nonpalindrome (m k n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (target m k).length)
    (hrep : ∀ i, i < (target m k).length →
      columnSum d (target m k).length i = targetColumn m k i) :
    ¬ Palindrome n := by
  intro hp
  rw [← hc.2.2.2] at hp
  have hs := (palindrome_value_iff d (target m k).length hc.2.1
    (Or.inr hc.2.2.1)).mp hp
  have hz := hs 0 hc.1
  have hq := hrep 0 hc.1
  rw [targetColumn_zero] at hq
  simp only [columnSum, reflected, Nat.sub_zero] at hq
  simp only [Nat.sub_zero] at hz
  omega

/-- An ordinary positive integer realizes the target and is safe at
all times `0, ..., k`, including the initial realization. -/
theorem target_positive_realization_safe_prefix (m k : Nat) (hk : 0 < k) :
    ∃ n d, 0 < n ∧ Canonical n d (target m k).length ∧
      (∀ i, i < (target m k).length →
        columnSum d (target m k).length i = targetColumn m k i) ∧
      ∀ t, t ≤ k → ¬ Palindrome (orbit n t) := by
  have ha := target_admissible m k hk
  obtain ⟨n, d, hn, hc, hrep⟩ := valid_word_realizable (targetColumn m k)
    (target m k).length ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  refine ⟨n, d, hn, hc, hrep, ?_⟩
  intro t ht
  cases t with
  | zero =>
      exact target_realization_nonpalindrome m k n d hc hrep
  | succ t =>
      exact target_numeric_safe_prefix m k hk n d hc hrep t (by omega)

end P196.Agent3.OverflowHorizon
