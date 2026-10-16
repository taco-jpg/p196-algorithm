import Agent423.FiniteEnsemble

set_option autoImplicit false

/-! Agent #17's written finite-ensemble theorem, repaired by Agent #423.
Explicit complete enumeration replaces the unavailable Fintype interface.
The original author's mathematical provenance is retained. -/
namespace Agent17

universe u
variable {α : Type u}

abbrev PrefixSafe (Safe : α → Nat → Prop) (x : α) (N : Nat) : Prop :=
  Agent423.FiniteEnsemble.PrefixSafe Safe x N

abbrev ForeverSafe (Safe : α → Nat → Prop) (x : α) : Prop :=
  Agent423.FiniteEnsemble.ForeverSafe Safe x

/-- Every candidate in this type occurs in the fixed finite enumeration. -/
theorem finite_uniform_extraction (enum : List α)
    (complete : ∀ x : α, x ∈ enum)
    (Safe : α → Nat → Prop)
    (hprefix : ∀ N, ∃ x : α, PrefixSafe Safe x N) :
    ∃ x : α, ForeverSafe Safe x :=
  Agent423.FiniteEnsemble.enumerated_type_uniform_extraction enum complete Safe hprefix

theorem unrestricted_quantifier_swap_counterexample :
    ¬ ((∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x) →
       ∃ x : Nat, ∀ t, t < x) :=
  Agent423.FiniteEnsemble.unrestricted_quantifier_swap_counterexample

#print axioms finite_uniform_extraction
#print axioms unrestricted_quantifier_swap_counterexample

end Agent17
