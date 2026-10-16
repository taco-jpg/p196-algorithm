import resume_renewal_extraction
import resume_normalization_bridge

namespace CarryHistory
open DecimalDigits FoldedDecimal

/-- When complete carries agree, the first differing pair-sum coefficient
is doubled by non-overflow and unchanged by overflow. -/
theorem next_first_difference (q r : Nat → Nat) (L m : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hm : m < L)
    (hlow : ∀ j, j < m → q j = r j)
    (hc : ∀ j, j ≤ L → carry q j = carry r j) :
    (nextColumns q L m : Int) - nextColumns r L m =
      (if carry q L=0 then 2 else 1) * ((q m : Int)-r m) := by
  have hcm := hc L (by omega)
  by_cases ho : carry q L=0
  · have hor : carry r L=0 := by omega
    have hqnext := next_column_no_overflow q L m hm hq.2.2.2.1 ho
    have hrnext := next_column_no_overflow r L m hm hr.2.2.2.1 hor
    rw [←hc (m+1) (by omega), ←hc (L-m) (by omega),
      ←hc m (by omega), ←hc (L-1-m) (by omega)] at hrnext
    simp only [ho,if_true]
    omega
  · have hoq : carry q L=1 := by
      have := carry_bounded q L hq.2.2.1 L (by omega)
      omega
    have hor : carry r L=1 := by omega
    simp only [ho,if_false,Int.one_mul]
    by_cases hz : m=0
    · subst m
      have hqnext := next_column_overflow_outer q L hq.1 hoq
      have hrnext := next_column_overflow_outer r L hr.1 hor
      rw [←hc 1 (by omega)] at hrnext
      omega
    · have hqnext := next_column_overflow_interior q L m (by omega) hm hq.2.2.2.1 hoq
      have hrnext := next_column_overflow_interior r L m (by omega) hm hr.2.2.2.1 hor
      rw [←hc (m+1) (by omega), ←hc (L-m+1) (by omega),
        ←hc m (by omega), ←hc (L-m) (by omega), ←hlow (m-1) (by omega)] at hrnext
      omega

/-- No earlier difference is introduced when the carry words agree. -/
theorem next_lower_equal (q r : Nat → Nat) (L m : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hm : m < L)
    (hlow : ∀ j, j < m → q j = r j)
    (hc : ∀ j, j ≤ L → carry q j = carry r j) :
    ∀ j, j < m → nextColumns q L j = nextColumns r L j := by
  intro j hj
  have he := next_first_difference q r L j hq hr (by omega)
    (fun k hk => hlow k (by omega)) hc
  rw [hlow j hj] at he
  simp only [Int.sub_self,Int.mul_zero] at he
  omega

def noOverflowCount (left : Nat → Nat → Nat) (width : Nat → Nat) : Nat → Nat
  | 0 => 0
  | k+1 => noOverflowCount left width k + if carry (left k) (width k)=0 then 1 else 0

/-- This statement concerns genuine exact pair-sum dynamics with a shared
width and identical complete carry words, not an approximate model. -/
theorem first_difference_over_time
    (left right : Nat → Nat → Nat) (width : Nat → Nat) (K m : Nat)
    (ha : ∀ t, t ≤ K → Admissible (width t) (left t))
    (hb : ∀ t, t ≤ K → Admissible (width t) (right t))
    (hw : ∀ t, t < K → width (t+1)=nextWidth (left t) (width t))
    (hl : ∀ t, t < K → ∀ i, i < width (t+1) →
      left (t+1) i = nextColumns (left t) (width t) i)
    (hr : ∀ t, t < K → ∀ i, i < width (t+1) →
      right (t+1) i = nextColumns (right t) (width t) i)
    (hc : ∀ t, t < K → ∀ i, i ≤ width t → carry (left t) i = carry (right t) i)
    (hm : m < width 0)
    (hfirst : ∀ j, j < m → left 0 j = right 0 j) :
    m < width K ∧ (∀ j, j < m → left K j=right K j) ∧
      (left K m : Int)-right K m =
        (2:Int)^(noOverflowCount left width K) * ((left 0 m : Int)-right 0 m) := by
  have hind : ∀ t, t ≤ K → m < width t ∧
      (∀ j, j < m → left t j=right t j) ∧
      (left t m : Int)-right t m =
        (2:Int)^(noOverflowCount left width t) * ((left 0 m : Int)-right 0 m) := by
    intro t
    induction t with
    | zero => intro _; simpa [noOverflowCount] using And.intro hm hfirst
    | succ t ih =>
      intro ht
      obtain ⟨hmt,hlo,hdelta⟩ := ih (by omega)
      have hgt : width t ≤ width (t+1) := by
        rw [hw t (by omega)]
        unfold nextWidth
        split <;> omega
      have hmnext : m < width (t+1) := by omega
      refine ⟨hmnext,?_,?_⟩
      · intro j hj
        rw [hl t (by omega) j (by omega),hr t (by omega) j (by omega)]
        exact next_lower_equal (left t) (right t) (width t) m
          (ha t (by omega)) (hb t (by omega)) hmt hlo (hc t (by omega)) j hj
      · rw [hl t (by omega) m hmnext,hr t (by omega) m hmnext]
        rw [next_first_difference (left t) (right t) (width t) m
          (ha t (by omega)) (hb t (by omega)) hmt hlo (hc t (by omega)),hdelta]
        by_cases ho : carry (left t) (width t)=0
        · simp [noOverflowCount,ho,Int.pow_succ,Int.mul_assoc,Int.mul_comm,Int.mul_left_comm]
        · simp [noOverflowCount,ho]
  exact hind K (by omega)

