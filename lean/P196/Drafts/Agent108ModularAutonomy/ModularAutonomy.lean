import P196.Drafts.Agent108ModularAutonomy.AutonomyBasic
import P196.Drafts.Agent108ModularAutonomy.Necessity

/-!
Complete classification for actual finite decimal integers. The eventual
condition still quantifies over every sufficiently large exact width.
-/
namespace ModularAutonomy

open Lychrel196 DecimalDigits

theorem eventual_reverse_residue_determinism_iff (M : Nat) (hM : 0 < M) :
    EventualReverseResidueDet M ↔ M ∣ 99 := by
  exact ⟨eventual_reverse_residue_determinism_necessity M hM,
    eventual_reverse_residue_det_of_dvd99 M⟩

theorem eventual_step_residue_determinism_iff (M : Nat) (hM : 0 < M) :
    EventualStepResidueDet M ↔ M ∣ 99 := by
  rw [eventual_step_residue_det_iff_reverse,
    eventual_reverse_residue_determinism_iff M hM]

/-- Every excluded modulus has genuine same-width same-residue witnesses
beyond any requested width, even for the actual reverse-and-add map. -/
theorem arbitrarily_wide_step_counterexamples (M B : Nat) (hM : 0 < M)
    (hbad : ¬ M ∣ 99) :
    ∃ L n m, ∃ d e : Nat → Nat, B ≤ L ∧
      Canonical n d L ∧ Canonical m e L ∧ n % M = m % M ∧
      step n % M ≠ step m % M := by
  classical
  apply Classical.byContradiction
  intro hnone
  apply hbad
  apply (eventual_step_residue_determinism_iff M hM).mp
  refine ⟨B, ?_⟩
  intro L hL n m d e hn hm heq
  apply Classical.byContradiction
  intro hne
  exact hnone ⟨L, n, m, d, e, hL, hn, hm, heq, hne⟩

#print axioms eventual_reverse_residue_determinism_iff
#print axioms eventual_step_residue_determinism_iff
#print axioms arbitrarily_wide_step_counterexamples

end ModularAutonomy
