import P196.Drafts.Agent108ModularAutonomy.DigitPerturbation

set_option autoImplicit false

/-!
Agent #6. Ordinary decimal reversal on positive predecessor fibers whose
target ends in zero. Reversal is an involution when the input has nonzero
units, and the existing zero-units obstruction supplies that condition
for every member of the complete positive predecessor fiber.
-/

namespace ZeroEndingPredecessorParity

open Lychrel196 DecimalDigits

private theorem canonical_reversed (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hu : n % 10 ≠ 0) :
    Canonical (reverse10 n) (reflected d L) L := by
  refine ⟨hc.1, ?_, ?_, ?_⟩
  · intro i hi
    exact hc.2.1 (L - 1 - i) (by omega)
  · have hzero := ModularAutonomy.canonical_units n L d hc
    have hp : 0 < d 0 := by omega
    simpa only [reflected, Nat.sub_self] using hp
  · rw [← hc.2.2.2, reverse10_value d L hc.2.1 (Or.inr hc.2.2.1)]

/-- Ordinary reversal is an involution precisely on the needed domain:
positive decimal inputs whose units digit is nonzero. -/
theorem reverse10_involutive_of_units_ne_zero (n : Nat)
    (hn : 0 < n) (hu : n % 10 ≠ 0) :
    reverse10 (reverse10 n) = n := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hr := canonical_reversed n d L hc hu
  calc
    reverse10 (reverse10 n) = value (reflected (reflected d L) L) L := by
      rw [← hr.2.2.2]
      exact reverse10_value (reflected d L) L hr.2.1 (Or.inr hr.2.2.1)
    _ = value d L := by
      apply value_congr
      intro i hi
      simp only [reflected]
      have hindex : L - 1 - (L - 1 - i) = i := by omega
      rw [hindex]
    _ = n := hc.2.2.2

/-- Every positive predecessor of a target ending in zero has nonzero units. -/
theorem predecessor_units_ne_zero (Y n : Nat) (hzero : Y % 10 = 0)
    (hn : 0 < n) (hstep : step n = Y) : n % 10 ≠ 0 := by
  intro hu
  apply AstraModular.zero_units_step_nonzero n hn hu
  simpa only [hstep] using hzero

/-- Reversal preserves the complete positive ordinary-integer predecessor
fiber of any target ending in zero, without a source-width restriction. -/
theorem reverse10_preserves_predecessor (Y n : Nat) (hzero : Y % 10 = 0)
    (hn : 0 < n) (hstep : step n = Y) :
    0 < reverse10 n ∧ step (reverse10 n) = Y := by
  have hu := predecessor_units_ne_zero Y n hzero hn hstep
  have hi := reverse10_involutive_of_units_ne_zero n hn hu
  have hp : 0 < reverse10 n := by
    by_cases hz : reverse10 n = 0
    · rw [hz] at hi
      change 0 = n at hi
      omega
    · omega
  refine ⟨hp, ?_⟩
  calc
    step (reverse10 n) = reverse10 n + n := by rw [step, hi]
    _ = step n := by simp only [step, Nat.add_comm]
    _ = Y := hstep

#print axioms reverse10_involutive_of_units_ne_zero
#print axioms predecessor_units_ne_zero
#print axioms reverse10_preserves_predecessor

end ZeroEndingPredecessorParity
