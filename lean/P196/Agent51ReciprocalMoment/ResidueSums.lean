import P196.Agent51ReciprocalMoment.OverflowDigits

/-!
Literal evaluations of the overflow-saturating mirrored coefficient word.
All sums use the source coefficients, including the actual positional powers.
No ordinary-integer congruence modulo eleven is asserted at even width.
-/

namespace P196.Agent51

/-- A finite integer sum over exactly the indices below n. -/
def finiteSum (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n + 1 => finiteSum f n + f n

private theorem int_sum_append (xs ys : List Int) :
    (xs ++ ys).sum = xs.sum + ys.sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih, Int.add_assoc]

/-- The recursive helper agrees with the literal finite list sum. -/
theorem finiteSum_eq_range (f : Nat → Int) (n : Nat) :
    finiteSum f n = ((List.range n).map f).sum := by
  induction n with
  | zero => simp [finiteSum]
  | succ n ih => simp [finiteSum, List.range_succ, List.map_append,
      int_sum_append, ih]

/-- The ordinary polynomial evaluation appearing in the source report. -/
def polynomialValue (q : Nat → Nat) (L : Nat) (x : Int) : Int :=
  ((List.range L).map (fun i => (q i : Int) * x ^ i)).sum

theorem polynomialValue_eq_finiteSum (q : Nat → Nat) (L : Nat) (x : Int) :
    polynomialValue q L x = finiteSum (fun i => (q i : Int) * x ^ i) L := by
  exact (finiteSum_eq_range _ _).symm

theorem finiteSum_congr (f g : Nat → Int) (n : Nat)
    (h : ∀ i < n, f i = g i) : finiteSum f n = finiteSum g n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [finiteSum]
    rw [ih (fun i hi => h i (by omega)), h n (by omega)]

theorem finiteSum_add_length (f : Nat → Int) (a b : Nat) :
    finiteSum f (a + b) = finiteSum f a + finiteSum (fun i => f (a + i)) b := by
  induction b with
  | zero => simp [finiteSum]
  | succ b ih => simp [finiteSum, ih, Int.add_assoc]

theorem finiteSum_const (c : Int) (n : Nat) :
    finiteSum (fun _ => c) n = (n : Int) * c := by
  induction n with
  | zero => simp [finiteSum]
  | succ n ih => simp [finiteSum, ih, Int.ofNat_add, Int.add_mul]

theorem finiteSum_mul_left (c : Int) (f : Nat → Int) (n : Nat) :
    finiteSum (fun i => c * f i) n = c * finiteSum f n := by
  induction n with
  | zero => simp [finiteSum]
  | succ n ih => simp [finiteSum, ih, Int.mul_add]

/-- Splitting the literal polynomial into its two disjoint coefficient blocks. -/
theorem pairWord_polynomial_blocks (L k : Nat) (hL : 2 * k ≤ L) (x : Int) :
    polynomialValue (pairWord L k) L x =
      finiteSum (fun i => 11 * x ^ i) k +
      finiteSum (fun i => 11 * x ^ (L - k + i)) k := by
  let f := fun i => (pairWord L k i : Int) * x ^ i
  have hlen : L - k + k = L := by omega
  have hmidlen : k + (L - 2 * k) = L - k := by omega
  have hlo : finiteSum f k = finiteSum (fun i => 11 * x ^ i) k := by
    apply finiteSum_congr
    intro i hi
    simp [f, pairWord, hi]
  have hmid : finiteSum (fun i => f (k + i)) (L - 2 * k) = 0 := by
    calc
      _ = finiteSum (fun _ => (0 : Int)) (L - 2 * k) := by
        apply finiteSum_congr
        intro i hi
        have hfirst : ¬ k + i < k := by omega
        have hlast : ¬ (L - k ≤ k + i ∧ k + i < L) := by omega
        simp [f, pairWord, hfirst, hlast]
      _ = 0 := by simp [finiteSum_const]
  have hhi : finiteSum (fun i => f (L - k + i)) k =
      finiteSum (fun i => 11 * x ^ (L - k + i)) k := by
    apply finiteSum_congr
    intro i hi
    have hb : L - k ≤ L - k + i ∧ L - k + i < L := by omega
    simp [f, pairWord, hb]
  have hprefix : finiteSum f (L - k) = finiteSum (fun i => 11 * x ^ i) k := by
    calc
      _ = finiteSum f k + finiteSum (fun i => f (k + i)) (L - 2 * k) := by
        simpa only [hmidlen] using finiteSum_add_length f k (L - 2 * k)
      _ = _ := by rw [hlo, hmid]; simp
  rw [polynomialValue_eq_finiteSum]
  change finiteSum f L = _
  calc
    _ = finiteSum f (L - k) + finiteSum (fun i => f (L - k + i)) k := by
      simpa only [hlen] using finiteSum_add_length f (L - k) k
    _ = _ := by rw [hprefix, hhi]

