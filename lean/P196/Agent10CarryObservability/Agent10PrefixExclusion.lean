import P196.Agent10EightCarry.Agent10EightCarry
import P196.Agent10CarryObservability.Agent10PrefixWitness

/-!
Agent #10: the coefficient-six smoothing witness is incompatible with seven
actual complete carry observations. The exclusion uses only its first two
coefficients, so it applies to every admissible width at least two.

The additional eight-word theorem identifies the exterior pair coefficient
without an initial-nonoverflow premise. It does not identify every coefficient.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace Agent10PrefixExclusion
open CarryObservability Agent10PrefixWitness
open DifferenceObservability CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

theorem survives_step_of (n : Nat) (s r : State) (v : Bool)
    (hc : compatible s r v = true)
    (hs : survives n (next s v) (next r v) = true) :
    survives (n + 1) s r = true := by
  cases v <;> simp_all [survives]

theorem survives_of_trajectory (s r : Nat → State) (bits : Nat → Bool) (K : Nat)
    (hc : ∀ t, t < K → compatible (s t) (r t) (bits t) = true)
    (hs : ∀ t, t < K → s (t + 1) = next (s t) (bits t))
    (hr : ∀ t, t < K → r (t + 1) = next (r t) (bits t)) :
    survives K (s 0) (r 0) = true := by
  induction K generalizing s r bits with
  | zero => rfl
  | succ K ih =>
    apply survives_step_of K (s 0) (r 0) (bits 0) (hc 0 (by omega))
    have h := ih (fun t => s (t + 1)) (fun t => r (t + 1))
      (fun t => bits (t + 1))
      (by intro t ht; exact hc (t + 1) (by omega))
      (by intro t ht; exact hs (t + 1) (by omega))
      (by intro t ht; exact hr (t + 1) (by omega))
    simpa only [hs 0 (by omega), hr 0 (by omega)] using h

/-- Every synchronized actual carry history maps into the finite graph using
one shared observed inner bit. The actual update remains unchanged. -/
theorem actual_history_survives (q r : Nat → Nat) (L K : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 2 ≤ L)
    (hc : ∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    survives K (q 0, q 1) (r 0, r 1) = true := by
  let statesQ : Nat → State := fun t =>
    ((iterPairs q L t).2 0, (iterPairs q L t).2 1)
  let statesR : Nat → State := fun t =>
    ((iterPairs r L t).2 0, (iterPairs r L t).2 1)
  let bits : Nat → Bool := fun t =>
    observedBit (iterPairs q L t).2 (iterPairs q L t).1
  have hw : ∀ t, t ≤ K → (iterPairs q L t).1 = (iterPairs r L t).1 := by
    intro t ht
    exact matched_widths q r L t (fun j hj => hc j (by omega))
  have hwq : ∀ t, 2 ≤ (iterPairs q L t).1 := by
    intro t
    have h := iterPairs_width_ge_initial q L t
    omega
  have hwr : ∀ t, 2 ≤ (iterPairs r L t).1 := by
    intro t
    have h := iterPairs_width_ge_initial r L t
    omega
  have hbits : ∀ t, t < K →
      observedBit (iterPairs q L t).2 (iterPairs q L t).1 =
      observedBit (iterPairs r L t).2 (iterPairs r L t).1 := by
    intro t ht
    unfold observedBit
    rw [←hw t (by omega), hc t ht ((iterPairs q L t).1 - 2) (by omega)]
  have hcomp : ∀ t, t < K → compatible (statesQ t) (statesR t) (bits t) = true := by
    intro t ht
    simp only [compatible, decide_eq_true_eq]
    constructor
    · have h := hc t ht 1 (by have := hwq t; omega)
      simpa [carry, statesQ, statesR] using h
    constructor
    · have h := hc t ht 2 (hwq t)
      simpa [carry, statesQ, statesR] using h
    · change overflow
        ((iterPairs q L t).2 0, (iterPairs q L t).2 1)
        (observedBit (iterPairs q L t).2 (iterPairs q L t).1) =
        overflow ((iterPairs r L t).2 0, (iterPairs r L t).2 1)
        (observedBit (iterPairs q L t).2 (iterPairs q L t).1)
      calc
        _ = carry (iterPairs q L t).2 (iterPairs q L t).1 :=
          prefix_overflow _ _ (iterPairs_admissible q L t hq) (hwq t)
        _ = carry (iterPairs r L t).2 (iterPairs r L t).1 := by
          rw [←hw t (by omega)]
          exact hc t ht _ (Nat.le_refl _)
        _ = _ := by
          rw [hbits t ht]
          exact (prefix_overflow _ _ (iterPairs_admissible r L t hr) (hwr t)).symm
  have hs : ∀ t, t < K → statesQ (t + 1) = next (statesQ t) (bits t) := by
    intro t ht
    exact prefix_step_exact _ _ (iterPairs_admissible q L t hq) (hwq t)
  have ht : ∀ t, t < K → statesR (t + 1) = next (statesR t) (bits t) := by
    intro t ht
    change _ = next ((iterPairs r L t).2 0, (iterPairs r L t).2 1)
      (observedBit (iterPairs q L t).2 (iterPairs q L t).1)
    rw [hbits t ht]
    exact prefix_step_exact _ _ (iterPairs_admissible r L t hr) (hwr t)
  have h := survives_of_trajectory statesQ statesR bits K hcomp hs ht
  simpa only [statesQ, statesR, iterPairs] using h

/-- Seven complete words exclude the witness orientation (1,-3), independently
of width and every coefficient beyond the first two. -/
theorem seven_carries_exclude_positive_witness_prefix
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 2 ≤ L)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ¬ (q 0 = r 0 + 1 ∧ r 1 = q 1 + 3) := by
  rintro ⟨hp, hq'⟩
  have hs := actual_history_survives q r L 7 hq hr hL hc
  have hf := seven_prefix_exclusion (q 0, q 1) (r 0, r 1)
    (prefix_valid q L hq hL) (prefix_valid r L hr hL) hp hq'
  rw [hf] at hs
  cases hs

