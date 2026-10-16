import Mathlib

/-!
Agent #217 — uniformity condition for finite-horizon-to-all-time extraction.

The central quantifier distinction is:
  finite horizons:   ∀ R, ∃ n, ∀ t ≤ R, Safe n t
  uniform seed:      ∃ n, ∀ R, ∀ t ≤ R, Safe n t
  all-time seed:     ∃ n, ∀ t, Safe n t

The first formula cannot in general be converted into either of the latter two.
The uniform-seed formula is exactly equivalent to the all-time formula.
-/

namespace Agent217.Uniformity

variable {α : Type*} {Safe : α → Nat → Prop}

/-- A single fixed seed that survives every finite horizon survives every time. -/
theorem fixed_seed_uniformity_to_all_time
    (h : ∃ n : α, ∀ R : Nat, ∀ t : Nat, t ≤ R → Safe n t) :
    ∃ n : α, ∀ t : Nat, Safe n t := by
  obtain ⟨n, hn⟩ := h
  refine ⟨n, ?_⟩
  intro t
  exact hn t t (le_rfl)

/-- An all-time safe seed is automatically uniform over every finite horizon. -/
theorem all_time_to_fixed_seed_uniformity
    (h : ∃ n : α, ∀ t : Nat, Safe n t) :
    ∃ n : α, ∀ R : Nat, ∀ t : Nat, t ≤ R → Safe n t := by
  obtain ⟨n, hn⟩ := h
  refine ⟨n, ?_⟩
  intro R t ht
  exact hn t

/-- Exact equivalence: uniformity in the horizon is the missing bridge. -/
theorem fixed_seed_uniformity_iff_all_time :
    (∃ n : α, ∀ R : Nat, ∀ t : Nat, t ≤ R → Safe n t) ↔
      ∃ n : α, ∀ t : Nat, Safe n t := by
  constructor
  · exact fixed_seed_uniformity_to_all_time
  · exact all_time_to_fixed_seed_uniformity

/-
WARNING: the finite-horizon statement has the seed existential *inside* the
horizon universal:
    ∀ R, ∃ n, ∀ t ≤ R, Safe n t.

The desired conclusion has one seed chosen before all times:
    ∃ n, ∀ t, Safe n t.

These are different quantifier orders. No proof may replace the first with the
second without an additional compactness/finiteness/uniformity argument.
The repository already contains a formal countermodel for this exact logical
failure (Agent122.Countermodel.finite_prefix_extraction_fails).
-/

end Agent217.Uniformity
