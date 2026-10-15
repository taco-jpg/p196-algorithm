import ReturnCertificate
import ExteriorCharge

/-! Charge constraints for actual Agent109 return certificates.  No maximal
trimming, realizability, or chosen carry sequence is assumed. -/

namespace Agent110.CertificateBudget

open Agent109 Agent109.Cert

theorem norm_eq_normalize (w : Word) (e : Nat) :
    norm w e = Agent2Exterior.normalize w e := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [norm, Agent2Exterior.normalize, ih]

theorem kOf_eq_div (c : Nat) (hc : c ≤ 18) : kOf c = c / 10 := by
  unfold kOf
  split <;> omega

theorem next_eq_phase (c : Nat) (hc : c ≤ 18) :
    tOf c + tOf c = Agent2Exterior.phase c := by
  simp only [tOf, kOf_eq_div c hc, Agent2Exterior.phase]
  omega

theorem gam_eq_overflow (s : State) (hc : s.c ≤ 18) :
    gam s = Agent2Exterior.overflow s.c s.B := by
  simp [gam, data, Agent2Exterior.overflow, norm_eq_normalize, kOf_eq_div s.c hc]

theorem Br_eq_rawExterior (c : Nat) (B A C : Word) (hc : c ≤ 18) :
    Br c B A C = Agent2Exterior.rawExterior c B := by
  simp only [Br, data, u0, tOf, zipAdd_eq_zipWith, norm_eq_normalize,
    kOf_eq_div c hc, Agent2Exterior.rawExterior]
  rfl

theorem sum_replicate (n c : Nat) : (List.replicate n c).sum = n * c := by
  induction n with
  | zero => simp
  | succ n ih => simp [List.replicate_succ, ih, Nat.succ_mul, Nat.add_comm]

/-- Any suffix consisting of the current band coefficient has zero charge. -/
theorem charge_append_replicate (c : Nat) (B : Word) (n : Nat) :
    Agent2Exterior.charge c (B ++ List.replicate n c) = Agent2Exterior.charge c B := by
  simp only [Agent2Exterior.charge, Agent2Exterior.sum_append, sum_replicate,
    List.length_append, List.length_replicate, Int.natCast_add, Int.natCast_mul,
    Int.add_mul]
  omega

theorem local_charge_step (s s' : State) (L L' : Link)
    (hl : LocalOK s s' L L') :
    Agent2Exterior.charge s'.c s'.B % 9 =
      (2 * Agent2Exterior.charge s.c s.B - (gam s : Int) * (s.c : Int)) % 9 := by
  have hc : s.c ≤ 18 := by have := hl.1.2.1; omega
  have hp : s'.c = Agent2Exterior.phase s.c := by
    rw [← hl.2.2.2.2.1, next_eq_phase s.c hc]
  have hb : Agent2Exterior.rawExterior s.c s.B = s'.B ++ List.replicate L.j s'.c := by
    rw [← Br_eq_rawExterior s.c s.B s.A s.C hc]
    exact hl.2.2.2.2.2.1
  have hg : Agent2Exterior.overflow s.c s.B ≤ 1 := by
    rw [← gam_eq_overflow s hc]
    exact gamma_le s.c s.B s.A s.C hl.2.1
  have h := Agent2Exterior.raw_charge_mod9 s.c s.B hg
  rw [hb, ← hp, charge_append_replicate, ← gam_eq_overflow s hc] at h
  exact h

theorem valid_sixPhase (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    ∀ i, i < cert.P → Agent2Exterior.SixPhase (cert.st i).c := by
  intro i
  induction i with
  | zero => intro _; exact h0
  | succ i ih =>
    intro hi
    have hl := hv.2 i (by omega)
    have hphase := Agent2Exterior.sixPhase_next (cert.st i).c (ih (by omega))
    have hc : (cert.st i).c ≤ 18 := by have := hl.1.2.1; omega
    have hs : tOf (cert.st i).c + tOf (cert.st i).c = (cert.st (i+1)).c := by
      simpa only [Nat.mod_eq_of_lt hi] using hl.2.2.2.2.1
    rw [← next_eq_phase _ hc, hs] at hphase
    exact hphase

theorem local_J_step (s s' : State) (L L' : Link)
    (hl : LocalOK s s' L L') (hc : Agent2Exterior.SixPhase s.c) :
    Agent2Exterior.J s'.c (Agent2Exterior.charge s'.c s'.B) =
      (Agent2Exterior.J s.c (Agent2Exterior.charge s.c s.B) - (gam s : Int)) % 9 := by
  have hb : s.c ≤ 18 := by have := hl.1.2.1; omega
  have hp : s'.c = Agent2Exterior.phase s.c := by
    rw [← hl.2.2.2.2.1, next_eq_phase s.c hb]
  have h := Agent2Exterior.J_step s.c (Agent2Exterior.charge s.c s.B)
    (Agent2Exterior.charge s'.c s'.B) (gam s : Int) hc (local_charge_step s s' L L' hl)
  rw [← hp] at h
  exact h

/-- Closed accepted certificate: its *actual* final carries sum to zero mod 9. -/
theorem certificate_gamma_mod9 (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    Agent2Exterior.prefixCount (fun i => gam (cert.st i)) cert.P % 9 = 0 := by
  apply Agent2Exterior.closed_J_count_mod9
    (fun i => Agent2Exterior.J (cert.st (i % cert.P)).c
      (Agent2Exterior.charge (cert.st (i % cert.P)).c (cert.st (i % cert.P)).B))
  · intro i hi
    have h := local_J_step (cert.st i) (cert.st ((i+1) % cert.P))
      (cert.lk i) (cert.lk ((i+1) % cert.P)) (hv.2 i hi)
      (valid_sixPhase cert hv h0 i hi)
    simpa only [Nat.mod_eq_of_lt hi] using h
  · simp

theorem checked_certificate_gamma_mod9 (cert : Certificate) (hv : check cert = true)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    Agent2Exterior.prefixCount (fun i => gam (cert.st i)) cert.P % 9 = 0 :=
  certificate_gamma_mod9 cert (check_sound cert hv) h0

#print axioms norm_eq_normalize
#print axioms kOf_eq_div
#print axioms next_eq_phase
#print axioms gam_eq_overflow
#print axioms Br_eq_rawExterior
#print axioms sum_replicate
#print axioms charge_append_replicate
#print axioms local_charge_step
#print axioms valid_sixPhase
#print axioms local_J_step
#print axioms certificate_gamma_mod9
#print axioms checked_certificate_gamma_mod9

end Agent110.CertificateBudget
