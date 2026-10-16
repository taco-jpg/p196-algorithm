import Agent423.FiniteEnsemble

set_option autoImplicit false

/-!
Agent #423: executable finite-obstruction certificates and inclusive prefix
checkers. These operate on explicit finite lists and Boolean safety predicates.
They do not silently identify an abstract predicate with decimal reverse-add.
-/
namespace Agent423.FiniteCertificate

open Agent423.FiniteEnsemble
universe u
variable {α : Type u}

def maxWitness : List α → (α → Nat) → Nat
  | [], _ => 0
  | a :: K, witness => max (witness a) (maxWitness K witness)

def check (K : List α) (safeAt : α → Nat → Bool) (witness : α → Nat) : Bool :=
  K.all (fun x => !(safeAt x (witness x)))

def checkPrefix (safeAt : α → Nat → Bool) (x : α) (N : Nat) : Bool :=
  (List.range (N + 1)).all (safeAt x)

def checkSurvivor (K : List α) (safeAt : α → Nat → Bool) (N : Nat) : Bool :=
  K.any (fun x => checkPrefix safeAt x N)

theorem witness_le_max (K : List α) (witness : α → Nat) (x : α)
    (hx : x ∈ K) : witness x ≤ maxWitness K witness := by
  induction K with
  | nil => simp at hx
  | cons a K ih =>
      rcases List.mem_cons.mp hx with hxa | hxK
      · subst x
        exact Nat.le_max_left _ _
      · exact Nat.le_trans (ih hxK) (Nat.le_max_right _ _)

theorem check_iff (K : List α) (safeAt : α → Nat → Bool) (witness : α → Nat) :
    check K safeAt witness = true ↔
      ∀ x, x ∈ K → safeAt x (witness x) = false := by
  rw [check, List.all_eq_true]
  constructor
  · intro h x hx
    have hh := h x hx
    cases hs : safeAt x (witness x) <;> simp_all
  · intro h x hx
    simp [h x hx]

/-- Every declared failure time is checked; no external computation is trusted. -/
theorem check_forbids_prefix (K : List α) (safeAt : α → Nat → Bool)
    (witness : α → Nat) (hc : check K safeAt witness = true) :
    ∀ x, x ∈ K → ¬ PrefixSafe (fun x t => safeAt x t = true)
      x (maxWitness K witness) := by
  intro x hx hp
  have hf := (check_iff K safeAt witness).mp hc x hx
  have ht := hp (witness x) (witness_le_max K witness x hx)
  simp [hf] at ht

theorem check_forbids_alltime (K : List α) (safeAt : α → Nat → Bool)
    (witness : α → Nat) (hc : check K safeAt witness = true) :
    ¬ ∃ x, x ∈ K ∧ ForeverSafe (fun x t => safeAt x t = true) x := by
  intro h
  obtain ⟨x, hx, hf⟩ := h
  exact check_forbids_prefix K safeAt witness hc x hx
    (foreverSafe_prefix hf (maxWitness K witness))

/-- Completeness only asserts existence of a certificate when every candidate
has a finite failure. It gives no effective search bound. -/
theorem certificate_exists (K : List α) (safeAt : α → Nat → Bool)
    (hfail : ∀ x, x ∈ K → ∃ t, safeAt x t = false) :
    ∃ witness, check K safeAt witness = true := by
  classical
  let witness : α → Nat := fun x =>
    if hx : x ∈ K then Classical.choose (hfail x hx) else 0
  refine ⟨witness, (check_iff K safeAt witness).mpr ?_⟩
  intro x hx
  have hspec := Classical.choose_spec (hfail x hx)
  simpa [witness, hx] using hspec

theorem certificate_iff_no_alltime (K : List α) (safeAt : α → Nat → Bool) :
    (∃ witness, check K safeAt witness = true) ↔
      ¬ ∃ x, x ∈ K ∧ ForeverSafe (fun x t => safeAt x t = true) x := by
  constructor
  · intro h
    obtain ⟨witness, hc⟩ := h
    exact check_forbids_alltime K safeAt witness hc
  · intro hn
    apply certificate_exists K safeAt
    intro x hx
    have hnf : ¬ ForeverSafe (fun x t => safeAt x t = true) x := by
      intro hf
      exact hn ⟨x, hx, hf⟩
    obtain ⟨t, ht⟩ := (not_forever_iff_exists_failure
      (fun x t => safeAt x t = true) x).mp hnf
    refine ⟨t, ?_⟩
    cases hs : safeAt x t <;> simp_all

