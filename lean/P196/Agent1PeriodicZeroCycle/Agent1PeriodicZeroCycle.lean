import P196.Agent1PeriodicZeroCycle.Agent1PeriodicZeroExponent
import P196.Foundations.Agent1PeriodicZeroNumeric
import P196.Agent1PeriodicZeroCycle.Agent1PeriodicZeroMass
import P196.Foundations.Agent1PeriodicRealizability

/-!
The literal maximal quotient has no positive return on its zero-period branch.
One positive ordinary seed is lifted through every actual transition. Bounded
interfaces would bound its digit sums, contradicting the existing unconditional
digit-sum escape theorem. No safety or palindrome-avoidance premise is used.
-/
namespace Agent1.Periodic
open Agent8

/-- The same ordinary seed, rather than a newly selected realization at each
time, realizes every word of the guarded exact quotient lift. -/
theorem zeroLiftWord_actual_orbit (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M : Nat)
    (hbound : ∀ t, 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M)
    (n : Nat) (d : Nat → Nat)
    (hc : DecimalDigits.Canonical n d (zeroLiftWord s (M+3) 0).length)
    (hr : ∀ i, i < (zeroLiftWord s (M+3) 0).length →
      DecimalDigits.columnSum d (zeroLiftWord s (M+3) 0).length i =
        ((zeroLiftWord s (M+3) 0)[i]?).getD 0) :
    ∀ t, ∃ d', DecimalDigits.Canonical (Lychrel196.orbit n t) d'
        (zeroLiftWord s (M+3) t).length ∧
      ∀ i, i < (zeroLiftWord s (M+3) t).length →
        DecimalDigits.columnSum d' (zeroLiftWord s (M+3) t).length i =
          ((zeroLiftWord s (M+3) t)[i]?).getD 0 := by
  intro t
  induction t with
  | zero => exact ⟨d, hc, hr⟩
  | succ t ih =>
    obtain ⟨d', hc', hr'⟩ := ih
    obtain ⟨d'', hc'', hr''⟩ := actual_step_representation
      (Lychrel196.orbit n t) d' (zeroLiftWord s (M+3) t) hc' hr'
    rw [zeroLiftWord_step s hv M hbound t] at hc'' hr''
    exact ⟨d'', hc'', hr''⟩

/-- Bounded exterior/center size and mass are impossible along the exact
zero-period quotient orbit of any original valid state. -/
theorem zeroStateOrbit_not_bounded (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) :
    ¬ ∃ M, ∀ t,
      2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M ∧
      2*(zeroStateOrbit s t).1.sum+(zeroStateOrbit s t).2.sum ≤ M := by
  rintro ⟨M, hbound⟩
  obtain ⟨n, d, hn, hc, hr⟩ := periodicWord_realizable s.1 s.2 [0,0,0,0]
    (M+3) hv (by omega)
  have hlength : ∀ t,
      2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M :=
    fun t => (hbound t).1
  have hreal := zeroLiftWord_actual_orbit s hv M hlength n d hc hr
  apply DecimalUnboundedMass.not_eventually_bounded_digitSum n hn
  refine ⟨0, M, ?_⟩
  intro t _
  obtain ⟨d', hc', hr'⟩ := hreal t
  exact zero_period_digitSum_le (zeroStateOrbit s t).1 (zeroStateOrbit s t).2
    (zeroExponent s (M+3) t) (Lychrel196.orbit n t) d' M hc' hr' (hbound t).2

/-- No positive-length cycle exists in the exact maximal quotient once its
period is four zeros. This does not assert termination or a palindrome hit. -/
theorem zeroStateOrbit_no_cycle (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (P : Nat) (hP : 0 < P) :
    zeroStateOrbit s P ≠ s := by
  intro hcycle
  exact zeroStateOrbit_not_bounded s hv (zeroStateOrbit_cycle_bounded s P hP hcycle)

end Agent1.Periodic
#print axioms Agent1.Periodic.zeroLiftWord_actual_orbit
#print axioms Agent1.Periodic.zeroStateOrbit_not_bounded
#print axioms Agent1.Periodic.zeroStateOrbit_no_cycle
