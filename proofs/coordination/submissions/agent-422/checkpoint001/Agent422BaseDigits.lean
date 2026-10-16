import Std

/-!
# Base-parametric natural-number digit semantics

Agent #422. Generalization of the independent decimal definitions and proofs in
`proofs/research/Lychrel196Research.lean`, namespaces `Lychrel196` and
`DecimalDigits`, at commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5.
The definitions agree with ordinary numeric reversal, including dropping zeros
at the front of the reversed representation. No symbolic-to-numeric bridge is
assumed. The base is any natural number greater than one.

This module supplies dependencies for the base-parametric normalization
sharpness proof; it does not assert an infinite palindrome-avoiding orbit.
-/

namespace Agent422BaseDigits

/-- Numeric reversal by repeated quotient and remainder. -/
def reverseAux (b : Nat) (hb : 1 < b) (n acc : Nat) : Nat :=
  if h : n = 0 then acc
  else reverseAux b hb (n / b) (b * acc + n % b)
termination_by n
decreasing_by exact Nat.div_lt_self (Nat.pos_of_ne_zero h) hb

def reverse (b : Nat) (hb : 1 < b) (n : Nat) : Nat := reverseAux b hb n 0

def Palindrome (b : Nat) (hb : 1 < b) (n : Nat) : Prop := reverse b hb n = n

def step (b : Nat) (hb : 1 < b) (n : Nat) : Nat := n + reverse b hb n

/-- Iteration continues after reaching a palindrome and includes time zero. -/
def orbit (b : Nat) (hb : 1 < b) (n : Nat) : Nat → Nat
  | 0 => n
  | k + 1 => step b hb (orbit b hb n k)

/-- Positional value of a least-significant-first, fixed-width word. -/
def value (b : Nat) (d : Nat → Nat) : Nat → Nat
  | 0 => 0
  | L + 1 => value b d L + d L * b ^ L

def reflected (d : Nat → Nat) (L : Nat) (i : Nat) : Nat := d (L - 1 - i)

def columnSum (d : Nat → Nat) (L : Nat) (i : Nat) : Nat :=
  d i + reflected d L i

