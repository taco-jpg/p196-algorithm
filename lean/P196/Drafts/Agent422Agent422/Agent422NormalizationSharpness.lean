import P196.Drafts.Agent422Agent422.Agent422BaseDigits

/-!
# Universal positive-time sharpness of the width-five normalization example

Agent #422. Exact source: `resume_general_base_normalization_proof.txt`,
SHARPNESS, BOTH PARITIES, at 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5.
All transitions below refer to the independent numeric reversal algorithm via
the proved base-digit and column-certificate soundness theorems.

The all-width, four-step normalization UPPER bound is not a theorem of this
module. Its universal sharpness component is a separate source claim.
-/

namespace Agent422NormalizationSharpness
open Agent422BaseDigits

/-- Complete carry trace includes both c_0 and c_5. -/
def slowCarry (i : Nat) : Nat := if i < 3 then 0 else 1

def pairWord (b z : Nat) : Nat → Nat
  | 0 => b - 1
  | 1 => b - 1
  | 2 => b + z
  | 3 => b - 1
  | 4 => b - 1
  | _ => 0

def firstDigits (b z : Nat) : Nat → Nat
  | 0 => b - 1
  | 1 => b - 1
  | 2 => z
  | 5 => 1
  | _ => 0

def secondDigits (b z : Nat) : Nat → Nat
  | 2 => z + 1
  | 3 => z
  | 4 => b - 1
  | 6 => 1
  | _ => 0

def thirdDigits (b z : Nat) : Nat → Nat
  | 0 => 1
  | 2 => z
  | 3 => (2 * z + 1) % b
  | 4 => z + (2 * z + 1) / b
  | 5 => 1
  | 6 => 1
  | _ => 0

def secondCarry (i : Nat) : Nat := if i = 1 ∨ i = 2 ∨ i = 6 then 1 else 0

def thirdCarry (b z : Nat) : Nat → Nat
  | 3 => 1
  | 4 => (2 * z + 1) / b
  | 5 => 1
  | _ => 0

/-- The observed complete carry word determines the pair sums, apart from the
center parameter. This is universal over every canonical input with that trace. -/
theorem pairWord_forced_by_slow_carry (b : Nat) (hb : 1 < b) (n : Nat)
    (d : Nat → Nat) (hcan : Canonical b n d 5)
    (hc : ∀ i, i ≤ 5 → carry b (columnSum d 5) i = slowCarry i) :
    ∃ z, z ≤ b - 2 ∧ b + z = 2 * d 2 ∧
      ∀ i, i < 5 → columnSum d 5 i = pairWord b z i := by
  let q := columnSum d 5
  have c1 : carry b q 1 = 0 := hc 1 (by decide)
  have c2 : carry b q 2 = 0 := hc 2 (by decide)
  have c3 : carry b q 3 = 1 := hc 3 (by decide)
  have c4 : carry b q 4 = 1 := hc 4 (by decide)
  have c5 : carry b q 5 = 1 := hc 5 (by decide)
  have q4 : q 4 = q 0 := by simp [q, columnSum, reflected, Nat.add_comm]
  have q3 : q 3 = q 1 := by simp [q, columnSum, reflected, Nat.add_comm]
  have q2 : q 2 = 2 * d 2 := by simp [q, columnSum, reflected]; omega
  have e1 : q 0 / b = 0 := by simpa [carry] using c1
  have e2 : (q 1 + carry b q 1) / b = 0 := c2
  have e3 : (q 2 + carry b q 2) / b = 1 := c3
  have e4 : (q 3 + carry b q 3) / b = 1 := c4
  have e5 : (q 4 + carry b q 4) / b = 1 := c5
  rw [c1, Nat.add_zero] at e2
  rw [c2, Nat.add_zero] at e3
  rw [c3, q3] at e4
  rw [c4, q4] at e5
  have hq0lo := le_of_div_one b (q 0 + 1) e5
  have hq0hi := lt_of_div_zero b (by omega) (q 0) e1
  have hq1lo := le_of_div_one b (q 1 + 1) e4
  have hq1hi := lt_of_div_zero b (by omega) (q 1) e2
  have hq0 : q 0 = b - 1 := by omega
  have hq1 : q 1 = b - 1 := by omega
  have hq2lo := le_of_div_one b (q 2) e3
  have hq2hi := columnSum_bounded b d 5 hcan.2.1 2 (by decide)
  change q 2 ≤ 2 * (b - 1) at hq2hi
  refine ⟨q 2 - b, by omega, by omega, ?_⟩
  intro i hi
  change q i = pairWord b (q 2 - b) i
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl <;> simp only [pairWord] <;> omega

