import P196.Foundations.LychrelDigitSums

/-! Agent #13. Exact actual-decimal complementary predecessor family.
Source contract: FINITE_SEED_OBSTRUCTIONS.md section 3; k = m - 1 > 0.
No claim about an infinite safe orbit or about 196. -/

namespace Agent13SafeFamily
open DecimalDigits Lychrel196

/-- The high word a, then two nines, then its reversed nine-complement.
Indices run from the units digit toward the leading digit. -/
def familyDigit (a : Nat → Nat) (k i : Nat) : Nat :=
  if i < k then 9 - a (k - 1 - i)
  else if i < k + 2 then 9
  else a (i - (k + 2))

def family (a : Nat → Nat) (k : Nat) : Nat := value (familyDigit a k) (2*k+2)

def familyColumn (k i : Nat) : Nat := if i = k ∨ i = k+1 then 18 else 9

def target (k : Nat) : Nat := 10^(2*k+2) + 99*10^k - 1

/-- Original safe set: positive, not palindromic now, nor after one step. -/
def Safe (n : Nat) : Prop := 0 < n ∧ ¬ Palindrome n ∧ ¬ Palindrome (step n)

theorem familyDigit_bounded (a : Nat → Nat) (k : Nat)
    (ha : ∀ i, i < k → a i ≤ 9) :
    ∀ i, i < 2*k+2 → familyDigit a k i ≤ 9 := by
  intro i hi
  unfold familyDigit
  split
  · omega
  · split
    · omega
    · exact ha _ (by omega)

theorem familyDigit_leading (a : Nat → Nat) (k : Nat) (hk : 0 < k) :
    familyDigit a k (2*k+2-1) = a (k-1) := by
  simp only [familyDigit, show ¬ 2*k+2-1 < k by omega,
    show ¬ 2*k+2-1 < k+2 by omega, if_false]
  congr 1 <;> omega

theorem family_canonical (a : Nat → Nat) (k : Nat) (hk : 0 < k)
    (ha : ∀ i, i < k → a i ≤ 9) (hlead : 0 < a (k-1)) :
    Canonical (family a k) (familyDigit a k) (2*k+2) := by
  refine ⟨by omega, familyDigit_bounded a k ha, ?_, rfl⟩
  rw [familyDigit_leading a k hk]
  exact hlead

theorem family_columns (a : Nat → Nat) (k : Nat)
    (ha : ∀ i, i < k → a i ≤ 9) :
    ∀ i, i < 2*k+2 → columnSum (familyDigit a k) (2*k+2) i = familyColumn k i := by
  intro i hi
  by_cases hlo : i < k
  · have hr : ¬ 2*k+2-1-i < k := by omega
    have hr2 : ¬ 2*k+2-1-i < k+2 := by omega
    have hj : 2*k+2-1-i-(k+2) = k-1-i := by omega
    have hb := ha (k-1-i) (by omega)
    simp only [columnSum, reflected, familyDigit, hlo, if_true,
      hr, hr2, if_false, hj, familyColumn,
      show ¬ (i = k ∨ i = k+1) by omega]
    omega
  · by_cases hmid : i < k+2
    · have hr : ¬ 2*k+2-1-i < k := by omega
      have hr2 : 2*k+2-1-i < k+2 := by omega
      simp only [columnSum, reflected, familyDigit, hlo, hmid, hr, hr2,
        if_true, if_false, familyColumn, show i = k ∨ i = k+1 by omega]
    · have hr : 2*k+2-1-i < k := by omega
      have hj : k-1-(2*k+2-1-i) = i-(k+2) := by omega
      have hb := ha (i-(k+2)) (by omega)
      simp only [columnSum, reflected, familyDigit, hlo, hmid, if_false,
        hr, if_true, hj, familyColumn,
        show ¬ (i = k ∨ i = k+1) by omega]
      omega

theorem family_not_palindrome (a : Nat → Nat) (k : Nat) (hk : 0 < k)
    (ha : ∀ i, i < k → a i ≤ 9) (hlead : 0 < a (k-1)) :
    ¬ Palindrome (family a k) := by
  intro hp
  have hc := family_canonical a k hk ha hlead
  have hs := (palindrome_value_iff _ _ hc.2.1 (Or.inr hc.2.2.1)).mp hp
  have hz := hs 0 (by omega)
  have hb := ha (k-1) (by omega)
  simp only [Nat.sub_zero, familyDigit_leading a k hk] at hz
  have hu : familyDigit a k 0 = 9-a (k-1) := by simp [familyDigit, hk]
  rw [hu] at hz
  omega

