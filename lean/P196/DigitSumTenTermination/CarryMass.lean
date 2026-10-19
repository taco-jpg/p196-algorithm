import P196.LowDigitSumTermination.Main

/-!
Digit-mass and carry-count estimates for the digit-sum-ten termination
argument. The finite coefficient inequality and carry-count lower bounds
apply to arbitrary natural-number words. The numeric consequences use the
existing exact decimal digit-sum balance for ordinary reverse-and-add.
-/

namespace DigitSumTenTermination

open DecimalDigits DecimalMass Lychrel196 LowDigitSumTermination

/-- Four pairwise distinct active coefficients fit within the word sum. -/
theorem wordSum_four_le (d : Nat → Nat) (L i j k l : Nat)
    (hi : i < L) (hj : j < L) (hk : k < L) (hl : l < L)
    (hij : i ≠ j) (hik : i ≠ k) (hil : i ≠ l)
    (hjk : j ≠ k) (hjl : j ≠ l) (hkl : k ≠ l) :
    d i + d j + d k + d l ≤ wordSum d L := by
  induction L generalizing i j k l with
  | zero => omega
  | succ L ih =>
      by_cases hiL : i = L
      · subst i
        have h := wordSum_triple_le d L j k l
          (by omega) (by omega) (by omega) hjk hjl hkl
        change d L + d j + d k + d l ≤ wordSum d L + d L
        omega
      · by_cases hjL : j = L
        · subst j
          have h := wordSum_triple_le d L i k l
            (by omega) (by omega) (by omega) hik hil hkl
          change d i + d L + d k + d l ≤ wordSum d L + d L
          omega
        · by_cases hkL : k = L
          · subst k
            have h := wordSum_triple_le d L i j l
              (by omega) (by omega) (by omega) hij hil hjl
            change d i + d j + d L + d l ≤ wordSum d L + d L
            omega
          · by_cases hlL : l = L
            · subst l
              have h := wordSum_triple_le d L i j k
                (by omega) (by omega) (by omega) hij hik hjk
              change d i + d j + d k + d L ≤ wordSum d L + d L
              omega
            · have h := ih i j k l (by omega) (by omega) (by omega) (by omega)
                hij hik hil hjk hjl hkl
              change d i + d j + d k + d l ≤ wordSum d L + d L
              omega

/-- With digit sum at most four, every input column sum is at most eight. -/
theorem step_palindrome_of_digitSum_le_four (n : Nat) (hn : 0 < n)
    (hs : digitSum n ≤ 4) : Palindrome (step n) := by
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  have hmass : wordSum d L ≤ 4 := by
    rw [← digitSum_value d L hcan.2.1, hcan.2.2.2]
    exact hs
  have hsmall : ∀ i, i < L → columnSum d L i ≤ 9 := by
    intro i hi
    have ha := wordSum_single_le d L i hi
    have hb := wordSum_single_le d L (L - 1 - i) (by omega)
    simp only [columnSum, reflected]
    omega
  have hp := (step_palindrome_iff d L hcan.1 hcan.2.1 hcan.2.2.1).mpr
    (Or.inl hsmall)
  rw [hcan.2.2.2] at hp
  exact hp

/-- An input column of at least ten produces a positive outgoing carry. -/
theorem one_le_carry_of_high_column (q : Nat → Nat) (i : Nat)
    (hq : 10 ≤ q i) : 1 ≤ carry q (i + 1) := by
  change 1 ≤ (q i + carry q i) / 10
  omega

/-- One high active column contributes at least one to the carry count. -/
theorem one_le_carryCount_of_high_column (q : Nat → Nat) (L i : Nat)
    (hi : i < L) (hq : 10 ≤ q i) : 1 ≤ carryCount q L := by
  have hc := one_le_carry_of_high_column q i hq
  have hsum := wordSum_single_le (fun j => carry q (j + 1)) L i hi
  change carry q (i + 1) ≤ carryCount q L at hsum
  omega

/-- Two distinct high active columns contribute at least two carries. -/
theorem two_le_carryCount_of_high_columns (q : Nat → Nat) (L i j : Nat)
    (hi : i < L) (hj : j < L) (hij : i ≠ j)
    (hqi : 10 ≤ q i) (hqj : 10 ≤ q j) : 2 ≤ carryCount q L := by
  have hci := one_le_carry_of_high_column q i hqi
  have hcj := one_le_carry_of_high_column q j hqj
  have hsum := wordSum_pair_le (fun k => carry q (k + 1)) L i j hi hj hij
  change carry q (i + 1) + carry q (j + 1) ≤ carryCount q L at hsum
  omega

/-- A high column removes at least nine from the doubled input digit sum. -/
theorem digitSum_step_add_nine_le (n : Nat) (d : Nat → Nat) (L i : Nat)
    (hcan : Canonical n d L) (hi : i < L)
    (hq : 10 ≤ columnSum d L i) :
    digitSum (step n) + 9 ≤ 2 * digitSum n := by
  have hcount := one_le_carryCount_of_high_column (columnSum d L) L i hi hq
  have hbalance := digitSum_step_balance d L hcan.2.1 (Or.inr hcan.2.2.1)
  rw [hcan.2.2.2] at hbalance
  omega

/-- Two distinct high columns remove at least eighteen units of digit sum. -/
theorem digitSum_step_add_eighteen_le (n : Nat) (d : Nat → Nat) (L i j : Nat)
    (hcan : Canonical n d L) (hi : i < L) (hj : j < L) (hij : i ≠ j)
    (hqi : 10 ≤ columnSum d L i) (hqj : 10 ≤ columnSum d L j) :
    digitSum (step n) + 18 ≤ 2 * digitSum n := by
  have hcount := two_le_carryCount_of_high_columns (columnSum d L) L i j
    hi hj hij hqi hqj
  have hbalance := digitSum_step_balance d L hcan.2.1 (Or.inr hcan.2.2.1)
  rw [hcan.2.2.2] at hbalance
  omega

/-- A high noncentral column at digit sum at most ten forces a palindrome
at the second actual reverse-and-add step. -/
theorem second_step_palindrome_of_noncentral_high (n : Nat) (d : Nat → Nat)
    (L i : Nat) (hcan : Canonical n d L) (hs : digitSum n ≤ 10)
    (hi : i < L) (hne : i ≠ L - 1 - i) (hq : 10 ≤ columnSum d L i) :
    Palindrome (step (step n)) := by
  have hr : L - 1 - i < L := by omega
  have hqr : 10 ≤ columnSum d L (L - 1 - i) := by
    rw [← columnSum_symmetric d L i hi]
    exact hq
  have hbound := digitSum_step_add_eighteen_le n d L i (L - 1 - i)
    hcan hi hr hne hq hqr
  have hmass : digitSum (step n) ≤ 2 := by omega
  have hn : 0 < n := by
    rw [← hcan.2.2.2]
    exact value_positive d L hcan.1 hcan.2.2.1
  apply step_palindrome_of_digitSum_le_four (step n)
  · unfold step
    omega
  · omega

#print axioms wordSum_four_le
#print axioms step_palindrome_of_digitSum_le_four
#print axioms one_le_carry_of_high_column
#print axioms one_le_carryCount_of_high_column
#print axioms two_le_carryCount_of_high_columns
#print axioms digitSum_step_add_nine_le
#print axioms digitSum_step_add_eighteen_le
#print axioms second_step_palindrome_of_noncentral_high

end DigitSumTenTermination
