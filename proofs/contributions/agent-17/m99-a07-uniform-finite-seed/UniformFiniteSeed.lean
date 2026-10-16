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

/-- A seed-dependent choice at each horizon is insufficient: the seed may
change with the horizon, so no fixed seed follows without a finite candidate
set or another uniformity condition. -/
theorem unrestricted_quantifier_swap_counterexample :
    ¬ ((∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x) →
       ∃ x : Nat, ∀ t, t < x) := by
  intro h
  obtain ⟨x, hx⟩ := h x
  have : x < x := hx x (le_rfl)
  exact Nat.lt_irrefl x this

#print axioms finite_uniform_extraction
#print axioms unrestricted_quantifier_swap_counterexample

end Agent17
