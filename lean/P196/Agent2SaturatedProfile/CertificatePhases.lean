import P196.Agent2SaturatedProfile.CertificateCharge

/-! Phase and period restrictions for the existing finite certificate format.
No concrete accepted certificate is supplied. -/
namespace Agent110.Phases
open Agent109 Agent109.Cert
open Agent110.CertificateBudget

/-- Every state on a closed certificate has an even phase, including state zero. -/
theorem valid_phase_even (cert : Certificate) (hv : Valid cert)
    (i : Nat) (hi : i < cert.P) : (cert.st i).c % 2 = 0 := by
  cases i with
  | zero =>
    have hp : cert.P - 1 < cert.P := by omega
    have hs : cert.P - 1 + 1 = cert.P := by omega
    have h := (hv.2 (cert.P - 1) hp).2.2.2.2.1
    simp only [hs, Nat.mod_self] at h
    omega
  | succ i =>
    have h := (hv.2 i (by omega)).2.2.2.2.1
    simp only [Nat.mod_eq_of_lt hi] at h
    omega

def sixCode (c : Nat) : Nat :=
  if c = 2 then 0 else if c = 4 then 1 else if c = 8 then 2 else
  if c = 16 then 3 else if c = 14 then 4 else if c = 10 then 5 else 0

theorem six_code_step (c : Nat) (hc : Agent2Exterior.SixPhase c) :
    sixCode (Agent2Exterior.phase c) = (sixCode c + 1) % 6 := by
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;>
    decide

theorem counter_telescope (r : Nat → Nat) (n : Nat)
    (h : ∀ i, i < n → r (i+1) % 6 = (r i + 1) % 6) :
    r n % 6 = (r 0 + n) % 6 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have ht := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    omega

/-- A six-phase checked return has period divisible by six. -/
theorem valid_period_mod6 (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) : cert.P % 6 = 0 := by
  let r := fun i => sixCode (cert.st (i % cert.P)).c
  have ht : r cert.P % 6 = (r 0 + cert.P) % 6 := by
    apply counter_telescope
    intro i hi
    have hl := hv.2 i hi
    have hc : (cert.st i).c ≤ 18 := by have := hl.1.2.1; omega
    have hp : Agent2Exterior.phase (cert.st i).c = (cert.st ((i+1)%cert.P)).c := by
      rw [← next_eq_phase _ hc]
      exact hl.2.2.2.2.1
    have hs := six_code_step (cert.st i).c (valid_sixPhase cert hv h0 i hi)
    rw [hp] at hs
    simp only [r, Nat.mod_eq_of_lt hi]
    omega
  have hr : r cert.P = r 0 := by simp [r]
  rw [hr] at ht
  omega

theorem checked_period_mod6 (cert : Certificate) (hv : check cert = true)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) : cert.P % 6 = 0 :=
  valid_period_mod6 cert (check_sound cert hv) h0

#print axioms valid_phase_even
#print axioms six_code_step
#print axioms counter_telescope
#print axioms valid_period_mod6
#print axioms checked_period_mod6
end Agent110.Phases