/-- Incoming carry, including the initial zero at index zero. -/
def carry (b : Nat) (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | i + 1 => (q i + carry b q i) / b

def output (b : Nat) (q : Nat → Nat) (i : Nat) : Nat :=
  (q i + carry b q i) % b

/-- Nonempty canonical numeral: bounded digits and nonzero leading digit. -/
def Canonical (b n : Nat) (d : Nat → Nat) (L : Nat) : Prop :=
  0 < L ∧ (∀ i, i < L → d i < b) ∧ 0 < d (L - 1) ∧ n = value b d L

theorem orbit_from_step (b : Nat) (hb : 1 < b) (n k : Nat) :
    orbit b hb (step b hb n) k = orbit b hb n (k + 1) := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [orbit, ih]

theorem value_congr (b : Nat) (a d : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → a i = d i) : value b a L = value b d L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    simp only [value, ih (fun i hi => h i (by omega)), h L (by omega)]

theorem value_add (b : Nat) (a d : Nat → Nat) (L : Nat) :
    value b (fun i => a i + d i) L = value b a L + value b d L := by
  induction L with
  | zero => rfl
  | succ L ih => simp only [value, ih, Nat.add_mul]; omega

theorem value_shift (b : Nat) (d : Nat → Nat) (L : Nat) :
    value b d (L + 1) = d 0 + b * value b (fun i => d (i + 1)) L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    simp only [value, Nat.pow_succ] at ih ⊢
    have hm : d (L + 1) * (b ^ L * b) = b * (d (L + 1) * b ^ L) := by
      simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
    rw [Nat.mul_add, hm]
    omega

theorem reflected_value_shift (b : Nat) (d : Nat → Nat) (L : Nat) :
    value b (reflected d (L + 1)) (L + 1) =
      value b (reflected (fun i => d (i + 1)) L) L + d 0 * b ^ L := by
  simp only [value]
  have h : value b (reflected d (L + 1)) L =
      value b (reflected (fun i => d (i + 1)) L) L := by
    apply value_congr
    intro i hi
    simp only [reflected]
    congr 1
    omega
  rw [h]
  simp [reflected]

theorem value_positive (b : Nat) (hb : 0 < b) (d : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hlead : 0 < d (L - 1)) : 0 < value b d L := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  have hlead' : 0 < d k := by simpa using hlead
  have hm := Nat.mul_pos hlead' (Nat.pow_pos hb : 0 < b ^ k)
  simp only [value]
  omega

theorem value_mod (b : Nat) (d : Nat → Nat) (L : Nat) (h0 : d 0 < b) :
    value b d (L + 1) % b = d 0 := by
  rw [value_shift, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt h0]

theorem value_div (b : Nat) (hb : 0 < b) (d : Nat → Nat) (L : Nat)
    (h0 : d 0 < b) :
    value b d (L + 1) / b = value b (fun i => d (i + 1)) L := by
  rw [value_shift, Nat.add_mul_div_left _ _ hb, Nat.div_eq_of_lt h0, Nat.zero_add]

/-- Independent numeric reversal equals fixed-width positional reflection.
The leading-digit hypothesis is essential and is not silently dropped. -/
theorem reverseAux_value (b : Nat) (hb : 1 < b) (d : Nat → Nat) (L acc : Nat)
    (hd : ∀ i, i < L → d i < b)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    reverseAux b hb (value b d L) acc =
      acc * b ^ L + value b (reflected d L) L := by
  induction L generalizing d acc with
  | zero => simp [value, reverseAux]
  | succ L ih =>
    have hd0 := hd 0 (by omega)
    have hlead' : 0 < d L := by simpa using hlead
    have hpos := value_positive b (by omega) d (L + 1) (by omega)
      (by simpa using hlead')
    rw [reverseAux]
    simp only [Nat.ne_of_gt hpos, ↓reduceDIte, ↓reduceIte,
      value_mod b d L hd0, value_div b (by omega) d L hd0]
    rw [ih]
    · rw [reflected_value_shift, Nat.pow_succ, Nat.add_mul]
      have hm : b * acc * b ^ L = acc * (b ^ L * b) := by
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
      rw [hm]
      omega
    · intro i hi
      exact hd (i + 1) (by omega)
    · by_cases h : L = 0
      · exact Or.inl h
      · right
        have hi : L - 1 + 1 = L := by omega
        simpa only [hi] using hlead'

theorem reverse_value (b : Nat) (hb : 1 < b) (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i < b)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    reverse b hb (value b d L) = value b (reflected d L) L := by
  simpa [reverse] using reverseAux_value b hb d L 0 hd hlead

theorem value_injective (b : Nat) (hb : 0 < b) (a d : Nat → Nat) (L : Nat)
    (ha : ∀ i, i < L → a i < b) (hd : ∀ i, i < L → d i < b)
    (heq : value b a L = value b d L) : ∀ i, i < L → a i = d i := by
  induction L generalizing a d with
  | zero => intro i hi; omega
  | succ L ih =>
    have ha0 := ha 0 (by omega)
    have hd0 := hd 0 (by omega)
    have hz := congrArg (fun n => n % b) heq
    change value b a (L + 1) % b = value b d (L + 1) % b at hz
    rw [value_mod b a L ha0, value_mod b d L hd0] at hz
    have ht := congrArg (fun n => n / b) heq
    change value b a (L + 1) / b = value b d (L + 1) / b at ht
    rw [value_div b hb a L ha0, value_div b hb d L hd0] at ht
    intro i hi
    cases i with
    | zero => exact hz
    | succ i =>
      exact ih (fun j => a (j + 1)) (fun j => d (j + 1))
        (fun j hj => ha (j + 1) (by omega))
        (fun j hj => hd (j + 1) (by omega)) ht i (by omega)

/-- Palindromicity of an actual natural number, not a newly defined word target. -/
theorem palindrome_value_iff (b : Nat) (hb : 1 < b) (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i < b)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    Palindrome b hb (value b d L) ↔ ∀ i, i < L → d i = d (L - 1 - i) := by
  unfold Palindrome
  rw [reverse_value b hb d L hd hlead]
  constructor
  · intro h
    exact value_injective b (by omega) d (reflected d L) L hd
      (fun i hi => hd (L - 1 - i) (by omega)) h.symm
  · intro h
    exact (value_congr b d (reflected d L) L h).symm

theorem columnSum_symmetric (d : Nat → Nat) (L i : Nat) (hi : i < L) :
    columnSum d L i = columnSum d L (L - 1 - i) := by
  have h : L - 1 - (L - 1 - i) = i := by omega
  simp only [columnSum, reflected, h]
  omega

theorem columnSum_bounded (b : Nat) (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i < b) :
    ∀ i, i < L → columnSum d L i ≤ 2 * (b - 1) := by
  intro i hi
  have ha := hd i hi
  have hb := hd (L - 1 - i) (by omega)
  simp only [columnSum, reflected]
  omega

theorem column_equation (b : Nat) (q : Nat → Nat) (i : Nat) :
    output b q i + b * carry b q (i + 1) = q i + carry b q i := by
  simp only [output, carry]
  exact Nat.mod_add_div _ _

theorem carry_bounded (b : Nat) (hb : 0 < b) (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 2 * (b - 1)) :
    ∀ i, i ≤ L → carry b q i ≤ 1 := by
  intro i
  induction i with
  | zero => intro _; simp [carry]
  | succ i ih =>
    intro hi
    have hc := ih (by omega)
    have hqi := hq i (by omega)
    have hx : q i + carry b q i < 2 * b := by omega
    have hy := (Nat.div_lt_iff_lt_mul hb).2 hx
    change (q i + carry b q i) / b ≤ 1
    omega

theorem output_bounded (b : Nat) (hb : 0 < b) (q : Nat → Nat) (i : Nat) :
    output b q i < b := Nat.mod_lt _ hb

/-- Column carrying preserves the exact positional value. -/
theorem value_output (b : Nat) (q : Nat → Nat) (L : Nat) :
    value b (output b q) L + carry b q L * b ^ L = value b q L := by
  induction L with
  | zero => simp [value, carry]
  | succ L ih =>
    have h := congrArg (fun x => x * b ^ L) (column_equation b q L)
    simp only [Nat.add_mul] at h
    simp only [value, Nat.pow_succ]
    have hc : carry b q (L + 1) * (b ^ L * b) =
        b * carry b q (L + 1) * b ^ L := by
      simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
    rw [hc]
    omega

theorem reverse_add_value (b : Nat) (d : Nat → Nat) (L : Nat) :
    value b (output b (columnSum d L)) L + carry b (columnSum d L) L * b ^ L =
      value b d L + value b (reflected d L) L := by
  rw [value_output]
  exact value_add b d (reflected d L) L

theorem step_value (b : Nat) (hb : 1 < b) (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i < b)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    step b hb (value b d L) =
      value b (output b (columnSum d L)) L + carry b (columnSum d L) L * b ^ L := by
  rw [step, reverse_value b hb d L hd hlead]
  exact (reverse_add_value b d L).symm

/-- An uncarried pair-sum word already equals the next numeric iterate. -/
theorem step_eq_word_value (b : Nat) (hb : 1 < b) (n : Nat)
    (d q : Nat → Nat) (L : Nat) (hcan : Canonical b n d L)
    (hq : ∀ i, i < L → q i = columnSum d L i) :
    step b hb n = value b q L := by
  rw [hcan.2.2.2, step_value b hb d L hcan.2.1 (Or.inr hcan.2.2.1), value_output]
  exact value_congr b (columnSum d L) q L (fun i hi => (hq i hi).symm)

/-- A quotient-zero fact gives the exact input range, even for variable bases. -/
theorem lt_of_div_zero (b : Nat) (hb : 0 < b) (n : Nat) (h : n / b = 0) :
    n < b := by
  have hm := Nat.mod_lt n hb
  have he := Nat.mod_add_div n b
  rw [h, Nat.mul_zero, Nat.add_zero] at he
  omega

theorem le_of_div_one (b n : Nat) (h : n / b = 1) : b ≤ n := by
  have he := Nat.mod_add_div n b
  rw [h, Nat.mul_one] at he
  omega

/-- Soundness of a finite column certificate. Every local equation is an
ordinary natural-number equality; no external evaluator is trusted. -/
theorem column_certificate_sound (b : Nat) (hb : 0 < b)
    (q e c : Nat → Nat) (L : Nat) (hc0 : c 0 = 0)
    (he : ∀ i, i < L → e i < b)
    (hcol : ∀ i, i < L → q i + c i = e i + b * c (i + 1)) :
    (∀ i, i ≤ L → carry b q i = c i) ∧
      (∀ i, i < L → output b q i = e i) := by
  have hc : ∀ i, i ≤ L → carry b q i = c i := by
    intro i
    induction i with
    | zero => intro _; simpa [carry] using hc0.symm
    | succ i ih =>
      intro hi
      change (q i + carry b q i) / b = c (i + 1)
      rw [ih (by omega), hcol i (by omega),
        Nat.add_mul_div_left _ _ hb, Nat.div_eq_of_lt (he i (by omega)), Nat.zero_add]
  refine ⟨hc, ?_⟩
  intro i hi
  unfold output
  rw [hc i (by omega), hcol i hi, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt (he i hi)]

/-- Certificate-to-conclusion bridge for actual integer reverse-and-add. -/
theorem step_of_column_equations (b : Nat) (hb : 1 < b) (n : Nat)
    (d e c : Nat → Nat) (L : Nat) (hcan : Canonical b n d L)
    (hc0 : c 0 = 0) (he : ∀ i, i < L → e i < b)
    (hcol : ∀ i, i < L → columnSum d L i + c i = e i + b * c (i + 1)) :
    step b hb n = value b e L + c L * b ^ L := by
  obtain ⟨hcarry, hout⟩ := column_certificate_sound b (by omega) (columnSum d L) e c L hc0 he hcol
  rw [hcan.2.2.2, step_value b hb d L hcan.2.1 (Or.inr hcan.2.2.1), hcarry L (by omega)]
  rw [value_congr b (output b (columnSum d L)) e L hout]

/-- Equal input columns give equal complete carry prefixes. -/
theorem carry_congr (b : Nat) (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) :
    ∀ i, i ≤ L → carry b q i = carry b r i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    simp only [carry, h i (by omega), ih (by omega)]

end Agent422BaseDigits
