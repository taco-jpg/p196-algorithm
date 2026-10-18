import P196.Agent1PeriodicReturnCore.CondensationBound

/-! Finite downward composition of cyclic-interval lift bounds.

A path family must explicitly be closed under restriction. It need not
contain every graph path: actual orbit projections may impose extra carry
correlations. The lift premise is required for every positive-length
valid path lying inside one cyclic component, at every starting phase.
-/

namespace LiftHierarchy

open CondensationBound

/-- Validity may encode actual-orbit realizability in addition to graph
edges. Restriction closure is an explicit obligation at every level. -/
structure PathFamily (V : Type) where
  valid : Nat → (Nat → V) → Nat → Prop
  restrict : ∀ level path n, valid level path n →
    ∀ start length, start + length ≤ n →
      valid level (fun i => path (start + i)) length

/-- A concrete family of windows in one orbit's level projections.
Level-dependent eligibility can specify clock preservation and membership
in that level's retained graph; there is no phase-zero restriction. -/
def orbitPathFamily {V : Type} (projection : Nat → Nat → V)
    (eligible : Nat → Nat → Prop) : PathFamily V where
  valid level path n := ∃ start,
    (∀ i, i < n → eligible level (start + i)) ∧
    (∀ i, i < n → path i = projection level (start + i))
  restrict := by
    intro level path n hvalid a length hlength
    obtain ⟨start, heligible, hprojection⟩ := hvalid
    refine ⟨start + a, ?_, ?_⟩
    · intro i hi
      have h := heligible (a + i) (by omega)
      simpa only [Nat.add_assoc] using h
    · intro i hi
      have h := hprojection (a + i) (by omega)
      simpa only [Nat.add_assoc] using h

theorem orbit_interval_valid {V : Type} (projection : Nat → Nat → V)
    (eligible : Nat → Nat → Prop) (level start n : Nat)
    (heligible : ∀ i, i < n → eligible level (start + i)) :
    (orbitPathFamily projection eligible).valid level
      (fun i => projection level (start + i)) n :=
  ⟨start, heligible, fun _ _ => rfl⟩

variable {V C : Type} [DecidableEq C]

omit [DecidableEq C] in
/-- Lifting whole valid paths inside a cyclic component also lifts every
such interval, including intervals starting at a nonzero time or phase. -/
theorem cyclic_interval_lifts (family : PathFamily V)
    (component : Nat → V → C) (cyclic : Nat → C → Bool) (level : Nat)
    (hlift : ∀ path n, family.valid level path n → 0 < n →
      cyclic level (component level (path 0)) = true →
      (∀ i, i < n → component level (path i) = component level (path 0)) →
      ∃ lifted, family.valid (level + 1) lifted n)
    (path : Nat → V) (n a b : Nat) (hvalid : family.valid level path n)
    (hab : a ≤ b) (hb : b < n)
    (hcyclic : cyclic level (component level (path b)) = true)
    (hconstant : ∀ i, a ≤ i → i ≤ b →
      component level (path i) = component level (path b)) :
    ∃ lifted, family.valid (level + 1) lifted (b + 1 - a) := by
  have hsource := family.restrict level path n hvalid a (b + 1 - a) (by omega)
  apply hlift (fun i => path (a + i)) (b + 1 - a) hsource (by omega)
  · have hstart := hconstant a (Nat.le_refl a) hab
    simpa only [Nat.add_zero, hstart] using hcyclic
  · intro i hi
    have hhere := hconstant (a + i) (by omega) (by omega)
    have hstart := hconstant a (Nat.le_refl a) hab
    simpa only [Nat.add_zero] using hhere.trans hstart.symm

/-- Weighted rank bounds compose down a finite hierarchy.

The hypotheses do not assert that every path in an overapproximating
graph lifts. They quantify over the supplied restriction-closed family.
At the terminal level all visited components are acyclic. -/
theorem hierarchy_path_vertices_le (family : PathFamily V)
    (component : Nat → V → C) (cyclic : Nat → C → Bool)
    (rank : Nat → C → Nat) (bound : Nat → Nat) (depth : Nat)
    (hterminal : ∀ path n, family.valid depth path n →
      ∀ i, i < n → cyclic depth (component depth (path i)) = false)
    (hlift : ∀ level, level < depth → ∀ path n, family.valid level path n → 0 < n →
      cyclic level (component level (path 0)) = true →
      (∀ i, i < n → component level (path i) = component level (path 0)) →
      ∃ lifted, family.valid (level + 1) lifted n)
    (hacyclic : ∀ level, level ≤ depth → ∀ path n, family.valid level path n →
      ∀ i, i + 1 < n → cyclic level (component level (path i)) = false →
      component level (path i) ≠ component level (path (i + 1)))
    (hcertificate : ∀ level, level ≤ depth → ∀ path n, family.valid level path n →
      RankCertificate (fun i => component level (path i))
        (componentWeight (cyclic level) (bound (level + 1))) (rank level) n)
    (hstart : ∀ level, level ≤ depth → ∀ path n, family.valid level path n → 0 < n →
      rank level (component level (path 0)) ≤ bound level) :
    ∀ level, level ≤ depth → ∀ path n, family.valid level path n → n ≤ bound level := by
  have hmain : ∀ remaining level, level + remaining = depth →
      ∀ path n, family.valid level path n → n ≤ bound level := by
    intro remaining
    induction remaining with
    | zero =>
      intro level hlevel path n hvalid
      have he : level = depth := by omega
      subst level
      by_cases hn : n = 0
      · simp [hn]
      · have hbound := cyclic_path_vertices_le_rank
          (fun i => component depth (path i)) (cyclic depth) (rank depth)
          (bound (depth + 1)) n (by
            intro a b _ hb hc _
            have hf := hterminal path n hvalid b hb
            simp [hf] at hc)
          (hacyclic depth (Nat.le_refl depth) path n hvalid)
          (hcertificate depth (Nat.le_refl depth) path n hvalid)
        exact Nat.le_trans hbound
          (hstart depth (Nat.le_refl depth) path n hvalid (by omega))
    | succ remaining ih =>
      intro level hlevel path n hvalid
      have hlt : level < depth := by omega
      by_cases hn : n = 0
      · simp [hn]
      · have hbound := cyclic_path_vertices_le_rank
          (fun i => component level (path i)) (cyclic level) (rank level)
          (bound (level + 1)) n (by
            intro a b hab hb hc hconstant
            obtain ⟨lifted, hvalidLifted⟩ := cyclic_interval_lifts family component cyclic level
              (hlift level hlt) path n a b hvalid hab hb hc hconstant
            exact ih (level + 1) (by omega) lifted (b + 1 - a) hvalidLifted)
          (hacyclic level (by omega) path n hvalid)
          (hcertificate level (by omega) path n hvalid)
        exact Nat.le_trans hbound (hstart level (by omega) path n hvalid (by omega))
  intro level hlevel path n hvalid
  exact hmain (depth - level) level (by omega) path n hvalid

end LiftHierarchy
