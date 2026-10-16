import CertificatePhases

namespace Agent15.Temporal

open Agent109 Agent109.Cert
open Agent110.Phases

/-- Exact temporal phase-code evolution along a valid six-phase certificate. -/
theorem valid_phase_code_at (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c)
    (i : Nat) (hi : i < cert.P) :
    sixCode (cert.st i).c =
      (sixCode (cert.st 0).c + i) % 6 := by
  induction i with
  | zero =>
      simp
  | succ i ih =>
      have hi' : i < cert.P := by omega
      have hsucc : i + 1 < cert.P := hi
      have hl := hv.2 i hi'
      have hc : (cert.st i).c ≤ 18 := by
        have h := hl.1.2.1
        omega
      have hp : Agent2Exterior.phase (cert.st i).c =
          (cert.st ((i + 1) % cert.P)).c := by
        rw [← next_eq_phase _ hc]
        exact hl.2.2.2.2.1
      have hs := six_code_step (cert.st i).c
        (valid_sixPhase cert hv h0 i hi')
      rw [hp] at hs
      have hs' : sixCode (cert.st (i + 1)).c =
          (sixCode (cert.st i).c + 1) % 6 := by
        simpa only [Nat.mod_eq_of_lt hsucc] using hs
      rw [hs', ih]
      omega

/-- Existing period divisibility retained as a separately named interface. -/
theorem phase_code_periodic (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    cert.P % 6 = 0 := by
  exact valid_period_mod6 cert hv h0

#print axioms valid_phase_code_at
#print axioms phase_code_periodic

end Agent15.Temporal
