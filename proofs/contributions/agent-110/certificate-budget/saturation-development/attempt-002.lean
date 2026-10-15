import CertificateConsequences
import SaturationTheorem

/-!
Agent #110: compose exact return-certificate accounting with Agent #4's
three-column saturation obstruction. A closed prefix path in this file records
the actual certificate gamma on every edge. Numerical congruences are derived
from `six_phase_constraints`, never additional hypotheses of the final bounds.

This concerns necessary conditions on accepted certificates. It does not
construct any accepted certificate, infinite seed, or proof concerning 196.
-/

namespace Agent110.CertificateSaturation

open Agent109 Agent109.Cert Agent110.Accounting

/-- Exact finite projection, retaining the actual overflow on every edge. -/
structure ClosedPrefixPath (cert : Certificate) where
  state : Nat → P196.Agent4.Saturation.Prefix
  input : Nat → Nat
  valid : ∀ i, i < cert.P → P196.Agent4.Saturation.Valid (state i)
  input_le : ∀ i, i < cert.P → input i ≤ 1
  transition : ∀ i, i < cert.P →
    P196.Agent4.Saturation.advance (state i) (input i) =
      (state (i + 1), gam (cert.st i))
  closed : state cert.P = state 0

/-- A pointwise exact prefix projection yields a closed certificate path.
The hypotheses are structural projection facts, not numerical budget premises. -/
theorem closed_prefix_path_of_projection (cert : Certificate) (hv : Valid cert)
    (hpos : 0 < Agent110.CarryBudget.exterior (cert.st 0))
    (proj : State → P196.Agent4.Saturation.Prefix)
    (hvalid : ∀ s, Phase s.c → Bounded s.B →
      0 < Agent110.CarryBudget.exterior s → P196.Agent4.Saturation.Valid (proj s))
    (hstep : ∀ s s' L L', LocalOK s s' L L' →
      ∃ e, e ≤ 1 ∧ P196.Agent4.Saturation.advance (proj s) e = (proj s', gam s)) :
    Nonempty (ClosedPrefixPath cert) := by
  classical
  let p := fun i => proj (cert.st (i % cert.P))
  have hl : ∀ i, i < cert.P → ∃ e, e ≤ 1 ∧
      P196.Agent4.Saturation.advance (p i) e = (p (i + 1), gam (cert.st i)) := by
    intro i hi
    simpa only [p, Nat.mod_eq_of_lt hi] using hstep _ _ _ _ (hv.2 i hi)
  let e := fun i => if hi : i < cert.P then Classical.choose (hl i hi) else 0
  have he : ∀ i, i < cert.P → e i ≤ 1 ∧
      P196.Agent4.Saturation.advance (p i) (e i) = (p (i + 1), gam (cert.st i)) := by
    intro i hi
    simpa only [e, dif_pos hi] using Classical.choose_spec (hl i hi)
  refine ⟨⟨p, e, ?_, ?_, ?_, ?_⟩⟩
  · intro i hi
    have hp := Agent110.CarryBudget.exterior_positive_along cert hv hpos i (by omega)
    rw [Nat.mod_eq_of_lt hi] at hp
    simpa only [p, Nat.mod_eq_of_lt hi] using
      hvalid (cert.st i) (hv.2 i hi).1 (hv.2 i hi).2.1 hp
  · exact fun i hi => (he i hi).1
  · exact fun i hi => (he i hi).2
  · simp [p]

/-- The Agent #4 natural sum agrees with the accounting module's signed sum. -/
theorem saturation_total_cast (f : Nat → Nat) (n : Nat) :
    (P196.Agent4.Saturation.total f n : Int) = sumPrefix (fun i => (f i : Int)) n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [P196.Agent4.Saturation.total, sumPrefix, Int.natCast_add, ih]

/-- The projected path's overflow count is exactly the actual certificate count. -/
theorem path_total_eq_totalGam (cert : Certificate) (path : ClosedPrefixPath cert) :
    (P196.Agent4.Saturation.total
      (fun i => (P196.Agent4.Saturation.advance (path.state i) (path.input i)).2)
      cert.P : Int) = totalGam cert := by
  rw [saturation_total_cast]
  apply sumPrefix_congr
  intro i hi
  rw [path.transition i hi]

/-- Conditional composition checkpoint; the direct theorem below supplies the path. -/
theorem period_at_least_forty_two_of_path (cert : Certificate) (hv : Valid cert)
    (hpos : 0 < Agent110.CarryBudget.exterior (cert.st 0))
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) (path : ClosedPrefixPath cert) :
    42 ≤ cert.P := by
  have hn := Agent110.Consequences.six_phase_constraints cert hv hpos h0
  have hc := path_total_eq_totalGam cert path
  apply P196.Agent4.Saturation.unit_phase_full_cycle_period_at_least_forty_two
    path.state path.input cert.P path.valid path.input_le
    (fun i hi => congrArg Prod.fst (path.transition i hi)) path.closed hv.1
  · omega
  · omega
  · omega

/-- Saturation forces the period to be divisible by 72, without a width bound. -/
theorem saturated_period_constraints_of_path (cert : Certificate) (hv : Valid cert)
    (hpos : 0 < Agent110.CarryBudget.exterior (cert.st 0))
    (h0 : Agent2Exterior.SixPhase (cert.st 0).c) (path : ClosedPrefixPath cert)
    (hsat : 2 * totalGam cert = (cert.P : Int)) :
    cert.P % 72 = 0 ∧ 72 ≤ cert.P := by
  have hn := Agent110.Consequences.six_phase_constraints cert hv hpos h0
  have hc := path_total_eq_totalGam cert path
  have hnat : 2 * P196.Agent4.Saturation.total
      (fun i => (P196.Agent4.Saturation.advance (path.state i) (path.input i)).2)
      cert.P = cert.P := by omega
  have h8 := P196.Agent4.Saturation.saturated_closed_prefix_period
    path.state path.input cert.P path.valid path.input_le
    (fun i hi => congrArg Prod.fst (path.transition i hi)) path.closed hnat
  have hP := hv.1
  omega

end Agent110.CertificateSaturation
