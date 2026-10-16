import LeadingWitness

/-!
Agent #112 / 2026-10-16: precise unit-digit image of an ordinary
reverse-and-add map on an arbitrarily narrow decimal-adic cylinder.

STATUS: UNCOMPILED WIP. This exact source has NOT been checked with Lean.
Do not import it into an accepted build or describe it as LEAN-CHECKED
without a clean Lean 4.19.0 build and #print axioms audit.

Intended original-layout dependencies:
  Lychrel196Research, astra_lean_modular, AutonomyDefs, LeadingWitness.

The statement quantifies over ordinary positive natural integers, not
abstract two-sided words or a completed 10-adic integer type.
-/

namespace Agent112.CylinderImage

open Lychrel196 DecimalDigits

/-- The residue `r` occurs as a step's units digit among the positive
ordinary integers in the `a` cylinder modulo `10^k`. -/
def Occurs (k a r : Nat) : Prop :=
  ∃ m : Nat, 0 < m ∧ m % (10 ^ k) = a ∧ step m % 10 = r

private theorem ten_dvd_pow (k : Nat) (hk : 0 < k) : 10 ∣ 10 ^ k := by
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : k ≠ 0)
  exact ⟨10 ^ j, by simp [Nat.pow_succ, Nat.mul_comm]⟩

/-- Each choice of nonzero leading decimal digit gives a concrete ordinary
integer witness, including cylinders whose K-digit suffix begins with zero. -/
theorem occurs_for_leading_digit (k a c : Nat)
    (hk : 0 < k) (ha : a < 10 ^ k)
    (hc1 : 1 ≤ c) (hc9 : c ≤ 9) :
    Occurs k a ((a + c) % 10) := by
  let P : Nat := 10 ^ k
  let m : Nat := c * P + a
  have hp : 0 < P := by dsimp [P]; exact Nat.pow_pos (by decide)
  have halo : a < P := by simpa only [P] using ha
  have hmlo : P ≤ m := by
    have h := Nat.mul_le_mul_right P hc1
    dsimp [m]
    omega
  have hbound : m < (c + 1) * P := by
    dsimp [m]
    simp only [Nat.add_mul, Nat.one_mul]
    omega
  have hbound2 : (c + 1) * P ≤ 10 * P :=
    Nat.mul_le_mul_right P (by omega)
  have hmhi : m < 10 ^ (k + 1) := by
    calc
      m < (c + 1) * P := hbound
      _ ≤ 10 * P := hbound2
      _ = 10 ^ (k + 1) := by simp [P, Nat.pow_succ, Nat.mul_comm]
  obtain ⟨d, hd⟩ := ModularAutonomy.canonical_of_pow_bounds m (k + 1)
    (by omega) (by simpa only [Nat.add_sub_cancel, P] using hmlo) hmhi
  have hlead : d k = c :=
    ModularAutonomy.canonical_lead_of_interval m k c d hd
      (by dsimp [m, P]; omega)
      (by simpa only [P] using hbound)
  have hr : reverse10 m % 10 = c := by
    have h := AstraModular.reverse10_mod10 m d (k + 1) hd
    simpa only [Nat.add_sub_cancel, hlead] using h
  have hres : m % (10 ^ k) = a := by
    dsimp [m, P]
    simp [Nat.add_mod, Nat.mul_mod, Nat.mod_eq_of_lt ha]
  have hunit : m % 10 = a % 10 := by
    have h := congrArg (fun v : Nat => v % 10) hres
    simpa only [Nat.mod_mod_of_dvd _ (ten_dvd_pow k hk)] using h
  have hstep : step m % 10 = (a + c) % 10 := by
    change (m + reverse10 m) % 10 = (a + c) % 10
    calc
      (m + reverse10 m) % 10
          = (m % 10 + reverse10 m % 10) % 10 := Nat.add_mod _ _ _
      _ = (a % 10 + c % 10) % 10 := by rw [hunit, hr]
      _ = (a + c) % 10 := by
        simpa only [Nat.mod_eq_of_lt (show c < 10 by omega)] using
          (Nat.add_mod a c 10).symm
  refine ⟨m, ?_, hres, hstep⟩
  omega

/-- Necessity: the leading digit of every positive decimal input is one
of 1..9; it becomes the units digit of its ordinary reversal. -/
theorem any_occurrence_has_leading_digit (k a m : Nat)
    (hk : 0 < k) (hm : 0 < m) (hres : m % (10 ^ k) = a) :
    ∃ c : Nat, 1 ≤ c ∧ c ≤ 9 ∧ step m % 10 = (a + c) % 10 := by
  obtain ⟨d, L, hd⟩ := canonical_exists m hm
  let c : Nat := d (L - 1)
  have hc1 : 1 ≤ c := by simpa only [c] using hd.2.2.1
  have hc9 : c ≤ 9 := hd.2.1 (L - 1) (by have hL := hd.1; omega)
  have hr : reverse10 m % 10 = c := by
    simpa only [c] using AstraModular.reverse10_mod10 m d L hd
  have hunit : m % 10 = a % 10 := by
    have h := congrArg (fun v : Nat => v % 10) hres
    simpa only [Nat.mod_mod_of_dvd _ (ten_dvd_pow k hk)] using h
  refine ⟨c, hc1, hc9, ?_⟩
  change (m + reverse10 m) % 10 = (a + c) % 10
  calc
    (m + reverse10 m) % 10
        = (m % 10 + reverse10 m % 10) % 10 := Nat.add_mod _ _ _
    _ = (a % 10 + c % 10) % 10 := by rw [hunit, hr]
    _ = (a + c) % 10 := by
      simpa only [Nat.mod_eq_of_lt (show c < 10 by omega)] using
        (Nat.add_mod a c 10).symm

/-- Exact nine-element image theorem. In particular, the output residue
`a % 10` never occurs in this cylinder for `k >= 1`. -/
theorem occurs_iff_nine_residues (k a r : Nat)
    (hk : 0 < k) (ha : a < 10 ^ k) :
    Occurs k a r ↔ ∃ c : Nat, 1 ≤ c ∧ c ≤ 9 ∧ r = (a + c) % 10 := by
  constructor
  · rintro ⟨m, hm, hres, hstep⟩
    obtain ⟨c, hc1, hc9, hformula⟩ :=
      any_occurrence_has_leading_digit k a m hk hm hres
    exact ⟨c, hc1, hc9, hstep.symm.trans hformula⟩
  · rintro ⟨c, hc1, hc9, rfl⟩
    exact occurs_for_leading_digit k a c hk ha hc1 hc9

/-- A whole congruence cylinder omits its own units residue after one step. -/
theorem source_units_excluded (k a : Nat)
    (hk : 0 < k) (ha : a < 10 ^ k) :
    ¬ Occurs k a (a % 10) := by
  intro h
  obtain ⟨c, hc1, hc9, heq⟩ := (occurs_iff_nine_residues k a (a % 10) hk ha).mp h
  omega

#print axioms occurs_for_leading_digit
#print axioms any_occurrence_has_leading_digit
#print axioms occurs_iff_nine_residues
#print axioms source_units_excluded

end Agent112.CylinderImage
