import FamilyStates

namespace Agent13ProductWeights
open DecimalDigits FoldedDecimal Agent13FoldedFamily
open scoped BigOperators

noncomputable section

def blockWeight (a : Nat → ℝ) (e : Bool) : ℝ := if e then a 14 ^ 2 * a 4 ^ 2 else a 9 ^ 4

def coefficientWeight (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ) (s : FiniteWord) : ℝ :=
  if s.1 % 2 = 0 then A s.1 * ∏ i ∈ Finset.range (s.1/2), a (digits s i) else oddWeight s

theorem coefficientWeight_pos (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L%2=0 → 0 < A L) (ha : ∀ i, i ≤ 18 → 0 < a i)
    (ho : ∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s)
    (s : FiniteWord) (hs : SafeState s) :
    0 < coefficientWeight A a oddWeight s := by
  unfold coefficientWeight
  split
  · apply mul_pos (hA _ hs.1.1 ‹_›)
    apply Finset.prod_pos
    intro i _
    exact ha _ (digits_bounded s i)
  · exact ho s hs ‹_›

theorem encoded_reflection_weight (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (H : Nat → Nat) (h : Nat) (hb : ∀ i, i < 2*h → reflectHalf H h i ≤ 18) :
    coefficientWeight A a oddWeight (encodeWord (reflectHalf H h) (2*h) hb) =
      A (2*h) * ∏ i ∈ Finset.range h, a (H i) := by
  simp only [coefficientWeight,encodeWord_width,show (2*h)%2=0 by omega,if_true,show 2*h/2=h by omega]
  congr 1
  apply Finset.prod_congr rfl
  intro i hi
  have hi' := Finset.mem_range.mp hi
  rw [digits_encodeWord _ _ _ i (by omega),reflect_low H h i hi']

theorem single_block_product (a : Nat → ℝ) (e : Bool) :
    (∏ i ∈ Finset.range 4, a (blockDigit e i)) = blockWeight a e := by
  cases e <;> norm_num [Finset.prod_range_succ,blockDigit,blockWeight] <;> ring

theorem all_blocks_product (a : Nat → ℝ) (e : Nat → Bool) (r : Nat) :
    (∏ i ∈ Finset.range (4*r), a (blockDigit (e (i/4)) (i%4))) =
      ∏ j ∈ Finset.range r, blockWeight a (e j) := by
  induction r with
  | zero => simp
  | succ r ih =>
    rw [show 4*(r+1)=4*r+4 by omega,Finset.prod_range_add,ih,Finset.prod_range_succ (fun j => blockWeight a (e j)) r]
    congr 1
    rw [← single_block_product a (e r)]
    apply Finset.prod_congr rfl
    intro i hi
    have hb := Finset.mem_range.mp hi
    have hd : (4*r+i)/4=r := by omega
    have hr : (4*r+i)%4=i := by omega
    rw [hd,hr]

theorem input_half_product (a : Nat → ℝ) (e : Nat → Bool) (r k : Nat) :
    (∏ i ∈ Finset.range (halfWidth r k), a (inputHalf e r i)) =
      a 5 * a 14 * a 18 ^ k * ∏ j ∈ Finset.range r, blockWeight a (e j) := by
  have hpre : (∏ i ∈ Finset.range (4*r+1), a (inputHalf e r i)) =
      (∏ j ∈ Finset.range r, blockWeight a (e j)) * a 5 := by
    rw [Finset.prod_range_succ']
    have hp : (∏ i ∈ Finset.range (4*r), a (inputHalf e r (i+1))) =
        ∏ j ∈ Finset.range r, blockWeight a (e j) := by
      rw [← all_blocks_product a e r]
      apply Finset.prod_congr rfl
      intro i hi
      have hb := Finset.mem_range.mp hi
      simp [inputHalf,show i+1 < 4*r+1 by omega]
    rw [hp]
    simp [inputHalf]
  have htail : (∏ i ∈ Finset.range (k+1), a (inputHalf e r (4*r+1+i))) = a 18^k * a 14 := by
    rw [Finset.prod_range_succ']
    have hp : (∏ i ∈ Finset.range k, a (inputHalf e r (4*r+1+(i+1)))) = a 18^k := by
      have he : ∀ i, a (inputHalf e r (4*r+1+(i+1))) = a 18 := by
        intro i
        simp [inputHalf,show 4*r+1+(i+1) ≠ 0 by omega,
          show ¬ 4*r+1+(i+1) < 4*r+1 by omega,
          show 4*r+1+(i+1) ≠ 4*r+1 by omega]
      simp_rw [he]
      simp
    rw [hp]
    simp [inputHalf]
  have hw : halfWidth r k = (4*r+1)+(k+1) := by unfold halfWidth; omega
  rw [hw,Finset.prod_range_add,hpre,htail]
  ring

theorem target_half_product (a : Nat → ℝ) (r k : Nat) :
    (∏ i ∈ Finset.range (halfWidth r k), a (targetHalf r i)) =
      a 11 * a 9^(4*r+1) * a 18^k := by
  have hpre : (∏ i ∈ Finset.range (4*r+2), a (targetHalf r i)) = a 9^(4*r+1) * a 11 := by
    rw [show 4*r+2=(4*r+1)+1 by omega,Finset.prod_range_succ']
    have hp : (∏ i ∈ Finset.range (4*r+1), a (targetHalf r (i+1))) = a 9^(4*r+1) := by
      calc
        _ = ∏ _i ∈ Finset.range (4*r+1), a 9 := by
          apply Finset.prod_congr rfl
          intro i hi
          have hb := Finset.mem_range.mp hi
          simp [targetHalf,show i+1 ≤ 4*r+1 by omega]
        _ = _ := by simp
    rw [hp]
    simp [targetHalf]
  have htail : (∏ i ∈ Finset.range k, a (targetHalf r (4*r+2+i))) = a 18^k := by
    have he : ∀ i, a (targetHalf r (4*r+2+i)) = a 18 := by
      intro i
      simp [targetHalf,show 4*r+2+i ≠ 0 by omega,show ¬ 4*r+2+i ≤ 4*r+1 by omega]
    simp_rw [he]
    simp
  have hw : halfWidth r k = (4*r+2)+k := by unfold halfWidth; omega
  rw [hw,Finset.prod_range_add,hpre,htail]
  ring

theorem familyState_weight (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (r k : Nat) (e : Fin r → Bool) :
    coefficientWeight A a oddWeight (familyState r k e) =
      A (2*halfWidth r k) * a 5 * a 14 * a 18^k * ∏ j : Fin r, blockWeight a (e j) := by
  unfold familyState inputWord
  rw [encoded_reflection_weight,input_half_product]
  have hp : (∏ j ∈ Finset.range r, blockWeight a (extendBits e j)) = ∏ j : Fin r, blockWeight a (e j) := by
    rw [← Fin.prod_univ_eq_prod_range]
    apply Finset.prod_congr rfl
    intro j _
    simp [extendBits,j.isLt]
  rw [hp]
  ring

theorem targetState_weight (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ) (r k : Nat) :
    coefficientWeight A a oddWeight (targetState r k) =
      A (2*halfWidth r k) * a 11 * a 9^(4*r+1) * a 18^k := by
  unfold targetState targetWord
  rw [encoded_reflection_weight,target_half_product]
  ring

/-- Exact finite binary product expansion, not a numerical enumeration. -/
theorem binary_product_sum (a : Nat → ℝ) (r : Nat) :
    (∑ e : Fin r → Bool, ∏ j : Fin r, blockWeight a (e j)) =
      (a 9^4+a 14^2*a 4^2)^r := by
  rw [← Fintype.prod_sum (fun (_ : Fin r) (b : Bool) => blockWeight a b)]
  simp [blockWeight,add_comm]

/-- The exact source family contribution, before comparison with the full fiber. -/
theorem family_weight_sum (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ) (r k : Nat) :
    (∑ e : Fin r → Bool, coefficientWeight A a oddWeight (familyState r k e)) =
      A (2*halfWidth r k) * a 5 * a 14 * a 18^k * (a 9^4+a 14^2*a 4^2)^r := by
  simp_rw [familyState_weight]
  rw [← Finset.mul_sum,binary_product_sum]

end
end Agent13ProductWeights
