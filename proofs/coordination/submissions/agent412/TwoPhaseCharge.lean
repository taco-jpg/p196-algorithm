import CertificateCharge
import CertificateAccounting
import SmallPeriodObstruction

/-! Agent #412: charge transport without an unjustified divisibility premise.
The unchanged Agent109 checker supplies every local arithmetic transition.
The initial phase-scaled charge residue is retained, not silently set to zero.
No accepting certificate or infinite decimal orbit is asserted here. -/
namespace Agent412.TwoPhaseCharge
open Agent109 Agent109.Cert Agent110.Accounting
open Agent110.CertificateBudget Agent112.SmallPeriod

set_option maxHeartbeats 4000000

def phaseWeight (c : Nat) : Int := if c = 6 then 1 else 2

def scaled (c : Nat) (Q : Int) : Int := phaseWeight c * Q

def rho (s : State) : Int := scaled s.c (Agent2Exterior.charge s.c s.B)

/-- A local identity valid for arbitrary signed charges and carry values.
The factor three is exact: division by a nonunit modulo nine is not used. -/
theorem scaled_step (c c' : Nat) (Q Q' g : Int)
    (hc : TwoPhase c) (hp : c' = Agent2Exterior.phase c)
    (hQ : Q' % 9 = (2 * Q - g * (c : Int)) % 9) :
    (scaled c' Q' - scaled c Q -
      3 * ((if c = 6 then scaled c Q else 0) - g)) % 9 = 0 := by
  rcases hc with rfl | rfl
  · simp [Agent2Exterior.phase] at hp
    subst c'
    simp [scaled, phaseWeight] at *
    omega
  · simp [Agent2Exterior.phase] at hp
    subst c'
    simp [scaled, phaseWeight] at *
    omega

theorem local_rho_step (s s' : State) (L L' : Link)
    (hl : LocalOK s s' L L') (hc : TwoPhase s.c) :
    (rho s' - rho s -
      3 * ((if s.c = 6 then rho s else 0) - (gam s : Int))) % 9 = 0 := by
  have hb : s.c ≤ 18 := by have := hl.1.2.1; omega
  have hp : s'.c = Agent2Exterior.phase s.c := by
    rw [← next_eq_phase _ hb]
    exact hl.2.2.2.2.1.symm
  exact scaled_step s.c s'.c _ _ _ hc hp (local_charge_step s s' L L' hl)

theorem local_rho_mod3 (s s' : State) (L L' : Link)
    (hl : LocalOK s s' L L') (hc : TwoPhase s.c) :
    rho s' % 3 = rho s % 3 := by
  have h := local_rho_step s s' L L' hl hc
  omega

/-- The count is an exact signed finite sum, not a guessed half-period. -/
def sixPrefix (cert : Certificate) (n : Nat) : Int :=
  sumPrefix (fun i => if (cert.st i).c = 6 then 1 else 0) n

theorem prefix_rho_mod3 (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) (n : Nat) (hn : n ≤ cert.P) :
    rho (cert.st (n % cert.P)) % 3 = rho (cert.st 0) % 3 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hi : n < cert.P := by omega
    have hp := ih (by omega)
    have hs := local_rho_mod3 _ _ _ _ (hv.2 n hi)
      (valid_two_phase cert hv h0 n hi)
    simpa only [Nat.mod_eq_of_lt hi] using hs.trans
      (by simpa only [Nat.mod_eq_of_lt hi] using hp)

/-- The residue carried by the initial exterior is preserved through the
entire telescope. No division by a phase coefficient modulo nine occurs. -/
theorem prefix_charge_identity (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) (n : Nat) (hn : n ≤ cert.P) :
    (rho (cert.st (n % cert.P)) - rho (cert.st 0) -
      3 * ((rho (cert.st 0) % 3) * sixPrefix cert n -
        sumPrefix (fun i => (gam (cert.st i) : Int)) n)) % 9 = 0 := by
  induction n with
  | zero => simp [sixPrefix, sumPrefix]
  | succ n ih =>
    have hi : n < cert.P := by omega
    have ht := ih (by omega)
    have hr := prefix_rho_mod3 cert hv h0 n (by omega)
    have hs := local_rho_step _ _ _ _ (hv.2 n hi)
      (valid_two_phase cert hv h0 n hi)
    simp only [Nat.mod_eq_of_lt hi] at ht hr
    by_cases hc : (cert.st n).c = 6
    · simp only [if_pos hc] at hs
      simp only [sixPrefix, sumPrefix, if_pos hc,
        Int.mul_add, Int.mul_one]
      change (rho (cert.st n) - rho (cert.st 0) -
        3 * ((rho (cert.st 0) % 3) *
          sumPrefix (fun i => if (cert.st i).c = 6 then 1 else 0) n -
          sumPrefix (fun i => (gam (cert.st i) : Int)) n)) % 9 = 0 at ht
      omega
    · simp only [if_neg hc] at hs
      simp only [sixPrefix, sumPrefix, if_neg hc,
        Int.add_zero, Int.mul_add, Int.mul_zero]
      change (rho (cert.st n) - rho (cert.st 0) -
        3 * ((rho (cert.st 0) % 3) *
          sumPrefix (fun i => if (cert.st i).c = 6 then 1 else 0) n -
          sumPrefix (fun i => (gam (cert.st i) : Int)) n)) % 9 = 0 at ht
      omega

/-- The number of phase6 states is forced by the actual phase transitions. -/
theorem six_count_exact (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) :
    2 * sixPrefix cert cert.P = (cert.P : Int) := by
  let f : Nat → Int := fun i => if (cert.st i).c = 6 then 1 else 0
  have hz := sumPrefix_cyclic_difference f cert.P
  rw [sumPrefix_sub] at hz
  have hl : ∀ i, i < cert.P → f ((i+1)%cert.P) + f i = 1 := by
    intro i hi
    have h := hv.2 i hi
    have hb : (cert.st i).c ≤ 18 := by have := h.1.2.1; omega
    have hp : (cert.st ((i+1)%cert.P)).c =
        Agent2Exterior.phase (cert.st i).c := by
      rw [← next_eq_phase _ hb]
      exact h.2.2.2.2.1.symm
    rcases valid_two_phase cert hv h0 i hi with hc | hc
    · simp [f, hp, hc, Agent2Exterior.phase]
    · simp [f, hp, hc, Agent2Exterior.phase]
  have he := sumPrefix_congr cert.P hl
  rw [sumPrefix_add, sumPrefix_one] at he
  change 2 * sumPrefix f cert.P = (cert.P : Int)
  omega

theorem six_count_half_period (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) :
    sixPrefix cert cert.P = (cert.P / 2 : Nat) := by
  have h := six_count_exact cert hv h0
  have he := valid_two_period_even cert hv h0
  omega

/-- Exact two-phase overflow congruence from the original full checker.
The initial scaled charge remains visible and may be nonzero modulo3. -/
theorem valid_two_phase_charge_law (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) :
    totalGam cert % 3 =
      (rho (cert.st 0) * (cert.P / 2 : Nat)) % 3 := by
  have ht := prefix_charge_identity cert hv h0 cert.P (Nat.le_refl _)
  simp only [Nat.mod_self] at ht
  rw [six_count_half_period cert hv h0] at ht
  change (rho (cert.st 0) - rho (cert.st 0) -
    3 * ((rho (cert.st 0) % 3) * (cert.P / 2 : Nat) - totalGam cert)) % 9 = 0 at ht
  have h : totalGam cert % 3 =
      ((rho (cert.st 0) % 3) * (cert.P / 2 : Nat)) % 3 := by omega
  simpa only [Int.mul_emod, Int.emod_emod] using h

theorem checked_two_phase_charge_law (cert : Certificate) (hc : check cert = true)
    (h0 : TwoPhase (cert.st 0).c) :
    totalGam cert % 3 =
      (rho (cert.st 0) * (cert.P / 2 : Nat)) % 3 :=
  valid_two_phase_charge_law cert (check_sound cert hc) h0

#print axioms scaled_step
#print axioms local_rho_step
#print axioms local_rho_mod3
#print axioms prefix_rho_mod3
#print axioms prefix_charge_identity
#print axioms six_count_exact
#print axioms six_count_half_period
#print axioms valid_two_phase_charge_law
#print axioms checked_two_phase_charge_law
end Agent412.TwoPhaseCharge
