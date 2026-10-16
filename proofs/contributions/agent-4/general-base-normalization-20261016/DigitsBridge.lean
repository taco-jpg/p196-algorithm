import ArithmeticBridge

/-!
Agent #4: independent numeric digit extraction and arbitrary-positive-integer
normalization. The final theorem includes the prescribed normalized coefficients;
it is not the trivial assertion that an integer shares its own carry word.
-/
namespace P196.Agent4.GeneralBase

theorem value_congr (b n : Nat) (d e : Nat → Nat)
    (h : ∀ i < n, d i = e i) : value b d n = value b e n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [value]
      rw [ih (fun i hi => h i (by omega)), h n (by omega)]

def consDigit (a : Nat) (d : Nat → Nat) : Nat → Nat
  | 0 => a
  | i + 1 => d i

theorem consDigit_eta (d : Nat → Nat) :
    consDigit (d 0) (fun i => d (i + 1)) = d := by
  funext i
  cases i <;> rfl

theorem value_consDigit (b a : Nat) (d : Nat → Nat) (n : Nat) :
    value b (consDigit a d) (n + 1) = a + b * value b d n := by
  induction n with
  | zero => simp [value, consDigit]
  | succ n ih =>
      change value b (consDigit a d) (n + 1) + d n * b ^ (n + 1) =
        a + b * (value b d n + d n * b ^ n)
      rw [ih, Nat.pow_succ, Nat.mul_add]
      simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm, Nat.add_assoc]

theorem value_shift (b n : Nat) (d : Nat → Nat) :
    value b d (n + 1) = d 0 + b * value b (fun i => d (i + 1)) n := by
  calc
    value b d (n + 1) =
        value b (consDigit (d 0) (fun i => d (i + 1))) (n + 1) :=
      congrArg (fun e => value b e (n + 1)) (consDigit_eta d).symm
    _ = d 0 + b * value b (fun i => d (i + 1)) n :=
      value_consDigit b (d 0) (fun i => d (i + 1)) n

theorem value_mod_base (b n : Nat) (d : Nat → Nat) (hd : d 0 < b) :
    value b d (n + 1) % b = d 0 := by
  rw [value_shift]
  simp [Nat.add_mod, Nat.mul_mod, Nat.mod_eq_of_lt hd]

theorem value_div_base (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : d 0 < b) :
    value b d (n + 1) / b = value b (fun i => d (i + 1)) n := by
  rw [value_shift]
  apply (Nat.div_eq_iff hb).2
  have hm : b * value b (fun i => d (i + 1)) n =
      value b (fun i => d (i + 1)) n * b := Nat.mul_comm _ _
  rw [hm]
  constructor <;> omega

def integerDigit (b a : Nat) : Nat → Nat
  | 0 => a % b
  | i + 1 => integerDigit b (a / b) i

theorem integerDigit_value (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : ∀ i < n, d i < b) (i : Nat) (hi : i < n) :
    integerDigit b (value b d n) i = d i := by
  induction n generalizing d i with
  | zero => omega
  | succ n ih =>
      cases i with
      | zero => exact value_mod_base b n d (hd 0 (by omega))
      | succ i =>
          rw [integerDigit, value_div_base b n d hb (hd 0 (by omega))]
          apply ih
          · intro j hj
            exact hd (j + 1) (by omega)
          · omega

/-- Every positive natural; the auxiliary bound is universally quantified. -/
theorem positive_has_digit_representation (b a : Nat) (hb : 2 ≤ b) (ha : 0 < a) :
    ∃ n : Nat, ∃ d : Nat → Nat, CanonicalDigits b n d ∧ value b d n = a := by
  have H : ∀ N x : Nat, x ≤ N → 0 < x →
      ∃ n : Nat, ∃ d : Nat → Nat, CanonicalDigits b n d ∧ value b d n = x := by
    intro N
    induction N with
    | zero =>
        intro x hle hx
        omega
    | succ N ih =>
        intro x hle hx
        by_cases hsmall : x < b
        · refine ⟨1, (fun _ => x), ?_, ?_⟩
          · exact ⟨by decide, (fun _ _ => hsmall), hx⟩
          · simp [value]
        · have hqpos : 0 < x / b := by
            have hq : 1 ≤ x / b :=
              (Nat.le_div_iff_mul_le (by omega : 0 < b)).2 (by
                simp only [Nat.one_mul]
                omega)
            omega
          have hqlt : x / b < x := by
            apply (Nat.div_lt_iff_lt_mul (by omega : 0 < b)).2
            have hm := Nat.mul_le_mul_right x hb
            rw [Nat.mul_comm b x] at hm
            omega
          obtain ⟨n, d, hd, hval⟩ := ih (x / b) (by omega) hqpos
          refine ⟨n + 1, consDigit (x % b) d, ?_, ?_⟩
          · refine ⟨by omega, ?_, ?_⟩
            · intro i hi
              cases i with
              | zero => exact Nat.mod_lt x (by omega)
              | succ i => exact hd.2.1 i (by omega)
            · cases n with
              | zero => have hn := hd.1; omega
              | succ k => simpa [consDigit] using hd.2.2
          · rw [value_consDigit, hval]
            exact Nat.mod_add_div x b
  exact H a a (by omega) ha

def CanonicalNumeral (b n a : Nat) : Prop :=
  CanonicalDigits b n (integerDigit b a) ∧ value b (integerDigit b a) n = a