theorem int_one_pow (n : Nat) : (1 : Int) ^ n = 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [Int.pow_succ, ih]

/-- The source mass Q(1) is exactly twenty-two times the pair count. -/
theorem pairWord_value_one (L k : Nat) (hL : 2 * k ≤ L) :
    polynomialValue (pairWord L k) L 1 = 22 * (k : Int) := by
  rw [pairWord_polynomial_blocks L k hL]
  simp only [int_one_pow, Int.mul_one, finiteSum_const]
  omega

theorem int_pow_add (x : Int) (a b : Nat) :
    x ^ (a + b) = x ^ a * x ^ b := by
  induction b with
  | zero => simp
  | succ b ih =>
    rw [← Nat.add_assoc, Int.pow_succ, ih, Int.pow_succ, Int.mul_assoc]

theorem neg_one_pow (n : Nat) :
    (-1 : Int) ^ n = if n % 2 = 0 then 1 else -1 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [Int.pow_succ, ih]
    by_cases hn : n % 2 = 0
    · have hs : (n + 1) % 2 ≠ 0 := by omega
      simp [hn, hs]
    · have hs : (n + 1) % 2 = 0 := by omega
      simp [hn, hs]

theorem alternating_prefix (n : Nat) :
    finiteSum (fun i => (-1 : Int) ^ i) n = if n % 2 = 0 then 0 else 1 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [finiteSum, ih, neg_one_pow]
    by_cases hn : n % 2 = 0
    · have hs : (n + 1) % 2 ≠ 0 := by omega
      simp [hn, hs]
    · have hs : (n + 1) % 2 = 0 := by omega
      simp [hn, hs]

theorem power_prefix_shift (x : Int) (a n : Nat) :
    finiteSum (fun i => x ^ (a + i)) n = x ^ a * finiteSum (fun i => x ^ i) n := by
  calc
    _ = finiteSum (fun i => x ^ a * x ^ i) n := by
      apply finiteSum_congr
      intro i _
      exact int_pow_add x a i
    _ = _ := finiteSum_mul_left _ _ _

/-- Exact signed evaluation for the contiguous outer-pair construction. -/
theorem pairWord_value_neg_one (L k : Nat) (hL : 2 * k ≤ L) :
    polynomialValue (pairWord L k) L (-1) =
      if L % 2 = 1 ∧ k % 2 = 1 then 22 else 0 := by
  rw [pairWord_polynomial_blocks L k hL,
    finiteSum_mul_left, finiteSum_mul_left, power_prefix_shift,
    alternating_prefix, neg_one_pow]
  by_cases hk : k % 2 = 0
  · have hk1 : k % 2 ≠ 1 := by omega
    simp [hk, hk1]
  · have hk1 : k % 2 = 1 := by omega
    by_cases hLeven : L % 2 = 0
    · have hshift : (L - k) % 2 ≠ 0 := by omega
      have hLodd : L % 2 ≠ 1 := by omega
      simp [hk, hk1, hshift, hLodd]
    · have hshift : (L - k) % 2 = 0 := by omega
      have hLodd : L % 2 = 1 := by omega
      simp [hk, hk1, hshift, hLodd]

/-- The alternating source coefficient evaluation is always divisible by 22. -/
theorem pairWord_neg_one_dvd (L k : Nat) (hL : 2 * k ≤ L) :
    (22 : Int) ∣ polynomialValue (pairWord L k) L (-1) := by
  rw [pairWord_value_neg_one L k hL]
  split <;> decide

/-- At every even width the literal alternating polynomial evaluation is zero. -/
theorem pairWord_neg_one_even (L k : Nat) (hL : 2 * k ≤ L) (heven : L % 2 = 0) :
    polynomialValue (pairWord L k) L (-1) = 0 := by
  have hodd : L % 2 ≠ 1 := by omega
  simp [pairWord_value_neg_one L k hL, hodd]

