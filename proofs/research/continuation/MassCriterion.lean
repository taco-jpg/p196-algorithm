import Lychrel196Research

/-!
# Decimal digit-sum obstruction to a palindromic reverse-and-add output

This file is a sidecar to `Lychrel196Research.lean`, checked using Lean 4.19
and Std only. `digitSum` is the usual terminating decimal digit-sum
algorithm. Its connection to bounded positional decimal digits is proved.

If the actual reverse-and-add output is a palindrome, its digit sum is
either twice the input digit sum, or four elevenths of it. In particular,
a positive step preserving digit sum cannot output a palindrome.

The all-time consequences are CONDITIONAL: no integer with the required
all-time digit-sum invariant is exhibited or asserted to exist. The later
unbounded-digit-sum theorem in this continuation rules out that invariant
for every positive finite seed. These implications remain valid but cannot
supply an existence witness. Because
`IsLychrel` includes time zero, the unconditional starting-state conclusion
from that invariant is `IsLychrel (step n)`, not `IsLychrel n`.
-/

namespace DecimalMass

open DecimalDigits Lychrel196

/-- Ordinary decimal digit sum, including `digitSum 0 = 0`. -/
def digitSum (n : Nat) : Nat :=
  if h : n = 0 then 0 else n % 10 + digitSum (n / 10)
termination_by n
decreasing_by
  exact Nat.div_lt_self (Nat.pos_of_ne_zero h) (by decide)

theorem digitSum_zero : digitSum 0 = 0 := by
  rw [digitSum]
  simp

/-- The decimal recursion is valid at zero as well. -/
theorem digitSum_mod_div (n : Nat) :
    digitSum n = n % 10 + digitSum (n / 10) := by
  by_cases hn : n = 0
  · subst n
    simp
  · rw [digitSum]
    simp [hn]

/-- Sum of a finite positional word. The coefficients need not be digits. -/
def wordSum (d : Nat → Nat) : Nat → Nat
  | 0 => 0
  | L + 1 => wordSum d L + d L

theorem wordSum_congr (a b : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → a i = b i) : wordSum a L = wordSum b L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    simp only [wordSum, ih (fun i hi => h i (by omega)), h L (by omega)]

theorem wordSum_add (a b : Nat → Nat) (L : Nat) :
    wordSum (fun i => a i + b i) L = wordSum a L + wordSum b L := by
  induction L with
  | zero => rfl
  | succ L ih => simp only [wordSum, ih]; omega

theorem wordSum_mul (a : Nat → Nat) (L c : Nat) :
    wordSum (fun i => c * a i) L = c * wordSum a L := by
  induction L with
  | zero => simp [wordSum]
  | succ L ih => simp [wordSum, ih, Nat.mul_add]

theorem wordSum_zero (L : Nat) : wordSum (fun _ => 0) L = 0 := by
  induction L with
  | zero => rfl
  | succ L ih => simp [wordSum, ih]

theorem wordSum_shift (d : Nat → Nat) (L : Nat) :
    wordSum d (L + 1) = d 0 + wordSum (fun i => d (i + 1)) L := by
  induction L with
  | zero => simp [wordSum]
  | succ L ih => simp only [wordSum] at ih ⊢; omega

/-- Positional reflection preserves the unweighted digit sum. -/
theorem wordSum_reflected (d : Nat → Nat) (L : Nat) :
    wordSum (reflected d L) L = wordSum d L := by
  induction L generalizing d with
  | zero => rfl
  | succ L ih =>
    have hr : wordSum (reflected d (L + 1)) L =
        wordSum (reflected (fun i => d (i + 1)) L) L := by
      apply wordSum_congr
      intro i hi
      simp only [reflected]
      congr 1
      omega
    rw [wordSum, hr, ih, wordSum_shift]
    simp [reflected, Nat.add_comm]

/-- The mirrored pair-sum word has twice the ordinary digit sum. -/
theorem wordSum_columns (d : Nat → Nat) (L : Nat) :
    wordSum (columnSum d L) L = 2 * wordSum d L := by
  unfold columnSum
  rw [wordSum_add, wordSum_reflected]
  omega

/-- The recursive decimal sum agrees with every bounded positional
representation, even one containing additional leading zeroes. -/
theorem digitSum_value (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9) :
    digitSum (value d L) = wordSum d L := by
  induction L generalizing d with
  | zero => exact digitSum_zero
  | succ L ih =>
    have hd0 := hd 0 (by omega)
    have hm : value d (L + 1) % 10 = d 0 := by
      rw [value_shift]
      omega
    have hv : value d (L + 1) / 10 = value (fun i => d (i + 1)) L := by
      rw [value_shift]
      omega
    rw [digitSum_mod_div, hm, hv, ih, wordSum_shift]
    intro i hi
    exact hd (i + 1) (by omega)