/-- A geometric-sum identity with no truncated subtraction. -/
theorem value_nines (L : Nat) : value (fun _ => 9) L + 1 = 10^L := by
  induction L with
  | zero => simp [value]
  | succ L ih => simp only [value, Nat.pow_succ]; omega

theorem value_single (j a L : Nat) :
    value (fun i => if i = j then a else 0) L = if j < L then a*10^j else 0 := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    simp only [value, ih]
    by_cases h : j < L
    · simp [h, show j < L+1 by omega, show L ≠ j by omega]
    · by_cases he : L = j
      · subst j; simp
      · simp [h, he, show ¬ j < L+1 by omega]

theorem familyColumn_value (k : Nat) : value (familyColumn k) (2*k+2) = target k := by
  have hpoint : ∀ i, i < 2*k+2 → familyColumn k i =
      9 + ((if i=k then 9 else 0) + (if i=k+1 then 9 else 0)) := by
    intro i hi
    unfold familyColumn
    by_cases h : i=k <;> by_cases h' : i=k+1 <;> simp [h,h'] <;> omega
  rw [value_congr _ _ _ hpoint, value_add, value_add, value_single, value_single]
  simp only [show k < 2*k+2 by omega, show k+1 < 2*k+2 by omega, if_true]
  have h := value_nines (2*k+2)
  unfold target
  rw [Nat.pow_succ]
  omega

theorem family_step (a : Nat → Nat) (k : Nat) (hk : 0 < k)
    (ha : ∀ i, i < k → a i ≤ 9) (hlead : 0 < a (k-1)) :
    step (family a k) = target k := by
  rw [FoldedDecimal.step_eq_word_value _ _ _ _
    (family_canonical a k hk ha hlead) (family_columns a k ha)]
  exact familyColumn_value k

/-- Uniform carry computation across the central two high columns. -/
theorem familyColumn_carry (k i : Nat) :
    carry (familyColumn k) i = if i ≤ k then 0 else 1 := by
  induction i with
  | zero => simp [carry]
  | succ i ih =>
    simp only [carry, ih, familyColumn]
    by_cases h : i < k
    · simp [show i ≤ k by omega, show i+1 ≤ k by omega,
        show ¬ (i=k ∨ i=k+1) by omega]
    · by_cases he : i = k
      · subst i; simp [show ¬ k+1 ≤ k by omega]
      · by_cases he' : i = k+1
        · subst i; simp [show ¬ k+1 ≤ k by omega, show ¬ k+1+1 ≤ k by omega]
        · simp [show ¬ i ≤ k by omega, show ¬ i+1 ≤ k by omega,
            show ¬ (i=k ∨ i=k+1) by omega]

theorem family_column_overflow (a : Nat → Nat) (k : Nat)
    (ha : ∀ i, i < k → a i ≤ 9) :
    carry (columnSum (familyDigit a k) (2*k+2)) (2*k+2) = 1 := by
  rw [FoldedDecimal.carry_congr_upto _ _ _ (family_columns a k ha) _ (by omega),
    familyColumn_carry]
  simp [show ¬ 2*k+2 ≤ k by omega]

/-- Equality of full family values recovers every digit of the high word. -/
theorem family_injective (a b : Nat → Nat) (k : Nat)
    (ha : ∀ i, i < k → a i ≤ 9) (hb : ∀ i, i < k → b i ≤ 9)
    (heq : family a k = family b k) : ∀ i, i < k → a i = b i := by
  have hs := value_injective _ _ _ (familyDigit_bounded a k ha)
    (familyDigit_bounded b k hb) heq
  intro i hi
  have h := hs (i+k+2) (by omega)
  simpa [familyDigit, show ¬ i+k+2 < k by omega,
    show ¬ i+k+2 < k+2 by omega, show i+k+2-(k+2)=i by omega] using h

end Agent13SafeFamily