/-- Swapping the two actual words excludes the opposite orientation as well. -/
theorem seven_carries_exclude_negative_witness_prefix
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 2 ≤ L)
    (hc : ∀ t, t < 7 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ¬ (r 0 = q 0 + 1 ∧ q 1 = r 1 + 3) := by
  apply seven_carries_exclude_positive_witness_prefix r q L hr hq hL
  intro t ht i hi
  have hw := matched_widths q r L t (fun j hj => hc j (by omega))
  have hi' : i ≤ (iterPairs q L t).1 := by rw [hw]; exact hi
  exact (hc t ht i hi').symm

theorem smooth_four_first_coefficients (f : Series) :
    smoothPow 4 f 0 = f 0 ∧
    smoothPow 4 f 1 = 4*f 0 + f 1 ∧
    smoothPow 4 f 2 = 6*f 0 + 4*f 1 + f 2 ∧
    smoothPow 4 f 3 = 4*f 0 + 6*f 1 + 4*f 2 + f 3 := by
  simp [smoothPow, smooth]
  omega

/-- A nonzero exterior coefficient in the four-smoothing unit box forces the
same (1,-3) prefix as the symmetric coefficient-six example, up to sign. -/
theorem smooth_four_nonzero_first_prefix (f : Series)
    (hf : ∀ i, -9 ≤ f i ∧ f i ≤ 9)
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1)
    (hn : f 0 ≠ 0) :
    (f 0 = 1 ∧ f 1 = -3) ∨ (f 0 = -1 ∧ f 1 = 3) := by
  rcases smooth_four_first_coefficients f with ⟨h0, h1, h2, h3⟩
  have hb0 := hg 0
  have hb1 := hg 1
  have hb2 := hg 2
  have hb3 := hg 3
  rw [h0] at hb0
  rw [h1] at hb1
  rw [h2] at hb2
  rw [h3] at hb3
  have hf1 := hf 1
  have hf2 := hf 2
  have hf3 := hf 3
  omega

/-- Universal eight-word exterior reconstruction. The initial addition may
overflow; no claim about all the interior pair coefficients is made here. -/
theorem eight_carries_determine_exterior_pair
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    q 0 = r 0 := by
  by_cases hN : 4 ≤ orbitCount q L 7
  · have h := iterPairs_endpoint_carry_history_injective q r L 7 hq hr
      (by intro t ht i hi; exact hc t (by omega) i hi) hN
    exact h 0 hq.1
  · have hlo := Agent10SevenStepCount.actual_seven_step_count_all_widths q L hq
    have hn : orbitCount q L 7 = 3 := by omega
    have hf := matched_difference_formula q r L 7 hq hr
      (fun t ht => hc t (by omega))
    have hb := cappedDiff_bounds (iterPairs q L 7).2 (iterPairs r L 7).2
      (iterPairs q L 7).1 (hc 7 (by decide))
    have hg : ∀ i, -1 ≤ smoothPow 4 (cappedDiff q r L) i ∧
        smoothPow 4 (cappedDiff q r L) i ≤ 1 := by
      intro i
      have hfi := hf i
      simp only [hn] at hfi
      change _ = 8 * smoothPow 4 (cappedDiff q r L) i at hfi
      have hbi := hb i
      omega
    apply Classical.byContradiction
    intro he
    have hz : cappedDiff q r L 0 ≠ 0 := by
      simp only [cappedDiff, if_pos hq.1]
      omega
    have hp := smooth_four_nonzero_first_prefix (cappedDiff q r L)
      (cappedDiff_bounds q r L (hc 0 (by decide))) hg hz
    by_cases hL : 2 ≤ L
    · have h1 : 1 < L := by omega
      simp only [cappedDiff, if_pos hq.1, if_pos h1] at hp
      rcases hp with hp | hp
      · apply seven_carries_exclude_positive_witness_prefix q r L hq hr hL
          (fun t ht => hc t (by omega))
        omega
      · apply seven_carries_exclude_negative_witness_prefix q r L hq hr hL
          (fun t ht => hc t (by omega))
        omega
    · have hi : ¬1 < L := by omega
      have hz1 : cappedDiff q r L 1 = 0 := by simp [cappedDiff, hi]
      rw [hz1] at hp
      omega

#print axioms survives_step_of
#print axioms survives_of_trajectory
#print axioms actual_history_survives
#print axioms seven_carries_exclude_positive_witness_prefix
#print axioms seven_carries_exclude_negative_witness_prefix
#print axioms smooth_four_first_coefficients
#print axioms smooth_four_nonzero_first_prefix
#print axioms eight_carries_determine_exterior_pair

end Agent10PrefixExclusion
