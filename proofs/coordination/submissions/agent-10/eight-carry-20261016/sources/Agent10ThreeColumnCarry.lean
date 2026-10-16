import Agent10ThreeColumnExclusion

/-!
Agent #10: transport the finite three-column exclusion to the unchanged actual
normalizer and derive eight-word reconstruction of the second pair coefficient.
The first two coefficients are recovered universally; the rest are not covered.
-/

set_option maxHeartbeats 10000000
set_option maxRecDepth 100000

namespace Agent10ThreeColumnCarry
open CarryObservability Agent10PrefixExclusion Agent10ThreeColumnExclusion
open DifferenceObservability CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

theorem survives3_step_of (n : Nat) (s r : State3) (v : Bool)
    (hvs : Valid3 s) (hvr : Valid3 r)
    (hc : compatible3 s r v = true)
    (hs : survives3 n (next3 s v) (next3 r v) = true) :
    survives3 (n+1) s r = true := by
  have hds := decode_encode3 s hvs
  have hdr := decode_encode3 r hvr
  cases v <;> simp_all [survives3,survivesCode,compatibleCode,nextCode]

theorem survives3_of_trajectory (s r : Nat → State3) (bits : Nat → Bool) (K : Nat)
    (hv : ∀ t, t ≤ K → Valid3 (s t) ∧ Valid3 (r t))
    (hc : ∀ t, t < K → compatible3 (s t) (r t) (bits t) = true)
    (hs : ∀ t, t < K → s (t+1) = next3 (s t) (bits t))
    (hr : ∀ t, t < K → r (t+1) = next3 (r t) (bits t)) :
    survives3 K (s 0) (r 0) = true := by
  induction K generalizing s r bits with
  | zero => rfl
  | succ K ih =>
    apply survives3_step_of K (s 0) (r 0) (bits 0)
      (hv 0 (by omega)).1 (hv 0 (by omega)).2 (hc 0 (by omega))
    have h := ih (fun t => s (t+1)) (fun t => r (t+1))
      (fun t => bits (t+1))
      (by intro t ht; exact hv (t+1) (by omega))
      (by intro t ht; exact hc (t+1) (by omega))
      (by intro t ht; exact hs (t+1) (by omega))
      (by intro t ht; exact hr (t+1) (by omega))
    simpa only [hs 0 (by omega),hr 0 (by omega)] using h

