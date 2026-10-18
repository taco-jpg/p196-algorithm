import P196.Drafts.Agent418Agent418.Agent418AllPatternsRealizable

/-! A separate corrected-assumption test: adding the proposed odd-input
balance condition does not make an eight-step reset persistent. The
counterexample realizes a balanced block in actual decimal arithmetic,
returns to the initial three-column state, and leaves the cycle next step.
-/
namespace Agent418.BalancedResetFailure
open Agent418.SaturatedInputAudit Agent418.FiniteDecimalWitness
  Agent418.AllPatternsRealizable

set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

def balancedPattern : Fin 16 := ⟨3, by decide⟩
def balancedSeed : Nat := candidate balancedPattern

theorem balanced_seed_value : balancedSeed = 899550185030 := by rfl

theorem balanced_seed_realizes : Realizes balancedSeed balancedPattern :=
  ⟨all_canonical_widths balancedPattern, all_observations balancedPattern,
    all_endpoints balancedPattern, all_saturated balancedPattern⟩

theorem odd_input_sum_two :
    observedInput balancedSeed 1 + observedInput balancedSeed 3 +
      observedInput balancedSeed 5 + observedInput balancedSeed 7 = 2 := by
  decide +kernel

theorem resets_at_eight :
    prefixOf (orbit balancedSeed 8) 16 = cycleState 0 :=
  all_endpoints balancedPattern

theorem loses_required_control : observedInput balancedSeed 8 = 0 := by
  decide +kernel

theorem exits_at_nine :
    prefixOf (orbit balancedSeed 9) 16 = ⟨17,4,9⟩ ∧
      prefixOf (orbit balancedSeed 9) 16 ≠ cycleState 1 := by
  decide +kernel

theorem ninth_width_is_canonical :
    10^15 ≤ orbit balancedSeed 9 ∧ orbit balancedSeed 9 < 10^16 := by
  decide +kernel

/-- Even the additional balanced-input premise is insufficient for the
first transition after an actual saturated block reset. -/
theorem balanced_reset_does_not_force_next_edge :
    ¬ (∀ (n : Nat) (p : Fin 16), Realizes n p →
      observedInput n 1 + observedInput n 3 +
        observedInput n 5 + observedInput n 7 = 2 →
      prefixOf (orbit n 9) 16 = cycleState 1) := by
  intro h
  exact exits_at_nine.2 (h balancedSeed balancedPattern balanced_seed_realizes
    odd_input_sum_two)

#print axioms balanced_seed_value
#print axioms balanced_seed_realizes
#print axioms odd_input_sum_two
#print axioms resets_at_eight
#print axioms loses_required_control
#print axioms exits_at_nine
#print axioms ninth_width_is_canonical
#print axioms balanced_reset_does_not_force_next_edge
end Agent418.BalancedResetFailure
