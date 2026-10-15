import AutonomyDefs

namespace ModularAutonomy

set_option maxRecDepth 10000

open Lychrel196 DecimalDigits

/-- Previously proved modulo-99 arithmetic supplies the entire sufficiency
branch, without any size threshold or new computational certificate. -/
theorem eventual_reverse_residue_det_of_dvd99 (M : Nat) (hM : M ∣ 99) :
    EventualReverseResidueDet M := by
  refine ⟨0, ?_⟩
  intro L _ n m d e hn hm heq
  rw [AstraModular.reverse10_mod_of_dvd99 M n d L hM hn,
    AstraModular.reverse10_mod_of_dvd99 M m e L hM hm,
    Nat.mul_mod _ n, Nat.mul_mod _ m, heq]

theorem add_mod_left_cancel (a b c M : Nat)
    (h : (a + b) % M = (a + c) % M) : b % M = c % M := by
  by_cases hM : M = 0
  · subst M
    simpa only [Nat.mod_zero, Nat.add_left_cancel_iff] using h
  · have hm : 0 < M := by omega
    have hb := Nat.mod_lt b hm
    have hc := Nat.mod_lt c hm
    have h1 := Nat.mod_add_mod_eq (a := a) (b := b) (c := M)
    have h2 := Nat.mod_add_mod_eq (a := a) (b := c) (c := M)
    split at h1 <;> split at h2 <;> omega

/-- Equal input residues allow cancellation of the input term in actual
reverse-and-add; eventual determinism is exactly reversal determinism. -/
theorem eventual_step_residue_det_iff_reverse (M : Nat) :
    EventualStepResidueDet M ↔ EventualReverseResidueDet M := by
  constructor
  · rintro ⟨B, hB⟩
    refine ⟨B, ?_⟩
    intro L hL n m d e hn hm hnm
    have hs := hB L hL n m d e hn hm hnm
    change (n + reverse10 n) % M = (m + reverse10 m) % M at hs
    rw [Nat.add_mod n, Nat.add_mod m, hnm] at hs
    have hcancel := add_mod_left_cancel _ _ _ _ hs
    simpa only [Nat.mod_mod] using hcancel
  · rintro ⟨B, hB⟩
    refine ⟨B, ?_⟩
    intro L hL n m d e hn hm hnm
    have hr := hB L hL n m d e hn hm hnm
    change (n + reverse10 n) % M = (m + reverse10 m) % M
    rw [Nat.add_mod n, Nat.add_mod m, hnm, hr]

#print axioms add_mod_left_cancel
#print axioms eventual_reverse_residue_det_of_dvd99
#print axioms eventual_step_residue_det_iff_reverse

end ModularAutonomy
