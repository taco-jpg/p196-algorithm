import Agent1PeriodicReturnClock
import Agent1PeriodicReturnCore

/-!
The original Agent8 lower potential, transported to the exact period-four
quotient with its actual clock. A returning overflow into outside nine or ten
has a two-unit gap. This uses the unchanged scalar potential and does not
classify minimum-overflow cycles or strengthen a generic growth coefficient.

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

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_path_lower_potential
