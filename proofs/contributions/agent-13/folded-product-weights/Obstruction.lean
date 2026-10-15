import Products
import Mathlib.Tactic.FieldSimp

namespace Agent13ProductWeights
open Agent13FoldedFamily
open scoped BigOperators

noncomputable section

def amplification (a : Nat → ℝ) (r : Nat) : ℝ :=
  (a 5*a 14)/(a 11*a 9) * (1+(a 4*a 14/(a 9)^2)^2)^r

theorem ratio_identity (A : ℝ) (a : Nat → ℝ) (r k : Nat)
    (hA : A ≠ 0) (h9 : a 9 ≠ 0) (h11 : a 11 ≠ 0) (h18 : a 18 ≠ 0) :
    (A*a 5*a 14*a 18^k*(a 9^4+a 14^2*a 4^2)^r) /
      (A*a 11*a 9^(4*r+1)*a 18^k) = amplification a r := by
  have hbase : 1+(a 4*a 14/(a 9)^2)^2 = (a 9^4+a 14^2*a 4^2)/(a 9^4) := by
    field_simp
    <;> ring
  have hpow : a 9^(4*r+1) = (a 9^4)^r*a 9 := by rw [pow_add,pow_mul,pow_one]
  unfold amplification
  rw [hbase,div_pow,hpow]
  field_simp
  <;> ring

/-- Exact original amplification for the full safe incoming operator, with
arbitrary positive odd-width extension and arbitrary positive width factors. -/
theorem incoming_product_ratio (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L%2=0 → 0 < A L) (ha : ∀ i, i ≤ 18 → 0 < a i)
    (ho : ∀ s, SafeState s → s.1%2 ≠ 0 → 0 < oddWeight s) (r k : Nat) (hk : 0 < k) :
    amplification a r ≤ incoming (coefficientWeight A a oddWeight) (targetState r k) /
      coefficientWeight A a oddWeight (targetState r k) := by
  have hp := coefficientWeight_pos A a oddWeight hA ha ho
  have hsum := partial_sum_le_incoming (coefficientWeight A a oddWeight)
    (fun s hs => (hp s hs).le) (targetState r k) (familyState r k)
    (familyState_injective r k) (fun e => familyState_spec r k e hk)
  have hratio := div_le_div_of_nonneg_right hsum (hp (targetState r k) (targetState_safe r k hk)).le
  rw [family_weight_sum, targetState_weight] at hratio
  rw [ratio_identity _ a r k (ne_of_gt (hA _ (by unfold halfWidth; omega) (by omega))) (ne_of_gt (ha 9 (by omega)))
    (ne_of_gt (ha 11 (by omega))) (ne_of_gt (ha 18 (by omega)))] at hratio
  simpa only [targetState_weight] using hratio

theorem amplification_unbounded (a : Nat → ℝ) (ha : ∀ i, i ≤ 18 → 0 < a i) (C : ℝ) :
    ∃ r : Nat, C < amplification a r := by
  have hp : 0 < (a 5*a 14)/(a 11*a 9) := div_pos
    (mul_pos (ha 5 (by omega)) (ha 14 (by omega)))
    (mul_pos (ha 11 (by omega)) (ha 9 (by omega)))
  have hb : 1 < 1+(a 4*a 14/(a 9)^2)^2 := by
    have h : 0 < (a 4*a 14/(a 9)^2)^2 := pow_pos (div_pos
      (mul_pos (ha 4 (by omega)) (ha 14 (by omega)))
      (pow_pos (ha 9 (by omega)) 2)) 2
    linarith
  obtain ⟨r,hr⟩ := pow_unbounded_of_one_lt (C / ((a 5*a 14)/(a 11*a 9))) hb
  refine ⟨r,?_⟩
  have h := (div_lt_iff₀ hp).mp hr
  simpa [amplification,mul_comm] using h

/-- No finite real uniform incoming multiplier exists for the original
coefficient-product weights on the full actual folded safe state space. -/
theorem no_uniform_product_multiplier (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L%2=0 → 0 < A L) (ha : ∀ i, i ≤ 18 → 0 < a i)
    (ho : ∀ s, SafeState s → s.1%2 ≠ 0 → 0 < oddWeight s) (C : ℝ) :
    ∃ t, SafeState t ∧ C*coefficientWeight A a oddWeight t < incoming (coefficientWeight A a oddWeight) t := by
  obtain ⟨r,hr⟩ := amplification_unbounded a ha C
  have hl := incoming_product_ratio A a oddWeight hA ha ho r 1 (by omega)
  refine ⟨targetState r 1,targetState_safe r 1 (by omega),?_⟩
  exact (lt_div_iff₀ (coefficientWeight_pos A a oddWeight hA ha ho _ (targetState_safe r 1 (by omega)))).mp (hr.trans_le hl)

theorem not_exists_uniform_product_bound (A a : Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L%2=0 → 0 < A L) (ha : ∀ i, i ≤ 18 → 0 < a i)
    (ho : ∀ s, SafeState s → s.1%2 ≠ 0 → 0 < oddWeight s) :
    ¬ ∃ C : ℝ, ∀ t, SafeState t → incoming (coefficientWeight A a oddWeight) t ≤ C*coefficientWeight A a oddWeight t := by
  rintro ⟨C,hC⟩
  obtain ⟨t,ht,hh⟩ := no_uniform_product_multiplier A a oddWeight hA ha ho C
  exact (not_lt_of_ge (hC t ht)) hh

end
end Agent13ProductWeights
