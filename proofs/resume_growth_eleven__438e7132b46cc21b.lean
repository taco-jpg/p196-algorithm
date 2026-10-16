import resume_growth_history
namespace CarryHistory
open DecimalDigits FoldedDecimal OverflowCarryNormalization

theorem four_nonoverflows_and_endpoint_determine_pair_sums
    (left right : Nat → Nat → Nat) (width : Nat → Nat) (K : Nat)
    (ha : ∀ t, t ≤ K → Admissible (width t) (left t))
    (hb : ∀ t, t ≤ K → Admissible (width t) (right t))
    (hw : ∀ t, t < K → width (t+1)=nextWidth (left t) (width t))
    (hl : ∀ t, t < K → ∀ i, i < width (t+1) →
      left (t+1) i = nextColumns (left t) (width t) i)
    (hr : ∀ t, t < K → ∀ i, i < width (t+1) →
      right (t+1) i = nextColumns (right t) (width t) i)
    (hc : ∀ t, t ≤ K → ∀ i, i ≤ width t → carry (left t) i = carry (right t) i)
    (hfour : 4 ≤ noOverflowCount left width K) :
    ∀ i, i < width 0 → left 0 i=right 0 i := by
  have hpow : ∀ n : Nat, (1:Int) ≤ (2:Int)^n := by
    intro n
    induction n with
    | zero => decide
    | succ n ih => rw [Int.pow_succ]; omega
  have hp : (16:Int) ≤ (2:Int)^(noOverflowCount left width K) := by
    have hsum : noOverflowCount left width K = (noOverflowCount left width K-4) + 4 := by omega
    rw [hsum]
    have := hpow (noOverflowCount left width K-4)
    change 16 ≤ (((((2:Int)^(noOverflowCount left width K-4))*2)*2)*2)*2
    omega
  intro i
  induction i using Nat.strongRecOn with
  | ind i ih =>
    intro hi
    have hfirst : ∀ j, j < i → left 0 j=right 0 j := by
      intro j hj
      exact ih j hj (by omega)
    obtain ⟨hiK,_,hd⟩ := first_difference_over_time left right width K i
      ha hb hw hl hr (fun t ht => hc t (by omega)) hi hfirst
    have hleft := output_bounded (left K) i
    have hright := output_bounded (right K) i
    have hle := column_equation (left K) i
    have hre := column_equation (right K) i
    rw [←hc K (by omega) i (by omega), ←hc K (by omega) (i+1) (by omega)] at hre
    by_cases he : left 0 i=right 0 i
    · exact he
    · have hz : (left 0 i : Int)-right 0 i ≤ -1 ∨
          1 ≤ (left 0 i : Int)-right 0 i := by omega
      rcases hz with hz|hz
      · have hmul := Int.mul_le_mul_of_nonneg_left hz
          (by omega : (0:Int) ≤ (2:Int)^noOverflowCount left width K)
        simp only [Int.mul_neg,Int.mul_one] at hmul
        omega
      · have hmul := Int.mul_le_mul_of_nonneg_left hz
          (by omega : (0:Int) ≤ (2:Int)^noOverflowCount left width K)
        simp only [Int.mul_one] at hmul
        omega

theorem iterPairs_endpoint_carry_history_injective (q r : Nat → Nat) (L K : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t ≤ K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (hfour : 4 ≤ noOverflowCount (fun t => (iterPairs q L t).2)
      (fun t => (iterPairs q L t).1) K) :
    ∀ i, i < L → q i = r i := by
  have hw : ∀ t, t ≤ K → (iterPairs q L t).1=(iterPairs r L t).1 := by
    intro t
    induction t with
    | zero => intro _; rfl
    | succ t ih =>
      intro ht
      have he := ih (by omega)
      have hcarry := hc t (by omega) (iterPairs q L t).1 (by omega)
      simp only [iterPairs]
      change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 =
        nextWidth (iterPairs r L t).2 (iterPairs r L t).1
      rw [←he]
      unfold nextWidth
      rw [hcarry]
  apply four_nonoverflows_and_endpoint_determine_pair_sums
    (fun t => (iterPairs q L t).2) (fun t => (iterPairs r L t).2)
    (fun t => (iterPairs q L t).1) K
  · intro t _; exact iterPairs_admissible q L t hq
  · intro t ht; rw [hw t ht]; exact iterPairs_admissible r L t hr
  · intro t _; rfl
  · intro t _ i _; rfl
  · intro t ht i _
    change nextColumns (iterPairs r L t).2 (iterPairs r L t).1 i =
      nextColumns (iterPairs r L t).2 (iterPairs q L t).1 i
    rw [hw t (by omega)]
  · exact hc
  · exact hfour


/-- Eleven complete carry words determine the pair-sum state. The endpoint
carry word narrows each possible difference to[-9,9], sharpening the
previous twelve-word bound. This statement does not claim optimality. -/
theorem eleven_carry_words_determine_pair_sums (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 11 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i=r i := by
  apply iterPairs_endpoint_carry_history_injective q r L 10 hq hr
  · intro t ht i hi
    exact hc t (by omega) i hi
  · have h := nonoverflow_growth_bound q L 10 hq
    omega

#print axioms four_nonoverflows_and_endpoint_determine_pair_sums
#print axioms eleven_carry_words_determine_pair_sums
end CarryHistory
