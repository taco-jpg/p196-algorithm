import resume_carry_history

namespace CarryHistory
open DecimalDigits FoldedDecimal OverflowCarryNormalization

/-- A finite outer-digit potential controlling the total number of overflows. -/
def outerPotential : Nat → Nat
  | 4 | 6 | 7 | 8 | 10 | 11 | 12 | 14 => 1
  | 9 | 13 | 15 | 16 | 17 => 2
  | 18 => 3
  | _ => 0

theorem outerPotential_bounded (a : Nat) : outerPotential a ≤ 3 := by
  unfold outerPotential
  split <;> omega

private theorem finite_no_overflow :
    ∀ a ∈ List.range 19, ∀ b ∈ [0,1], 0<a → a+b<10 →
      outerPotential (2*a+b)+1 ≤ outerPotential a+2 := by decide

private theorem finite_overflow :
    ∀ a ∈ List.range 19, ∀ b ∈ [0,1], 0<a → 10≤a+b →
      outerPotential (a+1-10*(a/10))+1 ≤ outerPotential a := by decide

/-- Every exact step satisfies the potential inequality, including the
neutral outer symbol9 and both possible incoming carries from the interior. -/
theorem outer_potential_step (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    outerPotential (nextColumns q L 0)+1 ≤ outerPotential (q 0)+
      2*(if carry q L=0 then 1 else 0) := by
  have hL := ha.1
  have houter := ha.2.1
  have hbound := ha.2.2.1 0 hL
  have hs := ha.2.2.2.1 0 hL
  simp only [Nat.sub_zero] at hs
  have hb := carry_bounded q L ha.2.2.1 (L-1) (by omega)
  have hfinal := carry_bounded q L ha.2.2.1 L (by omega)
  have hind : L=(L-1)+1 := by omega
  have hlast : carry q L=(q 0+carry q (L-1))/10 := by
    calc
      carry q L = carry q ((L-1)+1) := congrArg (carry q) hind
      _ = (q (L-1)+carry q (L-1))/10 := rfl
      _ = (q 0+carry q (L-1))/10 := by rw [←hs]
  have hmem : q 0 ∈ List.range 19 := by simp; omega
  have hbmem : carry q (L-1) ∈ [0,1] := by simp; omega
  by_cases hover : carry q L=0
  · have hsmall : q 0+carry q (L-1)<10 := by omega
    have hfirst : carry q 1=0 := by simp only [carry]; omega
    have he := next_column_no_overflow q L 0 hL ha.2.2.2.1 hover
    simp only [Nat.zero_add,Nat.sub_zero,carry,hover,hfirst] at he
    have hv := finite_no_overflow (q 0) hmem (carry q (L-1)) hbmem houter hsmall
    have hout : nextColumns q L 0=2*q 0+carry q (L-1) := by omega
    simpa only [hout,hover,if_true] using hv
  · have hsmall : 10≤q 0+carry q (L-1) := by omega
    have hc : carry q L=1 := by omega
    have he := next_column_overflow_outer q L hL hc
    have hf : carry q 1=q 0/10 := by simp [carry]
    rw [hf] at he
    have hout : nextColumns q L 0=q 0+1-10*(q 0/10) := by omega
    have hv := finite_overflow (q 0) hmem (carry q (L-1)) hbmem houter hsmall
    simpa only [hout,hover,if_false,Nat.mul_zero,Nat.add_zero] using hv

/-- Telescoping the potential bounds the number of non-overflows from below. -/
theorem nonoverflow_growth_bound (q : Nat → Nat) (L K : Nat) (ha : Admissible L q) :
    K ≤ 2*noOverflowCount (fun t => (iterPairs q L t).2)
      (fun t => (iterPairs q L t).1) K + 3 := by
  have hp : ∀ k : Nat,
      outerPotential ((iterPairs q L k).2 0)+k ≤ outerPotential (q 0)+
        2*noOverflowCount (fun t => (iterPairs q L t).2)
          (fun t => (iterPairs q L t).1) k := by
    intro k
    induction k with
    | zero => simp [iterPairs,noOverflowCount]
    | succ k ih =>
      have had := iterPairs_admissible q L k ha
      have hs := outer_potential_step (iterPairs q L k).2 (iterPairs q L k).1 had
      simp only [iterPairs,noOverflowCount]
      omega
  have h := hp K
  have hb := outerPotential_bounded (q 0)
  omega

/-- Twelve complete consecutive carry words determine the initial pair-sum
word. This is a fully numeric exact-dynamics statement, with no unproved
growth assumption and no bound on the number of initial digits. -/
theorem twelve_carry_words_determine_pair_sums (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 12 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i=r i := by
  apply iterPairs_carry_history_injective q r L 12 hq hr hc
  have h := nonoverflow_growth_bound q L 12 hq
  omega

#print axioms outer_potential_step
#print axioms nonoverflow_growth_bound
#print axioms twelve_carry_words_determine_pair_sums
end CarryHistory
