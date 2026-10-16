import Agent14CarryfreeResidues
import Agent14CarryfreeDigits
import Agent14CarryfreeCoordinates

/-!
# Carryfree saturation in the original decimal and spectral coordinates

This file formalizes the carryfree odd/even part of Theorem 3 in the
preserved source proofs/research/astra_spectral_carry_quotient.md, blob
eac5b8f61385a615d9cc3e7796a4d698c66b716b. It uses the exact three-digit
construction at odd width and the one-leading-digit construction at even
width. Ordinary integer, actual carry, and literal polynomial evaluation
conditions hold for the same witness. No quotient-ring classification or
claim about future orbit steps is included.
-/

namespace Agent14.Carryfree

open DecimalDigits DecimalMass FoldedDecimal

def oddSeed (u b L : Nat) : Nat :=
  min u 9 * 10 ^ (L - 1) + b * 10 ^ (L - 2) + (u - min u 9) * 10 ^ (L - 3)

def oddDigits (u b L : Nat) : Nat → Nat := threeDigits (min u 9) b (u - min u 9) L

theorem split_parameter (u : Nat) (hu1 : 1 ≤ u) (hu10 : u ≤ 10) :
    1 ≤ min u 9 ∧ min u 9 ≤ 9 ∧ u - min u 9 ≤ 1 ∧ min u 9 + (u - min u 9) = u := by
  by_cases h : u ≤ 9
  · rw [Nat.min_eq_left h]
    omega
  · rw [Nat.min_eq_right (by omega : 9 ≤ u)]
    omega

/-- The source's same explicit input simultaneously meets every ordinary condition. -/
theorem odd_seed_spec (u b L : Nat) (hL : 5 ≤ L) (hodd : L % 2 = 1)
    (hu1 : 1 ≤ u) (hu10 : u ≤ 10) (hb : b ≤ 9) :
    Canonical (oddSeed u b L) (oddDigits u b L) L ∧
      ¬ Lychrel196.Palindrome (oddSeed u b L) ∧
      (∀ i, i ≤ L → carry (columnSum (oddDigits u b L) L) i = 0) ∧
      Canonical (Lychrel196.step (oddSeed u b L))
        (output (columnSum (oddDigits u b L) L)) L ∧
      Lychrel196.Palindrome (Lychrel196.step (oddSeed u b L)) ∧
      digitSum (oddSeed u b L) = u + b ∧
      oddSeed u b L % 99 = (u + 10 * b) % 99 ∧
      (∀ i, i < L → columnSum (oddDigits u b L) L i ≤ 9) := by
  rcases split_parameter u hu1 hu10 with ⟨ha0, ha, hc, hac⟩
  have hd : Canonical (oddSeed u b L) (oddDigits u b L) L :=
    threeDigits_canonical (min u 9) b (u - min u 9) L hL ha0 ha hb hc
  have hn := threeDigits_not_palindrome (min u 9) b (u - min u 9) L hL ha0 ha hb hc
  rw [threeDigits_value _ _ _ _ (by omega : 3 ≤ L)] at hn
  have hq : ∀ i, i < L → columnSum (oddDigits u b L) L i ≤ 9 :=
    threeDigits_columns_bounded (min u 9) b (u - min u 9) L hL ha hb hc
  rcases small_columns_actual_step (oddSeed u b L) (oddDigits u b L) L hd hq with
    ⟨hz, hnext, hp⟩
  have hs : digitSum (oddSeed u b L) = u + b := by
    rw [← hd.2.2.2, digitSum_value _ _ hd.2.1]
    change wordSum (threeDigits (min u 9) b (u - min u 9) L) L = u + b
    rw [threeDigits_sum _ _ _ _ (by omega : 3 ≤ L)]
    omega
  have hm : oddSeed u b L % 99 = (u + 10 * b) % 99 := by
    unfold oddSeed
    rw [odd_three_digit_mod99 L (min u 9) b (u - min u 9) hL hodd]
    congr 1
    omega
  exact ⟨hd, hn, hz, hnext, hp, hs, hm, hq⟩

/-- All 99 physical odd-width classes have nonpalindromic carryfree predecessors. -/
theorem odd_carryfree_classes (L s r : Nat) (hL : 5 ≤ L) (hodd : L % 2 = 1)
    (hs : s < 9) (hr : r < 11) :
    ∃ n : Nat, ∃ d : Nat → Nat,
      Canonical n d L ∧ ¬ Lychrel196.Palindrome n ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = 0) ∧
      Canonical (Lychrel196.step n) (output (columnSum d L)) L ∧
      Lychrel196.Palindrome (Lychrel196.step n) ∧
      digitSum n % 9 = s ∧ n % 11 = r ∧
      (∀ i, i < L → columnSum d L i ≤ 9) := by
  obtain ⟨u, b, hu1, hu10, hb, hs9, hr11⟩ := residue_parameters s r hs hr
  rcases odd_seed_spec u b L hL hodd hu1 hu10 hb with
    ⟨hd, hn, hz, hnext, hp, hsum, hmod, hq⟩
  refine ⟨oddSeed u b L, oddDigits u b L, hd, hn, hz, hnext, hp, ?_, ?_, hq⟩
  · rw [hsum]
    exact hs9
  · omega