/-- Five non-overflow steps in identical complete carry histories determine
the whole initial pair-sum word. This does not claim uniqueness of the
initial integer, whose individual digit splits are invisible to q. -/
theorem five_nonoverflows_determine_pair_sums
    (left right : Nat → Nat → Nat) (width : Nat → Nat) (K : Nat)
    (ha : ∀ t, t ≤ K → Admissible (width t) (left t))
    (hb : ∀ t, t ≤ K → Admissible (width t) (right t))
    (hw : ∀ t, t < K → width (t+1)=nextWidth (left t) (width t))
    (hl : ∀ t, t < K → ∀ i, i < width (t+1) →
      left (t+1) i = nextColumns (left t) (width t) i)
    (hr : ∀ t, t < K → ∀ i, i < width (t+1) →
      right (t+1) i = nextColumns (right t) (width t) i)
    (hc : ∀ t, t < K → ∀ i, i ≤ width t → carry (left t) i = carry (right t) i)
    (hfive : 5 ≤ noOverflowCount left width K) :
    ∀ i, i < width 0 → left 0 i=right 0 i := by
  have hpow : ∀ n : Nat, (1:Int) ≤ (2:Int)^n := by
    intro n
    induction n with
    | zero => decide
    | succ n ih => rw [Int.pow_succ]; omega
  have hp : (32:Int) ≤ (2:Int)^(noOverflowCount left width K) := by
    have hsum : noOverflowCount left width K = (noOverflowCount left width K-5) + 5 := by omega
    rw [hsum]
    have := hpow (noOverflowCount left width K-5)
    change 32 ≤ ((((((2:Int)^(noOverflowCount left width K-5))*2)*2)*2)*2)*2
    omega
  intro i
  induction i using Nat.strongRecOn with
  | ind i ih =>
    intro hi
    have hfirst : ∀ j, j < i → left 0 j=right 0 j := by
      intro j hj
      exact ih j hj (by omega)
    obtain ⟨hiK,_,hd⟩ := first_difference_over_time left right width K i
      ha hb hw hl hr hc hi hfirst
    have hleft := (ha K (by omega)).2.2.1 i hiK
    have hright := (hb K (by omega)).2.2.1 i hiK
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

open OverflowCarryNormalization

theorem iterPairs_admissible (q : Nat → Nat) (L k : Nat) (ha : Admissible L q) :
    Admissible (iterPairs q L k).1 (iterPairs q L k).2 := by
  induction k with
  | zero => exact ha
  | succ k ih => exact NormalizationBridge.admissible_next _ _ ih

/-- Direct exact-orbit version: equal complete carries through a horizon with
five non-overflows force equality of the initial q words. -/
theorem iterPairs_carry_history_injective (q r : Nat → Nat) (L K : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (hfive : 5 ≤ noOverflowCount (fun t => (iterPairs q L t).2)
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
  apply five_nonoverflows_determine_pair_sums
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
  · exact hfive


#print axioms next_first_difference
#print axioms first_difference_over_time
#print axioms five_nonoverflows_determine_pair_sums
#print axioms iterPairs_carry_history_injective
end CarryHistory