/-- Every actual history agrees in the extra high carry at width-1 as well as
the three low carries and terminal overflow, including overlapping widths. -/
theorem actual_history_survives3 (q r : Nat → Nat) (L K : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 3 ≤ L)
    (hc : ∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    survives3 K (state3Of q) (state3Of r) = true := by
  let statesQ : Nat → State3 := fun t => state3Of (iterPairs q L t).2
  let statesR : Nat → State3 := fun t => state3Of (iterPairs r L t).2
  let bits : Nat → Bool := fun t =>
    observedBit3 (iterPairs q L t).2 (iterPairs q L t).1
  have hw : ∀ t, t ≤ K → (iterPairs q L t).1 = (iterPairs r L t).1 := by
    intro t ht
    exact matched_widths q r L t (fun j hj => hc j (by omega))
  have hwq : ∀ t, 3 ≤ (iterPairs q L t).1 := by
    intro t
    have h := iterPairs_width_ge_initial q L t
    omega
  have hwr : ∀ t, 3 ≤ (iterPairs r L t).1 := by
    intro t
    have h := iterPairs_width_ge_initial r L t
    omega
  have hbits : ∀ t, t < K →
      observedBit3 (iterPairs q L t).2 (iterPairs q L t).1 =
      observedBit3 (iterPairs r L t).2 (iterPairs r L t).1 := by
    intro t ht
    unfold observedBit3
    rw [←hw t (by omega),hc t ht ((iterPairs q L t).1-3) (by omega)]
  have hcomp : ∀ t, t < K → compatible3 (statesQ t) (statesR t) (bits t) = true := by
    intro t ht
    rcases prefix_carries3_exact _ _ (iterPairs_admissible q L t hq) (hwq t)
      with ⟨aq,bq,cq,uq,vq,hqf⟩
    rcases prefix_carries3_exact _ _ (iterPairs_admissible r L t hr) (hwr t)
      with ⟨ar,br,cr,ur,vr,hrf⟩
    simp only [compatible3,decide_eq_true_eq,statesQ,statesR,bits]
    rw [aq,ar,bq,br,cq,cr]
    refine ⟨hc t ht 1 (by have := hwq t; omega),
      hc t ht 2 (by have := hwq t; omega),hc t ht 3 (hwq t),?_,?_⟩
    · rw [vq,hbits t ht,vr,←hw t (by omega)]
      exact hc t ht _ (by omega)
    · rw [hqf,hbits t ht,hrf,←hw t (by omega)]
      exact hc t ht _ (Nat.le_refl _)
  have hs : ∀ t, t < K → statesQ (t+1) = next3 (statesQ t) (bits t) := by
    intro t ht
    exact prefix_step3_exact _ _ (iterPairs_admissible q L t hq) (hwq t)
  have ht : ∀ t, t < K → statesR (t+1) = next3 (statesR t) (bits t) := by
    intro t ht
    change _ = next3 (state3Of (iterPairs r L t).2)
      (observedBit3 (iterPairs q L t).2 (iterPairs q L t).1)
    rw [hbits t ht]
    exact prefix_step3_exact _ _ (iterPairs_admissible r L t hr) (hwr t)
  have hvalid : ∀ t, t ≤ K → Valid3 (statesQ t) ∧ Valid3 (statesR t) := by
    intro t ht
    exact ⟨state3_valid _ _ (iterPairs_admissible q L t hq) (hwq t),
      state3_valid _ _ (iterPairs_admissible r L t hr) (hwr t)⟩
  have h := survives3_of_trajectory statesQ statesR bits K hvalid hcomp hs ht
  simpa only [statesQ,statesR,iterPairs] using h

/-- The once-shifted witness prefix (0,1,-3) cannot share eight complete words,
for any width at least three and any remaining interior coefficients. -/
theorem eight_carries_exclude_positive_shifted_prefix
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 3 ≤ L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ¬ (q 0 = r 0 ∧ q 1 = r 1 + 1 ∧ r 2 = q 2 + 3) := by
  rintro ⟨hp,hq',hr'⟩
  have hs := actual_history_survives3 q r L 8 hq hr hL hc
  have hf := eight_three_prefix_exclusion (state3Of q) (state3Of r)
    (state3_valid q L hq hL) (state3_valid r L hr hL) hp hq' hr'
  rw [hf] at hs
  cases hs

theorem eight_carries_exclude_negative_shifted_prefix
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 3 ≤ L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ¬ (q 0 = r 0 ∧ r 1 = q 1 + 1 ∧ q 2 = r 2 + 3) := by
  rintro ⟨hp,hq',hr'⟩
  apply eight_carries_exclude_positive_shifted_prefix r q L hr hq hL
    (by
      intro t ht i hi
      have hw := matched_widths q r L t (fun j hj => hc j (by omega))
      have hi' : i ≤ (iterPairs q L t).1 := by rw [hw]; exact hi
      exact (hc t ht i hi').symm)
  exact ⟨hp.symm,hq',hr'⟩

/-- Eight complete words recover the second pair coefficient at every width
where that coefficient is active. No initial-nonoverflow premise is needed. -/
theorem eight_carries_determine_second_pair
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 2 ≤ L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    q 1 = r 1 := by
  have he0 := eight_carries_determine_exterior_pair q r L hq hr hc
  have h1 : 1 < L := by omega
  by_cases hN : 4 ≤ orbitCount q L 7
  · have h := iterPairs_endpoint_carry_history_injective q r L 7 hq hr
      (by intro t ht i hi; exact hc t (by omega) i hi) hN
    exact h 1 h1
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
      change _ = 8*smoothPow 4 (cappedDiff q r L) i at hfi
      have hbi := hb i
      omega
    have hz0 : cappedDiff q r L 0 = 0 := by
      simp only [cappedDiff,if_pos hq.1,he0,Int.sub_self]
    have hshift := smoothPow_tail (cappedDiff q r L) 1 4
      (by
        intro j hj
        have hj0 : j = 0 := by omega
        simpa only [hj0] using hz0)
    let g : Series := fun i => cappedDiff q r L (1+i)
    have hgf : ∀ i, -9 ≤ g i ∧ g i ≤ 9 := by
      intro i
      exact cappedDiff_bounds q r L (hc 0 (by decide)) (1+i)
    have hgg : ∀ i, -1 ≤ smoothPow 4 g i ∧ smoothPow 4 g i ≤ 1 := by
      intro i
      change -1 ≤ smoothPow 4 (fun j => cappedDiff q r L (1+j)) i ∧
        smoothPow 4 (fun j => cappedDiff q r L (1+j)) i ≤ 1
      rw [hshift i]
      exact hg (1+i)
    apply Classical.byContradiction
    intro he
    have hz : g 0 ≠ 0 := by
      change cappedDiff q r L 1 ≠ 0
      simp only [cappedDiff,if_pos h1]
      omega
    have hp := smooth_four_nonzero_first_prefix g hgf hgg hz
    change (cappedDiff q r L 1 = 1 ∧ cappedDiff q r L 2 = -3) ∨
      (cappedDiff q r L 1 = -1 ∧ cappedDiff q r L 2 = 3) at hp
    by_cases hL3 : 3 ≤ L
    · have h2 : 2 < L := by omega
      simp only [cappedDiff,if_pos h1,if_pos h2] at hp
      rcases hp with hp | hp
      · apply eight_carries_exclude_positive_shifted_prefix q r L hq hr hL3 hc
        exact ⟨he0,by omega,by omega⟩
      · apply eight_carries_exclude_negative_shifted_prefix q r L hq hr hL3 hc
        exact ⟨he0,by omega,by omega⟩
    · have hi : ¬2 < L := by omega
      have hz2 : cappedDiff q r L 2 = 0 := by simp [cappedDiff,hi]
      rw [hz2] at hp
      omega

theorem eight_carries_determine_first_two_pairs
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 2 ≤ L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    q 0 = r 0 ∧ q 1 = r 1 :=
  ⟨eight_carries_determine_exterior_pair q r L hq hr hc,
    eight_carries_determine_second_pair q r L hq hr hL hc⟩

/-- Only active coordinates are asserted at widths one and two. -/
theorem eight_carries_determine_first_two_active_pairs
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < 2 → i < L → q i = r i := by
  intro i hi hiL
  have hi' : i = 0 ∨ i = 1 := by omega
  rcases hi' with hi' | hi'
  · simpa only [hi'] using eight_carries_determine_exterior_pair q r L hq hr hc
  · have hL : 2 ≤ L := by omega
    simpa only [hi'] using eight_carries_determine_second_pair q r L hq hr hL hc

#print axioms survives3_step_of
#print axioms survives3_of_trajectory
#print axioms actual_history_survives3
#print axioms eight_carries_exclude_positive_shifted_prefix
#print axioms eight_carries_exclude_negative_shifted_prefix
#print axioms eight_carries_determine_second_pair
#print axioms eight_carries_determine_first_two_pairs
#print axioms eight_carries_determine_first_two_active_pairs

end Agent10ThreeColumnCarry
