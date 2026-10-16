import LychrelDigitSums

/-!
The literal sparse decimal witnesses from the carryfree saturation theorem.
All carry and palindrome conclusions use the original decimal definitions.
-/

namespace Agent14.Carryfree

open DecimalDigits DecimalMass FoldedDecimal

def threeDigits (a b c L i : Nat) : Nat :=
  if i = L - 1 then a else if i = L - 2 then b else if i = L - 3 then c else 0

def oneDigit (a L i : Nat) : Nat := if i = L - 1 then a else 0

def spike (k a i : Nat) : Nat := if i = k then a else 0

theorem threeDigits_bounded (a b c L : Nat) (ha : a ≤ 9) (hb : b ≤ 9)
    (hc : c ≤ 1) (i : Nat) : threeDigits a b c L i ≤ 9 := by
  unfold threeDigits
  split
  · exact ha
  · split
    · exact hb
    · split <;> omega

theorem threeDigits_leading (a b c L : Nat) : threeDigits a b c L (L - 1) = a := by
  simp [threeDigits]

theorem threeDigits_second (a b c L : Nat) (hL : 3 ≤ L) :
    threeDigits a b c L (L - 2) = b := by
  simp [threeDigits, show L - 2 ≠ L - 1 by omega]

theorem threeDigits_third (a b c L : Nat) (hL : 3 ≤ L) :
    threeDigits a b c L (L - 3) = c := by
  simp [threeDigits, show L - 3 ≠ L - 1 by omega, show L - 3 ≠ L - 2 by omega]

theorem threeDigits_prefix_zero (a b c L i : Nat) (hi : i < L - 3) :
    threeDigits a b c L i = 0 := by
  simp [threeDigits, show i ≠ L - 1 by omega, show i ≠ L - 2 by omega,
    show i ≠ L - 3 by omega]

theorem threeDigits_units_zero (a b c L : Nat) (hL : 5 ≤ L) :
    threeDigits a b c L 0 = 0 :=
  threeDigits_prefix_zero a b c L 0 (by omega)

theorem zero_digits_value (L : Nat) : value (fun _ => 0) L = 0 := by
  induction L with
  | zero => rfl
  | succ L ih => simp [value, ih]

theorem threeDigits_value (a b c L : Nat) (hL : 3 ≤ L) :
    value (threeDigits a b c L) L =
      a * 10 ^ (L - 1) + b * 10 ^ (L - 2) + c * 10 ^ (L - 3) := by
  have hp : value (threeDigits a b c L) (L - 3) = 0 := by
    rw [value_congr (threeDigits a b c L) (fun _ => 0) (L - 3)
      (fun i hi => threeDigits_prefix_zero a b c L i hi)]
    exact zero_digits_value (L - 3)
  calc
    value (threeDigits a b c L) L =
        value (threeDigits a b c L) (L - 3 + 1 + 1 + 1) :=
      congrArg (value (threeDigits a b c L)) (by omega)
    _ = _ := by
      simp only [value]
      rw [hp, show L - 3 + 1 = L - 2 by omega,
        show L - 3 + 1 + 1 = L - 1 by omega]
      rw [threeDigits_third a b c L hL, threeDigits_second a b c L hL,
        threeDigits_leading]
      omega

theorem threeDigits_sum (a b c L : Nat) (hL : 3 ≤ L) :
    wordSum (threeDigits a b c L) L = a + b + c := by
  have hp : wordSum (threeDigits a b c L) (L - 3) = 0 := by
    rw [wordSum_congr (threeDigits a b c L) (fun _ => 0) (L - 3)
      (fun i hi => threeDigits_prefix_zero a b c L i hi)]
    exact wordSum_zero (L - 3)
  calc
    wordSum (threeDigits a b c L) L =
        wordSum (threeDigits a b c L) (L - 3 + 1 + 1 + 1) :=
      congrArg (wordSum (threeDigits a b c L)) (by omega)
    _ = _ := by
      simp only [wordSum]
      rw [hp, show L - 3 + 1 = L - 2 by omega,
        show L - 3 + 1 + 1 = L - 1 by omega]
      rw [threeDigits_third a b c L hL, threeDigits_second a b c L hL,
        threeDigits_leading]
      omega

theorem threeDigits_canonical (a b c L : Nat) (hL : 5 ≤ L)
    (ha0 : 1 ≤ a) (ha : a ≤ 9) (hb : b ≤ 9) (hc : c ≤ 1) :
    Canonical (a * 10 ^ (L - 1) + b * 10 ^ (L - 2) + c * 10 ^ (L - 3))
      (threeDigits a b c L) L := by
  refine ⟨by omega, fun i _ => threeDigits_bounded a b c L ha hb hc i, ?_,
    threeDigits_value a b c L (by omega)⟩
  rw [threeDigits_leading]
  omega

theorem threeDigits_not_palindrome (a b c L : Nat) (hL : 5 ≤ L)
    (ha0 : 1 ≤ a) (ha : a ≤ 9) (hb : b ≤ 9) (hc : c ≤ 1) :
    ¬ Lychrel196.Palindrome (value (threeDigits a b c L) L) := by
  intro hp
  have hs := (palindrome_value_iff (threeDigits a b c L) L
    (fun i _ => threeDigits_bounded a b c L ha hb hc i)
    (Or.inr (by rw [threeDigits_leading]; omega))).mp hp
  have hz := hs 0 (by omega)
  rw [threeDigits_units_zero a b c L hL, Nat.sub_zero, threeDigits_leading] at hz
  omega