theorem firstDigits_bounded (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    ∀ i, i < 6 → firstDigits b z i < b := by
  intro i hi
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl | rfl <;> simp [firstDigits] <;> omega

theorem secondDigits_bounded (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    ∀ i, i < 7 → secondDigits b z i < b := by
  intro i hi
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> simp [secondDigits] <;> omega

theorem middle_carry_bounded (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    (2 * z + 1) / b ≤ 1 := by
  have ht : 2 * z + 1 < 2 * b := by omega
  have hd := (Nat.div_lt_iff_lt_mul (by omega : 0 < b)).2 ht
  omega

theorem thirdDigits_bounded (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    ∀ i, i < 7 → thirdDigits b z i < b := by
  have ht := middle_carry_bounded b z hb hz
  have hm := Nat.mod_lt (2 * z + 1) (by omega : 0 < b)
  intro i hi
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> simp [thirdDigits] <;> omega

/-- First iterate has exactly the six displayed canonical digits. -/
theorem first_step (b : Nat) (hb : 1 < b) (n z : Nat) (d : Nat → Nat)
    (hcan : Canonical b n d 5) (hz : z ≤ b - 2)
    (hq : ∀ i, i < 5 → columnSum d 5 i = pairWord b z i) :
    step b hb n = value b (firstDigits b z) 6 := by
  have hcol : ∀ i, i < 5 → columnSum d 5 i + slowCarry i =
      firstDigits b z i + b * slowCarry (i + 1) := by
    intro i hi
    rw [hq i hi]
    have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
    rcases hi' with rfl | rfl | rfl | rfl | rfl <;>
      simp [pairWord, firstDigits, slowCarry] <;> omega
  have hs := step_of_column_equations b hb n d (firstDigits b z) slowCarry 5 hcan
    (by decide) (fun i hi => firstDigits_bounded b z hb hz i (by omega)) hcol
  calc
    step b hb n = value b (firstDigits b z) 5 + slowCarry 5 * b ^ 5 := hs
    _ = value b (firstDigits b z) 6 := by rfl

/-- Second iterate: all parameter values are proved, not enumerated. -/
theorem second_step (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    step b hb (value b (firstDigits b z) 6) = value b (secondDigits b z) 7 := by
  have hcan : Canonical b (value b (firstDigits b z) 6) (firstDigits b z) 6 :=
    ⟨by decide, firstDigits_bounded b z hb hz, by simp [firstDigits], rfl⟩
  have hcol : ∀ i, i < 6 → columnSum (firstDigits b z) 6 i + secondCarry i =
      secondDigits b z i + b * secondCarry (i + 1) := by
    intro i hi
    have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
    rcases hi' with rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [columnSum, reflected, firstDigits, secondDigits, secondCarry] <;> omega
  have hs := step_of_column_equations b hb _ _ (secondDigits b z) secondCarry 6 hcan
    (by decide) (fun i hi => secondDigits_bounded b z hb hz i (by omega)) hcol
  calc
    step b hb (value b (firstDigits b z) 6) =
        value b (secondDigits b z) 6 + secondCarry 6 * b ^ 6 := hs
    _ = value b (secondDigits b z) 7 := by rfl

/-- Third iterate includes the exact variable-base center quotient and remainder. -/
theorem third_step (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    step b hb (value b (secondDigits b z) 7) = value b (thirdDigits b z) 7 := by
  have hcan : Canonical b (value b (secondDigits b z) 7) (secondDigits b z) 7 :=
    ⟨by decide, secondDigits_bounded b z hb hz, by simp [secondDigits], rfl⟩
  have hm := Nat.mod_add_div (2 * z + 1) b
  have hcol : ∀ i, i < 7 → columnSum (secondDigits b z) 7 i + thirdCarry b z i =
      thirdDigits b z i + b * thirdCarry b z (i + 1) := by
    intro i hi
    have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
    rcases hi' with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [columnSum, reflected, secondDigits, thirdDigits, thirdCarry] <;> omega
  have hs := step_of_column_equations b hb _ _ (thirdDigits b z) (thirdCarry b z) 7 hcan
    (by rfl) (thirdDigits_bounded b z hb hz) hcol
  simpa [thirdCarry] using hs

theorem first_not_palindrome (b z : Nat) (hb : 2 < b) (hz : z ≤ b - 2) :
    ¬ Palindrome b (by omega) (value b (firstDigits b z) 6) := by
  intro hp
  have h := (palindrome_value_iff b (by omega) _ 6 (firstDigits_bounded b z (by omega) hz)
    (Or.inr (by simp [firstDigits]))).1 hp 0 (by decide)
  simp [firstDigits] at h
  omega

theorem second_not_palindrome (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    ¬ Palindrome b hb (value b (secondDigits b z) 7) := by
  intro hp
  have h := (palindrome_value_iff b hb _ 7 (secondDigits_bounded b z hb hz)
    (Or.inr (by simp [secondDigits]))).1 hp 0 (by decide)
  simp [secondDigits] at h

theorem third_not_palindrome (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    ¬ Palindrome b hb (value b (thirdDigits b z) 7) := by
  intro hp
  have h := (palindrome_value_iff b hb _ 7 (thirdDigits_bounded b z hb hz)
    (Or.inr (by simp [thirdDigits]))).1 hp 1 (by decide)
  simp [thirdDigits] at h

/-- The source's universal lower bound: every canonical five-digit integer
with the complete carry trace 000111 avoids palindromes at times 1, 2 and 3.
The result even holds for every base at least 3; no parity premise is needed. -/
theorem slow_carry_requires_at_least_four (b : Nat) (hb : 2 < b) (n : Nat)
    (d : Nat → Nat) (hcan : Canonical b n d 5)
    (hc : ∀ i, i ≤ 5 → carry b (columnSum d 5) i = slowCarry i) :
    ∀ k, 0 < k → k ≤ 3 → ¬ Palindrome b (by omega) (orbit b (by omega) n k) := by
  obtain ⟨z, hz, _, hq⟩ := pairWord_forced_by_slow_carry b (by omega) n d hcan hc
  have h1 := first_step b (by omega) n z d hcan hz hq
  have h2 := second_step b z (by omega) hz
  have h3 := third_step b z (by omega) hz
  intro k hk hk3
  have hk' : k = 1 ∨ k = 2 ∨ k = 3 := by omega
  rcases hk' with rfl | rfl | rfl
  · simpa only [orbit, h1] using first_not_palindrome b z hb hz
  · simpa only [orbit, h1, h2] using second_not_palindrome b z (by omega) hz
  · simpa only [orbit, h1, h2, h3] using third_not_palindrome b z (by omega) hz

/-- The parameterized column word really has the advertised carry trace. -/
theorem pairWord_carries (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    ∀ i, i ≤ 5 → carry b (pairWord b z) i = slowCarry i := by
  apply (column_certificate_sound b (by omega) (pairWord b z) (firstDigits b z) slowCarry 5
    (by decide) (fun i hi => firstDigits_bounded b z hb hz i (by omega)) ?_).1
  intro i hi
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl <;>
    simp [pairWord, firstDigits, slowCarry] <;> omega

/-- A concrete five-digit realization, least significant digit first. -/
def witnessDigits (b z : Nat) (i : Nat) : Nat :=
  if i = 2 then (b + z) / 2 else if 3 ≤ i then b - 1 else 0

def witness (b z : Nat) : Nat := value b (witnessDigits b z) 5

theorem witness_canonical (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    Canonical b (witness b z) (witnessDigits b z) 5 := by
  refine ⟨by decide, ?_, ?_, rfl⟩
  · intro i hi
    unfold witnessDigits
    split
    · omega
    · split <;> omega
  · simp [witnessDigits]
    omega

theorem witness_positive (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2) :
    0 < witness b z := by
  have h := witness_canonical b z hb hz
  exact value_positive b (by omega) _ 5 (by decide) h.2.2.1

theorem witness_columns (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2)
    (heven : (b + z) % 2 = 0) :
    ∀ i, i < 5 → columnSum (witnessDigits b z) 5 i = pairWord b z i := by
  have hm := Nat.mod_add_div (b + z) 2
  rw [heven] at hm
  intro i hi
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl <;>
    simp [columnSum, reflected, witnessDigits, pairWord] <;> omega

theorem witness_carries (b z : Nat) (hb : 1 < b) (hz : z ≤ b - 2)
    (heven : (b + z) % 2 = 0) :
    ∀ i, i ≤ 5 → carry b (columnSum (witnessDigits b z) 5) i = slowCarry i := by
  have hc := carry_congr b (columnSum (witnessDigits b z) 5) (pairWord b z) 5
    (witness_columns b z hb hz heven)
  intro i hi
  exact (hc i hi).trans (pairWord_carries b z hb hz i hi)

/-- The source's even and odd fourth iterates are z=0 and z=1 specializations. -/
def fourthDigits (z : Nat) : Nat → Nat
  | 0 => 2
  | 1 => 1
  | 2 => 2 * z
  | 3 => 4 * z + 2
  | 4 => 2 * z
  | 5 => 1
  | 6 => 2
  | _ => 0

theorem fourthDigits_bounded (b z : Nat) (hsmall : 4 * z + 2 < b) :
    ∀ i, i < 7 → fourthDigits z i < b := by
  intro i hi
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [fourthDigits] <;> omega

/-- An additional proved strengthening: any center parameter with 4z+2<b
has this exact fourth iterate. No parity is required until realizing the seed. -/
theorem fourth_step (b z : Nat) (hsmall : 4 * z + 2 < b) :
    step b (by omega) (value b (thirdDigits b z) 7) = value b (fourthDigits z) 7 := by
  have hz : z ≤ b - 2 := by omega
  have hm : (2 * z + 1) % b = 2 * z + 1 := Nat.mod_eq_of_lt (by omega)
  have hd : (2 * z + 1) / b = 0 := Nat.div_eq_of_lt (by omega)
  have hcan : Canonical b (value b (thirdDigits b z) 7) (thirdDigits b z) 7 :=
    ⟨by decide, thirdDigits_bounded b z (by omega) hz, by simp [thirdDigits], rfl⟩
  apply step_eq_word_value b (by omega) _ _ _ 7 hcan
  intro i hi
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [fourthDigits, columnSum, reflected, thirdDigits, hm, hd] <;> omega

theorem fourth_palindrome (b z : Nat) (hsmall : 4 * z + 2 < b) :
    Palindrome b (by omega) (value b (fourthDigits z) 7) := by
  apply (palindrome_value_iff b (by omega) _ 7 (fourthDigits_bounded b z hsmall)
    (Or.inr (by simp [fourthDigits]))).2
  intro i hi
  have hi' : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases hi' with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> simp [fourthDigits]

theorem witness_fourth_iterate (b z : Nat) (hsmall : 4 * z + 2 < b)
    (heven : (b + z) % 2 = 0) :
    orbit b (by omega) (witness b z) 4 = value b (fourthDigits z) 7 := by
  have hb : 1 < b := by omega
  have hz : z ≤ b - 2 := by omega
  have h1 := first_step b hb (witness b z) z (witnessDigits b z)
    (witness_canonical b z hb hz) hz (witness_columns b z hb hz heven)
  have h2 := second_step b z hb hz
  have h3 := third_step b z hb hz
  have h4 := fourth_step b z hsmall
  simp only [orbit, h1, h2, h3, h4]

/-- For each base at least 7, this REALIZABLE complete carry word has minimum
strictly positive palindrome-hitting time exactly four. This does not assert
a four-step upper bound for every other complete carry word. -/
theorem four_is_optimal_for_slow_carry (b : Nat) (hb : 6 < b) :
    (∃ n d, 0 < n ∧ Canonical b n d 5 ∧
      (∀ i, i ≤ 5 → carry b (columnSum d 5) i = slowCarry i) ∧
      Palindrome b (by omega) (orbit b (by omega) n 4)) ∧
    (∀ n d, Canonical b n d 5 →
      (∀ i, i ≤ 5 → carry b (columnSum d 5) i = slowCarry i) →
      ∀ k, 0 < k → k ≤ 3 → ¬ Palindrome b (by omega) (orbit b (by omega) n k)) := by
  have hz : b % 2 ≤ b - 2 := by omega
  have heven : (b + b % 2) % 2 = 0 := by omega
  have hsmall : 4 * (b % 2) + 2 < b := by omega
  constructor
  · refine ⟨witness b (b % 2), witnessDigits b (b % 2),
      witness_positive b (b % 2) (by omega) hz,
      witness_canonical b (b % 2) (by omega) hz,
      witness_carries b (b % 2) (by omega) hz heven, ?_⟩
    rw [witness_fourth_iterate b (b % 2) hsmall heven]
    exact fourth_palindrome b (b % 2) hsmall
  · exact fun n d hcan hc => slow_carry_requires_at_least_four b (by omega) n d hcan hc

/-- Exact source-domain wrapper: all even bases >=10 and odd bases >=17. -/
theorem source_sharpness (b : Nat)
    (hbase : (b % 2 = 0 ∧ 10 ≤ b) ∨ (b % 2 = 1 ∧ 17 ≤ b)) :
    (∃ n d, 0 < n ∧ Canonical b n d 5 ∧
      (∀ i, i ≤ 5 → carry b (columnSum d 5) i = slowCarry i) ∧
      Palindrome b (by rcases hbase with h | h <;> omega)
        (orbit b (by rcases hbase with h | h <;> omega) n 4)) ∧
    (∀ n d, Canonical b n d 5 →
      (∀ i, i ≤ 5 → carry b (columnSum d 5) i = slowCarry i) →
      ∀ k, 0 < k → k ≤ 3 →
        ¬ Palindrome b (by rcases hbase with h | h <;> omega)
          (orbit b (by rcases hbase with h | h <;> omega) n k)) :=
  four_is_optimal_for_slow_carry b (by rcases hbase with h | h <;> omega)

end Agent422NormalizationSharpness
