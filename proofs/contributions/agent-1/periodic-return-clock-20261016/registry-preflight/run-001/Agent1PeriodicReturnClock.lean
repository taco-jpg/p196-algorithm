import Agent1PeriodicOuter
import Agent1PeriodicWidthPath

/-!
Positive clock and gain bounds for finite exact period-four quotient returns.
The outside evolution and carry bits are the actual ones of the original
quotient; the existing Agent8 exterior potential bound supplies the rate.

The positive-overflow/positive-gain argument was already written in the
original periodic_bulk_followup/METHOD_AND_PROOF.md, section 4 (blob
5c5f94c66d6c3adb0288b610f748fcbed32b115c). This module formalizes its exact
quotient-path adapter and combines the existing quantitative bounds with the
factor-eight width identity. It asserts no return exists.

The signed delta sum is formal quotient accounting. Interpreting it as a
natural exponent trajectory still requires the original guard k >= 3 at every
used transition; no such trajectory, safety hypothesis, or catalog premise
is introduced here.
-/
namespace Agent1.Periodic
open Agent8

/-- Original full validity propagates through every state of the finite
exact quotient path, including its endpoint, without a catalog premise. -/
theorem quotient_path_valid (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (i : Nat) (hi : i ≤ N) : ValidPeriodic (B i) (H i) (w i) := by
  revert hi
  induction i with
  | zero => intro _; exact hv
  | succ i ih =>
      intro hi
      have hprev := ih (by omega)
      obtain ⟨_, _, _, _, hB, hH, hw⟩ := hp i (by omega)
      have hnext := quotient_valid (B i) (H i) (w i) hprev
      simpa only [hB, hH, hw] using hnext

private theorem quotient_path_clock_total (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) :
    Agent8.total (fun i =>
      (Agent8.overflow (outside (B i) (w i))
        (lastInput (periodicWord (B i) (H i) (w i) 3)) : Int)) N =
      (quotientClockSum B H w N : Int) := by
  induction N with
  | zero => rfl
  | succ N ih =>
      have hprefix : QuotientPath B H w N := fun i hi => hp i (by omega)
      have hvN := quotient_path_valid B H w (N+1) hp hv N (by omega)
      have hgamma := (quotient_outside_step (B N) (H N) (w N) hvN).2.1
      simp only [Agent8.total, quotientClockSum, Int.natCast_add]
      rw [ih hprefix, ← hgamma]

/-- Closed physical outside coefficients obey the existing exterior carry
rate, with the actual clock sum. Zero-length paths are included. -/
theorem quotient_path_closed_outside_clock_bounds (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hclosed : outside (B N) (w N) = outside (B 0) (w 0)) :
    2 * quotientClockSum B H w N ≤ N ∧
      N ≤ 4 * quotientClockSum B H w N := by
  let p : Nat → Nat := fun i => outside (B i) (w i)
  let e : Nat → Nat := fun i => lastInput (periodicWord (B i) (H i) (w i) 3)
  have hvalid : ∀ i, i < N → 0 < p i ∧ p i ≤ 18 ∧ e i ≤ 1 := by
    intro i hi
    have hvi := quotient_path_valid B H w N hp hv i (by omega)
    have hb := outside_bounds (B i) (H i) (w i) hvi
    exact ⟨hb.1, hb.2, (quotient_outside_step (B i) (H i) (w i) hvi).1⟩
  have hevolves : ∀ i, i < N → p (i+1) = Agent8.nextExterior (p i) (e i) := by
    intro i hi
    have hvi := quotient_path_valid B H w N hp hv i (by omega)
    obtain ⟨_, _, _, _, hB, _, hw⟩ := hp i hi
    change outside (B (i+1)) (w (i+1)) = _
    rw [hB, hw]
    exact (quotient_outside_step (B i) (H i) (w i) hvi).2.2
  have hb := Agent8.closed_path_bounds p e N hvalid hevolves hclosed
  dsimp only [p, e] at hb
  rw [quotient_path_clock_total B H w N hp hv] at hb
  constructor <;> omega

/-- A positive complete-tuple return has a positive natural gain G: its
clock sum is exactly 8G, its signed shift is G, and its length lies in [16G,32G]. -/
theorem quotient_return_clock_gain (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ G : Nat, 0 < G ∧ quotientClockSum B H w N = 8 * G ∧
      quotientDeltaSum B H w N = (G : Int) ∧ 16 * G ≤ N ∧ N ≤ 32 * G := by
  have hclosed : outside (B N) (w N) = outside (B 0) (w 0) := by
    rw [hreturn.1, hreturn.2.2]
  obtain ⟨hlower, hupper⟩ :=
    quotient_path_closed_outside_clock_bounds B H w N hp hv hclosed
  have hwidth : 2*(B N).length + (H N).length =
      2*(B 0).length + (H 0).length := by rw [hreturn.1, hreturn.2.1]
  obtain ⟨_, hdiv, hdelta⟩ := quotient_path_equal_width_clock B H w N hp hwidth
  have hmultiple : quotientClockSum B H w N =
      8 * (quotientClockSum B H w N / 8) := by
    have hm := Nat.div_mul_cancel hdiv
    omega
  refine ⟨quotientClockSum B H w N / 8, ?_, hmultiple, hdelta, ?_, ?_⟩ <;> omega

/-- In particular a positive exact complete-tuple return takes at least
sixteen quotient transitions; no divisibility claim about N is made. -/
theorem quotient_return_length_ge_sixteen (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) : 16 ≤ N := by
  obtain ⟨G, hG, _, _, hlength, _⟩ := quotient_return_clock_gain B H w N hp hv hN hreturn
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_path_valid
#print axioms Agent1.Periodic.quotient_path_closed_outside_clock_bounds
#print axioms Agent1.Periodic.quotient_return_clock_gain
#print axioms Agent1.Periodic.quotient_return_length_ge_sixteen
