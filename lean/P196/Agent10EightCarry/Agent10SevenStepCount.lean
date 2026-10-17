import P196.Agent10EightCarry.DifferenceObservability

/-!
Agent #10: every seven actual decimal reverse-and-add transitions contain at
least three nonoverflow transitions.  The two-column graph, its rank data,
and its actual-word inclusion are imported unchanged from the accepted source.
The finite checks below are kernel proofs; no new transition rule or oracle is
introduced.  The final endpoint includes every positive admissible width.
-/
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Agent10SevenStepCount

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open CarryObservabilityActual

/-- The retained rank table already certifies three at horizon seven. -/
theorem rank_seven_minimum_fin :
    ∀ p : Fin 18, ∀ q : Fin 19,
      3 ≤ CarryObservability.rank 7 (p.val + 1, q.val) := by
  decide +kernel

theorem rank_seven_minimum (s : CarryObservability.State)
    (hs : CarryObservability.Valid s) :
    3 ≤ CarryObservability.rank 7 s := by
  rcases s with ⟨p, q⟩
  rcases hs with ⟨hp, hp', hq⟩
  have h := rank_seven_minimum_fin ⟨p - 1, by omega⟩ ⟨q, by omega⟩
  have he : p - 1 + 1 = p := by omega
  simpa only [he] using h

/-- The minimum ranges over both choices of the inner carry at every step. -/
theorem seven_step_minimum (s : CarryObservability.State)
    (hs : CarryObservability.Valid s) :
    3 ≤ CarryObservability.minCost 7 s := by
  exact Nat.le_trans (rank_seven_minimum s hs)
    (CarryObservability.rank_le_minCost 7 s (by decide) hs)

theorem seven_step_path_bound (s : CarryObservability.State)
    (hs : CarryObservability.Valid s) (vs : List Bool)
    (hlen : vs.length = 7) :
    3 ≤ CarryObservability.pathCost s vs := by
  have h := CarryObservability.minCost_le_pathCost s vs
  rw [hlen] at h
  exact Nat.le_trans (seven_step_minimum s hs) h

/-- Rank telescoping for any trajectory of the unchanged necessary graph. -/
theorem seven_step_trajectory_bound
    (states : Nat → CarryObservability.State) (bits : Nat → Bool)
    (count : Nat → Nat)
    (hstart : count 0 = 0)
    (hvalid : ∀ t, t ≤ 7 → CarryObservability.Valid (states t))
    (hnext : ∀ t, t < 7 →
      states (t + 1) = CarryObservability.next (states t) (bits t))
    (hcount : ∀ t, t < 7 →
      count (t + 1) = count t + CarryObservability.cost (states t) (bits t)) :
    3 ≤ count 7 := by
  have hpot : ∀ t, t ≤ 7 →
      3 ≤ count t + CarryObservability.rank (7 - t) (states t) := by
    intro t
    induction t with
    | zero =>
      intro _
      simpa only [Nat.sub_zero, hstart, Nat.zero_add] using
        rank_seven_minimum (states 0) (hvalid 0 (by decide))
    | succ t ih =>
      intro ht
      have hh := ih (by omega)
      have hs := CarryObservability.rank_step (6 - t) (states t)
        (by omega) (hvalid t (by omega)) (bits t)
      have ha : 6 - t + 1 = 7 - t := by omega
      rw [ha, ←hnext t (by omega)] at hs
      have hc := hcount t (by omega)
      have hb : 7 - (t + 1) = 6 - t := by omega
      rw [hb]
      omega
  have h := hpot 7 (by decide)
  simpa [CarryObservability.rank] using h

/-- Exact actual-word transport, including overlapping width-two/three cases. -/
theorem actual_seven_step_count (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) :
    3 ≤ orbitCount q L 7 := by
  let states : Nat → CarryObservability.State := fun t =>
    ((iterPairs q L t).2 0, (iterPairs q L t).2 1)
  let bits : Nat → Bool := fun t =>
    observedBit (iterPairs q L t).2 (iterPairs q L t).1
  have hw : ∀ t, 2 ≤ (iterPairs q L t).1 := by
    intro t
    have h := iterPairs_width_ge_initial q L t
    omega
  apply seven_step_trajectory_bound states bits (orbitCount q L)
  · rfl
  · intro t _
    exact prefix_valid _ _ (iterPairs_admissible q L t ha) (hw t)
  · intro t _
    exact prefix_step_exact _ _ (iterPairs_admissible q L t ha) (hw t)
  · intro t _
    change orbitCount q L t +
        (if carry (iterPairs q L t).2 (iterPairs q L t).1 = 0 then 1 else 0) =
      orbitCount q L t + CarryObservability.cost _ _
    rw [cost_eq_nooverflow _ _ (iterPairs_admissible q L t ha) (hw t)]

/-- The width-one case exhausts the 18 possible positive input coefficients. -/
theorem singleton_seven_count :
    ∀ a : Fin 18, 3 ≤ orbitCount (fun _ => a.val + 1) 1 7 := by
  decide +kernel

/-- All-width endpoint: no extra prefix, carry-pattern, or count premise. -/
theorem actual_seven_step_count_all_widths (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    3 ≤ orbitCount q L 7 := by
  by_cases hL : 2 ≤ L
  · exact actual_seven_step_count q L ha hL
  · have hp := ha.1
    have heL : L = 1 := by omega
    subst L
    have hq0 := ha.2.1
    have hq0' := ha.2.2.1 0 (by decide)
    have hidx : q 0 - 1 < 18 := by omega
    have h := singleton_seven_count ⟨q 0 - 1, hidx⟩
    change 3 ≤ orbitCount (fun _ => q 0 - 1 + 1) 1 7 at h
    have heq : q 0 - 1 + 1 = q 0 := by omega
    rw [heq] at h
    have he : ∀ i, i < 1 → q i = (fun _ => q 0) i := by
      intro i hi
      have hz : i = 0 := by omega
      subst i
      rfl
    rw [orbitCount_congr q (fun _ => q 0) 1 7 he]
    exact h

#print axioms rank_seven_minimum_fin
#print axioms rank_seven_minimum
#print axioms seven_step_minimum
#print axioms seven_step_path_bound
#print axioms seven_step_trajectory_bound
#print axioms actual_seven_step_count
#print axioms singleton_seven_count
#print axioms actual_seven_step_count_all_widths

end Agent10SevenStepCount