/-- A single positive leading digit supplies the source's even-width family. -/
theorem one_digit_seed_spec (a L : Nat) (hL : 2 ≤ L) (ha0 : 1 ≤ a) (ha : a ≤ 9) :
    Canonical (a * 10 ^ (L - 1)) (oneDigit a L) L ∧
      ¬ Lychrel196.Palindrome (a * 10 ^ (L - 1)) ∧
      (∀ i, i ≤ L → carry (columnSum (oneDigit a L) L) i = 0) ∧
      Canonical (Lychrel196.step (a * 10 ^ (L - 1)))
        (output (columnSum (oneDigit a L) L)) L ∧
      Lychrel196.Palindrome (Lychrel196.step (a * 10 ^ (L - 1))) ∧
      digitSum (a * 10 ^ (L - 1)) = a ∧
      (∀ i, i < L → columnSum (oneDigit a L) L i ≤ 9) := by
  have hd := oneDigit_canonical a L hL ha0 ha
  have hn := oneDigit_not_palindrome a L hL ha0 ha
  rw [oneDigit_value a L (by omega)] at hn
  have hq := oneDigit_columns_bounded a L hL ha
  rcases small_columns_actual_step (a * 10 ^ (L - 1)) (oneDigit a L) L hd hq with
    ⟨hz, hnext, hp⟩
  have hs : digitSum (a * 10 ^ (L - 1)) = a := by
    rw [← hd.2.2.2, digitSum_value _ _ hd.2.1, oneDigit_sum a L (by omega)]
  exact ⟨hd, hn, hz, hnext, hp, hs, hq⟩

/-- The nine even-width physical classes impose no divisibility-by-eleven condition. -/
theorem even_carryfree_classes (L s : Nat) (hL : 2 ≤ L) (_heven : L % 2 = 0)
    (hs : s < 9) :
    ∃ n : Nat, ∃ d : Nat → Nat,
      Canonical n d L ∧ ¬ Lychrel196.Palindrome n ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = 0) ∧
      Canonical (Lychrel196.step n) (output (columnSum d L)) L ∧
      Lychrel196.Palindrome (Lychrel196.step n) ∧ digitSum n % 9 = s ∧
      (∀ i, i < L → columnSum d L i ≤ 9) := by
  obtain ⟨a, ha0, ha, has⟩ := even_residue_parameters s hs
  rcases one_digit_seed_spec a L hL ha0 ha with ⟨hd, hn, hz, hnext, hp, hsum, hq⟩
  refine ⟨a * 10 ^ (L - 1), oneDigit a L, hd, hn, hz, hnext, hp, ?_, hq⟩
  rw [hsum]
  exact has

/-- The half of the literal evaluation at one is the ordinary digit sum. -/
theorem half_columns_eval_one (n : Nat) (d : Nat → Nat) (L : Nat)
    (hd : Canonical n d L) :
    coefficientEval (columnSum d L) L 1 / 2 = (digitSum n : Int) := by
  rw [canonical_columns_eval_one n d L hd]
  omega

/-- Splitting u across the leading and third digit preserves the signed coordinate. -/
theorem odd_seed_eval_neg_one (u b L : Nat) (hL : 5 ≤ L) (hodd : L % 2 = 1)
    (hu1 : 1 ≤ u) (hu10 : u ≤ 10) :
    coefficientEval (columnSum (oddDigits u b L) L) L (-1) =
      2 * ((u : Int) - (b : Int)) := by
  unfold oddDigits
  rw [odd_columns_eval_neg_one _ _ _ _ hL hodd]
  have hac := (split_parameter u hu1 hu10).2.2.2
  omega

/-- Division by two is exact even when the alternating half is negative. -/
theorem odd_seed_half_neg_one (u b L : Nat) (hL : 5 ≤ L) (hodd : L % 2 = 1)
    (hu1 : 1 ≤ u) (hu10 : u ≤ 10) :
    coefficientEval (columnSum (oddDigits u b L) L) L (-1) / 2 =
      (u : Int) - (b : Int) := by
  rw [odd_seed_eval_neg_one u b L hL hodd hu1 hu10]
  omega

/-- The source half-coordinate modulo eleven is the residue of the same input. -/
theorem odd_seed_half_mod_eleven (u b L : Nat) (hL : 5 ≤ L) (hodd : L % 2 = 1)
    (hu1 : 1 ≤ u) (hu10 : u ≤ 10) (hb : b ≤ 9) :
    (coefficientEval (columnSum (oddDigits u b L) L) L (-1) / 2) % 11 =
      (oddSeed u b L % 11 : Nat) := by
  rw [odd_seed_half_neg_one u b L hL hodd hu1 hu10]
  have hm := (odd_seed_spec u b L hL hodd hu1 hu10 hb).2.2.2.2.2.2.1
  omega

