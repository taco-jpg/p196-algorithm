import P196.Agent6NormalizedCarryAccounting.CertificateCarryAccounting

/-!
Exact controls for the normalized-carry accounting interface.

All examples below are original `State` values with empty interior words.
They do not assert that any return certificate is accepted. The two negative
controls separate carry drift under stripping from the loss of information
when an unbounded carry is replaced by its nonzero indicator.
-/

namespace Agent6.CarryControls

open Agent109 Agent109.Cert P196.Agent7.Finite
open Agent116.CertificateExterior Agent6.ExteriorCoordinates

/-- An original row used only to evaluate its exterior carry. -/
def controlState (c : Nat) (B : List Nat) : State :=
  { c := c, B := B, A := [], C := [] }

/-- Above the phase bound, stripping can change the carry while preserving
both nonzero indicators. -/
theorem phase19_carry_drift :
    stripSuffix 19 [19] = [] ∧
      gam (controlState 19 [19]) = 2 ∧
      overflow 19 [19] = 2 ∧
      overflow 19 (stripSuffix 19 [19]) = 1 ∧
      overflowBit { c := 19, B := [19] } = 1 ∧
      overflowBit (stateOuter (controlState 19 [19])) = 1 := by
  decide +kernel

/-- A permitted phase does not make an unbounded numerical carry a bit. -/
theorem phase2_unbounded_indicator :
    Phase 2 ∧ ¬ Bounded [20] ∧
      (stateOuter (controlState 2 [20])).B = [20] ∧
      gam (controlState 2 [20]) = 2 ∧
      overflow 2 [20] = 2 ∧
      overflowBit (stateOuter (controlState 2 [20])) = 1 := by
  refine ⟨by decide +kernel, ?_, by decide +kernel⟩
  intro hB
  have h := hB 20 (by decide +kernel)
  omega

/-- Removing the last phase letter preserves the incoming carry one,
including when the resulting exterior word is empty. -/
theorem phase18_empty_boundary :
    Bounded [18] ∧
      (stateOuter (controlState 18 [18])).B = [] ∧
      gam (controlState 18 [18]) = 1 ∧
      overflow 18 (stripSuffix 18 [18]) = 1 ∧
      overflowBit (stateOuter (controlState 18 [18])) = 1 := by
  refine ⟨?_, by decide +kernel⟩
  intro x hx
  simp only [List.mem_singleton] at hx
  omega

/-- Neutral and zero phases both retain zero carry after complete stripping. -/
theorem neutral_and_zero_boundaries :
    (stateOuter (controlState 9 [9])).B = [] ∧
      gam (controlState 9 [9]) = 0 ∧
      overflowBit (stateOuter (controlState 9 [9])) = 0 ∧
      (stateOuter (controlState 0 [0])).B = [] ∧
      gam (controlState 0 [0]) = 0 ∧
      overflowBit (stateOuter (controlState 0 [0])) = 0 := by
  decide +kernel

/-- A bounded word still gives the expected carry at a phase above eighteen;
no letter is removed in this example. -/
theorem bounded_phase19_boundary :
    Bounded [18] ∧
      (stateOuter (controlState 19 [18])).B = [18] ∧
      gam (controlState 19 [18]) = 1 ∧
      overflow 19 (stripSuffix 19 [18]) = 1 ∧
      overflowBit (stateOuter (controlState 19 [18])) = 1 := by
  refine ⟨?_, by decide +kernel⟩
  intro x hx
  simp only [List.mem_singleton] at hx
  omega

/-- Carry invariance cannot be asserted for all natural phases and words. -/
theorem unrestricted_strip_carry_invariance_false :
    ¬ (∀ (c : Nat) (B : List Nat),
      overflow c (stripSuffix c B) = overflow c B) := by
  intro h
  rcases phase19_carry_drift with ⟨_, _, hraw, htrim, _, _⟩
  have heq := h 19 [19]
  rw [htrim, hraw] at heq
  omega

/-- The indicator/carry identity is false without coefficient bounds,
even if the original permitted-phase condition is retained. -/
theorem indicator_eq_gam_without_bounded_false :
    (¬ (∀ s : State, overflowBit (stateOuter s) = gam s)) ∧
      (¬ (∀ s : State, Phase s.c →
        overflowBit (stateOuter s) = gam s)) := by
  have hphase : ¬ (∀ s : State, Phase s.c →
      overflowBit (stateOuter s) = gam s) := by
    intro h
    rcases phase2_unbounded_indicator with ⟨hc, _, _, hgam, _, hbit⟩
    have heq := h (controlState 2 [20]) hc
    rw [hbit, hgam] at heq
    omega
  exact ⟨fun h => hphase (fun s _ => h s), hphase⟩

end Agent6.CarryControls

#print axioms Agent6.CarryControls.phase19_carry_drift
#print axioms Agent6.CarryControls.phase2_unbounded_indicator
#print axioms Agent6.CarryControls.phase18_empty_boundary
#print axioms Agent6.CarryControls.neutral_and_zero_boundaries
#print axioms Agent6.CarryControls.bounded_phase19_boundary
#print axioms Agent6.CarryControls.unrestricted_strip_carry_invariance_false
#print axioms Agent6.CarryControls.indicator_eq_gam_without_bounded_false