/-- A semantic adapter must prove this reflection premise for its actual
model. The premise is not automatically discharged by the Boolean checker. -/
theorem check_sound_for_model (K : List α) (safeAt : α → Nat → Bool)
    (Safe : α → Nat → Prop) (witness : α → Nat)
    (reflect : ∀ x, x ∈ K → ∀ t, safeAt x t = false → ¬ Safe x t)
    (hc : check K safeAt witness = true) :
    ¬ ∃ x, x ∈ K ∧ ForeverSafe Safe x := by
  intro h
  obtain ⟨x, hx, hf⟩ := h
  exact reflect x hx (witness x) ((check_iff K safeAt witness).mp hc x hx)
    (hf (witness x))

/-- The finite checker includes both time zero and the endpoint N. -/
theorem checkPrefix_iff (safeAt : α → Nat → Bool) (x : α) (N : Nat) :
    checkPrefix safeAt x N = true ↔
      PrefixSafe (fun x t => safeAt x t = true) x N := by
  rw [checkPrefix, List.all_eq_true]
  constructor
  · intro h t ht
    exact h t (List.mem_range.mpr (Nat.lt_succ_of_le ht))
  · intro h t ht
    exact h t (Nat.le_of_lt_succ (List.mem_range.mp ht))

theorem checkSurvivor_iff (K : List α) (safeAt : α → Nat → Bool) (N : Nat) :
    checkSurvivor K safeAt N = true ↔
      ∃ x, x ∈ K ∧ PrefixSafe (fun x t => safeAt x t = true) x N := by
  rw [checkSurvivor, List.any_eq_true]
  constructor
  · intro h
    obtain ⟨x, hx, hp⟩ := h
    exact ⟨x, hx, (checkPrefix_iff safeAt x N).mp hp⟩
  · intro h
    obtain ⟨x, hx, hp⟩ := h
    exact ⟨x, hx, (checkPrefix_iff safeAt x N).mpr hp⟩

/-- The all-horizons premise remains a genuine infinite obligation. -/
theorem all_survivor_checks_iff (K : List α) (safeAt : α → Nat → Bool) :
    (∀ N, checkSurvivor K safeAt N = true) ↔
      ∃ x, x ∈ K ∧ ForeverSafe (fun x t => safeAt x t = true) x := by
  constructor
  · intro h
    apply finite_uniform_extraction K (fun x t => safeAt x t = true)
    intro N
    exact (checkSurvivor_iff K safeAt N).mp (h N)
  · intro h N
    obtain ⟨x, hx, hf⟩ := h
    exact (checkSurvivor_iff K safeAt N).mpr
      ⟨x, hx, foreverSafe_prefix hf N⟩

/- Kernel-reduced regression instances. These are countdown predicates,
not decimal orbits; they test exact endpoints, forgery rejection, and emptiness. -/
def countdown (x t : Nat) : Bool := decide (t < x)

theorem countdown_certificate_passes :
    check [2, 3, 5] countdown (fun x => x) = true := by decide

theorem countdown_horizon : maxWitness [2, 3, 5] (fun x => x) = 5 := by decide

theorem countdown_no_alltime :
    ¬ ∃ x, x ∈ [2, 3, 5] ∧ ForeverSafe (fun x t => countdown x t = true) x :=
  check_forbids_alltime [2, 3, 5] countdown (fun x => x) countdown_certificate_passes

theorem forged_countdown_certificate_rejected :
    check [2, 3, 5] countdown (fun _ => 0) = false := by decide

theorem countdown_endpoint_controls :
    checkSurvivor [2, 3, 5] countdown 4 = true ∧
    checkSurvivor [2, 3, 5] countdown 5 = false := by decide

theorem empty_ensemble_controls (safeAt : α → Nat → Bool) (witness : α → Nat)
    (N : Nat) :
    check [] safeAt witness = true ∧ checkSurvivor [] safeAt N = false := by
  exact ⟨rfl, rfl⟩

#print axioms witness_le_max
#print axioms check_iff
#print axioms check_forbids_prefix
#print axioms check_forbids_alltime
#print axioms certificate_exists
#print axioms certificate_iff_no_alltime
#print axioms check_sound_for_model
#print axioms checkPrefix_iff
#print axioms checkSurvivor_iff
#print axioms all_survivor_checks_iff
#print axioms countdown_certificate_passes
#print axioms countdown_horizon
#print axioms countdown_no_alltime
#print axioms forged_countdown_certificate_rejected
#print axioms countdown_endpoint_controls
#print axioms empty_ensemble_controls

end Agent423.FiniteCertificate