/-- Theorem 3, odd carryfree case, in the literal physical spectral coordinates.
All conditions use one canonical nonpalindromic input of every specified width. -/
theorem odd_source_coordinate_saturation (L s r : Nat)
    (hL : 5 ≤ L) (hodd : L % 2 = 1) (hs : s < 9) (hr : r < 11) :
    ∃ n : Nat, ∃ d : Nat → Nat,
      Canonical n d L ∧ ¬ Lychrel196.Palindrome n ∧
      Admissible L (columnSum d L) ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = 0) ∧
      Canonical (Lychrel196.step n) (output (columnSum d L)) L ∧
      Lychrel196.Palindrome (Lychrel196.step n) ∧
      digitSum n % 9 = s ∧ n % 11 = r ∧
      (∀ i, i < L → columnSum d L i ≤ 9) ∧
      coefficientEval (columnSum d L) L 1 = 2 * (digitSum n : Int) ∧
      (coefficientEval (columnSum d L) L 1 / 2) % 9 = (s : Int) ∧
      (coefficientEval (columnSum d L) L (-1) / 2) % 11 = (r : Int) := by
  obtain ⟨u, b, hu1, hu10, hb, hs9, hr11⟩ := residue_parameters s r hs hr
  rcases odd_seed_spec u b L hL hodd hu1 hu10 hb with
    ⟨hd, hn, hz, hnext, hp, hsum, hmod, hq⟩
  have had := NormalizationBridge.canonical_admissible _ _ _ hd
  have hds : digitSum (oddSeed u b L) % 9 = s := by rw [hsum]; exact hs9
  have hnr : oddSeed u b L % 11 = r := by omega
  have hpos := canonical_columns_eval_one _ _ _ hd
  have hhalf := half_columns_eval_one _ _ _ hd
  have hneg := odd_seed_half_mod_eleven u b L hL hodd hu1 hu10 hb
  refine ⟨oddSeed u b L, oddDigits u b L, hd, hn, had, hz, hnext, hp,
    hds, hnr, hq, hpos, ?_, ?_⟩
  · rw [hhalf]
    omega
  · rw [hneg, hnr]

/-- Theorem 3, even carryfree case: all nine s classes have spectral r=0.
The source's r=0 is not a divisibility-by-eleven assertion about the input. -/
theorem even_source_coordinate_saturation (L s : Nat)
    (hL : 2 ≤ L) (heven : L % 2 = 0) (hs : s < 9) :
    ∃ n : Nat, ∃ d : Nat → Nat,
      Canonical n d L ∧ ¬ Lychrel196.Palindrome n ∧
      Admissible L (columnSum d L) ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = 0) ∧
      Canonical (Lychrel196.step n) (output (columnSum d L)) L ∧
      Lychrel196.Palindrome (Lychrel196.step n) ∧ digitSum n % 9 = s ∧
      (∀ i, i < L → columnSum d L i ≤ 9) ∧
      coefficientEval (columnSum d L) L 1 = 2 * (digitSum n : Int) ∧
      (coefficientEval (columnSum d L) L 1 / 2) % 9 = (s : Int) ∧
      coefficientEval (columnSum d L) L (-1) = 0 ∧
      (coefficientEval (columnSum d L) L (-1) / 2) % 11 = 0 := by
  obtain ⟨a, ha0, ha, has⟩ := even_residue_parameters s hs
  rcases one_digit_seed_spec a L hL ha0 ha with ⟨hd, hn, hz, hnext, hp, hsum, hq⟩
  have had := NormalizationBridge.canonical_admissible _ _ _ hd
  have hds : digitSum (a * 10 ^ (L - 1)) % 9 = s := by rw [hsum]; exact has
  have hpos := canonical_columns_eval_one _ _ _ hd
  have hhalf := half_columns_eval_one _ _ _ hd
  have hneg := even_columns_eval_neg_one a L hL heven
  refine ⟨a * 10 ^ (L - 1), oneDigit a L, hd, hn, had, hz, hnext, hp,
    hds, hq, hpos, ?_, hneg, ?_⟩
  · rw [hhalf]
    omega
  · rw [hneg]
    decide

/-- A concrete negative alternating half guards against natural subtraction. -/
theorem negative_half_control :
    oddSeed 1 9 5 = 19000 ∧
      coefficientEval (columnSum (oddDigits 1 9 5) 5) 5 (-1) / 2 = -8 ∧
      (coefficientEval (columnSum (oddDigits 1 9 5) 5) 5 (-1) / 2) % 11 = 3 := by
  have h := odd_seed_half_neg_one 1 9 5 (by decide) (by decide) (by decide) (by decide)
  constructor
  · decide
  · rw [h]
    decide

/-- The simultaneous zero residues are realized at the minimum odd width. -/
theorem zero_classes_control :
    oddSeed 9 9 5 = 99000 ∧ Lychrel196.step (oddSeed 9 9 5) = 99099 ∧
      digitSum (oddSeed 9 9 5) % 9 = 0 ∧ oddSeed 9 9 5 % 11 = 0 := by
  have hs := (odd_seed_spec 9 9 5 (by decide) (by decide)
    (by decide) (by decide) (by decide)).2.2.2.2.2.1
  refine ⟨by decide, by decide, ?_, by decide⟩
  rw [hs]

end Agent14.Carryfree
