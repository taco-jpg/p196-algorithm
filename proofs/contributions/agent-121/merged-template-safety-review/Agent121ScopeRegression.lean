import NoPalCompat

/-!
Agent #121: semantic regression checks for the merged template-safety theorem.
These are review witnesses and contract checks, not a new all-time result.
Uses accepted Lychrel196 arithmetic; all finite computations use `decide`.
-/

set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

namespace Agent121.Review

open Agent109

/-- Restate the exact intended finite-time contract, with the original symbols. -/
theorem exact_finite_safety_contract (n c : Nat) (B A C : Word)
    (g h k : Nat) (hc : Phase c) (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hg : 2 * k + 2 ≤ g) (hh : 2 * k + 2 ≤ h)
    (hn : pairWord n = Agent8.template c B A C g h) :
    ∀ i, 1 ≤ i → i ≤ k + 1 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit n i) :=
  Agent109.NoPalCompat.lychrel_template_orbit_safe n c B A C g h k hc hB hA hC hg hh hn

/-- This concrete positive seed realizes a legal phase with both bands two. -/
theorem terminating_seed_template :
    pairWord 99770022 = Agent8.template 11 [] [] [] 2 2 := by decide

theorem terminating_seed_phase : Phase 11 := by decide

/-- Apply the author's theorem, rather than replacing it with direct computation. -/
theorem terminating_seed_certified_first_step :
    ¬ Lychrel196.Palindrome (Lychrel196.orbit 99770022 1) := by
  exact exact_finite_safety_contract 99770022 11 [] [] [] 2 2 0
    terminating_seed_phase (by simp [Bounded]) (by simp [Bounded]) (by simp [Bounded])
    (by decide) (by decide) terminating_seed_template 1 (by decide) (by decide)

/-- Complete short integer trace; no inference from a Python trace is used. -/
theorem terminating_seed_trace :
    Lychrel196.orbit 99770022 0 = 99770022 ∧
    Lychrel196.orbit 99770022 1 = 121777821 ∧
    Lychrel196.orbit 99770022 2 = 250554942 ∧
    Lychrel196.orbit 99770022 3 = 500009994 ∧
    Lychrel196.orbit 99770022 4 = 999909999 := by decide

/-- A qualifying seed can reach a palindrome beyond its guaranteed time interval. -/
theorem terminating_seed_first_hit :
    (∀ i : Fin 4, ¬ Lychrel196.Palindrome (Lychrel196.orbit 99770022 i.val)) ∧
    Lychrel196.Palindrome (Lychrel196.orbit 99770022 4) := by decide

theorem terminating_seed_not_lychrel : ¬ Lychrel196.IsLychrel 99770022 := by
  intro h
  exact h 4 terminating_seed_first_hit.2

/-- Time zero really needs to be excluded from the safety theorem. -/
theorem palindromic_initial_seed :
    Phase 2 ∧ pairWord 11888811 = Agent8.template 2 [] [] [] 2 2 ∧
    Lychrel196.Palindrome 11888811 := by decide

/-- Removing the nonneutral-phase condition admits an immediate palindrome. -/
theorem neutral_phase_counterexample :
    pairWord 99990000 = Agent8.template 9 [] [] [] 2 2 ∧
    Lychrel196.step 99990000 = 99999999 ∧
    Lychrel196.Palindrome (Lychrel196.step 99990000) := by decide

/-- Check the accepted decimal convention at zero and at trailing zeros. -/
theorem normalization_sentinels :
    Lychrel196.reverse10 0 = 0 ∧ Lychrel196.reverse10 100 = 1 ∧
    Lychrel196.step 100 = 101 ∧ pairWord 0 = [] := by decide

end Agent121.Review

#print axioms Agent121.Review.exact_finite_safety_contract
#print axioms Agent121.Review.terminating_seed_template
#print axioms Agent121.Review.terminating_seed_phase
#print axioms Agent121.Review.terminating_seed_certified_first_step
#print axioms Agent121.Review.terminating_seed_trace
#print axioms Agent121.Review.terminating_seed_first_hit
#print axioms Agent121.Review.terminating_seed_not_lychrel
#print axioms Agent121.Review.palindromic_initial_seed
#print axioms Agent121.Review.neutral_phase_counterexample
#print axioms Agent121.Review.normalization_sentinels
