import DifferenceObservability
import Agent10SmoothingBoundary

/-!
Exact connection to the accepted repository operator. Original definitions and
proofs are imported unchanged. The eight-word result below has explicit extra
hypotheses; it is not a universal improvement of nine-word reconstruction.
-/
set_option maxHeartbeats 10000000
namespace Agent10SmoothingBridge
open DifferenceObservability CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- No zero-extension convention is changed by the explicit binomial formula. -/
theorem four_eq_smoothPow (f : Series) (i : Nat) :
    Agent10SmoothingBoundary.four f i = smoothPow 4 f i := by
  by_cases h0 : i = 0
  · subst i; simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag,
      smoothPow, smooth]
  by_cases h1 : i = 1
  · subst i; simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag,
      smoothPow, smooth]; omega
  by_cases h2 : i = 2
  · subst i; simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag,
      smoothPow, smooth]; omega
  by_cases h3 : i = 3
  · subst i; simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag,
      smoothPow, smooth]; omega
  have hi : 4 ≤ i := by omega
  have hi1 : i - 1 ≠ 0 := by omega
  have hi2 : i - 2 ≠ 0 := by omega
  have hi3 : i - 3 ≠ 0 := by omega
  have le1 : 1 ≤ i := by omega
  have le2 : 2 ≤ i := by omega
  have le3 : 3 ≤ i := by omega
  simp [Agent10SmoothingBoundary.four, Agent10SmoothingBoundary.lag,
    smoothPow, smooth, h0, hi1, hi2, hi3, le1, le2, le3, hi, Nat.sub_sub]
  omega

theorem smooth_four_rigidity_at_five (f : Series)
    (hf : ∀ i, -5 ≤ f i ∧ f i ≤ 5)
    (hg : ∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) :
    ∀ i, f i = 0 := by
  apply Agent10SmoothingBoundary.four_rigidity_at_five f hf
  intro i
  rw [four_eq_smoothPow]
  exact hg i

theorem smooth_four_symmetric_counterexample :
    ∃ f : Series, (∀ i, -6 ≤ f i ∧ f i ≤ 6) ∧
      (∀ i, -1 ≤ smoothPow 4 f i ∧ smoothPow 4 f i ≤ 1) ∧
      (∀ i, 11 ≤ i → f i = 0) ∧
      (∀ i : Fin 11, f i.val = f (10-i.val)) ∧ f 0 ≠ 0 := by
  refine ⟨Agent10SmoothingBoundary.witness,
    Agent10SmoothingBoundary.witness_bounds, ?_,
    Agent10SmoothingBoundary.witness_zero_after,
    Agent10SmoothingBoundary.witness_symmetric, by decide⟩
  intro i
  rw [←four_eq_smoothPow]
  exact Agent10SmoothingBoundary.four_witness_bounds i

/-- A concrete conditional improvement: the three-nonoverflow case closes
when the initial capped pair difference lies in [-5,5]. -/
theorem eight_carries_small_difference (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (hn : orbitCount q L 7 = 3)
    (hd : ∀ i, -5 ≤ cappedDiff q r L i ∧ cappedDiff q r L i ≤ 5) :
    ∀ i, i < L → q i = r i := by
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
  have hz := smooth_four_rigidity_at_five (cappedDiff q r L) hd hg
  intro i hi
  have h := hz i
  simp only [cappedDiff, if_pos hi] at h
  omega

/-- The small-difference premise can itself be proved from an initial
nonoverflow transition and two matching full carry words. -/
theorem initial_nonoverflow_difference_bound (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 2 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (ho : carry q L = 0) :
    ∀ i, -4 ≤ cappedDiff q r L i ∧ cappedDiff q r L i ≤ 4 := by
  have hf := matched_difference_formula q r L 1 hq hr
    (fun t ht => hc t (by omega))
  have hb := cappedDiff_bounds (iterPairs q L 1).2 (iterPairs r L 1).2
    (iterPairs q L 1).1 (hc 1 (by decide))
  have hn : orbitCount q L 1 = 1 := by
    simp [orbitCount, noOverflowCount, iterPairs, ho]
  intro i
  have hfi := hf i
  simp [hn, smoothPow] at hfi
  have hbi := hb i
  omega

theorem eight_carries_initial_nonoverflow (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (hn : orbitCount q L 7 = 3)
    (ho : carry q L = 0) :
    ∀ i, i < L → q i = r i := by
  apply eight_carries_small_difference q r L hq hr hc hn
  have h := initial_nonoverflow_difference_bound q r L hq hr
    (fun t ht => hc t (by omega)) ho
  intro i
  have hi := h i
  omega

#print axioms four_eq_smoothPow
#print axioms smooth_four_rigidity_at_five
#print axioms smooth_four_symmetric_counterexample
#print axioms eight_carries_small_difference
#print axioms initial_nonoverflow_difference_bound
#print axioms eight_carries_initial_nonoverflow
end Agent10SmoothingBridge
