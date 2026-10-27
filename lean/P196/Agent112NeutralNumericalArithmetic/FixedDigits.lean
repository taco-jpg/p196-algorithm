import P196.Agent112NeutralNumericalArithmetic.Normalization

/-!
# Prescribed-width digits through the existing neutral normalizer

The digit extractor is the unchanged `Agent120.Neutral.norm` applied to a
zero word, with the entire number supplied as incoming carry. No second
digit algorithm is introduced. Equal widths 和 equal input totals determine
the complete normalization result, including the outgoing carry.

This is an all-base checker-API bridge for established positional arithmetic.
The decimal formula is prior work in
`Agent115.ExteriorFactorization.normalize_eq`; general-base indexed digit
extraction 和 reversal are prior work in
`P196.Drafts.Agent4GeneralBaseNormalization.DigitsBridge`.
No new arithmetic discovery, center return, or Lychrel result is claimed.
-/

namespace Agent112.NeutralNumericalArithmetic

open Agent120.Neutral

/-- Exactly `m` low digits, retaining all zero positions, from the existing
normalizer with a zero coefficient word. -/
def digitsAtWidth (b m N : Nat) : List Nat :=
  (norm b (List.replicate m 0) N).1

/-- Reversal retains the prescribed width, including leading zero positions. -/
def reverseAtWidth (b m N : Nat) : Nat :=
  val b (digitsAtWidth b m N).reverse

/-- Normalization depends only on the supplied width 和 total numeric input. -/
theorem norm_eq_zero_word (b : Nat) (hb : 0 < b) (C : List Nat) (e : Nat) :
    norm b C e = norm b (List.replicate C.length 0) (val b C + e) := by
  induction C generalizing e with
  | nil => simp
  | cons d C ih =>
      have htotal : val b (d :: C) + e = (d + e) + b * val b C := by
        simp only [val_cons]
        omega
      have hmod : (val b (d :: C) + e) % b = (d + e) % b := by
        rw [htotal, Nat.add_mul_mod_self_left]
      have hdiv : (val b (d :: C) + e) / b = val b C + (d + e) / b := by
        rw [htotal, Nat.add_mul_div_left _ _ hb]
        omega
      rw [norm_cons, List.length_cons, List.replicate_succ, norm_cons]
      simp only [Nat.zero_add]
      rw [hmod, hdiv, ih ((d + e) / b)]

/-- The actual normalized digit list is the prescribed-width numeric one. -/
theorem norm_digits_eq_digitsAtWidth (b : Nat) (hb : 0 < b)
    (C : List Nat) (e : Nat) :
    (norm b C e).1 = digitsAtWidth b C.length (val b C + e) := by
  unfold digitsAtWidth
  rw [norm_eq_zero_word b hb C e]

/-- Equal width 和 equal value-plus-carry force identical complete outputs. -/
theorem norm_eq_of_length_value (b : Nat) (hb : 0 < b)
    (C D : List Nat) (e f : Nat) (hlen : C.length = D.length)
    (hvalue : val b C + e = val b D + f) :
    norm b C e = norm b D f := by
  rw [norm_eq_zero_word b hb C e, norm_eq_zero_word b hb D f, hlen, hvalue]

/-- The numeric extractor preserves the requested width even for zero input. -/
theorem digitsAtWidth_length (b m N : Nat) : (digitsAtWidth b m N).length = m := by
  simpa only [digitsAtWidth, List.length_replicate] using
    norm_length b (List.replicate m 0) N

/-- Every extracted coefficient is an ordinary digit in a positive base. -/
theorem digitsAtWidth_digit_lt (b : Nat) (hb : 0 < b) (m N : Nat) :
    ∀ d ∈ digitsAtWidth b m N, d < b :=
  norm_digit_lt b hb (List.replicate m 0) N

private theorem val_replicate_zero (b m : Nat) :
    val b (List.replicate m 0) = 0 := by
  induction m with
  | zero => simp
  | succ m ih => simp [List.replicate_succ, ih]

/-- Extracting `m` positions retains exactly the residue modulo `b ^ m`. -/
theorem digitsAtWidth_value_eq_mod (b : Nat) (hb : 0 < b) (m N : Nat) :
    val b (digitsAtWidth b m N) = N % b ^ m := by
  simpa only [digitsAtWidth, val_replicate_zero, List.length_replicate, Nat.zero_add] using
    norm_digits_value_eq_mod b hb (List.replicate m 0) N

end Agent112.NeutralNumericalArithmetic