theorem digitSum_positive (n : Nat) (hn : 0 < n) : 0 < digitSum n := by
  obtain ⟨d, L, hL, hd, hlead, hv⟩ := canonical_exists n hn
  rw [← hv, digitSum_value d L hd]
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  have hlead' : 0 < d k := by simpa using hlead
  simp only [wordSum]
  omega

/-- Total count of the actual carries out of the first `L` columns. -/
def carryCount (q : Nat → Nat) (L : Nat) : Nat :=
  wordSum (fun i => carry q (i + 1)) L

/-- Summing all actual decimal column equations includes the final carry.
No coefficient bounds or palindrome assumption are required. -/
theorem wordSum_output (q : Nat → Nat) (L : Nat) :
    wordSum (output q) L + carry q L + 9 * carryCount q L = wordSum q L := by
  induction L with
  | zero => simp [wordSum, carry, carryCount]
  | succ L ih =>
    have hc := column_equation q L
    simp only [carryCount, wordSum] at ih ⊢
    omega

theorem wordSum_extended (q : Nat → Nat) (L : Nat) :
    wordSum (extended q L) (L + 1) = wordSum (output q) L + carry q L := by
  rw [wordSum]
  have h : wordSum (extended q L) L = wordSum (output q) L := by
    apply wordSum_congr
    intro i hi
    simp [extended, hi]
  rw [h]
  simp [extended]

