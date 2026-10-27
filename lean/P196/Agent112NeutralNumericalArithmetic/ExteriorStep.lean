import P196.Agent112NeutralNumericalArithmetic.FixedDigits

/-!
# Numerical factorization of the actual neutral exterior step

The existing `Agent120.Neutral.nextB` factors through the exterior width,
its positional value, 和 its reversed positional value. Both actual carries
are recovered from these data under the existing `Hyp`; no carry equality
is supplied to the determinism theorem. The untrimmed width is `m + gam`.

The related decimal value-coordinate update is prior work in
`Agent115.ExteriorFactorization.rawSucc_values`. Its phase-dependent
`rawSucc` has width `m + 1`; this file instead proves the formulas for the
unchanged all-base A120 checker interface. It reuses the existing normalizer
和 prescribed-width digit extractor. No trimming, canonicalization, cycle
classification, or Lychrel conclusion is claimed.
-/

namespace Agent112.NeutralNumericalArithmetic

open Agent120.Neutral

/-- The actual lower exterior carry is a quotient, for any positive base. -/
theorem e1_eq_div (b : Nat) (hb : 0 < b) (B : List Nat) :
    e1 b B = val b B / b ^ B.length := by
  simpa only [e1, Nat.add_zero] using norm_carry_eq_div b hb B 0

private theorem e2_eq_complement {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    e2 b B C = 1 - e1 b B := by
  have := h.e1_le
  have := h.e2_le
  have := h.flip
  omega

/-- The actual overflow is determined by the width 和 both exterior values. -/
theorem gam_eq_div {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    gam b B C =
      (val b B.reverse + (1 - val b B / b ^ B.length)) / b ^ B.length := by
  have hb : 0 < b := by have := h.base; omega
  unfold gam
  rw [norm_carry_eq_div b hb, List.length_reverse, e2_eq_complement h,
    e1_eq_div b hb B]

/-- Literal numeric digit-word description of the existing untrimmed step. -/
theorem nextB_eq_fixedDigits {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    nextB b B C =
      if gam b B C = 0 then
        List.zipWith (· + ·) (digitsAtWidth b B.length (val b B))
          (digitsAtWidth b B.length (val b B.reverse + (1 - e1 b B))).reverse
      else
        List.zipWith (· + ·)
          (digitsAtWidth b B.length (val b B) ++ [(b - 1) * (1 - e1 b B)])
          (1 :: (digitsAtWidth b B.length (val b B.reverse + (1 - e1 b B))).reverse) := by
  have hb : 0 < b := by have := h.base; omega
  have hD : DB b B = digitsAtWidth b B.length (val b B) := by
    simpa only [DB, Nat.add_zero] using norm_digits_eq_digitsAtWidth b hb B 0
  have hE : DR b B C =
      digitsAtWidth b B.length (val b B.reverse + (1 - e1 b B)) := by
    unfold DR
    rw [norm_digits_eq_digitsAtWidth b hb, List.length_reverse, e2_eq_complement h]
  simp only [nextB, hD, hE, xd]

/-- Low positional value of the actual raw exterior successor. -/
theorem val_nextB_eq_numerical_data {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    val b (nextB b B C) =
      val b B % b ^ B.length +
        b ^ gam b B C * reverseAtWidth b B.length (val b B.reverse + (1 - e1 b B)) +
        gam b B C * (1 + (b - 1) * (1 - e1 b B) * b ^ B.length) := by
  have hb : 0 < b := by have := h.base; omega
  have hg : gam b B C = 0 ∨ gam b B C = 1 := by have := h.gam_le; omega
  rw [nextB_eq_fixedDigits h]
  rcases hg with hg | hg
  · simp only [hg, ↓reduceIte, Nat.pow_zero, Nat.one_mul, Nat.zero_mul, Nat.add_zero]
    rw [val_zipWith_add b _ _ (by simp [digitsAtWidth_length])]
    rw [digitsAtWidth_value_eq_mod b hb]
    rfl
  · simp only [hg, Nat.one_ne_zero, ↓reduceIte, Nat.pow_one, Nat.one_mul]
    rw [val_zipWith_add b _ _ (by simp [digitsAtWidth_length])]
    rw [val_append, digitsAtWidth_length, digitsAtWidth_value_eq_mod b hb]
    simp only [val_cons, val_nil, Nat.mul_zero, Nat.add_zero, reverseAtWidth]
    ac_rfl

/-- Reversed positional value of the same actual raw exterior successor. -/
theorem val_reverse_nextB_eq_numerical_data {b : Nat} {B C : List Nat}
    (h : Hyp b B C) :
    val b (nextB b B C).reverse =
      b ^ gam b B C * reverseAtWidth b B.length (val b B) +
        (val b B.reverse + (1 - e1 b B)) % b ^ B.length +
        gam b B C * (b ^ B.length + (b - 1) * (1 - e1 b B)) := by
  have hb : 0 < b := by have := h.base; omega
  have hg : gam b B C = 0 ∨ gam b B C = 1 := by have := h.gam_le; omega
  rw [nextB_eq_fixedDigits h]
  rcases hg with hg | hg
  · simp only [hg, ↓reduceIte, Nat.pow_zero, Nat.one_mul, Nat.zero_mul, Nat.add_zero]
    rw [List.reverse_zipWith (by simp [digitsAtWidth_length]), List.reverse_reverse]
    rw [val_zipWith_add b _ _ (by simp [digitsAtWidth_length])]
    rw [digitsAtWidth_value_eq_mod b hb]
    rfl
  · simp only [hg, Nat.one_ne_zero, ↓reduceIte, Nat.pow_one, Nat.one_mul]
    rw [List.reverse_zipWith (by simp [digitsAtWidth_length])]
    simp only [List.reverse_append, List.reverse_cons, List.reverse_nil,
      List.nil_append, List.singleton_append, List.reverse_reverse]
    rw [val_zipWith_add b _ _ (by simp [digitsAtWidth_length])]
    rw [val_append, digitsAtWidth_length, digitsAtWidth_value_eq_mod b hb]
    simp only [val_cons, val_nil, Nat.mul_zero, Nat.add_zero, Nat.mul_one, reverseAtWidth]
    ac_rfl

/-- Equal width 和 both directional values force equal actual successors;
the actual carries need not be supplied as matching input data. -/
theorem nextB_eq_of_bidirectional_data {b : Nat} {B C B' C' : List Nat}
    (h : Hyp b B C) (h' : Hyp b B' C')
    (hlen : B.length = B'.length) (hval : val b B = val b B')
    (hrev : val b B.reverse = val b B'.reverse) :
    nextB b B C = nextB b B' C' := by
  have hb : 0 < b := by have := h.base; omega
  have he : e1 b B = e1 b B' := by
    rw [e1_eq_div b hb B, e1_eq_div b hb B', hlen, hval]
  have hg : gam b B C = gam b B' C' := by
    rw [gam_eq_div h, gam_eq_div h', hlen, hval, hrev]
  rw [nextB_eq_fixedDigits h, nextB_eq_fixedDigits h', hlen, hval, hrev, he, hg]

end Agent112.NeutralNumericalArithmetic
