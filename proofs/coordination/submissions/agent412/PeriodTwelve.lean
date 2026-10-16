import TwoPhaseInterface

/-! Agent #412: period-twelve obstruction for the unchanged full checker.
The overflow divisibility and saturation needed for the obstruction are
proved from check acceptance and the numerical period, not assumed. -/
namespace Agent412.PeriodTwelve
open Agent109 Agent109.Cert Agent110.Accounting
open Agent112.SmallPeriod Agent412.TwoPhaseCharge Agent412.TwoPhaseInterface

/-- All phase classes: a period divisible by six forces both band gains
into multiples of three and the actual overflow sum into multiples of six. -/
theorem checked_multiple_six_counts (cert : Certificate) (hc : check cert = true)
    (hp : cert.P % 6 = 0) :
    totalG cert % 3 = 0 ∧ totalH cert % 3 = 0 ∧ totalGam cert % 6 = 0 := by
  have hv := check_sound cert hc
  rcases valid_phase_class cert hv with hphase | hphase
  · obtain ⟨hw, hg, hh, hgm, hhm, hom, ho, hlo, hhi, hp6, h42⟩ :=
      Agent110.Checked.six_phase_constraints cert hc hphase
    omega
  · have hn : ((cert.P / 2 : Nat) : Int) % 3 = 0 := by omega
    have hz (a : Int) : (a * (cert.P / 2 : Nat)) % 3 = 0 := by
      rw [Int.mul_emod, hn]
      simp
    obtain ⟨hH, hG⟩ := checked_two_phase_gain_laws cert hc hphase
    rw [hz] at hH hG
    have he := totalGam_eq_twice_gains cert hv
    omega

/-- No original-checker accepting certificate has period twelve.
No phase restriction, width bound, charge divisibility, or saturation
hypothesis is added to the executable acceptance premise. -/
theorem checked_period_ne_twelve (cert : Certificate) (hc : check cert = true) :
    cert.P ≠ 12 := by
  intro hp
  have hm := checked_multiple_six_counts cert hc (by omega)
  have hv := check_sound cert hc
  have hb := Agent110.Consequences.total_carry_budget cert hv
    (checked_positive_exterior cert hc)
  have hs : 2 * totalGam cert = (cert.P : Int) := by omega
  have h8 := checked_saturated_period_mod8 cert hc hs
  omega

/-- A directly usable necessary-condition bound for all accepted periods
in the zero residue class modulo six. Other residue classes are not excluded. -/
theorem checked_multiple_six_period_at_least_eighteen (cert : Certificate)
    (hc : check cert = true) (hp : cert.P % 6 = 0) : 18 ≤ cert.P := by
  have h8 := checked_period_at_least_eight cert hc
  have h12 := checked_period_ne_twelve cert hc
  omega

#print axioms checked_multiple_six_counts
#print axioms checked_period_ne_twelve
#print axioms checked_multiple_six_period_at_least_eighteen
end Agent412.PeriodTwelve
