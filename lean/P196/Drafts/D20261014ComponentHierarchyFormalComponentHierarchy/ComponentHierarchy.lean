import P196.Agent1PeriodicReturnCore.CondensationBound

/-! Component-specific spatial-lift bounds, by induction on remaining width.
Jobs need not form a finite type. Every cyclic component selects its own
child job, whose height must be strictly smaller. Valid actual-path families
explicitly carry interval restriction closure. -/

namespace ComponentHierarchy

open CondensationBound

structure JobPathFamily (J V : Type) where
  valid : J → (Nat → V) → Nat → Prop
  restrict : ∀ job path n, valid job path n →
    ∀ start length, start + length ≤ n →
      valid job (fun i => path (start + i)) length

/-- Windows in an orbit, with graph membership allowed to depend on the job. -/
def orbitPathFamily {J V : Type} (projection : J → Nat → V)
    (eligible : J → Nat → Prop) : JobPathFamily J V where
  valid job path n := ∃ start,
    (∀ i, i < n → eligible job (start + i)) ∧
    (∀ i, i < n → path i = projection job (start + i))
  restrict := by
    intro job path n hvalid a length hlength
    obtain ⟨start, heligible, hprojection⟩ := hvalid
    refine ⟨start + a, ?_, ?_⟩
    · intro i hi
      have h := heligible (a + i) (by omega)
      simpa only [Nat.add_assoc] using h
    · intro i hi
      have h := hprojection (a + i) (by omega)
      simpa only [Nat.add_assoc] using h

theorem orbit_interval_valid {J V : Type} (projection : J → Nat → V)
    (eligible : J → Nat → Prop) (job : J) (start n : Nat)
    (heligible : ∀ i, i < n → eligible job (start + i)) :
    (orbitPathFamily projection eligible).valid job
      (fun i => projection job (start + i)) n :=
  ⟨start, heligible, fun _ _ => rfl⟩

variable {J V C : Type}

def componentWeight (cyclic : C → Bool) (cyclicBound : C → Nat) (c : C) : Nat :=
  if cyclic c then cyclicBound c else 1

def jobWeight (cyclic : J → C → Bool) (child : J → C → J)
    (bound : J → Nat) (job : J) : C → Nat :=
  componentWeight (cyclic job) (fun c => bound (child job c))

/-- Unlike a uniform next-level bound, each cyclic component may have its
own proven interval bound. Acyclic components still have weight one. -/
theorem interval_bound_of_component_bounds (component : Nat → C)
    (cyclic : C → Bool) (cyclicBound : C → Nat) (n : Nat)
    (hcyclic : ∀ a b, a ≤ b → b < n → cyclic (component b) = true →
      (∀ i, a ≤ i → i ≤ b → component i = component b) →
      b + 1 - a ≤ cyclicBound (component b))
    (hacyclic : ∀ i, i + 1 < n → cyclic (component i) = false →
      component i ≠ component (i + 1)) :
    IntervalBound component (componentWeight cyclic cyclicBound) n := by
  intro a b hab hb hconstant
  by_cases hc : cyclic (component b) = true
  · simpa only [componentWeight, hc, if_true] using hcyclic a b hab hb hc hconstant
  · have hf : cyclic (component b) = false := by
      cases hx : cyclic (component b) <;> simp_all
    have he : a = b := by
      by_cases heq : a = b
      · exact heq
      · have hstart := hconstant a (Nat.le_refl a) hab
        have hnext := hconstant (a + 1) (by omega) (by omega)
        have hfalse : cyclic (component a) = false := by rw [hstart]; exact hf
        have hne := hacyclic a (by omega) hfalse
        exact False.elim (hne (hstart.trans hnext.symm))
    simp only [componentWeight, hf, Bool.false_eq_true, if_false]
    omega

