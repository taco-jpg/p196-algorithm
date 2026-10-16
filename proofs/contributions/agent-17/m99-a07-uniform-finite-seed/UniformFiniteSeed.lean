import Std

/-!
Agent #17 — M99-A07 finite-seed uniformity (core Lean + Std only).

A fixed finite candidate ensemble is represented by a `List α`. If every
finite horizon has a member of that one fixed list that is safe through the
horizon, then some member of the list is safe at every time. The unrestricted
quantifier swap (candidate allowed to move with the horizon) is false.

No Mathlib, `sorry`, `native_decide` or new axiom is used.
-/

namespace Agent17

def PrefixSafe (Safe : α → Nat → Prop) (x : α) (N : Nat) : Prop :=
  ∀ t, t ≤ N → Safe x t

def ForeverSafe (Safe : α → Nat → Prop) (x : α) : Prop :=
  ∀ t, Safe x t

/-- Finitely many failing candidates fail by a common time bound. -/
theorem common_failure_bound (Safe : α → Nat → Prop) :
    ∀ K : List α, (∀ x, x ∈ K → ∃ t, ¬ Safe x t) →
      ∃ M, ∀ x, x ∈ K → ∃ t, t ≤ M ∧ ¬ Safe x t
  | [], _ => ⟨0, fun x hx => absurd hx (List.not_mem_nil)⟩
  | a :: K, h => by
      obtain ⟨ta, hta⟩ := h a List.mem_cons_self
      obtain ⟨M, hM⟩ := common_failure_bound Safe K
        (fun x hx => h x (List.mem_cons_of_mem a hx))
      refine ⟨max ta M, fun x hx => ?_⟩
      rcases List.mem_cons.mp hx with rfl | hxK
      · exact ⟨ta, Nat.le_max_left ta M, hta⟩
      · obtain ⟨t, htM, ht⟩ := hM x hxK
        exact ⟨t, Nat.le_trans htM (Nat.le_max_right ta M), ht⟩

/-- A finite, horizon-independent candidate list upgrades arbitrarily long
safe prefixes to one fixed all-time-safe candidate. -/
theorem finite_uniform_extraction
    (K : List α) (Safe : α → Nat → Prop)
    (hprefix : ∀ N, ∃ x, x ∈ K ∧ PrefixSafe Safe x N) :
    ∃ x, x ∈ K ∧ ForeverSafe Safe x := by
  apply Classical.byContradiction
  intro hnone
  have hbad : ∀ x, x ∈ K → ∃ t, ¬ Safe x t := by
    intro x hx
    apply Classical.byContradiction
    intro hno
    exact hnone ⟨x, hx, fun t =>
      Classical.byContradiction fun hnot => hno ⟨t, hnot⟩⟩
  obtain ⟨M, hM⟩ := common_failure_bound Safe K hbad
  obtain ⟨x, hxK, hx⟩ := hprefix M
  obtain ⟨t, htM, ht⟩ := hM x hxK
  exact ht (hx t htM)

/-- The unrestricted quantifier swap fails. For each horizon N one may choose
x=N+1, while no fixed natural x can dominate every t. -/
theorem unrestricted_quantifier_swap_counterexample :
    ¬ ((∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x) →
       ∃ x : Nat, ∀ t, t < x) := by
  intro h
  have hprefix : ∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x := by
    intro N
    exact ⟨N + 1, fun t ht => Nat.lt_succ_of_le ht⟩
  obtain ⟨x, hx⟩ := h hprefix
  exact Nat.lt_irrefl x (hx x)

#print axioms common_failure_bound
#print axioms finite_uniform_extraction
#print axioms unrestricted_quantifier_swap_counterexample

end Agent17
