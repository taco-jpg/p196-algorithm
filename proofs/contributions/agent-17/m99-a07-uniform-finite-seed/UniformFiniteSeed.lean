import All

namespace Agent17

def PrefixSafe (Safe : α → Nat → Prop) (x : α) (N : Nat) : Prop :=
  ∀ t, t ≤ N → Safe x t

def ForeverSafe (Safe : α → Nat → Prop) (x : α) : Prop :=
  ∀ t, Safe x t

/-- A finite, horizon-independent candidate set upgrades arbitrarily long
safe prefixes to one fixed all-time-safe candidate. -/
theorem finite_uniform_extraction
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

/-- The unrestricted quantifier swap fails. For each horizon N one may choose
x=N+1, while no fixed natural x can dominate every t. -/
theorem unrestricted_quantifier_swap_counterexample :
    ¬ ((∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x) →
       ∃ x : Nat, ∀ t, t < x) := by
  intro h
  have hprefix : ∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x := by
    intro N
    refine ⟨N + 1, ?_⟩
    intro t ht
    omega
  obtain ⟨x, hx⟩ := h hprefix
  exact Nat.lt_irrefl x (hx x le_rfl)

#print axioms finite_uniform_extraction
#print axioms unrestricted_quantifier_swap_counterexample

end Agent17
