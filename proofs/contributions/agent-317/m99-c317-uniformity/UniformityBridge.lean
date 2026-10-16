import Std

namespace Agent317

def PrefixSafe (Safe : α → Nat → Prop) (x : α) (N : Nat) : Prop :=
  ∀ t, t ≤ N → Safe x t

def ForeverSafe (Safe : α → Nat → Prop) (x : α) : Prop :=
  ∀ t, Safe x t

theorem fixed_finite_ensemble_uniformity
    {α : Type} [Fintype α] [Nonempty α]
    (Safe : α → Nat → Prop)
    (hprefix : ∀ N, ∃ x : α, PrefixSafe Safe x N) :
    ∃ x : α, ForeverSafe Safe x := by
  classical
  by_contra hnone
  have hbad : ∀ x : α, ∃ t : Nat, ¬ Safe x t := by
    intro x
    by_contra hno_bad
    apply hnone
    exact fun t => by
      by_contra hnot
      exact hno_bad ⟨t, hnot⟩
  let bad : α → Nat := fun x => Classical.choose (hbad x)
  let M : Nat := Finset.univ.sup bad
  have hM : ∀ x : α, bad x ≤ M := by
    intro x
    exact Finset.le_sup (Finset.mem_univ x)
  obtain ⟨x, hx⟩ := hprefix M
  obtain ⟨t, ht⟩ := hbad x
  have htM : t ≤ M := le_trans ht (hM x)
  exact ht (hx t htM)

theorem moving_seed_counterexample :
    (∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x) ∧
    ¬ (∃ x : Nat, ∀ t, t < x) := by
  constructor
  · intro N
    refine ⟨N + 1, ?_⟩
    intro t ht
    exact Nat.lt_succ_of_le ht
  · intro h
    obtain ⟨x, hx⟩ := h
    exact Nat.lt_irrefl x (hx x)

theorem finite_seed_horizon_to_all_time
    {α : Type} [Fintype α] [Nonempty α]
    (Safe : α → Nat → Prop)
    (h : ∀ N, ∃ x : α, ∀ t, t ≤ N → Safe x t) :
    ∃ x : α, ∀ t, Safe x t :=
  fixed_finite_ensemble_uniformity Safe h

#print axioms fixed_finite_ensemble_uniformity
#print axioms moving_seed_counterexample
#print axioms finite_seed_horizon_to_all_time

end Agent317