/-- Restriction preserves the component that selects the child job. -/
theorem cyclic_interval_lifts (family : JobPathFamily J V)
    (component : J → V → C) (cyclic : J → C → Bool) (child : J → C → J)
    (job : J)
    (hlift : ∀ path n, family.valid job path n → 0 < n →
      cyclic job (component job (path 0)) = true →
      (∀ i, i < n → component job (path i) = component job (path 0)) →
      ∃ lifted, family.valid (child job (component job (path 0))) lifted n)
    (path : Nat → V) (n a b : Nat) (hvalid : family.valid job path n)
    (hab : a ≤ b) (hb : b < n)
    (hcyclic : cyclic job (component job (path b)) = true)
    (hconstant : ∀ i, a ≤ i → i ≤ b →
      component job (path i) = component job (path b)) :
    ∃ lifted, family.valid (child job (component job (path b))) lifted (b + 1 - a) := by
  have hsource := family.restrict job path n hvalid a (b + 1 - a) (by omega)
  have hstart := hconstant a (Nat.le_refl a) hab
  have hc : cyclic job (component job ((fun i => path (a + i)) 0)) = true := by
    simpa only [Nat.add_zero, hstart] using hcyclic
  have hsame : ∀ i, i < b + 1 - a →
      component job ((fun j => path (a + j)) i) =
        component job ((fun j => path (a + j)) 0) := by
    intro i hi
    have hhere := hconstant (a + i) (by omega) (by omega)
    simpa only [Nat.add_zero] using hhere.trans hstart.symm
  have h := hlift (fun i => path (a + i)) (b + 1 - a) hsource (by omega) hc hsame
  simpa only [Nat.add_zero, hstart] using h

variable [DecidableEq C]

/-- Bounds compose through component-specific child jobs. Strict decrease
of the natural-number height supplies well-foundedness; no finite enumeration
of jobs or assumption that arbitrary graph paths lift is used. -/
theorem component_hierarchy_path_vertices_le (family : JobPathFamily J V)
    (component : J → V → C) (cyclic : J → C → Bool) (child : J → C → J)
    (height bound : J → Nat) (rank : J → C → Nat)
    (hdecrease : ∀ job c, cyclic job c = true → height (child job c) < height job)
    (hlift : ∀ job path n, family.valid job path n → 0 < n →
      cyclic job (component job (path 0)) = true →
      (∀ i, i < n → component job (path i) = component job (path 0)) →
      ∃ lifted, family.valid (child job (component job (path 0))) lifted n)
    (hacyclic : ∀ job path n, family.valid job path n →
      ∀ i, i + 1 < n → cyclic job (component job (path i)) = false →
      component job (path i) ≠ component job (path (i + 1)))
    (hcertificate : ∀ job path n, family.valid job path n →
      RankCertificate (fun i => component job (path i))
        (jobWeight cyclic child bound job) (rank job) n)
    (hstart : ∀ job path n, family.valid job path n → 0 < n →
      rank job (component job (path 0)) ≤ bound job) :
    ∀ job path n, family.valid job path n → n ≤ bound job := by
  have hmain : ∀ h job, height job = h →
      ∀ path n, family.valid job path n → n ≤ bound job := by
    intro h
    induction h using Nat.strongRecOn with
    | ind h ih =>
      intro job hheight path n hvalid
      by_cases hn : n = 0
      · simp [hn]
      · have hinterval : IntervalBound (fun i => component job (path i))
            (jobWeight cyclic child bound job) n := by
          apply interval_bound_of_component_bounds
            (fun i => component job (path i)) (cyclic job)
            (fun c => bound (child job c)) n
          · intro a b hab hb hc hconstant
            obtain ⟨lifted, hvalidLifted⟩ := cyclic_interval_lifts family component cyclic child job
              (hlift job) path n a b hvalid hab hb hc hconstant
            have hd := hdecrease job (component job (path b)) hc
            exact ih (height (child job (component job (path b)))) (by omega)
              (child job (component job (path b))) rfl lifted (b + 1 - a) hvalidLifted
          · exact hacyclic job path n hvalid
        have hr := path_vertices_le_rank (fun i => component job (path i))
          (jobWeight cyclic child bound job) (rank job) n hinterval
          (hcertificate job path n hvalid)
        exact Nat.le_trans hr (hstart job path n hvalid (by omega))
  intro job path n hvalid
  exact hmain (height job) job rfl path n hvalid

end ComponentHierarchy