/-- Exact general mass balance for the actual decimal reverse-and-add map.
Every outgoing carry removes nine from the input pair-sum total. -/
theorem digitSum_step_balance (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    digitSum (step (value d L)) + 9 * carryCount (columnSum d L) L =
      2 * digitSum (value d L) := by
  have hc := carry_bounded (columnSum d L) L (columnSum_bounded d L hd) L
    (Nat.le_refl L)
  have he : ∀ i, i < L + 1 → extended (columnSum d L) L i ≤ 9 := by
    intro i hi
    unfold extended
    split
    · exact output_bounded _ _
    · omega
  rw [step_value d L hd hlead, ← value_extended, digitSum_value _ _ he,
    wordSum_extended, digitSum_value d L hd]
  rw [← wordSum_columns d L]
  exact wordSum_output _ _

/-- In the low-column predecessor branch all actual carries vanish. -/
theorem carryCount_zero_of_small (d : Nat → Nat) (L : Nat)
    (hsmall : ∀ i, i < L → columnSum d L i ≤ 9) :
    carryCount (columnSum d L) L = 0 := by
  obtain ⟨hz, _⟩ := DecimalCarry.small_digit_sums_give_palindrome
    L (columnSum d L) (carry (columnSum d L)) (output (columnSum d L))
    (columnSum_symmetric d L) hsmall
    (fun i _ => column_equation _ i) rfl
  unfold carryCount
  calc
    wordSum (fun i => carry (columnSum d L) (i + 1)) L =
        wordSum (fun _ => 0) L := wordSum_congr _ _ L (fun i hi => hz _ (by omega))
    _ = 0 := wordSum_zero L

/-- In the exceptional palindrome branch each column sum is eleven
times its actual outgoing carry. -/
theorem columns_eq_eleven_carry (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hvalues : ∀ i, i < L → columnSum d L i = 0 ∨ columnSum d L i = 11) :
    ∀ i, i < L → columnSum d L i = 11 * carry (columnSum d L) (i + 1) := by
  intro i hi
  have hv := hvalues i hi
  have hc := carry_bounded (columnSum d L) L (columnSum_bounded d L hd) i
    (by omega)
  have ho := output_bounded (columnSum d L) i
  have ha := column_equation (columnSum d L) i
  omega

/-- Sharp necessary digit-sum alternatives for every positive actual input.
The disjunction is necessary, not a sufficient palindrome test. -/
theorem palindrome_step_digitSum (n : Nat) (hn : 0 < n)
    (hp : Palindrome (step n)) :
    digitSum (step n) = 2 * digitSum n ∨
      11 * digitSum (step n) = 4 * digitSum n := by
  obtain ⟨d, L, hL, hd, hlead, hv⟩ := canonical_exists n hn
  subst n
  have hb := digitSum_step_balance d L hd (Or.inr hlead)
  rcases (step_palindrome_iff d L hL hd hlead).mp hp with hsmall | hspecial
  · left
    rw [carryCount_zero_of_small d L hsmall] at hb
    simpa using hb
  · right
    have hlocal := columns_eq_eleven_carry d L hd hspecial.2
    have hsum : wordSum (columnSum d L) L = 11 * carryCount (columnSum d L) L := by
      calc
        wordSum (columnSum d L) L =
            wordSum (fun i => 11 * carry (columnSum d L) (i + 1)) L :=
          wordSum_congr _ _ L hlocal
        _ = 11 * carryCount (columnSum d L) L := wordSum_mul _ _ _
    rw [wordSum_columns, ← digitSum_value d L hd] at hsum
    omega

/-- Zero also obeys the same alternatives; no positivity assumption is
needed for the sharp necessary transition itself. -/
theorem palindrome_step_digitSum_all (n : Nat)
    (hp : Palindrome (step n)) :
    digitSum (step n) = 2 * digitSum n ∨
      11 * digitSum (step n) = 4 * digitSum n := by
  by_cases hn : n = 0
  · subst n
    left
    simp [step, reverse10, reverseFuel, digitSum_zero]
  · exact palindrome_step_digitSum n (by omega) hp

/-- A positive reverse-and-add step preserving digit sum has a
nonpalindromic output. -/
theorem nonpalindrome_of_digitSum_preserved (n : Nat) (hn : 0 < n)
    (hs : digitSum (step n) = digitSum n) : ¬ Palindrome (step n) := by
  intro hp
  have hpos := digitSum_positive n hn
  rcases palindrome_step_digitSum n hn hp with h | h <;> omega

/-- A positive all-time constant-digit-sum orbit yields a Lychrel witness
at its first output. The invariant remains an explicit hypothesis. -/
theorem step_isLychrel_of_constant_digitSum (n : Nat) (hn : 0 < n)
    (hs : ∀ k, digitSum (orbit n k) = digitSum n) : IsLychrel (step n) := by
  intro k
  rw [orbit_from_step]
  apply nonpalindrome_of_digitSum_preserved (orbit n k) (orbit_positive n hn k)
  change digitSum (orbit n (k + 1)) = digitSum (orbit n k)
  rw [hs, hs]

/-- Including a nonpalindromic starting value yields the time-zero version. -/
theorem isLychrel_of_constant_digitSum (n : Nat) (hn : 0 < n)
    (hzero : ¬ Palindrome n)
    (hs : ∀ k, digitSum (orbit n k) = digitSum n) : IsLychrel n := by
  intro k
  cases k with
  | zero => exact hzero
  | succ k =>
    have h := step_isLychrel_of_constant_digitSum n hn hs k
    rwa [orbit_from_step] at h

/-- This is a conditional extraction theorem, not an existence assertion. -/
theorem existence_of_constant_digitSum_orbit
    (h : ∃ n, 0 < n ∧ ∀ k, digitSum (orbit n k) = digitSum n) :
    DecimalLychrelExistence := by
  obtain ⟨n, hn, hs⟩ := h
  exact ⟨step n, step_isLychrel_of_constant_digitSum n hn hs⟩

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
/-- The doubling alternative is attained by an actual palindrome output. -/
theorem doubling_ratio_attained :
    step 12 = 33 ∧ Palindrome (step 12) ∧
      digitSum 12 = 3 ∧ digitSum (step 12) = 6 := by
  have hs : step 12 = 33 := by decide
  refine ⟨hs, ?_, ?_, ?_⟩
  · rw [hs]; decide
  · simp [digitSum]
  · rw [hs]; simp [digitSum]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
/-- The four-elevenths alternative is also attained, so the exceptional
branch cannot be omitted or replaced by strict digit-sum growth. -/
theorem exceptional_ratio_attained :
    step 605 = 1111 ∧ Palindrome (step 605) ∧
      digitSum 605 = 11 ∧ digitSum (step 605) = 4 := by
  have hs : step 605 = 1111 := by decide
  refine ⟨hs, ?_, ?_, ?_⟩
  · rw [hs]; decide
  · simp [digitSum]
  · rw [hs]; simp [digitSum]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
/-- The scalar disjunction is only a necessary test: its exceptional
equality can hold even when the actual output is not a palindrome. -/
theorem exceptional_ratio_not_sufficient :
    step 119 = 1030 ∧ ¬ Palindrome (step 119) ∧
      11 * digitSum (step 119) = 4 * digitSum 119 := by
  have hs : step 119 = 1030 := by decide
  refine ⟨hs, ?_, ?_⟩
  · rw [hs]; decide
  · rw [hs]; simp [digitSum]

#print axioms digitSum_value
#print axioms digitSum_positive
#print axioms digitSum_step_balance
#print axioms palindrome_step_digitSum
#print axioms palindrome_step_digitSum_all
#print axioms nonpalindrome_of_digitSum_preserved
#print axioms step_isLychrel_of_constant_digitSum
#print axioms isLychrel_of_constant_digitSum
#print axioms existence_of_constant_digitSum_orbit
#print axioms doubling_ratio_attained
#print axioms exceptional_ratio_attained
#print axioms exceptional_ratio_not_sufficient

end DecimalMass