/-- The source residue s, with integer division performed before reduction. -/
def sourceS (q : Nat → Nat) (L : Nat) : Int :=
  (polynomialValue q L 1 / 2) % 9

/-- The source residue r, retaining its literal signed polynomial evaluation. -/
def sourceR (q : Nat → Nat) (L : Nat) : Int :=
  (polynomialValue q L (-1) / 2) % 11

theorem pairWord_half_value_one (L k : Nat) (hL : 2 * k ≤ L) :
    polynomialValue (pairWord L k) L 1 / 2 = 11 * (k : Int) := by
  rw [pairWord_value_one L k hL]
  omega

/-- Exact source s-coordinate of the constructed coefficient word. -/
theorem pairWord_sourceS (L k : Nat) (hL : 2 * k ≤ L) :
    sourceS (pairWord L k) L = (11 * (k : Int)) % 9 := by
  unfold sourceS
  rw [pairWord_half_value_one L k hL]

/-- The same source s-coordinate expressed as a natural residue cast to integers. -/
theorem pairWord_sourceS_nat (L k : Nat) (hL : 2 * k ≤ L) :
    sourceS (pairWord L k) L = ((11 * k % 9 : Nat) : Int) := by
  rw [pairWord_sourceS L k hL]
  exact (Int.ofNat_emod (11 * k) 9).symm

/-- Exact source r-coordinate; this is not a claim about the seed modulo 11. -/
theorem pairWord_sourceR (L k : Nat) (hL : 2 * k ≤ L) :
    sourceR (pairWord L k) L = 0 := by
  unfold sourceR
  rw [pairWord_value_neg_one L k hL]
  split <;> decide

/-- Finite class selection, independent of the unbounded width construction. -/
theorem residue_parameter (s : Nat) (hs : s < 9) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 9 ∧ 11 * k % 9 = s := by
  have h : s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨ s = 4 ∨
      s = 5 ∨ s = 6 ∨ s = 7 ∨ s = 8 := by omega
  rcases h with h | h | h | h | h | h | h | h | h <;> subst s
  · exact ⟨9, by decide⟩
  · exact ⟨5, by decide⟩
  · exact ⟨1, by decide⟩
  · exact ⟨6, by decide⟩
  · exact ⟨2, by decide⟩
  · exact ⟨7, by decide⟩
  · exact ⟨3, by decide⟩
  · exact ⟨8, by decide⟩
  · exact ⟨4, by decide⟩

/-- Polynomial evaluation only uses coefficients at indices below the width. -/
theorem polynomialValue_congr (q r : Nat → Nat) (L : Nat) (x : Int)
    (h : ∀ i < L, q i = r i) :
    polynomialValue q L x = polynomialValue r L x := by
  rw [polynomialValue_eq_finiteSum, polynomialValue_eq_finiteSum]
  apply finiteSum_congr
  intro i hi
  rw [h i hi]

theorem sourceS_congr (q r : Nat → Nat) (L : Nat)
    (h : ∀ i < L, q i = r i) : sourceS q L = sourceS r L := by
  unfold sourceS
  rw [polynomialValue_congr q r L 1 h]

theorem sourceR_congr (q r : Nat → Nat) (L : Nat)
    (h : ∀ i < L, q i = r i) : sourceR q L = sourceR r L := by
  unfold sourceR
  rw [polynomialValue_congr q r L (-1) h]

#print axioms finiteSum
#print axioms polynomialValue
#print axioms finiteSum_eq_range
#print axioms polynomialValue_eq_finiteSum
#print axioms finiteSum_congr
#print axioms finiteSum_add_length
#print axioms finiteSum_const
#print axioms finiteSum_mul_left
#print axioms pairWord_polynomial_blocks
#print axioms int_one_pow
#print axioms pairWord_value_one
#print axioms int_pow_add
#print axioms neg_one_pow
#print axioms alternating_prefix
#print axioms power_prefix_shift
#print axioms pairWord_value_neg_one
#print axioms pairWord_neg_one_dvd
#print axioms pairWord_neg_one_even
#print axioms sourceS
#print axioms sourceR
#print axioms pairWord_half_value_one
#print axioms pairWord_sourceS
#print axioms pairWord_sourceS_nat
#print axioms pairWord_sourceR
#print axioms residue_parameter

#print axioms polynomialValue_congr
#print axioms sourceS_congr
#print axioms sourceR_congr

end P196.Agent51