theorem canonical_extracted_digits (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : CanonicalDigits b n d) :
    CanonicalNumeral b n (value b d n) ∧
      (∀ i < n, integerDigit b (value b d n) i = d i) := by
  have hrec : ∀ i < n, integerDigit b (value b d n) i = d i :=
    integerDigit_value b n d hb hd.2.1
  refine ⟨⟨⟨hd.1, ?_, ?_⟩, ?_⟩, hrec⟩
  · intro i hi
    rw [hrec i hi]
    exact hd.2.1 i hi
  · rw [hrec (n - 1) (by have hn := hd.1; omega)]
    exact hd.2.2
  · exact value_congr b n _ _ hrec

theorem positive_has_canonical_numeral (b a : Nat) (hb : 2 ≤ b) (ha : 0 < a) :
    ∃ n, CanonicalNumeral b n a := by
  obtain ⟨n, d, hd, hval⟩ := positive_has_digit_representation b a hb ha
  have h := (canonical_extracted_digits b n d (by omega) hd).1
  rw [hval] at h
  exact ⟨n, h⟩

theorem positive_power (b n : Nat) (hb : 0 < b) : 0 < b ^ n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Nat.pow_succ]
      exact Nat.mul_pos ih hb

theorem canonical_value_positive (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : CanonicalDigits b n d) : 0 < value b d n := by
  have hp := positive_power b (n - 1) hb
  have hl := (canonical_value_bounds b n d hd).1
  omega

theorem canonical_numeral_bounds (b n a : Nat) (ha : CanonicalNumeral b n a) :
    b ^ (n - 1) ≤ a ∧ a < b ^ n := by
  have h := canonical_value_bounds b n (integerDigit b a) ha.1
  rw [ha.2] at h
  exact h

theorem pairCoeff_congr (n : Nat) (d e : Nat → Nat)
    (h : ∀ i < n, d i = e i) (i : Nat) (hi : i < n) :
    pairCoeff n d i = pairCoeff n e i := by
  unfold pairCoeff
  rw [h i hi, h (n - 1 - i) (by omega)]

def reverseAtWidth (b n a : Nat) : Nat :=
  value b (fun i => integerDigit b a (n - 1 - i)) n

def firstCarry (b n a k : Nat) : Nat :=
  arithmeticCarry b (pairCoeff n (integerDigit b a)) k

theorem reverseAtWidth_value (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : ∀ i < n, d i < b) :
    reverseAtWidth b n (value b d n) =
      value b (fun i => d (n - 1 - i)) n := by
  apply value_congr
  intro i hi
  exact integerDigit_value b n d hb hd (n - 1 - i) (by omega)

theorem numeric_reverse_add_arithmetic (b n a : Nat)
    (ha : CanonicalNumeral b n a) :
    value b (arithmeticOutput b (pairCoeff n (integerDigit b a))) n +
      firstCarry b n a n * b ^ n = a + reverseAtWidth b n a := by
  have h := reverse_add_arithmetic b n (integerDigit b a)
  simpa only [firstCarry, reverseAtWidth, ha.2] using h

theorem normalized_integer_representative (b a : Nat)
    (hb : 4 ≤ b) (hbe : b % 2 = 0) (ha : 0 < a) :
    ∃ n z : Nat, CanonicalNumeral b n a ∧ CanonicalNumeral b n z ∧ 0 < z ∧
      (∀ i < n, pairCoeff n (integerDigit b z) i =
        normalized b (chosenLow b n (pairCoeff n (integerDigit b a))) n
          (pairCoeff n (integerDigit b a)) i) ∧
      (∀ k ≤ n, firstCarry b n z k = firstCarry b n a k) := by
  obtain ⟨n, hn⟩ := positive_has_canonical_numeral b a (by omega) ha
  obtain ⟨e, he, hpairs, hc⟩ :=
    canonical_normalization_representative b n (integerDigit b a) hb hbe hn.1
  have hdec := canonical_extracted_digits b n e (by omega) he
  refine ⟨n, value b e n, hn, hdec.1,
    canonical_value_positive b n e (by omega) he, ?_, ?_⟩
  · intro i hi
    calc
      pairCoeff n (integerDigit b (value b e n)) i = pairCoeff n e i :=
        pairCoeff_congr n _ _ hdec.2 i hi
      _ = _ := hpairs i hi
  · intro k hk
    change arithmeticCarry b (pairCoeff n (integerDigit b (value b e n))) k =
      arithmeticCarry b (pairCoeff n (integerDigit b a)) k
    calc
      arithmeticCarry b (pairCoeff n (integerDigit b (value b e n))) k =
          arithmeticCarry b (pairCoeff n e) k :=
        arithmeticCarry_congr b n _ _ (pairCoeff_congr n _ _ hdec.2) k hk
      _ = _ := hc k hk

end P196.Agent4.GeneralBase

#print axioms P196.Agent4.GeneralBase.value_congr
#print axioms P196.Agent4.GeneralBase.consDigit_eta
#print axioms P196.Agent4.GeneralBase.value_consDigit
#print axioms P196.Agent4.GeneralBase.value_shift
#print axioms P196.Agent4.GeneralBase.value_mod_base
#print axioms P196.Agent4.GeneralBase.value_div_base
#print axioms P196.Agent4.GeneralBase.integerDigit_value
#print axioms P196.Agent4.GeneralBase.positive_has_digit_representation
#print axioms P196.Agent4.GeneralBase.canonical_extracted_digits
#print axioms P196.Agent4.GeneralBase.positive_has_canonical_numeral
#print axioms P196.Agent4.GeneralBase.positive_power
#print axioms P196.Agent4.GeneralBase.canonical_value_positive
#print axioms P196.Agent4.GeneralBase.canonical_numeral_bounds
#print axioms P196.Agent4.GeneralBase.pairCoeff_congr
#print axioms P196.Agent4.GeneralBase.reverseAtWidth_value
#print axioms P196.Agent4.GeneralBase.numeric_reverse_add_arithmetic
#print axioms P196.Agent4.GeneralBase.normalized_integer_representative
