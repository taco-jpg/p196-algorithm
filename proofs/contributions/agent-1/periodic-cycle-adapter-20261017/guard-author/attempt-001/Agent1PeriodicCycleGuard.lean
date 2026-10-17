import Agent1PeriodicGuardedPath
import Agent1PeriodicReturnClock

/-!
One fixed guarded natural exponent schedule for a supplied positive complete
quotient cycle. The existing finite budget 2*N+3 protects one traversal.
The existing return clock theorem makes its total signed shift a positive
natural gain; successive traversals add that gain to the finite schedule.
Every conversion from natural subtraction to signed accounting uses the
previously established guard. No cycle existence or safety is asserted.
-/
namespace Agent1.Periodic
open Agent8

/-- Guarded literal exponent updates telescope to the existing signed delta.
No quotient-path or validity premise is needed for this arithmetic identity. -/
theorem quotientPathExponent_accounting (B H w : Nat → Word) (k0 N : Nat)
    (hguard : ∀ i, i < N → 3 ≤ quotientPathExponent B H w k0 i) :
    (quotientPathExponent B H w k0 N : Int) =
      (k0 : Int) + quotientDeltaSum B H w N := by
  induction N with
  | zero => simp only [quotientPathExponent, quotientDeltaSum, Int.add_zero]
  | succ N ih =>
      have hprev := ih (fun i hi => hguard i (by omega))
      have hstep := (quotient_exponent_accounting (B N) (H N) (w N)
        (quotientPathExponent B H w k0 N) (hguard N (by omega))).2
      change (quotientPathExponent B H w k0 (N+1) : Int) = _ at hstep
      simp only [quotientDeltaSum]
      omega

/-- Repeat the finite budget schedule and add G copies after each traversal.
The definition is total, but its cycle laws below require positive N. -/
def quotientCycleExponent (B H w : Nat → Word) (N G t : Nat) : Nat :=
  quotientPathExponent B H w (2*N+3) (t % N) + (t / N) * G

/-- The existing finite budget supplies the guard at every remainder; adding
a natural traversal gain cannot reduce it. -/
theorem quotientCycleExponent_guarded (B H w : Nat → Word) (N G : Nat)
    (hN : 0 < N) (t : Nat) : 3 ≤ quotientCycleExponent B H w N G t := by
  have hr := Nat.mod_lt t hN
  have h := quotientPathExponent_lower_bound B H w N (t % N) (by omega)
  unfold quotientCycleExponent
  omega

/-- The finite endpoint gain closes the wrap step of the literal natural
recurrence. The finite budget guard is used before subtracting two. -/
theorem quotientCycleExponent_step (B H w : Nat → Word) (N G : Nat)
    (hN : 0 < N)
    (hend : quotientPathExponent B H w (2*N+3) N = 2*N+3+G)
    (t : Nat) :
    quotientCycleExponent B H w N G (t+1) =
      (quotientCycleExponent B H w N G t - 2) +
        outerPeriods (B (t%N)) (H (t%N)) (w (t%N)) +
        centerPeriods (B (t%N)) (H (t%N)) (w (t%N)) := by
  have hr := Nat.mod_lt t hN
  have hguard := quotientPathExponent_lower_bound B H w N (t%N) (by omega)
  have hdecomp : t+1 = (t%N+1) + N*(t/N) := by
    have h := Nat.mod_add_div t N
    omega
  by_cases hwrap : t%N+1 = N
  · have hm : (t+1)%N = 0 := by
      rw [hdecomp, hwrap, Nat.add_mul_mod_self_left]
      exact Nat.mod_self N
    have hd : (t+1)/N = t/N+1 := by
      rw [hdecomp, hwrap, Nat.add_mul_div_left _ _ hN, Nat.div_self (by omega)]
      omega
    have hf : quotientPathExponent B H w (2*N+3) N =
        (quotientPathExponent B H w (2*N+3) (t%N)-2) +
          outerPeriods (B (t%N)) (H (t%N)) (w (t%N)) +
          centerPeriods (B (t%N)) (H (t%N)) (w (t%N)) := by
      conv_lhs => rw [← hwrap]
      rfl
    simp only [quotientCycleExponent, hm, hd, Nat.add_mul, Nat.one_mul,
      quotientPathExponent]
    omega
  · have hsmall : t%N+1 < N := by omega
    have hm : (t+1)%N = t%N+1 := by
      rw [hdecomp, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hsmall]
    have hd : (t+1)/N = t/N := by
      rw [hdecomp, Nat.add_mul_div_left _ _ hN, Nat.div_eq_of_lt hsmall]
      omega
    simp only [quotientCycleExponent, hm, hd, quotientPathExponent]
    omega

/-- One supplied positive complete-tuple quotient cycle has a single natural
exponent schedule for all time, starting at 2*N+3 and satisfying every guard
and the exact quotient recurrence. This does not construct a cycle or assert
safe words; those are separate hypotheses and obligations. -/
theorem quotient_return_guarded_schedule (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ k : Nat → Nat, k 0 = 2*N+3 ∧ (∀ t, 3 ≤ k t) ∧
      ∀ t, k (t+1) = (k t-2) +
        outerPeriods (B (t%N)) (H (t%N)) (w (t%N)) +
        centerPeriods (B (t%N)) (H (t%N)) (w (t%N)) := by
  obtain ⟨G, _, _, hdelta, _, _⟩ :=
    quotient_return_clock_gain B H w N hp hv hN hreturn
  have hguard : ∀ i, i < N → 3 ≤ quotientPathExponent B H w (2*N+3) i := by
    intro i hi
    have h := quotientPathExponent_lower_bound B H w N i (by omega)
    omega
  have haccount := quotientPathExponent_accounting B H w (2*N+3) N hguard
  have hend : quotientPathExponent B H w (2*N+3) N = 2*N+3+G := by omega
  refine ⟨quotientCycleExponent B H w N G, ?_, ?_, ?_⟩
  · simp only [quotientCycleExponent, Nat.zero_mod, Nat.zero_div, Nat.zero_mul,
      Nat.add_zero, quotientPathExponent]
  · exact quotientCycleExponent_guarded B H w N G hN
  · exact quotientCycleExponent_step B H w N G hN hend

end Agent1.Periodic

#print axioms Agent1.Periodic.quotientPathExponent_accounting
#print axioms Agent1.Periodic.quotientCycleExponent
#print axioms Agent1.Periodic.quotientCycleExponent_guarded
#print axioms Agent1.Periodic.quotientCycleExponent_step
#print axioms Agent1.Periodic.quotient_return_guarded_schedule
