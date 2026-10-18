import P196.Drafts.Agent9NooverflowHorizon.Agent9HorizonCounts
import P196.Drafts.Agent9NooverflowHorizon.Agent9HorizonSafety
import P196.Drafts.Agent9NooverflowHorizon.Agent9HorizonNumeric

/-!
Complete source-level endpoint for the preserved no-overflow finite-horizon
construction. The coefficient-word fiber is counted exactly; its target is
realized by an actual positive decimal integer, and all canonical target
realizations satisfy the stated finite-time conclusion.
-/

namespace P196.Agent9.NoOverflowHorizon

open InverseFibers Lychrel196 DecimalDigits FoldedDecimal

/-- The complete finite construction: an exact nonempty canonical fiber and
a genuine positive target realization safe through the prescribed horizon.
The statement also holds at k=0; the source's m,k>=1 case is included. -/
theorem protected_nooverflow_family (m k : Nat) (hm : 0 < m) :
    (inputWords m k).Nodup ∧
    (inputWords m k).length = fib m ∧
    (∃ q, q ∈ inputWords m k) ∧
    (∀ q, q ∈ inputWords m k ↔ FullActualFiber m k q) ∧
    ∃ n d, 0 < n ∧ Canonical n d (targetWord m k).length ∧
      (∀ i, i < (targetWord m k).length →
        columnSum d (targetWord m k).length i = targetColumns m k i) ∧
      ∀ j, j ≤ k → ¬ Palindrome (orbit n j) := by
  exact ⟨protected_fiber_nodup m k, protected_fiber_cardinality m k,
    protected_fiber_nonempty m k hm, protected_fiber_membership m k,
    protected_target_safe_realization m k⟩

/-- Safety is universal over canonical realizations, not just the witness
chosen by the preceding existential theorem. Time zero uses outer parity. -/
theorem protected_target_all_realizations_safe (m k n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (targetWord m k).length)
    (hr : ∀ i, i < (targetWord m k).length →
      columnSum d (targetWord m k).length i = targetColumns m k i)
    (j : Nat) (hj : j ≤ k) : ¬ Palindrome (orbit n j) := by
  cases j with
  | zero => exact protected_target_not_palindrome m k n d hc hr
  | succ j => exact protected_target_safe m k n d hc hr (j + 1) (by omega) hj

/-- Every member of the exactly counted word family has an ordinary positive
integer predecessor realizing the stated pair words and finite safe orbit.
The cardinality remains a count of coefficient words, not of digit splits. -/
theorem protected_nooverflow_integer_family (m k : Nat) (hm : 0 < m) :
    (inputWords m k).Nodup ∧
    (inputWords m k).length = fib m ∧
    (∃ q, q ∈ inputWords m k) ∧
    (∀ q, q ∈ inputWords m k ↔ FullActualFiber m k q) ∧
    ∀ q, q ∈ inputWords m k →
      ∃ n d, 0 < n ∧ Canonical n d q.length ∧
        (∀ i, i < q.length → columnSum d q.length i = q.getD i 0) ∧
        Agent109.pairWord n = q ∧
        Agent109.pairWord (step n) = targetWord m k ∧
        ∀ j, 1 ≤ j → j ≤ k + 1 → ¬ Palindrome (orbit n j) := by
  refine ⟨protected_fiber_nodup m k, protected_fiber_cardinality m k,
    protected_fiber_nonempty m k hm, protected_fiber_membership m k, ?_⟩
  intro q hq
  exact protected_predecessor_realizable m k q
    ((protected_fiber_membership m k q).mp hq)

#print axioms protected_nooverflow_family
#print axioms protected_target_all_realizations_safe
#print axioms protected_nooverflow_integer_family

end P196.Agent9.NoOverflowHorizon
