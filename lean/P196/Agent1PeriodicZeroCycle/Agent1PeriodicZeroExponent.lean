import P196.Agent1PeriodicZeroCycle.Agent1PeriodicZeroState

/-!
A bounded interface keeps the literal exponent recursion in the guard domain
when started sufficiently far out. The proof uses nondecreasing actual total
width, not an assumed nonnegative shift at every individual transition.
-/
namespace Agent1.Periodic
open Agent8

/-- Literal exponent update used by the exact quotient, with Nat subtraction. -/
def zeroExponent (s : ZeroState) (k0 : Nat) : Nat → Nat
  | 0 => k0
  | t+1 => (zeroExponent s k0 t - 2) +
      outerPeriods (zeroStateOrbit s t).1 (zeroStateOrbit s t).2 [0,0,0,0] +
      centerPeriods (zeroStateOrbit s t).1 (zeroStateOrbit s t).2 [0,0,0,0]

/-- The complete coefficient word along this coupled state/exponent recursion. -/
def zeroLiftWord (s : ZeroState) (k0 t : Nat) : Word :=
  periodicWord (zeroStateOrbit s t).1 (zeroStateOrbit s t).2 [0,0,0,0]
    (zeroExponent s k0 t)

/-- The existing signed balance becomes an exact Nat width identity only
once the current exponent satisfies its original threshold. -/
theorem zero_width_step (s : ZeroState) (k : Nat)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (hk : 3 ≤ k) :
    2*(zeroNext s).1.length+(zeroNext s).2.length +
      8*((k-2)+outerPeriods s.1 s.2 [0,0,0,0]+centerPeriods s.1 s.2 [0,0,0,0]) =
    2*s.1.length+s.2.length+8*k+rawGamma s.1 s.2 [0,0,0,0] := by
  have hb := quotient_width_balance s.1 s.2 [0,0,0,0]
    hv.outer_bounded hv.center_bounded hv.period_bounded hv.period_length
  have he := (quotient_exponent_accounting s.1 s.2 [0,0,0,0] k hk).2
  simp only [zeroNext]
  omega

/-- A fixed bound on interface widths, together with the literal starting
exponent M+3, supplies every later guard before that guard is invoked. -/
theorem zeroExponent_guarded (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M : Nat)
    (hbound : ∀ t, 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M) :
    ∀ t, 3 ≤ zeroExponent s (M+3) t ∧
      M+24 ≤ 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length +
        8*zeroExponent s (M+3) t := by
  intro t
  induction t with
  | zero => simp only [zeroExponent, zeroStateOrbit]; omega
  | succ t ih =>
    have hw := zero_width_step (zeroStateOrbit s t) (zeroExponent s (M+3) t)
      (zeroStateOrbit_valid s hv t) ih.1
    have hnext := hbound (t+1)
    simp only [zeroStateOrbit] at hnext ⊢
    simp only [zeroExponent]
    constructor <;> omega

/-- One fixed lifted word sequence follows the exact original list dynamics
at every time, without any safety premise. -/
theorem zeroLiftWord_step (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M : Nat)
    (hbound : ∀ t, 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length ≤ M)
    (t : Nat) :
    stepWord (zeroLiftWord s (M+3) t) = zeroLiftWord s (M+3) (t+1) := by
  have hv' := zeroStateOrbit_valid s hv t
  have hk := (zeroExponent_guarded s hv M hbound t).1
  have hs := quotient_step_bounded (zeroStateOrbit s t).1 (zeroStateOrbit s t).2
    [0,0,0,0] (zeroExponent s (M+3) t) hv'.outer_bounded hv'.center_bounded
    hv'.period_bounded hv'.period_length hk
  rw [rawPeriod_zero _ _ hv'.outer_bounded hv'.center_bounded] at hs
  simpa only [zeroLiftWord, zeroStateOrbit, zeroNext, zeroExponent] using hs

end Agent1.Periodic
#print axioms Agent1.Periodic.zero_width_step
#print axioms Agent1.Periodic.zeroExponent_guarded
#print axioms Agent1.Periodic.zeroLiftWord_step
