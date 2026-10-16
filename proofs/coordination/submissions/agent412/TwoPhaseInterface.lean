import TwoPhaseCharge

/-! Agent #412: original-checker interface transport and band-gain residues.
This extends the exterior charge law without assuming any initial mass residue.
No accepting certificate, period exclusion, or all-time seed is asserted. -/
namespace Agent412.TwoPhaseInterface
open Agent109 Agent109.Cert Agent110.Accounting
open Agent110.CertificateBudget Agent112.SmallPeriod Agent412.TwoPhaseCharge

set_option maxHeartbeats 4000000

def tau (s : State) : Int := scaled s.c (s.A.sum : Int)

/-- Phase scaling is by one or two, never by an inverse of six modulo nine. -/
theorem scaled_interface_step (c c' : Nat) (S S' : Int) (j1 j2 : Nat)
    (hc : TwoPhase c) (hp : c' = Agent2Exterior.phase c)
    (hS : (S' + (j1 : Int) * (c' : Int) +
      (j2 : Int) * ((18-c' : Nat) : Int)) % 9 = (2*S) % 9) :
    (scaled c' S' - scaled c S -
      3 * ((if c = 6 then scaled c S else 0) + (j1 : Int) - (j2 : Int))) % 9 = 0 := by
  rcases hc with rfl | rfl
  · simp [Agent2Exterior.phase] at hp
    subst c'
    simp [scaled, phaseWeight] at *
    omega
  · simp [Agent2Exterior.phase] at hp
    subst c'
    simp [scaled, phaseWeight] at *
    omega

theorem local_tau_step (s s' : State) (L L' : Link)
    (hl : LocalOK s s' L L') (hc : TwoPhase s.c) :
    (tau s' - tau s -
      3 * ((if s.c = 6 then tau s else 0) + (L.j1 : Int) - (L.j2 : Int))) % 9 = 0 := by
  have hb : s.c ≤ 18 := by have := hl.1.2.1; omega
  have hp : s'.c = Agent2Exterior.phase s.c := by
    rw [← next_eq_phase _ hb]
    exact hl.2.2.2.2.1.symm
  exact scaled_interface_step s.c s'.c _ _ L.j1 L.j2 hc hp
    (local_interface_sum s s' L L' hl)

theorem local_tau_mod3 (s s' : State) (L L' : Link)
    (hl : LocalOK s s' L L') (hc : TwoPhase s.c) :
    tau s' % 3 = tau s % 3 := by
  have h := local_tau_step s s' L L' hl hc
  omega

theorem prefix_tau_mod3 (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) (n : Nat) (hn : n ≤ cert.P) :
    tau (cert.st (n % cert.P)) % 3 = tau (cert.st 0) % 3 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hi : n < cert.P := by omega
    have hp := ih (by omega)
    have hs := local_tau_mod3 _ _ _ _ (hv.2 n hi)
      (valid_two_phase cert hv h0 n hi)
    simpa only [Nat.mod_eq_of_lt hi] using hs.trans
      (by simpa only [Nat.mod_eq_of_lt hi] using hp)

/-- The residue carried by the initial exterior is preserved through the
entire telescope. The interface and both trimming sides are accounted for. -/
theorem prefix_interface_identity (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) (n : Nat) (hn : n ≤ cert.P) :
    (tau (cert.st (n % cert.P)) - tau (cert.st 0) -
      3 * ((tau (cert.st 0) % 3) * sixPrefix cert n +
        sumPrefix (fun i => ((cert.lk i).j1 : Int) - ((cert.lk i).j2 : Int)) n)) % 9 = 0 := by
  induction n with
  | zero => simp [sixPrefix, sumPrefix]
  | succ n ih =>
    have hi : n < cert.P := by omega
    have ht := ih (by omega)
    have hr := prefix_tau_mod3 cert hv h0 n (by omega)
    have hs := local_tau_step _ _ _ _ (hv.2 n hi)
      (valid_two_phase cert hv h0 n hi)
    simp only [Nat.mod_eq_of_lt hi] at ht hr
    by_cases hc : (cert.st n).c = 6
    · simp only [if_pos hc] at hs
      simp only [sixPrefix, sumPrefix, if_pos hc,
        Int.mul_add, Int.mul_one]
      change (tau (cert.st n) - tau (cert.st 0) -
        3 * ((tau (cert.st 0) % 3) *
          sumPrefix (fun i => if (cert.st i).c = 6 then 1 else 0) n +
          sumPrefix (fun i => ((cert.lk i).j1 : Int) - ((cert.lk i).j2 : Int)) n)) % 9 = 0 at ht
      omega
    · simp only [if_neg hc] at hs
      simp only [sixPrefix, sumPrefix, if_neg hc,
        Int.add_zero, Int.mul_add, Int.mul_zero]
      change (tau (cert.st n) - tau (cert.st 0) -
        3 * ((tau (cert.st 0) % 3) *
          sumPrefix (fun i => if (cert.st i).c = 6 then 1 else 0) n +
          sumPrefix (fun i => ((cert.lk i).j1 : Int) - ((cert.lk i).j2 : Int)) n)) % 9 = 0 at ht
      omega

/-- The original full interface enforces this cyclic trim congruence.
No zero-residue assumption for the initial interface is supplied. -/
theorem valid_interface_trim_law (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) :
    (totalJ1 cert - totalJ2 cert) % 3 =
      (-(tau (cert.st 0) * (cert.P / 2 : Nat))) % 3 := by
  have ht := prefix_interface_identity cert hv h0 cert.P (Nat.le_refl _)
  simp only [Nat.mod_self] at ht
  rw [six_count_half_period cert hv h0, sumPrefix_sub] at ht
  change (tau (cert.st 0) - tau (cert.st 0) -
    3 * ((tau (cert.st 0) % 3) * (cert.P / 2 : Nat) +
      (totalJ1 cert - totalJ2 cert))) % 9 = 0 at ht
  have h : (totalJ1 cert - totalJ2 cert) % 3 =
      (-((tau (cert.st 0) % 3) * (cert.P / 2 : Nat))) % 3 := by omega
  have hm : ((tau (cert.st 0) % 3) * (cert.P / 2 : Nat)) % 3 =
      (tau (cert.st 0) * (cert.P / 2 : Nat)) % 3 := by
    simp only [Int.mul_emod, Int.emod_emod]
  omega

/-- The actual block-length accounting identifies the trim imbalance exactly. -/
theorem trim_difference_eq_negative_twice_inner (cert : Certificate) (hv : Valid cert) :
    totalJ1 cert - totalJ2 cert = -2 * totalH cert := by
  have ha := totalJ1_add_totalJ2 cert hv
  have hb := two_totalK cert hv
  have hc := totalH_eq_totalK_sub_totalJ1 cert hv
  omega

theorem valid_inner_gain_law (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) :
    (2 * totalH cert) % 3 = (tau (cert.st 0) * (cert.P / 2 : Nat)) % 3 := by
  have h := valid_interface_trim_law cert hv h0
  rw [trim_difference_eq_negative_twice_inner cert hv] at h
  omega

theorem valid_outer_gain_law (cert : Certificate) (hv : Valid cert)
    (h0 : TwoPhase (cert.st 0).c) :
    (2 * totalG cert) % 3 =
      ((rho (cert.st 0) - tau (cert.st 0)) * (cert.P / 2 : Nat)) % 3 := by
  have hO := valid_two_phase_charge_law cert hv h0
  have hH := valid_inner_gain_law cert hv h0
  have hGH := totalGam_eq_twice_gains cert hv
  rw [Int.sub_mul]
  omega

/-- Both band-gain residues follow from the unchanged executable checker.
The initial interface/exterior residues remain explicit data, not hypotheses. -/
theorem checked_two_phase_gain_laws (cert : Certificate) (hc : check cert = true)
    (h0 : TwoPhase (cert.st 0).c) :
    (2 * totalH cert) % 3 = (tau (cert.st 0) * (cert.P / 2 : Nat)) % 3 ∧
    (2 * totalG cert) % 3 =
      ((rho (cert.st 0) - tau (cert.st 0)) * (cert.P / 2 : Nat)) % 3 :=
  ⟨valid_inner_gain_law cert (check_sound cert hc) h0,
    valid_outer_gain_law cert (check_sound cert hc) h0⟩

#print axioms scaled_interface_step
#print axioms local_tau_step
#print axioms local_tau_mod3
#print axioms prefix_tau_mod3
#print axioms prefix_interface_identity
#print axioms valid_interface_trim_law
#print axioms trim_difference_eq_negative_twice_inner
#print axioms valid_inner_gain_law
#print axioms valid_outer_gain_law
#print axioms checked_two_phase_gain_laws
end Agent412.TwoPhaseInterface
