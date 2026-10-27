import P196.Agent112NeutralNumericalArithmetic.FixedDigits

/-!
# The actual A120 raw center step in numerical coordinates

The fixed-width digit API identifies the complete raw `nextC` word from its
source width, coefficient value, incoming carry, 和 overflow bit. The signed
value identity formalizes the raw numerical formula of Agent 112's prior
paper model (PR #349), reusing the unchanged A120 pair/append arithmetic.

The hypotheses are exactly the imported `Agent120.Neutral.Hyp`; source
symmetry 和 positive center width are not additional assumptions. This file
does not formalize padding, trimming, symmetric injectivity, cycle lifting,
or a new Lychrel certificate.
-/

namespace Agent112.NeutralNumericalArithmetic

open Agent120.Neutral

/-- The upper-band digit is determined by the actual incoming center bit. -/
private theorem hyp_yd_eq_incoming {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    yd b B C = (b - 1) * e1 b B := by
  have h1 := h.e1_le
  have h2 := h.e2_le
  have hf := h.flip
  have hc : 1 - e2 b B C = e1 b B := by omega
  unfold yd
  rw [hc]

/-- Literal raw center word, using only fixed-width numerical input data. -/
theorem nextC_eq_pairs_fixedDigits {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    nextC b B C =
      pairs (digitsAtWidth b C.length (val b C + e1 b B) ++
        List.replicate (gam b B C) ((b - 1) * e1 b B)) := by
  have hb : 0 < b := by have := h.base; omega
  have hd : DC b B C = digitsAtWidth b C.length (val b C + e1 b B) :=
    norm_digits_eq_digitsAtWidth b hb C (e1 b B)
  have hy := hyp_yd_eq_incoming h
  have hg : gam b B C = 0 ∨ gam b B C = 1 := by have := h.gam_le; omega
  rcases hg with hg | hg <;>
    simp [nextC, hg, hd, hy, pairs, List.reverse_append]

/-- The exact raw output has the original width plus its overflow bit. -/
private theorem nextC_length_eq {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    (nextC b B C).length = C.length + gam b B C := by
  rw [nextC_eq_pairs_fixedDigits h]
  simp [pairs, digitsAtWidth_length, Nat.add_comm]

/-- Equal numerical center data force equal actual raw coefficient words. -/
theorem nextC_eq_of_numerical_data {b : Nat} {B C B' C' : List Nat}
    (h : Hyp b B C) (h' : Hyp b B' C')
    (hlen : C.length = C'.length) (hval : val b C = val b C')
    (he : e1 b B = e1 b B') (hg : gam b B C = gam b B' C') :
    nextC b B C = nextC b B' C' := by
  rw [nextC_eq_pairs_fixedDigits h, nextC_eq_pairs_fixedDigits h']
  rw [hlen, hval, he, hg]

/-- Ordinary natural value of the raw center, before any neutral trimming. -/
theorem val_nextC_eq_numerical_data {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    val b (nextC b B C) =
      val b (DC b B C) +
      b ^ gam b B C * reverseAtWidth b C.length (val b C + e1 b B) +
      (b - 1) * e1 b B * gam b B C * (b ^ C.length + 1) := by
  have hb : 0 < b := by have := h.base; omega
  have hd : DC b B C = digitsAtWidth b C.length (val b C + e1 b B) :=
    norm_digits_eq_digitsAtWidth b hb C (e1 b B)
  rw [nextC_eq_pairs_fixedDigits h, val_pairs]
  have hg : gam b B C = 0 ∨ gam b B C = 1 := by have := h.gam_le; omega
  rcases hg with hg | hg
  · simp [hg, hd, reverseAtWidth]
  · simp [hg, hd, reverseAtWidth, val_append, digitsAtWidth_length,
      List.reverse_append, val_cons, Nat.mul_add, Nat.add_mul]
    ac_rfl

/-- Signed raw center update under the actual checker hypotheses.

The reverse term retains the source width, including leading zero padding.
The identity concerns the raw output; no trim or cycle theorem is used. -/
theorem signedValue_nextC {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    signedValue b (nextC b B C) = signedValue b C +
      ((b ^ gam b B C : Nat) : Int) *
        ((reverseAtWidth b C.length (val b C + e1 b B) : Int) +
          (e1 b B : Int) * (((b ^ C.length : Nat) : Int) + 1) -
          ((b ^ C.length : Nat) : Int)) := by
  have h1 := h.e1_le
  have h2 := h.e2_le
  have hf := h.flip
  have hflip : e2 b B C = 1 - e1 b B := by omega
  have hn : val b (DC b B C) + b ^ C.length * (1 - e1 b B) =
      val b C + e1 b B := by
    have hv := norm_val b C (e1 b B)
    change val b (DC b B C) + b ^ C.length * e2 b B C = val b C + e1 b B at hv
    rwa [hflip] at hv
  have hv := val_nextC_eq_numerical_data h
  have hb1 : 1 ≤ b := by have := h.base; omega
  have hs : ((b - 1 : Nat) : Int) = (b : Int) - 1 := Int.ofNat_sub hb1
  have hc : ((b ^ C.length : Nat) : Int) * (b : Int) =
      (b : Int) * ((b ^ C.length : Nat) : Int) := Int.mul_comm _ _
  unfold signedValue
  rw [nextC_length_eq h, hv, Nat.pow_add]
  have he : e1 b B = 0 ∨ e1 b B = 1 := by omega
  have hg : gam b B C = 0 ∨ gam b B C = 1 := by have := h.gam_le; omega
  rcases he with he | he <;> rcases hg with hg | hg <;>
    simp only [he, hg, Nat.pow_zero, Nat.pow_one, Nat.mul_zero, Nat.zero_mul,
      Nat.mul_one, Nat.one_mul, Nat.add_zero, Nat.zero_add, Nat.sub_zero,
      Nat.sub_self, Int.ofNat_add, Int.ofNat_mul, Int.ofNat_one, Int.ofNat_zero,
      hs, hc, Int.mul_zero, Int.zero_mul, Int.mul_one, Int.one_mul,
      Int.add_zero, Int.zero_add, Int.mul_add, Int.mul_sub, Int.sub_mul] at * <;>
    omega

end Agent112.NeutralNumericalArithmetic
