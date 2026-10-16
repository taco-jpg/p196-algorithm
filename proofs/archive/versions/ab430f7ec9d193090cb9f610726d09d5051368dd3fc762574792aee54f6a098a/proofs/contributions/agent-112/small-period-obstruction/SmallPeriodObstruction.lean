import CertificateChecked

/-! Agent #112: small-period necessary conditions for the original checker.
No certificate instance or all-time palindrome-avoidance result is supplied. -/
namespace Agent112.SmallPeriod
open Agent109 Agent109.Cert Agent110.Accounting
open Agent110.CertificateBudget

set_option maxHeartbeats 8000000

def TwoPhase (c : Nat) : Prop := c = 6 ∨ c = 12

def twoCode (c : Nat) : Nat := if c = 6 then 0 else 1

theorem two_phase_next (c : Nat) (hc : TwoPhase c) :
    TwoPhase (Agent2Exterior.phase c) := by
  rcases hc with rfl | rfl <;> simp [TwoPhase, Agent2Exterior.phase]

theorem two_code_step (c : Nat) (hc : TwoPhase c) :
    twoCode (Agent2Exterior.phase c) = (twoCode c + 1) % 2 := by
  rcases hc with rfl | rfl <;> decide

theorem valid_two_phase (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) :
    ∀ i, i < cert.P → TwoPhase (cert.st i).c := by
  intro i
  induction i with
  | zero => intro _; exact h0
  | succ i ih =>
    intro hi
    have hl := hv.2 i (by omega)
    have hphase := two_phase_next (cert.st i).c (ih (by omega))
    have hc : (cert.st i).c ≤ 18 := by have := hl.1.2.1; omega
    have hs : tOf (cert.st i).c + tOf (cert.st i).c = (cert.st (i+1)).c := by
      simpa only [Nat.mod_eq_of_lt hi] using hl.2.2.2.2.1
    rw [← next_eq_phase _ hc, hs] at hphase
    exact hphase

theorem parity_telescope (r : Nat → Nat) (n : Nat)
    (h : ∀ i, i < n → r (i+1) % 2 = (r i + 1) % 2) :
    r n % 2 = (r 0 + n) % 2 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have ht := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    omega

theorem valid_two_period_even (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) : cert.P % 2 = 0 := by
  let r := fun i => twoCode (cert.st (i % cert.P)).c
  have ht : r cert.P % 2 = (r 0 + cert.P) % 2 := by
    apply parity_telescope
    intro i hi
    have hl := hv.2 i hi
    have hc : (cert.st i).c ≤ 18 := by have := hl.1.2.1; omega
    have hp : Agent2Exterior.phase (cert.st i).c = (cert.st ((i+1)%cert.P)).c := by
      rw [← next_eq_phase _ hc]
      exact hl.2.2.2.2.1
    have hs := two_code_step (cert.st i).c (valid_two_phase cert hv h0 i hi)
    rw [hp] at hs
    simp only [r, Nat.mod_eq_of_lt hi]
    omega
  have hr : r cert.P = r 0 := by simp [r]
  rw [hr] at ht
  omega

theorem checked_positive_exterior (cert : Certificate) (hc : check cert = true) :
    0 < Agent110.CarryBudget.exterior (cert.st 0) := by
  obtain ⟨H, M, ha⟩ := Agent112.Admissibility.automatic_admissibility cert hc
  have hv := check_sound cert hc
  exact Agent110.CarryBudget.exterior_pos _ (hv.2 0 hv.1).1 ha.2.2.2

/-- All phase classes, without assuming the six-phase restriction. -/
theorem checked_saturated_period_mod8 (cert : Certificate) (hc : check cert = true)
    (hsat : 2 * totalGam cert = (cert.P : Int)) : cert.P % 8 = 0 := by
  have hv := check_sound cert hc
  obtain ⟨path⟩ := Agent110.CertificateSaturation.certificate_closed_prefix_path
    cert hv (checked_positive_exterior cert hc)
  have hcCount := Agent110.CertificateSaturation.path_total_eq_totalGam cert path
  have hnat : 2 * P196.Agent4.Saturation.total
      (fun i => (P196.Agent4.Saturation.advance (path.state i) (path.input i)).2)
      cert.P = cert.P := by omega
  exact P196.Agent4.Saturation.saturated_closed_prefix_period
    path.state path.input cert.P path.valid path.input_le
    (fun i hi => congrArg Prod.fst (path.transition i hi)) path.closed hnat

theorem checked_period_ne_four (cert : Certificate) (hc : check cert = true) :
    cert.P ≠ 4 := by
  intro hp
  have hv := check_sound cert hc
  have hb := Agent110.Consequences.total_carry_budget cert hv (checked_positive_exterior cert hc)
  obtain ⟨k, hk, he⟩ := totalGam_even cert hv
  have hs : 2 * totalGam cert = (cert.P : Int) := by omega
  have hm := checked_saturated_period_mod8 cert hc hs
  omega

/-- Even returned phases split into the existing six-phase class and6/12. -/
theorem valid_phase_class (cert : Certificate) (hv : Valid cert) :
    Agent2Exterior.SixPhase (cert.st 0).c ∨ TwoPhase (cert.st 0).c := by
  have he := Agent110.Phases.valid_phase_even cert hv 0 hv.1
  have hp := (hv.2 0 hv.1).1
  unfold Agent2Exterior.SixPhase TwoPhase Phase at *
  omega

