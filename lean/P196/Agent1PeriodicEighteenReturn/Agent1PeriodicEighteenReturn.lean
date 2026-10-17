import P196.Agent1PeriodicEighteenReturn.Agent1PeriodicEighteenBand
import P196.Agent1PeriodicEighteenReturn.Agent1PeriodicEighteenTrack
import P196.Agent1PeriodicEighteenReturn.Agent1PeriodicEighteenClock
import P196.Agent1PeriodicCycleAdapter.Agent1PeriodicCycleGuard

/-!
A constant-eighteen period cannot participate in a positive full-tuple
quotient return. A sufficiently wide initial band contains one selected
maximal run whose descendant survives the whole finite path. Full return
fixes its left boundary, while the actual positive overflow sum forces that
same boundary to advance. No population, safety, or 196 conclusion is used.
-/

namespace Agent1.Periodic
open Agent8

/-- Original-valid finite quotient paths starting with the constant-eighteen
period cannot return their complete exterior, center and period tuple.
Empty exteriors/centers and joined eighteen bands are included. -/
theorem quotient_path_eighteen_no_return
    (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw : w 0 = [18,18,18,18]) (hN : 0 < N) :
    ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0) := by
  intro hreturn
  let k := quotientPathExponent B H w (2*N+3)
  have hk0 : k 0 = 2*N+3 := rfl
  have hguard : ∀ t, t < N → 3 ≤ k t := by
    intro t ht
    have hl := quotientPathExponent_lower_bound B H w N t (by omega)
    change 3 ≤ quotientPathExponent B H w (2*N+3) t
    omega
  have hkstep : ∀ t, t < N → k (t+1) = (k t-2) +
      outerPeriods (B t) (H t) (w t) + centerPeriods (B t) (H t) (w t) := by
    intro t _
    rfl
  obtain ⟨G, hG, hC, hdelta, _, _⟩ :=
    quotient_return_clock_gain B H w N hp hv hN hreturn
  have haccount := quotientPathExponent_accounting B H w (2*N+3) N hguard
  have hkN : k N = 2*N+3+G := by
    change (k N : Int) = (2*N+3 : Nat) + quotientDeltaSum B H w N at haccount
    omega
  obtain ⟨a, b, hr, ha, hb⟩ :=
    periodic_eighteen_band_run (B 0) (H 0) (k 0) (by omega)
  have hr0 : RunAncestry.MaximalRun
      (fun j => ((quotientPathWord B H w k 0)[j]?).getD 0)
      (quotientPathWord B H w k 0).length 18 a b := by
    simpa only [quotientPathWord, hw] using hr
  have hcarry : ∀ t, t < N → quotientClockSum B H w (t+1) =
      quotientClockSum B H w t + DecimalDigits.carry
        (fun j => ((quotientPathWord B H w k t)[j]?).getD 0)
        (quotientPathWord B H w k t).length := by
    intro t ht
    exact quotient_path_actual_carry_step B H w k N hp t ht
      (by have hg := hguard t ht; omega)
  obtain ⟨hrN, _, _, hadvance, haiN, hibN⟩ :=
    quotient_eighteen_track B H w k (quotientClockSum B H w) N a b
      ((B 0).length+N) hp hv hguard hkstep rfl hcarry hr0
      (by omega) (by omega) N (Nat.le_refl N)
  let p := quotientEighteenTrack B H w k a b N
  have hrN' : RunAncestry.MaximalRun
      (fun j => ((periodicWord (B 0) (H 0) [18,18,18,18] (k N))[j]?).getD 0)
      (periodicWord (B 0) (H 0) [18,18,18,18] (k N)).length 18 p.1 p.2 := by
    simpa only [quotientPathWord, hreturn.1, hreturn.2.1, hreturn.2.2, hw]
      using hrN
  have heq := periodic_eighteen_band_left_eq (B 0) (H 0) (H 0)
    (k 0) (k N) ((B 0).length+N) a b p.1 p.2 hr hrN'
    (by omega) (by omega) (by omega) (by omega) (by omega) haiN hibN
  change a + quotientClockSum B H w N ≤ p.1 at hadvance
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_path_eighteen_no_return
