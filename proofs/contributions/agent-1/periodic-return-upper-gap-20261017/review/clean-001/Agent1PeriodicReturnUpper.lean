import Agent1PeriodicReturnClock
import Agent1PeriodicReturnCore
import Agent1PeriodicInitialIncoming

/-!
The original initial phase forces the final return clock to be one. The
returned outside coefficient is nine or ten, so the original Agent8 lower
potential has a two-unit gap on that last edge. Transporting its open-path
bound gives N+2 <= 4*C for the exact period-four quotient's actual clock.
No minimum-overflow cycle classification, generic coefficient improvement,
arbitrary-path realization or safe infinite trajectory is asserted.

The open-path adapter strengthens the closed-path interface already supplied
by Agent1PeriodicReturnClock. It uses exterior_bounds directly, so no copy of
that module's private clock-total conversion is required.
-/
namespace Agent1.Periodic
open Agent8

private theorem returning_overflow_gap (p e : Nat)
    (hp : 0 < p) (hp18 : p ≤ 18) (he : e ≤ 1)
    (hg : overflow p e = 1)
    (ht : nextExterior p e = 9 ∨ nextExterior p e = 10) :
    (3 : Int) ≤ 4 * (overflow p e : Int) +
      lowerPotential p - lowerPotential (nextExterior p e) := by
  have h : ∀ p : Fin 19, ∀ e : Fin 2, 0 < p.val →
      overflow p.val e.val = 1 →
      (nextExterior p.val e.val = 9 ∨ nextExterior p.val e.val = 10) →
      (3 : Int) ≤ 4 * (overflow p.val e.val : Int) +
        lowerPotential p.val - lowerPotential (nextExterior p.val e.val) := by decide
  exact h ⟨p, by omega⟩ ⟨e, by omega⟩ hp hg ht

/-- The existing lower potential bounds every open exact quotient path,
with its actual clock and both physical outside endpoint potentials. -/
theorem quotient_path_lower_potential (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) :
    (N : Int) ≤ 4 * (quotientClockSum B H w N : Int) +
      lowerPotential (outside (B 0) (w 0)) -
      lowerPotential (outside (B N) (w N)) := by
  induction N with
  | zero => simp only [quotientClockSum]; omega
  | succ N ih =>
      have hprefix : QuotientPath B H w N := fun i hi => hp i (by omega)
      have hprev := ih hprefix
      have hvN := quotient_path_valid B H w (N+1) hp hv N (by omega)
      have hb := outside_bounds (B N) (H N) (w N) hvN
      have hs := quotient_outside_step (B N) (H N) (w N) hvN
      have he := (Agent8.exterior_bounds (outside (B N) (w N))
        (lastInput (periodicWord (B N) (H N) (w N) 3)) hb.1 hb.2 hs.1).2
      obtain ⟨_, _, _, _, hB, _, hw⟩ := hp N (by omega)
      have hnext : outside (B (N+1)) (w (N+1)) =
          nextExterior (outside (B N) (w N))
            (lastInput (periodicWord (B N) (H N) (w N) 3)) := by
        rw [hB, hw]
        exact hs.2.2
      rw [← hs.2.1, ← hnext] at he
      simp only [quotientClockSum, Int.natCast_add]
      omega

/-- A positive full return at the original phase has a two-unit gap below
the upper length bound supplied by the original exterior potential. -/
theorem quotient_return_initial_upper_gap (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hphase : w 0 = [14,14,4,4]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    N + 2 ≤ 4 * quotientClockSum B H w N := by
  cases N with
  | zero => omega
  | succ N =>
      have hprefix : QuotientPath B H w N := fun i hi => hp i (by omega)
      have hprev := quotient_path_lower_potential B H w N hprefix hv
      have hvN := quotient_path_valid B H w (N+1) hp hv N (by omega)
      have hb := outside_bounds (B N) (H N) (w N) hvN
      have hs := quotient_outside_step (B N) (H N) (w N) hvN
      have hlast := quotient_return_initial_last_clock B H w (N+1)
        hp hv hphase hN hreturn
      have hg : rawGamma (B N) (H N) (w N) = 1 := by simpa only [Nat.add_sub_cancel] using hlast
      obtain ⟨_, _, _, _, hB, _, hw⟩ := hp N (by omega)
      have hnext : outside (B (N+1)) (w (N+1)) =
          nextExterior (outside (B N) (w N))
            (lastInput (periodicWord (B N) (H N) (w N) 3)) := by
        rw [hB, hw]
        exact hs.2.2
      have ht : nextExterior (outside (B N) (w N))
          (lastInput (periodicWord (B N) (H N) (w N) 3)) = 9 ∨
          nextExterior (outside (B N) (w N))
          (lastInput (periodicWord (B N) (H N) (w N) 3)) = 10 := by
        rw [← hnext, hreturn.1, hreturn.2.2]
        exact quotient_return_initial_outside B H w (N+1) hp hv hphase hN hreturn
      have hgap := returning_overflow_gap (outside (B N) (w N))
        (lastInput (periodicWord (B N) (H N) (w N) 3)) hb.1 hb.2 hs.1
        (hs.2.1.symm.trans hg) ht
      rw [← hs.2.1, ← hnext, hreturn.1, hreturn.2.2] at hgap
      simp only [quotientClockSum]
      omega

/-- The existing positive return gain retains the two-unit upper length gap.
The signed delta is formal quotient accounting, with no exponent lift assumed. -/
theorem quotient_return_initial_upper_gain (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hphase : w 0 = [14,14,4,4]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ G : Nat, 0 < G ∧ quotientClockSum B H w N = 8 * G ∧
      quotientDeltaSum B H w N = (G : Int) ∧ 16 * G ≤ N ∧ N + 2 ≤ 32 * G := by
  obtain ⟨G, hG, hclock, hdelta, hlower, _⟩ :=
    quotient_return_clock_gain B H w N hp hv hN hreturn
  have hgap := quotient_return_initial_upper_gap B H w N hp hv hphase hN hreturn
  exact ⟨G, hG, hclock, hdelta, hlower, by omega⟩

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_path_lower_potential
#print axioms Agent1.Periodic.quotient_return_initial_upper_gap
#print axioms Agent1.Periodic.quotient_return_initial_upper_gain