/-- Six actual links in the two-phase class force the overflow sum to vanish
modulo3. No divisibility assumption on the initial exterior charge is used. -/
theorem period_six_overflow_mod3 (cert : Certificate) (hv : Valid cert)
    (hp : cert.P = 6) (htwo : TwoPhase (cert.st 0).c) :
    totalGam cert % 3 = 0 := by
  let Q := fun i => Agent2Exterior.charge (cert.st i).c (cert.st i).B
  have hs (i : Nat) (hi : i < 6) :
      (cert.st ((i+1)%6)).c = Agent2Exterior.phase (cert.st i).c := by
    have hl := hv.2 i (by omega)
    have hb : (cert.st i).c ≤ 18 := by have := hl.1.2.1; omega
    have he := hl.2.2.2.2.1
    rw [next_eq_phase _ hb] at he
    simpa only [hp] using he.symm
  have hQ (i : Nat) (hi : i < 6) :
      Q ((i+1)%6) % 9 =
      (2 * Q i - (gam (cert.st i) : Int) * ((cert.st i).c : Int)) % 9 := by
    have hh := local_charge_step _ _ _ _ (hv.2 i (by omega))
    simpa only [Q, hp] using hh
  have hs0 := hs 0 (by decide)
  have hs1 := hs 1 (by decide)
  have hs2 := hs 2 (by decide)
  have hs3 := hs 3 (by decide)
  have hs4 := hs 4 (by decide)
  have hq0 := hQ 0 (by decide)
  have hq1 := hQ 1 (by decide)
  have hq2 := hQ 2 (by decide)
  have hq3 := hQ 3 (by decide)
  have hq4 := hQ 4 (by decide)
  have hq5 := hQ 5 (by decide)
  simp only [Nat.reduceAdd, Nat.reduceMod] at hs0 hs1 hs2 hs3 hs4 hq0 hq1 hq2 hq3 hq4 hq5
  rcases htwo with hc | hc
  · simp only [hc, Agent2Exterior.phase] at hs0
    simp only [hs0, Agent2Exterior.phase] at hs1
    simp only [hs1, Agent2Exterior.phase] at hs2
    simp only [hs2, Agent2Exterior.phase] at hs3
    simp only [hs3, Agent2Exterior.phase] at hs4
    simp only [hc, hs0, hs1, hs2, hs3, hs4] at hq0 hq1 hq2 hq3 hq4 hq5
    simp only [totalGam, hp, sumPrefix, Int.zero_add]
    omega
  · simp only [hc, Agent2Exterior.phase] at hs0
    simp only [hs0, Agent2Exterior.phase] at hs1
    simp only [hs1, Agent2Exterior.phase] at hs2
    simp only [hs2, Agent2Exterior.phase] at hs3
    simp only [hs3, Agent2Exterior.phase] at hs4
    simp only [hc, hs0, hs1, hs2, hs3, hs4] at hq0 hq1 hq2 hq3 hq4 hq5
    simp only [totalGam, hp, sumPrefix, Int.zero_add]
    omega

/-- A period-six certificate is excluded in both possible phase classes. -/
theorem checked_period_ne_six (cert : Certificate) (hc : check cert = true) :
    cert.P ≠ 6 := by
  intro hp
  have hv := check_sound cert hc
  rcases valid_phase_class cert hv with hphase | hphase
  · have h := Agent110.Checked.six_phase_constraints cert hc hphase
    omega
  · have hm := period_six_overflow_mod3 cert hv hp hphase
    have hb := Agent110.Consequences.total_carry_budget cert hv
      (checked_positive_exterior cert hc)
    obtain ⟨k, hk, he⟩ := totalGam_even cert hv
    omega

theorem checked_period_even (cert : Certificate) (hc : check cert = true) :
    cert.P % 2 = 0 := by
  have hv := check_sound cert hc
  rcases valid_phase_class cert hv with hphase | hphase
  · have h := Agent110.Phases.valid_period_mod6 cert hv hphase
    omega
  · exact valid_two_period_even cert hv hphase

/-- Every accepted certificate in the original format has period at least8.
There is no exterior-length bound or separate admissibility premise. -/
theorem checked_period_at_least_eight (cert : Certificate)
    (hc : check cert = true) : 8 ≤ cert.P := by
  have hb := Agent110.Checked.period_at_least_four cert hc
  have he := checked_period_even cert hc
  have h4 := checked_period_ne_four cert hc
  have h6 := checked_period_ne_six cert hc
  omega

#print axioms two_phase_next
#print axioms two_code_step
#print axioms valid_two_phase
#print axioms parity_telescope
#print axioms valid_two_period_even
#print axioms checked_positive_exterior
#print axioms checked_saturated_period_mod8
#print axioms checked_period_ne_four
#print axioms valid_phase_class
#print axioms period_six_overflow_mod3
#print axioms checked_period_ne_six
#print axioms checked_period_even
#print axioms checked_period_at_least_eight
end Agent112.SmallPeriod
