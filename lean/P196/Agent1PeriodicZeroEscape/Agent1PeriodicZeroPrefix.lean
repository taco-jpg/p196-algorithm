import P196.Agent1PeriodicZeroCycle.Agent1PeriodicZeroExponent

/-!
Finite-prefix versions of the exact zero-period exponent guard and lifted
word transition. A cap is assumed only through the stated endpoint N;
no all-time bound, safety premise, or independent carry choice is introduced.
-/

namespace Agent1.Periodic

open Agent8

/-- The literal starting exponent M+3 stays in the guard domain through N
whenever the original quotient interfaces are capped through N. -/
theorem zeroExponent_guarded_prefix (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M N : Nat)
    (hbound : ∀ t, t ≤ N →
      2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M)
    (t : Nat) (ht : t ≤ N) :
    3 ≤ zeroExponent s (M+3) t ∧
      M+24 ≤ 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length +
        8*zeroExponent s (M+3) t := by
  revert ht
  induction t with
  | zero =>
    intro _
    simp only [zeroExponent, zeroStateOrbit]
    omega
  | succ t ih =>
    intro ht
    have hprev := ih (by omega)
    have hw := zero_width_step (zeroStateOrbit s t) (zeroExponent s (M+3) t)
      (zeroStateOrbit_valid s hv t) hprev.1
    have hnext := hbound (t+1) ht
    simp only [zeroStateOrbit] at hnext ⊢
    simp only [zeroExponent]
    constructor <;> omega

/-- Every transition strictly before the finite endpoint is the original
actual word step. The cap at the endpoint is retained for the next guard. -/
theorem zeroLiftWord_step_prefix (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M N : Nat)
    (hbound : ∀ t, t ≤ N →
      2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M)
    (t : Nat) (ht : t < N) :
    stepWord (zeroLiftWord s (M+3) t) = zeroLiftWord s (M+3) (t+1) := by
  have hv' := zeroStateOrbit_valid s hv t
  have hk := (zeroExponent_guarded_prefix s hv M N hbound t (by omega)).1
  have hs := quotient_step_bounded (zeroStateOrbit s t).1 (zeroStateOrbit s t).2
    [0,0,0,0] (zeroExponent s (M+3) t) hv'.outer_bounded hv'.center_bounded
    hv'.period_bounded hv'.period_length hk
  rw [rawPeriod_zero _ _ hv'.outer_bounded hv'.center_bounded] at hs
  simpa only [zeroLiftWord, zeroStateOrbit, zeroNext, zeroExponent] using hs

end Agent1.Periodic

#print axioms Agent1.Periodic.zeroExponent_guarded_prefix
#print axioms Agent1.Periodic.zeroLiftWord_step_prefix
