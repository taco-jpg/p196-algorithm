import GeneralBaseNormalization

/-!
Agent #4: ordinary arithmetic bridge for the checked normalization subclaims.
Every coefficient is connected to genuine bounded digits before the threshold
carry is identified with the quotient carry. Positional evaluation is ordinary
natural-number arithmetic; reflection retains input width and leading zeroes
in the reversed numeral. No infinite orbit or four-step theorem is asserted.
-/
namespace P196.Agent4.GeneralBase

/-- The threshold carry agrees with ordinary division for genuine pair sums. -/
theorem carryStep_eq_div (b q c : Nat) (hb : 2 ≤ b)
    (hq : q ≤ 2 * (b - 1)) (hc : c ≤ 1) :
    carryStep b q c = (q + c) / b := by
  unfold carryStep
  split
  · next h =>
      symm
      apply (Nat.div_eq_iff (by omega : 0 < b)).2
      constructor <;> simp only [Nat.one_mul] <;> omega
  · next h =>
      symm
      apply Nat.div_eq_of_lt
      omega

/-- Ordinary schoolbook quotient carries, independently of threshold carries. -/
def arithmeticCarry (b : Nat) (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | k + 1 => (q k + arithmeticCarry b q k) / b

theorem arithmeticCarry_eq_carryAt (b n : Nat) (q : Nat → Nat)
    (hb : 2 ≤ b) (hq : ∀ i < n, q i ≤ 2 * (b - 1))
    (k : Nat) (hk : k ≤ n) : arithmeticCarry b q k = carryAt b q k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simp only [arithmeticCarry, carryAt]
      rw [ih (by omega)]
      exact (carryStep_eq_div b (q k) (carryAt b q k) hb
        (hq k (by omega)) (carryAt_bit b q k)).symm

theorem arithmeticCarry_congr (b n : Nat) (q r : Nat → Nat)
    (heq : ∀ i < n, q i = r i) (k : Nat) (hk : k ≤ n) :
    arithmeticCarry b q k = arithmeticCarry b r k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simp only [arithmeticCarry]
      rw [heq k (by omega), ih (by omega)]

def pairCoeff (n : Nat) (d : Nat → Nat) (i : Nat) : Nat :=
  d i + d (n - 1 - i)

def CanonicalDigits (b n : Nat) (d : Nat → Nat) : Prop :=
  0 < n ∧ (∀ i < n, d i < b) ∧ 0 < d (n - 1)

theorem pairCoeff_symmetric (n : Nat) (d : Nat → Nat) :
    Symmetric n (pairCoeff n d) := by
  intro i hi
  unfold pairCoeff
  rw [mirror_index n i hi]
  omega

theorem pairCoeff_bound (b n : Nat) (d : Nat → Nat)
    (hd : ∀ i < n, d i < b) (i : Nat) (hi : i < n) :
    pairCoeff n d i ≤ 2 * (b - 1) := by
  have h1 := hd i hi
  have h2 := hd (n - 1 - i) (by omega)
  unfold pairCoeff
  omega

theorem normalized_arithmetic_carries (b n : Nat) (q : Nat → Nat)
    (hb : 4 ≤ b) (hs : Symmetric n q)
    (hq : ∀ i < n, q i ≤ 2 * (b - 1)) (k : Nat) (hk : k ≤ n) :
    arithmeticCarry b (normalized b (chosenLow b n q) n q) k =
      arithmeticCarry b q k := by
  have hlow := chosenLow_bound b n q hb
  have hnorm : ∀ i < n,
      normalized b (chosenLow b n q) n q i ≤ 2 * (b - 1) := by
    intro i hi
    have h := normalSum_le_base b (chosenLow b n q)
      (carryAt b q (i + 1)) (carryAt b q (n - i)) (by omega)
    change normalSum b (chosenLow b n q) _ _ ≤ 2 * (b - 1)
    omega
  calc
    arithmeticCarry b (normalized b (chosenLow b n q) n q) k =
        carryAt b (normalized b (chosenLow b n q) n q) k :=
      arithmeticCarry_eq_carryAt b n _ (by omega) hnorm k hk
    _ = carryAt b q k :=
      complete_carry_word_preserved b (chosenLow b n q) n q
        (by omega) hlow hs k hk
    _ = arithmeticCarry b q k :=
      (arithmeticCarry_eq_carryAt b n q (by omega) hq k hk).symm

/-- The same canonical width and the entire actual first-addition carry word. -/
theorem canonical_normalization_representative (b n : Nat) (d : Nat → Nat)
    (hb : 4 ≤ b) (hbe : b % 2 = 0) (hd : CanonicalDigits b n d) :
    ∃ e : Nat → Nat, CanonicalDigits b n e ∧
      (∀ i < n, pairCoeff n e i =
        normalized b (chosenLow b n (pairCoeff n d)) n (pairCoeff n d) i) ∧
      (∀ k ≤ n, arithmeticCarry b (pairCoeff n e) k =
        arithmeticCarry b (pairCoeff n d) k) := by
  obtain ⟨e, he, hpos, hpairs, _⟩ :=
    normalization_has_same_width_representative b n (pairCoeff n d)
      hb hbe hd.1 (pairCoeff_symmetric n d)
  refine ⟨e, ⟨hd.1, he, hpos⟩, hpairs, ?_⟩
  intro k hk
  calc
    arithmeticCarry b (pairCoeff n e) k =
        arithmeticCarry b
          (normalized b (chosenLow b n (pairCoeff n d)) n (pairCoeff n d)) k :=
      arithmeticCarry_congr b n _ _ hpairs k hk
    _ = arithmeticCarry b (pairCoeff n d) k :=
      normalized_arithmetic_carries b n (pairCoeff n d) hb
        (pairCoeff_symmetric n d) (pairCoeff_bound b n d hd.2.1) k hk

/-- Positional value of a finite least-significant-first digit function. -/
def value (b : Nat) (d : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => value b d n + d n * b ^ n

theorem value_add (b n : Nat) (d e : Nat → Nat) :
    value b (fun i => d i + e i) n = value b d n + value b e n := by
  induction n with
  | zero => simp [value]
  | succ n ih =>
      simp only [value, ih, Nat.add_mul]
      omega

theorem pair_value (b n : Nat) (d : Nat → Nat) :
    value b (pairCoeff n d) n =
      value b d n + value b (fun i => d (n - 1 - i)) n := by
  exact value_add b n d (fun i => d (n - 1 - i))

/-- Ordinary output digits: Euclidean remainders, not a modeled safety label. -/
def arithmeticOutput (b : Nat) (q : Nat → Nat) (i : Nat) : Nat :=
  (q i + arithmeticCarry b q i) % b

/-- The complete schoolbook sum, including the final carry, is exact. -/
theorem value_carry_conservation (b : Nat) (q : Nat → Nat) (n : Nat) :
    value b (arithmeticOutput b q) n + arithmeticCarry b q n * b ^ n =
      value b q n := by
  induction n with
  | zero => simp [value, arithmeticCarry]
  | succ n ih =>
      have hlocal := congrArg (fun x : Nat => x * b ^ n)
        (Nat.mod_add_div (q n + arithmeticCarry b q n) b)
      simp only [Nat.add_mul] at hlocal
      have hrearr : (q n + arithmeticCarry b q n) / b * (b ^ n * b) =
          (b * ((q n + arithmeticCarry b q n) / b)) * b ^ n := by
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
      simp only [value, arithmeticOutput, arithmeticCarry, Nat.pow_succ]
      rw [hrearr]
      omega

/-- The digit algorithm computes the ordinary number plus its width-aware reverse. -/
theorem reverse_add_arithmetic (b n : Nat) (d : Nat → Nat) :
    value b (arithmeticOutput b (pairCoeff n d)) n +
      arithmeticCarry b (pairCoeff n d) n * b ^ n =
        value b d n + value b (fun i => d (n - 1 - i)) n := by
  rw [value_carry_conservation, pair_value]

theorem arithmeticOutput_lt_base (b : Nat) (q : Nat → Nat) (i : Nat)
    (hb : 0 < b) : arithmeticOutput b q i < b := by
  exact Nat.mod_lt _ hb

theorem value_lt_pow (b n : Nat) (d : Nat → Nat)
    (hd : ∀ i < n, d i < b) : value b d n < b ^ n := by
  induction n with
  | zero => simp [value]
  | succ n ih =>
      have hp := ih (fun i hi => hd i (by omega))
      have hn := hd n (by omega)
      have hm := Nat.mul_le_mul_right (b ^ n) (show d n + 1 ≤ b by omega)
      have hsum := Nat.add_lt_add_right hp (d n * b ^ n)
      have hrewrite : b ^ n + d n * b ^ n = (d n + 1) * b ^ n := by
        simp [Nat.add_mul, Nat.add_comm]
      calc
        value b d (n + 1) = value b d n + d n * b ^ n := rfl
        _ < b ^ n + d n * b ^ n := hsum
        _ = (d n + 1) * b ^ n := hrewrite
        _ ≤ b * b ^ n := hm
        _ = b ^ (n + 1) := by simp [Nat.pow_succ, Nat.mul_comm]

theorem value_ge_top_power (b n : Nat) (d : Nat → Nat)
    (hn : 0 < n) (hd : 0 < d (n - 1)) : b ^ (n - 1) ≤ value b d n := by
  cases n with
  | zero => omega
  | succ k =>
      simp only [Nat.succ_sub_one] at hd ⊢
      have hm := Nat.mul_le_mul_right (b ^ k) (show 1 ≤ d k by omega)
      simp only [Nat.one_mul] at hm
      simp only [value]
      omega

/-- Canonical digits certify the actual natural-number width, not a nominal width. -/
theorem canonical_value_bounds (b n : Nat) (d : Nat → Nat)
    (hd : CanonicalDigits b n d) :
    b ^ (n - 1) ≤ value b d n ∧ value b d n < b ^ n := by
  exact ⟨value_ge_top_power b n d hd.1 hd.2.2,
    value_lt_pow b n d hd.2.1⟩

/-- Numeric witnesses retain the source's real width and actual quotient carries. -/
theorem normalization_numeric_witness (b n : Nat) (d : Nat → Nat)
    (hb : 4 ≤ b) (hbe : b % 2 = 0) (hd : CanonicalDigits b n d) :
    ∃ e : Nat → Nat, CanonicalDigits b n e ∧
      b ^ (n - 1) ≤ value b e n ∧ value b e n < b ^ n ∧
      (∀ k ≤ n, arithmeticCarry b (pairCoeff n e) k =
        arithmeticCarry b (pairCoeff n d) k) := by
  obtain ⟨e, he, _, hc⟩ := canonical_normalization_representative b n d hb hbe hd
  obtain ⟨hlo, hhi⟩ := canonical_value_bounds b n e he
  exact ⟨e, he, hlo, hhi, hc⟩

end P196.Agent4.GeneralBase

#print axioms P196.Agent4.GeneralBase.carryStep_eq_div
#print axioms P196.Agent4.GeneralBase.arithmeticCarry_eq_carryAt
#print axioms P196.Agent4.GeneralBase.arithmeticCarry_congr
#print axioms P196.Agent4.GeneralBase.pairCoeff_symmetric
#print axioms P196.Agent4.GeneralBase.pairCoeff_bound
#print axioms P196.Agent4.GeneralBase.normalized_arithmetic_carries
#print axioms P196.Agent4.GeneralBase.canonical_normalization_representative
#print axioms P196.Agent4.GeneralBase.value_add
#print axioms P196.Agent4.GeneralBase.pair_value
#print axioms P196.Agent4.GeneralBase.value_carry_conservation
#print axioms P196.Agent4.GeneralBase.reverse_add_arithmetic
#print axioms P196.Agent4.GeneralBase.arithmeticOutput_lt_base
#print axioms P196.Agent4.GeneralBase.value_lt_pow
#print axioms P196.Agent4.GeneralBase.value_ge_top_power
#print axioms P196.Agent4.GeneralBase.canonical_value_bounds
#print axioms P196.Agent4.GeneralBase.normalization_numeric_witness
