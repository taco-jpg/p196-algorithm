import P196.Agent2SaturatedProfile.CertificateAccounting
import P196.Agent2SaturatedProfile.CertificateCharge
import P196.Agent2SaturatedProfile.CertificateCarryBudget
import P196.Agent2SaturatedProfile.CertificatePhases

/-! Necessary conditions derived from the actual accepted return checker.
A valid certificate is NOT supplied; these conclusions prune candidate cycles.
No bound on block widths or maximal trimming premise is used. -/
namespace Agent110.Consequences
open Agent109 Agent109.Cert Agent110.Accounting

/-- Identify independently implemented natural and integer sums. -/
theorem count_cast (f : Nat → Nat) (n : Nat) :
    (Agent2Exterior.prefixCount f n : Int) = sumPrefix (fun i => (f i : Int)) n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [Agent2Exterior.prefixCount, sumPrefix, Int.natCast_add, ih]

theorem carry_count_cast (f : Nat → Nat) (n : Nat) :
    (Agent110.CarryBudget.count f n : Int) = sumPrefix (fun i => (f i : Int)) n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [Agent110.CarryBudget.count, sumPrefix, Int.natCast_add, ih]

theorem totalGam_eq_carryCount (cert : Certificate) :
    totalGam cert = (Agent110.CarryBudget.carryCount cert : Int) :=
  (carry_count_cast _ _).symm

theorem totalGam_mod9 (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) : totalGam cert % 9 = 0 := by
  have h := Agent110.CertificateBudget.certificate_gamma_mod9 cert hv h0
  have hcast := count_cast (fun i => gam (cert.st i)) cert.P
  change (Agent2Exterior.prefixCount (fun i => gam (cert.st i)) cert.P : Int) = totalGam cert at hcast
  omega

theorem trim_difference_mod9 (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    (totalJ1 cert - totalJ2 cert) % 9 = 0 := by
  have h := Agent110.CertificateBudget.certificate_interface_trim_mod9 cert hv h0
  rw [count_cast, count_cast] at h
  exact h

/-- Each coordinate separately gains a multiple of nine in the six-phase case. -/
theorem total_gains_mod9 (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    totalG cert % 9 = 0 ∧ totalH cert % 9 = 0 := by
  have hγ := totalGam_mod9 cert hv h0
  have hd := trim_difference_mod9 cert hv h0
  have hj := totalJ1_add_totalJ2 cert hv
  have hg := totalG_eq_totalJ1 cert hv
  have hw := totalGam_eq_twice_gains cert hv
  omega

/-- Physical carry budget for an accepted certificate, with only initial
canonical exterior positivity required. -/
theorem total_carry_budget (cert : Certificate) (hv : Valid cert)
    (hpos : 0 < Agent110.CarryBudget.exterior (cert.st 0)) :
    0 < totalGam cert ∧ 2 * totalGam cert ≤ (cert.P : Int) ∧
      (cert.P : Int) ≤ 4 * totalGam cert := by
  have h := Agent110.CarryBudget.certificate_carry_budget_of_positive cert hv hpos
  rw [totalGam_eq_carryCount]
  omega

/-- All phase classes: a realizable accepted certificate has period at least four. -/
theorem period_at_least_four (cert : Certificate) (hv : Valid cert)
    (hpos : 0 < Agent110.CarryBudget.exterior (cert.st 0)) : 4 ≤ cert.P := by
  have hb := total_carry_budget cert hv hpos
  have he := totalGam_even cert hv
  obtain ⟨q, hq, he⟩ := he
  omega

/-- Six-phase return certificate: exact accounting, separate positive-coordinate
restrictions, nonzero overflow in multiples of eighteen, and period at least 36. -/
theorem six_phase_constraints (cert : Certificate) (hv : Valid cert)
    (hpos : 0 < Agent110.CarryBudget.exterior (cert.st 0))
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    totalGam cert = 2 * (totalG cert + totalH cert) ∧
    0 ≤ totalG cert ∧ 0 ≤ totalH cert ∧
    totalG cert % 9 = 0 ∧ totalH cert % 9 = 0 ∧
    totalGam cert % 18 = 0 ∧ 18 ≤ totalGam cert ∧
    2 * totalGam cert ≤ (cert.P : Int) ∧ (cert.P : Int) ≤ 4 * totalGam cert ∧
    cert.P % 6 = 0 ∧ 36 ≤ cert.P := by
  have hw := totalGam_eq_twice_gains cert hv
  have hg := totalG_nonneg cert hv
  have hh := totalH_nonneg cert hv
  have hm := total_gains_mod9 cert hv h0
  have hb := total_carry_budget cert hv hpos
  have hp := Agent110.Phases.valid_period_mod6 cert hv h0
  refine ⟨hw, hg, hh, hm.1, hm.2, ?_, ?_, hb.2.1, hb.2.2, hp, ?_⟩ <;> omega

/-- Direct checker endpoint with the original canonical-realizability premise. -/
theorem checked_six_phase_constraints (cert : Certificate) (hcheck : check cert = true)
    (H M : Word) (ha : Admissible0 cert H M)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) :
    totalGam cert = 2 * (totalG cert + totalH cert) ∧
    0 ≤ totalG cert ∧ 0 ≤ totalH cert ∧
    totalG cert % 9 = 0 ∧ totalH cert % 9 = 0 ∧
    totalGam cert % 18 = 0 ∧ 18 ≤ totalGam cert ∧
    2 * totalGam cert ≤ (cert.P : Int) ∧ (cert.P : Int) ≤ 4 * totalGam cert ∧
    cert.P % 6 = 0 ∧ 36 ≤ cert.P := by
  have hv := check_sound cert hcheck
  exact six_phase_constraints cert hv
    (Agent110.CarryBudget.exterior_pos _ (hv.2 0 hv.1).1 ha.2.2.2) h0

/-- Smallest overflow budget forces all nine gained columns into one coordinate. -/
theorem eighteen_overflows_gain_cases (cert : Certificate) (hv : Valid cert)
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) (hγ : totalGam cert = 18) :
    (totalG cert = 9 ∧ totalH cert = 0) ∨
    (totalG cert = 0 ∧ totalH cert = 9) := by
  have hw := totalGam_eq_twice_gains cert hv
  have hg := totalG_nonneg cert hv
  have hh := totalH_nonneg cert hv
  have hm := total_gains_mod9 cert hv h0
  omega

#print axioms count_cast
#print axioms carry_count_cast
#print axioms totalGam_eq_carryCount
#print axioms totalGam_mod9
#print axioms trim_difference_mod9
#print axioms total_gains_mod9
#print axioms total_carry_budget
#print axioms period_at_least_four
#print axioms six_phase_constraints
#print axioms checked_six_phase_constraints
#print axioms eighteen_overflows_gain_cases
end Agent110.Consequences
