import Agent423.FiniteCertificate
import Lychrel196Research

set_option autoImplicit false

/-!
Agent #423: semantic bridge from executable finite certificates to the
repository's ordinary decimal orbit and its original IsLychrel predicate.
No alternative decimal reversal, width, or palindrome convention is introduced.
The concrete example excludes five explicitly named terminating seeds only.
-/
namespace Agent423.DecimalEnsemble

open Lychrel196 Agent423.FiniteEnsemble Agent423.FiniteCertificate

def safeAt (n t : Nat) : Bool := decide (¬ Palindrome (orbit n t))

theorem safeAt_true_iff (n t : Nat) :
    safeAt n t = true ↔ ¬ Palindrome (orbit n t) := by
  simp [safeAt]

theorem safeAt_false_iff (n t : Nat) :
    safeAt n t = false ↔ Palindrome (orbit n t) := by
  simp [safeAt]

theorem forever_iff_isLychrel (n : Nat) :
    ForeverSafe (fun x t => safeAt x t = true) n ↔ IsLychrel n := by
  constructor
  · intro h t
    exact (safeAt_true_iff n t).mp (h t)
  · intro h t
    exact (safeAt_true_iff n t).mpr (h t)

/-- Soundness of a checked finite failure certificate for actual decimal
orbits. Positivity is not silently assumed, and time zero is included. -/
theorem certificate_excludes_lychrel (K : List Nat) (witness : Nat → Nat)
    (hc : check K safeAt witness = true) :
    ∀ n, n ∈ K → ¬ IsLychrel n := by
  intro n hn hL
  exact check_forbids_alltime K safeAt witness hc
    ⟨n, hn, (forever_iff_isLychrel n).mpr hL⟩

/-- The numeric finite prefix checker agrees with the repository predicate. -/
theorem checked_prefix_iff (n N : Nat) :
    checkPrefix safeAt n N = true ↔
      ∀ t, t ≤ N → ¬ Palindrome (orbit n t) := by
  rw [checkPrefix_iff]
  constructor
  · intro h t ht
    exact (safeAt_true_iff n t).mp (h t ht)
  · intro h t ht
    exact (safeAt_true_iff n t).mpr (h t ht)

/-- Genuine arithmetic specialization of fixed-ensemble extraction. The
universal all-horizons premise is preserved, not supplied by a finite run. -/
theorem fixed_ensemble_all_checks_iff (K : List Nat) :
    (∀ N, checkSurvivor K safeAt N = true) ↔ ∃ n, n ∈ K ∧ IsLychrel n := by
  rw [all_survivor_checks_iff]
  constructor
  · intro h
    obtain ⟨n, hn, hL⟩ := h
    exact ⟨n, hn, (forever_iff_isLychrel n).mp hL⟩
  · intro h
    obtain ⟨n, hn, hL⟩ := h
    exact ⟨n, hn, (forever_iff_isLychrel n).mpr hL⟩

/-- Conditional endpoint in the exact original existence definition. No K
satisfying the premise has been proved for a decimal Lychrel witness here. -/
theorem existence_of_fixed_ensemble_checks (K : List Nat)
    (h : ∀ N, checkSurvivor K safeAt N = true) : DecimalLychrelExistence := by
  obtain ⟨n, _, hn⟩ := (fixed_ensemble_all_checks_iff K).mp h
  exact ⟨n, hn⟩

def sampleSeeds : List Nat := [10, 19, 56, 57, 59]

def sampleWitness (n : Nat) : Nat :=
  if n = 59 then 3 else if n = 19 ∨ n = 57 then 2 else 1

/-- Each finite failure is checked by Lean's kernel, with no native_decide. -/
theorem sample_certificate_passes : check sampleSeeds safeAt sampleWitness = true := by
  decide

theorem sample_max_horizon : maxWitness sampleSeeds sampleWitness = 3 := by decide

/-- Completed certificate-to-actual-decimal-conclusion chain for these five
seeds; no conclusion about another seed, especially 196, follows. -/
theorem sample_seeds_not_lychrel : ∀ n, n ∈ sampleSeeds → ¬ IsLychrel n :=
  certificate_excludes_lychrel sampleSeeds sampleWitness sample_certificate_passes

theorem sample_endpoint_controls :
    checkSurvivor sampleSeeds safeAt 2 = true ∧
    checkSurvivor sampleSeeds safeAt 3 = false := by decide

theorem sample_forgery_rejected : check sampleSeeds safeAt (fun _ => 0) = false := by
  decide

#print axioms safeAt_true_iff
#print axioms safeAt_false_iff
#print axioms forever_iff_isLychrel
#print axioms certificate_excludes_lychrel
#print axioms checked_prefix_iff
#print axioms fixed_ensemble_all_checks_iff
#print axioms existence_of_fixed_ensemble_checks
#print axioms sample_certificate_passes
#print axioms sample_max_horizon
#print axioms sample_seeds_not_lychrel
#print axioms sample_endpoint_controls
#print axioms sample_forgery_rejected

end Agent423.DecimalEnsemble
