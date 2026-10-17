import Agent1PeriodicPrefix
import Agent1PeriodicReturnClock
import Agent2SaturatedProfile

/-!
The exact period-four quotient projects to the already classified saturated
three-column cycle. The prefix and carry at each transition come from the
actual exponent-three word; no freely chosen carry, extra tightness premise,
ordinary multi-step lift, or input-balance condition is introduced.

The classification is Agent2.SaturatedProfile.saturated_overflow_profile,
using the original Agent215 cycle states and Agent4 prefix relation. This
module supplies only the quotient-path adapter and its outside consequence.
It does not exclude the archived alternating outside-17/8 witness, construct
a finite interface return, or assert safety of an ordinary infinite orbit.
-/

namespace Agent1.Periodic
open Agent8

private theorem prefix_total_eq_quotientClockSum
    (B H w : Nat → Word) (g : Nat → Nat) (N : Nat)
    (hg : ∀ i, i < N → g i = rawGamma (B i) (H i) (w i)) :
    P196.Agent4.Saturation.total g N = quotientClockSum B H w N := by
  induction N with
  | zero => rfl
  | succ N ih =>
    simp only [P196.Agent4.Saturation.total, quotientClockSum]
    rw [ih (fun i hi => hg i (by omega)), hg N (by omega)]

/-- Every used state of a saturated complete-tuple quotient return follows
the original eight-state prefix cycle, with its actual alternating overflow.
The zero-length case is retained and has a vacuous state conclusion. -/
theorem quotient_return_saturated_profile (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
    (hsat : 2 * quotientClockSum B H w N = N) :
    ∃ r : Fin 8, ∀ i, i < N →
      physicalPrefix (B i) (w i) = Agent215.Saturated8.cycleState (r.val + i) ∧
      rawGamma (B i) (H i) (w i) = (r.val + i) % 2 := by
  let s := fun i => physicalPrefix (B i) (w i)
  let e := fun i => inputThree (periodicWord (B i) (H i) (w i) 3)
  have hlocal : ∀ i, i < N →
      P196.Agent4.Saturation.Valid (s i) ∧ e i ≤ 1 ∧
      P196.Agent4.Saturation.advance (s i) (e i) =
        (s (i+1), rawGamma (B i) (H i) (w i)) := by
    intro i hi
    have hvi := quotient_path_valid B H w N hp hv i (by omega)
    obtain ⟨_, _, _, _, hB, _, hw⟩ := hp i hi
    dsimp only [s, e]
    simpa only [hB, hw] using physicalPrefix_step (B i) (H i) (w i) hvi
  have hgamma : ∀ i, i < N →
      (P196.Agent4.Saturation.advance (s i) (e i)).2 =
        rawGamma (B i) (H i) (w i) := by
    intro i hi
    exact congrArg Prod.snd (hlocal i hi).2.2
  have hclose : s N = s 0 := by
    dsimp only [s]
    rw [hreturn.1, hreturn.2.2]
  have htotal := prefix_total_eq_quotientClockSum B H w
    (fun i => (P196.Agent4.Saturation.advance (s i) (e i)).2) N hgamma
  have hsat' : 2 * P196.Agent4.Saturation.total
      (fun i => (P196.Agent4.Saturation.advance (s i) (e i)).2) N = N := by
    rw [htotal]
    exact hsat
  obtain ⟨r, hprofile⟩ := Agent2.SaturatedProfile.saturated_overflow_profile s e N
    (fun i hi => (hlocal i hi).1) (fun i hi => (hlocal i hi).2.1)
    (fun i hi => congrArg Prod.fst (hlocal i hi).2.2) hclose hsat'
  refine ⟨r, ?_⟩
  intro i hi
  have h := hprofile i hi
  exact ⟨h.1, (hgamma i hi).symm.trans h.2⟩

/-- A positive saturated full return has initial outside coefficient 8 or 17.
Positivity of N is essential when extracting the first used state. -/
theorem quotient_return_saturated_outside (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
    (hsat : 2 * quotientClockSum B H w N = N) :
    outside (B 0) (w 0) = 8 ∨ outside (B 0) (w 0) = 17 := by
  obtain ⟨r, hprofile⟩ := quotient_return_saturated_profile B H w N hp hv hreturn hsat
  have ha := congrArg P196.Agent4.Saturation.Prefix.a (hprofile 0 hN).1
  rw [physicalPrefix_a (B 0) (w 0) hv.period_length] at ha
  have hcycle : (Agent215.Saturated8.cycleState (r.val + 0)).a = 8 ∨
      (Agent215.Saturated8.cycleState (r.val + 0)).a = 17 := by
    unfold Agent215.Saturated8.cycleState
    split <;> simp
  rw [← ha] at hcycle
  exact hcycle

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_return_saturated_profile
#print axioms Agent1.Periodic.quotient_return_saturated_outside
