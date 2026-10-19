import Std

/-!
Shared finite-list bridges for the original symmetric-word census.
The injectivity hypothesis is restricted to the enumerated domain.
-/

set_option autoImplicit false

namespace SymmetricCarryCensus

theorem nodup_map_of_injOn {α β : Type} (xs : List α) (f : α → β)
    (hx : xs.Nodup)
    (hf : ∀ a ∈ xs, ∀ b ∈ xs, f a = f b → a = b) :
    (xs.map f).Nodup := by
  apply List.pairwise_map.mpr
  apply List.Pairwise.imp_of_mem (p := hx)
  intro a b ha hb hne heq
  exact hne (hf a ha b hb heq)

theorem perm_of_nodup_mem_iff {α : Type} [DecidableEq α]
    (xs ys : List α) (hx : xs.Nodup) (hy : ys.Nodup)
    (hmem : ∀ a, a ∈ xs ↔ a ∈ ys) : xs.Perm ys := by
  induction xs generalizing ys with
  | nil =>
    cases ys with
    | nil => exact List.Perm.nil
    | cons a ys =>
      have h := (hmem a).mpr (by simp)
      simp at h
  | cons x xs ih =>
    have hxs := List.nodup_cons.mp hx
    have hxy : x ∈ ys := (hmem x).mp (by simp)
    have htail : xs.Perm (ys.erase x) := by
      apply ih (ys := ys.erase x) hxs.2 (hy.erase x)
      intro a
      rw [hy.mem_erase_iff]
      constructor
      · intro ha
        refine ⟨?_, (hmem a).mp (List.mem_cons_of_mem x ha)⟩
        intro heq
        subst a
        exact hxs.1 ha
      · rintro ⟨hne, ha⟩
        rcases List.mem_cons.mp ((hmem a).mpr ha) with heq | htail
        · exact False.elim (hne heq)
        · exact htail
    exact (htail.cons x).trans (List.perm_cons_erase hxy).symm

end SymmetricCarryCensus
