import Agent1PeriodicZeroPrefix
import Agent1PeriodicZeroInterfaceMass
import Agent1PeriodicZeroNumeric
import Agent1PeriodicRealizability

/-!
An explicit finite horizon for escaping every fixed zero-period interface cap.
Only the finite prefix under contradiction is lifted to one ordinary seed.
The quantitative digit-sum theorem is reused unchanged.
-/
namespace Agent1.Periodic
open Agent8

/-- One fixed ordinary seed represents every word through a capped finite
prefix. No all-time cap is assumed. -/
theorem zeroLiftWord_actual_prefix (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M N : Nat)
    (hbound : ∀ t, t ≤ N →
      2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M)
    (n : Nat) (d : Nat → Nat)
    (hc : DecimalDigits.Canonical n d (zeroLiftWord s (M+3) 0).length)
    (hr : ∀ i, i < (zeroLiftWord s (M+3) 0).length →
      DecimalDigits.columnSum d (zeroLiftWord s (M+3) 0).length i =
        ((zeroLiftWord s (M+3) 0)[i]?).getD 0)
    (t : Nat) (ht : t ≤ N) :
    ∃ d', DecimalDigits.Canonical (Lychrel196.orbit n t) d'
        (zeroLiftWord s (M+3) t).length ∧
      ∀ i, i < (zeroLiftWord s (M+3) t).length →
        DecimalDigits.columnSum d' (zeroLiftWord s (M+3) t).length i =
          ((zeroLiftWord s (M+3) t)[i]?).getD 0 := by
  revert ht
  induction t with
  | zero => intro _; exact ⟨d, hc, hr⟩
  | succ t ih =>
    intro ht
    obtain ⟨d', hc', hr'⟩ := ih (by omega)
    obtain ⟨d'', hc'', hr''⟩ := actual_step_representation
      (Lychrel196.orbit n t) d' (zeroLiftWord s (M+3) t) hc' hr'
    rw [zeroLiftWord_step_prefix s hv M N hbound t (by omega)] at hc'' hr''
    exact ⟨d'', hc'', hr''⟩

/-- Every original valid zero-period quotient orbit exceeds every interface
width cap by the existing explicit quantitative digit-sum escape horizon.
The initial interface may already exceed the cap, including when M=0. -/
theorem zeroStateOrbit_escape (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M : Nat) :
    ∃ t, t ≤ DecimalQuantitativeMass.escapeBound
        (periodicWord s.1 s.2 [0,0,0,0] (M+3)).length (9*M) ∧
      M < 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length := by
  apply Classical.byContradiction
  intro hnone
  let N := DecimalQuantitativeMass.escapeBound
    (periodicWord s.1 s.2 [0,0,0,0] (M+3)).length (9*M)
  have hbound : ∀ t, t ≤ N →
      2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M := by
    intro t ht
    have hnot : ¬ M < 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length :=
      fun hgt => hnone ⟨t, ht, hgt⟩
    omega
  obtain ⟨n, d, _, hc, hr⟩ := periodicWord_realizable s.1 s.2 [0,0,0,0]
    (M+3) hv (by omega)
  obtain ⟨t, ht, hgt⟩ := DecimalQuantitativeMass.digitSum_escape_of_canonical
    n d (periodicWord s.1 s.2 [0,0,0,0] (M+3)).length (9*M) hc
  obtain ⟨d', hc', hr'⟩ := zeroLiftWord_actual_prefix s hv M N hbound n d hc hr t ht
  have hle := zero_period_digitSum_le_width (zeroStateOrbit s t).1
    (zeroStateOrbit s t).2 (zeroExponent s (M+3) t) (Lychrel196.orbit n t) d' M
    (zeroStateOrbit_valid s hv t) hc' hr' (hbound t ht)
  omega

end Agent1.Periodic
#print axioms Agent1.Periodic.zeroLiftWord_actual_prefix
#print axioms Agent1.Periodic.zeroStateOrbit_escape
