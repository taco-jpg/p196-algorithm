import P196.Agent1PeriodicPrefixSaturation.Agent1PeriodicSaturation
import P196.Agent1PeriodicReturnCore.Agent1PeriodicReturnCore

/-!
The original phase `[14,14,4,4]` rules out equality in the lower
clock-rate bound for a positive complete quotient return. The proof combines
the actual-prefix saturation classification with the independently checked
return-component restriction. It does not assert that a return exists, or
identify an ordinary integer orbit with an arbitrary quotient path.
-/
namespace Agent1.Periodic
open Agent8

/-- At the original phase a positive full-tuple return has strictly fewer
than one overflow per two transitions. -/
theorem quotient_return_initial_clock_strict (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hphase : w 0 = [14,14,4,4]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    2 * quotientClockSum B H w N < N := by
  have hclosed : outside (B N) (w N) = outside (B 0) (w 0) := by
    rw [hreturn.1, hreturn.2.2]
  have hlower :=
    (quotient_path_closed_outside_clock_bounds B H w N hp hv hclosed).1
  have hcore := quotient_return_initial_outside B H w N hp hv hphase hN hreturn
  have hne : 2 * quotientClockSum B H w N ≠ N := by
    intro hsat
    have hs := quotient_return_saturated_outside B H w N hp hv hN hreturn hsat
    omega
  omega

/-- The positive gain of an initial-phase full return obeys the strict
lower length bound `16*G < N`, with the previous upper bound unchanged. -/
theorem quotient_return_initial_clock_gain (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hphase : w 0 = [14,14,4,4]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ G : Nat, 0 < G ∧ quotientClockSum B H w N = 8 * G ∧
      quotientDeltaSum B H w N = (G : Int) ∧ 16 * G < N ∧ N ≤ 32 * G := by
  obtain ⟨G, hG, hclock, hdelta, _, hupper⟩ :=
    quotient_return_clock_gain B H w N hp hv hN hreturn
  have hs := quotient_return_initial_clock_strict B H w N hp hv hphase hN hreturn
  refine ⟨G, hG, hclock, hdelta, ?_, hupper⟩
  omega

/-- A positive full return at the original phase needs at least seventeen
quotient transitions. This is a necessary condition, not an existence claim. -/
theorem quotient_return_initial_length_ge_seventeen (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hphase : w 0 = [14,14,4,4]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) : 17 ≤ N := by
  obtain ⟨G, hG, _, _, hlength, _⟩ :=
    quotient_return_initial_clock_gain B H w N hp hv hphase hN hreturn
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_return_initial_clock_strict
#print axioms Agent1.Periodic.quotient_return_initial_clock_gain
#print axioms Agent1.Periodic.quotient_return_initial_length_ge_seventeen
