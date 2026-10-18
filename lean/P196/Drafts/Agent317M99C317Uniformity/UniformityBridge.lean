import Std

/-!
Agent #317 — M99-C317 uniformity bridge (core Lean + Std only).

A fixed finite candidate ensemble is a `List α`. Prefix safety at every
horizon, witnessed inside that one fixed list, yields one all-time-safe
candidate. A moving seed universe does not. Same mathematics as Agent #17's
M99-A07 extraction lemma, kept under this namespace for the C317 audit.
-/

namespace Agent317

def PrefixSafe (Safe : α → Nat → Prop) (x : α) (N : Nat) : Prop :=
  ∀ t, t ≤ N → Safe x t

def ForeverSafe (Safe : α → Nat → Prop) (x : α) : Prop :=
  ∀ t, Safe x t

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

theorem fixed_finite_ensemble_uniformity
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

theorem moving_seed_counterexample :
    (∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x) ∧
    ¬ (∃ x : Nat, ∀ t, t < x) := by
  constructor
  · intro N
    exact ⟨N + 1, fun t ht => Nat.lt_succ_of_le ht⟩
  · intro h
    obtain ⟨x, hx⟩ := h
    exact Nat.lt_irrefl x (hx x)

theorem finite_seed_horizon_to_all_time
    (K : List α) (Safe : α → Nat → Prop)
    (h : ∀ N, ∃ x, x ∈ K ∧ ∀ t, t ≤ N → Safe x t) :
    ∃ x, x ∈ K ∧ ∀ t, Safe x t :=
  fixed_finite_ensemble_uniformity K Safe h

#print axioms fixed_finite_ensemble_uniformity
#print axioms moving_seed_counterexample
#print axioms finite_seed_horizon_to_all_time

end Agent317
