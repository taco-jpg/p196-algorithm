import P196.Drafts.Agent120NeutralBandCalibration.A120Template

/-!
# Exact numerical semantics of the neutral center carry

This module connects the existing `Agent120.Neutral.norm` checker API to
Euclidean quotient/remainder arithmetic 和 the signed center carry gate.
It formalizes the sign observation already used in
`calculation/neutral_band/bases/decouple.py`; no new arithmetic discovery is
claimed. The decimal list formula is prior work:
`Agent115.ExteriorFactorization.normalize_eq` in
`P196.Agent6CoordinateThreshold.ExteriorFactorizationProof`. General-base
indexed positional bounds 和 carry conservation are also prior work in
`P196.Drafts.Agent4GeneralBaseNormalization.ArithmeticBridge`.

The quotient/remainder results allow arbitrary natural coefficients 和
incoming carries. The sign results require coefficients at most `2 * (b - 1)`
和 an incoming bit, but require neither symmetry nor positive width.
No trimming, padding, cycle realization, or Lychrel existence is asserted.
-/

namespace Agent112.NeutralNumericalArithmetic

open Agent120.Neutral

/-- A fixed-width list of ordinary digits has value below the width power. -/
theorem val_lt_pow_of_digits (b : Nat) :
    ∀ (D : List Nat), (∀ d ∈ D, d < b) → val b D < b ^ D.length
  | [], _ => by simp
  | d :: D, hD => by
      have hd := hD d List.mem_cons_self
      have ht := val_lt_pow_of_digits b D
        (fun x hx => hD x (List.mem_cons_of_mem d hx))
      have hm := Nat.mul_le_mul_left b
        (show val b D + 1 ≤ b ^ D.length by omega)
      simp only [Nat.mul_add, Nat.mul_one] at hm
      simp only [val_cons, List.length_cons, Nat.pow_succ]
      rw [Nat.mul_comm (b ^ D.length) b]
      omega

/-- Normalized digits occupy exactly the original width, including zeroes. -/
theorem norm_digits_value_lt_pow (b : Nat) (hb : 0 < b) (C : List Nat) (e : Nat) :
    val b (norm b C e).1 < b ^ C.length := by
  have h := val_lt_pow_of_digits b (norm b C e).1 (norm_digit_lt b hb C e)
  simpa only [norm_length] using h

/-- The actual outgoing carry is the quotient, for arbitrary input values. -/
theorem norm_carry_eq_div (b : Nat) (hb : 0 < b) (C : List Nat) (e : Nat) :
    (norm b C e).2 = (val b C + e) / b ^ C.length := by
  have hp : 0 < b ^ C.length := Nat.pow_pos hb
  have hr := norm_digits_value_lt_pow b hb C e
  symm
  rw [← norm_val b C e, Nat.add_mul_div_left _ _ hp, Nat.div_eq_of_lt hr]
  simp

/-- The value of the actual normalized digit list is the remainder. -/
theorem norm_digits_value_eq_mod (b : Nat) (hb : 0 < b) (C : List Nat) (e : Nat) :
    val b (norm b C e).1 = (val b C + e) % b ^ C.length := by
  have hr := norm_digits_value_lt_pow b hb C e
  symm
  rw [← norm_val b C e, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hr]

/-- The value measured relative to the neutral word of the same width.
The integer definition avoids truncated natural subtraction. -/
def signedValue (b : Nat) (C : List Nat) : Int :=
  (val b C : Int) + 1 - ((b ^ C.length : Nat) : Int)

/-- Exact numerical threshold for a bounded center to flip an incoming bit. -/
theorem center_carry_flip_iff (b : Nat) (hb : 2 ≤ b) (C : List Nat)
    (hC : ∀ d ∈ C, d ≤ 2 * (b - 1)) (e : Nat) (he : e ≤ 1) :
    (norm b C e).2 = 1 - e ↔
      (e = 0 ∧ b ^ C.length ≤ val b C) ∨
      (e = 1 ∧ val b C + 1 < b ^ C.length) := by
  have hb0 : 0 < b := by omega
  have hp : 0 < b ^ C.length := Nat.pow_pos hb0
  have hcarry := norm_carry_le_one b hb0 C e hC he
  rcases (by omega : e = 0 ∨ e = 1) with rfl | rfl
  · have hdiv := norm_carry_eq_div b hb0 C 0
    simp only [Nat.add_zero] at hdiv
    have hge : 1 ≤ val b C / b ^ C.length ↔ b ^ C.length ≤ val b C := by
      simpa only [Nat.one_mul] using
        (Nat.le_div_iff_mul_le (x := 1) (y := val b C) hp)
    have hiff : (norm b C 0).2 = 1 ↔ b ^ C.length ≤ val b C := by
      omega
    simpa using hiff
  · rw [norm_carry_eq_div b hb0 C 1]
    simpa using (Nat.div_eq_zero_iff_lt (x := val b C + 1) hp)