/-- This includes width five, where the central column equals twice c. -/
theorem threeDigits_columns_bounded (a b c L : Nat) (hL : 5 ≤ L)
    (ha : a ≤ 9) (hb : b ≤ 9) (hc : c ≤ 1) :
    ∀ i, i < L → columnSum (threeDigits a b c L) L i ≤ 9 := by
  intro i hi
  unfold columnSum reflected threeDigits
  repeat (first | omega | split)

/-- Exact coefficients of the source polynomial, with coincident terms added. -/
theorem threeDigits_column_formula (a b c L i : Nat) (hL : 5 ≤ L) (hi : i < L) :
    columnSum (threeDigits a b c L) L i =
      spike 0 a i + spike (L - 1) a i + spike 1 b i + spike (L - 2) b i +
        spike 2 c i + spike (L - 3) c i := by
  unfold columnSum reflected threeDigits spike
  repeat (first | omega | split)

theorem oneDigit_bounded (a L i : Nat) (ha : a ≤ 9) : oneDigit a L i ≤ 9 := by
  unfold oneDigit
  split <;> omega

theorem oneDigit_leading (a L : Nat) : oneDigit a L (L - 1) = a := by
  simp [oneDigit]

theorem oneDigit_units_zero (a L : Nat) (hL : 2 ≤ L) : oneDigit a L 0 = 0 := by
  simp [oneDigit, show (0 : Nat) ≠ L - 1 by omega]

theorem oneDigit_value (a L : Nat) (hL : 1 ≤ L) :
    value (oneDigit a L) L = a * 10 ^ (L - 1) := by
  have hp : value (oneDigit a L) (L - 1) = 0 := by
    rw [value_congr (oneDigit a L) (fun _ => 0) (L - 1)
      (by intro i hi; simp [oneDigit, show i ≠ L - 1 by omega])]
    exact zero_digits_value (L - 1)
  calc
    value (oneDigit a L) L = value (oneDigit a L) (L - 1 + 1) :=
      congrArg (value (oneDigit a L)) (by omega)
    _ = _ := by simp [value, hp, oneDigit]

theorem oneDigit_sum (a L : Nat) (hL : 1 ≤ L) : wordSum (oneDigit a L) L = a := by
  have hp : wordSum (oneDigit a L) (L - 1) = 0 := by
    rw [wordSum_congr (oneDigit a L) (fun _ => 0) (L - 1)
      (by intro i hi; simp [oneDigit, show i ≠ L - 1 by omega])]
    exact wordSum_zero (L - 1)
  calc
    wordSum (oneDigit a L) L = wordSum (oneDigit a L) (L - 1 + 1) :=
      congrArg (wordSum (oneDigit a L)) (by omega)
    _ = _ := by simp [wordSum, hp, oneDigit]

theorem oneDigit_canonical (a L : Nat) (hL : 2 ≤ L) (ha0 : 1 ≤ a) (ha : a ≤ 9) :
    Canonical (a * 10 ^ (L - 1)) (oneDigit a L) L := by
  refine ⟨by omega, fun i _ => oneDigit_bounded a L i ha, ?_,
    oneDigit_value a L (by omega)⟩
  rw [oneDigit_leading]
  omega

theorem oneDigit_not_palindrome (a L : Nat) (hL : 2 ≤ L) (ha0 : 1 ≤ a) (ha : a ≤ 9) :
    ¬ Lychrel196.Palindrome (value (oneDigit a L) L) := by
  intro hp
  have hs := (palindrome_value_iff (oneDigit a L) L
    (fun i _ => oneDigit_bounded a L i ha)
    (Or.inr (by rw [oneDigit_leading]; omega))).mp hp
  have hz := hs 0 (by omega)
  rw [oneDigit_units_zero a L hL, Nat.sub_zero, oneDigit_leading] at hz
  omega

theorem oneDigit_columns_bounded (a L : Nat) (hL : 2 ≤ L) (ha : a ≤ 9) :
    ∀ i, i < L → columnSum (oneDigit a L) L i ≤ 9 := by
  intro i hi
  unfold columnSum reflected oneDigit
  repeat (first | omega | split)

theorem oneDigit_column_formula (a L i : Nat) (hL : 2 ≤ L) (hi : i < L) :
    columnSum (oneDigit a L) L i = spike 0 a i + spike (L - 1) a i := by
  unfold columnSum reflected oneDigit spike
  repeat (first | omega | split)

/-- Reuse the original small-column theorem and its ordinary decimal bridges. -/
theorem small_columns_actual_step (n : Nat) (d : Nat → Nat) (L : Nat)
    (hd : Canonical n d L) (hq : ∀ i, i < L → columnSum d L i ≤ 9) :
    (∀ i, i ≤ L → carry (columnSum d L) i = 0) ∧
      Canonical (Lychrel196.step n) (output (columnSum d L)) L ∧
      Lychrel196.Palindrome (Lychrel196.step n) := by
  have hz := (DecimalCarry.small_digit_sums_give_palindrome L (columnSum d L)
    (carry (columnSum d L)) (output (columnSum d L))
    (columnSum_symmetric d L) hq (fun i _ => column_equation (columnSum d L) i) rfl).1
  have hf := hz L (by omega)
  have hp := (step_palindrome_iff_no_overflow d L hd.1 hd.2.1 hd.2.2.1 hf).mpr hq
  rw [hd.2.2.2] at hp
  exact ⟨hz, canonical_next_no_overflow n d L hd hf, hp⟩

end Agent14.Carryfree