/-- A positive signed center needs incoming zero; a negative one needs one. -/
theorem center_carry_flip_iff_sign (b : Nat) (hb : 2 ≤ b) (C : List Nat)
    (hC : ∀ d ∈ C, d ≤ 2 * (b - 1)) (e : Nat) (he : e ≤ 1) :
    (norm b C e).2 = 1 - e ↔
      (e = 0 ∧ 0 < signedValue b C) ∨
      (e = 1 ∧ signedValue b C < 0) := by
  rw [center_carry_flip_iff b hb C hC e he]
  unfold signedValue
  omega

/-- A zero signed value transmits either incoming bit unchanged. -/
theorem center_zero_transmits (b : Nat) (hb : 2 ≤ b) (C : List Nat)
    (hC : ∀ d ∈ C, d ≤ 2 * (b - 1)) (e : Nat) (he : e ≤ 1)
    (hz : signedValue b C = 0) : (norm b C e).2 = e := by
  have hcarry := norm_carry_le_one b (by omega) C e hC he
  have hnot : (norm b C e).2 ≠ 1 - e := by
    intro hf
    have hs := (center_carry_flip_iff_sign b hb C hC e he).mp hf
    rcases hs with hs | hs <;> omega
  omega

/-- A bounded center admits a carry-flipping bit exactly away from zero. -/
theorem center_flip_exists_iff (b : Nat) (hb : 2 ≤ b) (C : List Nat)
    (hC : ∀ d ∈ C, d ≤ 2 * (b - 1)) :
    (∃ e : Nat, e ≤ 1 ∧ (norm b C e).2 = 1 - e) ↔ signedValue b C ≠ 0 := by
  constructor
  · rintro ⟨e, he, hf⟩
    have hs := (center_carry_flip_iff_sign b hb C hC e he).mp hf
    rcases hs with hs | hs <;> omega
  · intro hz
    by_cases hp : 0 < signedValue b C
    · refine ⟨0, by decide, ?_⟩
      exact (center_carry_flip_iff_sign b hb C hC 0 (by decide)).mpr
        (Or.inl ⟨rfl, hp⟩)
    · have hn : signedValue b C < 0 := by omega
      refine ⟨1, by decide, ?_⟩
      exact (center_carry_flip_iff_sign b hb C hC 1 (by decide)).mpr
        (Or.inr ⟨rfl, hn⟩)

/-- Any carry-flipping incoming bit is unique. -/
theorem center_flip_unique (b : Nat) (hb : 2 ≤ b) (C : List Nat)
    (hC : ∀ d ∈ C, d ≤ 2 * (b - 1)) (e f : Nat) (he : e ≤ 1) (hf : f ≤ 1)
    (heflip : (norm b C e).2 = 1 - e) (hfflip : (norm b C f).2 = 1 - f) : e = f := by
  have hes := (center_carry_flip_iff_sign b hb C hC e he).mp heflip
  have hfs := (center_carry_flip_iff_sign b hb C hC f hf).mp hfflip
  rcases hes with hes | hes <;> rcases hfs with hfs | hfs <;> omega

/-- The sign gate holds for the actual incoming carry in the template checker. -/
theorem hyp_center_sign {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    (e1 b B = 0 ∧ 0 < signedValue b C) ∨
    (e1 b B = 1 ∧ signedValue b C < 0) := by
  have hflip : (norm b C (e1 b B)).2 = 1 - e1 b B := by
    change e2 b B C = 1 - e1 b B
    have h1 := h.e1_le
    have h2 := h.e2_le
    have hf := h.flip
    omega
  exact (center_carry_flip_iff_sign b h.base C h.boundC (e1 b B) h.e1_le).mp hflip

/-- An accepted template step cannot have zero signed center value. -/
theorem hyp_center_nonzero {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    signedValue b C ≠ 0 := by
  have hs := hyp_center_sign h
  rcases hs with hs | hs <;> omega

end Agent112.NeutralNumericalArithmetic
