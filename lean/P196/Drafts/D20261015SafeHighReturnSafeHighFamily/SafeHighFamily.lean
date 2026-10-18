import P196.Drafts.D20261015SafeHighReturnSafeHighWitness.SafeHighWitness

/-!
All-parameter family of three safe high-region returns.  Only Std and the
finite witness's definitions are imported.  No finite search is a premise.
Parameter m corresponds to k=m+5 copies of coefficient 18 in the initial word.
-/
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace SafeHighFamily
open SafeHighWitness

/-- Evaluate a least-significant-first digit or coefficient word. -/
def value : List Nat → Nat
  | [] => 0
  | d :: ds => d + 10 * value ds

/-- Actual decimal carry normalization; append the final carry if nonzero. -/
def normalize : List Nat → Nat → List Nat
  | [], c => if c = 0 then [] else [c]
  | a :: xs, c => (a + c) % 10 :: normalize xs ((a + c) / 10)

/-- Pair coefficients of a digit word at its actual physical width. -/
def pair (ds : List Nat) : List Nat := List.zipWith Nat.add ds ds.reverse

/-- At carry one, any number of 18 columns produces nines and preserves carry. -/
theorem normalize_eighteens (m : Nat) (tail : List Nat) :
    normalize (List.replicate m 18 ++ tail) 1 =
      List.replicate m 9 ++ normalize tail 1 := by
  induction m with
  | zero => simp
  | succ m ih => simp [List.replicate_succ, normalize, ih]

theorem value_normalize (xs : List Nat) (c : Nat) :
    value (normalize xs c) = value xs + c := by
  induction xs generalizing c with
  | nil => by_cases h : c = 0 <;> simp [normalize, value, h]
  | cons a xs ih =>
      simp only [normalize, value, ih]
      have h := Nat.mod_add_div (a + c) 10
      omega

theorem pair_blocks (a b : List Nat) (m : Nat) (h : a.length = b.length) :
    pair (a ++ List.replicate m 9 ++ b) =
      List.zipWith Nat.add a b.reverse ++ List.replicate m 18 ++
        List.zipWith Nat.add b a.reverse := by
  simp only [pair, List.reverse_append, List.reverse_replicate, List.append_assoc]
  rw [List.zipWith_append (by simpa using h)]
  rw [List.zipWith_append (by simp)]
  simp

-- The seven successive pair words.
def q0 (m : Nat) := [17,9] ++ List.replicate (m+5) 18 ++ [9,17]
def q1 (m : Nat) := [8,8,9] ++ List.replicate (m+4) 18 ++ [9,8,8]
def q2 (m : Nat) := [16,17,9,17] ++ List.replicate (m+2) 18 ++ [17,9,17,16]
def q3 (m : Nat) := [7,15,8,8,17] ++ List.replicate (m+1) 18 ++ [17,8,8,15,7]
def q4 (m : Nat) := [15,10,17,17,15] ++ List.replicate (m+1) 18 ++ [15,17,17,10,15]
def q5 (m : Nat) := [6,7,9,16,14,15] ++ List.replicate m 18 ++ [15,14,16,9,7,6]
def q6 (m : Nat) := [12,15,9,13,10,12] ++ List.replicate m 18 ++ [12,10,13,9,15,12]

-- Actual canonical decimal digits; each row has balanced finite sides.
def dSeed (m : Nat) := [9,9] ++ List.replicate (m+5) 9 ++ [0,8]
def d0 (m : Nat) := [7,0,9] ++ List.replicate (m+4) 9 ++ [0,8,1]
def d1 (m : Nat) := [8,8,9,8] ++ List.replicate (m+2) 9 ++ [9,0,9,8]
def d2 (m : Nat) := [6,8,0,8,9] ++ List.replicate (m+1) 9 ++ [8,0,8,7,1]
def d3 (m : Nat) := [7,5,9,8,7] ++ List.replicate (m+1) 9 ++ [8,9,8,5,8]
def d4 (m : Nat) := [5,1,8,8,6,9] ++ List.replicate m 9 ++ [6,8,8,1,6,1]
def d5 (m : Nat) := [6,7,9,6,5,6] ++ List.replicate m 9 ++ [6,5,7,0,8,6]

theorem seed_pair (m : Nat) : pair (dSeed m) = q0 m := by
  simpa [dSeed, q0] using pair_blocks [9,9] [0,8] (m+5) (by decide)

theorem d0_pair (m : Nat) : pair (d0 m) = q1 m := by
  simpa [d0, q1] using pair_blocks [7,0,9] [0,8,1] (m+4) (by decide)
theorem d1_pair (m : Nat) : pair (d1 m) = q2 m := by
  simpa [d1, q2] using pair_blocks [8,8,9,8] [9,0,9,8] (m+2) (by decide)
theorem d2_pair (m : Nat) : pair (d2 m) = q3 m := by
  simpa [d2, q3] using pair_blocks [6,8,0,8,9] [8,0,8,7,1] (m+1) (by decide)
theorem d3_pair (m : Nat) : pair (d3 m) = q4 m := by
  simpa [d3, q4] using pair_blocks [7,5,9,8,7] [8,9,8,5,8] (m+1) (by decide)
theorem d4_pair (m : Nat) : pair (d4 m) = q5 m := by
  simpa [d4, q5] using pair_blocks [5,1,8,8,6,9] [6,8,8,1,6,1] m (by decide)
theorem d5_pair (m : Nat) : pair (d5 m) = q6 m := by
  simpa [d5, q6] using pair_blocks [6,7,9,6,5,6] [6,5,7,0,8,6] m (by decide)

theorem norm0 (m : Nat) : normalize (q0 m) 0 = d0 m := by
  simp [q0, d0, List.replicate_succ, normalize, normalize_eighteens]
theorem nine_commute (m : Nat) (tail : List Nat) :
    9 :: (List.replicate m 9 ++ tail) = List.replicate m 9 ++ 9 :: tail := by
  induction m with
  | zero => rfl
  | succ m ih => simpa [List.replicate_succ] using congrArg (List.cons 9) ih

theorem norm1 (m : Nat) : normalize (q1 m) 0 = d1 m := by
  simp [q1, d1, List.replicate_succ, normalize, normalize_eighteens]
  exact nine_commute m [0,9,8]
theorem norm2 (m : Nat) : normalize (q2 m) 0 = d2 m := by
  simp [q2, d2, List.replicate_succ, normalize, normalize_eighteens]
theorem norm3 (m : Nat) : normalize (q3 m) 0 = d3 m := by
  simp [q3, d3, List.replicate_succ, normalize, normalize_eighteens]
theorem norm4 (m : Nat) : normalize (q4 m) 0 = d4 m := by
  simp [q4, d4, List.replicate_succ, normalize, normalize_eighteens]
theorem norm5 (m : Nat) : normalize (q5 m) 0 = d5 m := by
  simp [q5, d5, List.replicate_succ, normalize, normalize_eighteens]

/-- A nonempty canonical decimal representation of a positive integer. -/
inductive DecimalDigits : List Nat → Prop where
  | single (d : Nat) (positive : 0 < d) (bound : d < 10) : DecimalDigits [d]
  | cons (d : Nat) (ds : List Nat) (bound : d < 10)
      (tail : DecimalDigits ds) : DecimalDigits (d :: ds)

theorem decimal_value_positive {ds : List Nat} (h : DecimalDigits ds) :
    0 < value ds := by
  induction h with
  | single d hp hb => simpa [value] using hp
  | cons d ds hb ht ih => simp only [value]; omega

theorem decimal_length_bound {ds : List Nat} (h : DecimalDigits ds) :
    ds.length ≤ value ds := by
  induction h with
  | single d hp hb => simp [value]; omega
  | cons d ds hb ht ih =>
      have hp := decimal_value_positive ht
      simp only [List.length_cons, value]
      omega

theorem digitsAux_zero (fuel : Nat) : digitsAux fuel 0 = [] := by
  cases fuel <;> simp [digitsAux]

theorem digitsAux_value {ds : List Nat} (h : DecimalDigits ds)
    (fuel : Nat) (hf : ds.length ≤ fuel) :
    digitsAux fuel (value ds) = ds := by
  induction h generalizing fuel with
  | single d hp hb =>
      cases fuel with
      | zero => simp at hf
      | succ fuel =>
          have hz : d ≠ 0 := by omega
          simp [value, digitsAux, hz, Nat.mod_eq_of_lt hb,
            Nat.div_eq_of_lt hb, digitsAux_zero]
  | cons d ds hb ht ih =>
      cases fuel with
      | zero => simp at hf
      | succ fuel =>
          have hp := decimal_value_positive ht
          have hz : d + 10 * value ds ≠ 0 := by omega
          have hm : (d + 10 * value ds) % 10 = d := by omega
          have hd : (d + 10 * value ds) / 10 = value ds := by omega
          have hfl : ds.length ≤ fuel := by simpa using hf
          simp only [value, digitsAux, hz, ↓reduceIte, hm, hd]
          exact congrArg (List.cons d) (ih fuel hfl)

theorem digits10_value {ds : List Nat} (h : DecimalDigits ds) :
    digits10 (value ds) = ds :=
  digitsAux_value h (value ds) (decimal_length_bound h)

theorem value_eq_foldr (ds : List Nat) :
    value ds = ds.foldr (fun d a => d + 10 * a) 0 := by
  induction ds with
  | nil => rfl
  | cons d ds ih => simpa [value] using congrArg (fun a => d + 10*a) ih

theorem reverse10_value {ds : List Nat} (h : DecimalDigits ds) :
    reverse10 (value ds) = value ds.reverse := by
  unfold reverse10
  rw [digits10_value h]
  simp [value_eq_foldr, List.foldr_reverse, Nat.add_comm]

theorem value_zipWith_add (xs ys : List Nat) (h : xs.length = ys.length) :
    value (List.zipWith Nat.add xs ys) = value xs + value ys := by
  induction xs generalizing ys with
  | nil =>
      have hy : ys = [] := by simpa using h.symm
      simp [hy, value]
  | cons x xs ih =>
      cases ys with
      | nil => simp at h
      | cons y ys =>
          have hlen : xs.length = ys.length := by simpa using h
          simp only [List.zipWith_cons_cons, value, ih ys hlen]
          change (x + y) + 10 * (value xs + value ys) = (x + 10 * value xs) + (y + 10 * value ys)
          omega

theorem value_pair (ds : List Nat) : value (pair ds) = value ds + value ds.reverse := by
  exact value_zipWith_add ds ds.reverse (by simp)

/-- Semantic bridge: canonical digits and actual natural-number reverse-and-add. -/
theorem ordinary_step {ds : List Nat} (h : DecimalDigits ds) :
    step (value ds) = value (normalize (pair ds) 0) := by
  rw [value_normalize, value_pair, Nat.add_zero]
  simp [step, reverse10_value h]

theorem decimal_append (xs ys : List Nat) (hx : ∀ d ∈ xs, d < 10)
    (hy : DecimalDigits ys) : DecimalDigits (xs ++ ys) := by
  induction xs with
  | nil => simpa using hy
  | cons d xs ih =>
      apply DecimalDigits.cons d (xs ++ ys) (hx d (by simp))
      apply ih
      intro a ha
      exact hx a (by simp [ha])

theorem decimal_replicate (m : Nat) {ys : List Nat} (hy : DecimalDigits ys) :
    DecimalDigits (List.replicate m 9 ++ ys) := by
  apply decimal_append _ _ _ hy
  intro d hd
  have : d = 9 := (List.mem_replicate.mp hd).2
  omega

theorem decimal_balanced (a b : List Nat) (m : Nat)
    (ha : ∀ d ∈ a, d < 10) (hb : DecimalDigits b) :
    DecimalDigits (a ++ List.replicate m 9 ++ b) := by
  simpa [List.append_assoc] using decimal_append a _ ha (decimal_replicate m hb)

theorem canonical_dSeed (m : Nat) : DecimalDigits (dSeed m) := by
  exact decimal_balanced [9, 9] [0, 8] (m+5) (by decide) (DecimalDigits.cons 0 _ (by decide) (DecimalDigits.single 8 (by decide) (by decide)))

theorem not_palindrome_dSeed (m : Nat) : dSeed m ≠ (dSeed m).reverse := by
  simp [dSeed, List.reverse_append, List.reverse_replicate]

theorem canonical_d0 (m : Nat) : DecimalDigits (d0 m) := by
  exact decimal_balanced [7, 0, 9] [0, 8, 1] (m+4) (by decide) (DecimalDigits.cons 0 _ (by decide) (DecimalDigits.cons 8 _ (by decide) (DecimalDigits.single 1 (by decide) (by decide))))

theorem not_palindrome_d0 (m : Nat) : d0 m ≠ (d0 m).reverse := by
  simp [d0, List.reverse_append, List.reverse_replicate]

theorem canonical_d1 (m : Nat) : DecimalDigits (d1 m) := by
  exact decimal_balanced [8, 8, 9, 8] [9, 0, 9, 8] (m+2) (by decide) (DecimalDigits.cons 9 _ (by decide) (DecimalDigits.cons 0 _ (by decide) (DecimalDigits.cons 9 _ (by decide) (DecimalDigits.single 8 (by decide) (by decide)))))

theorem not_palindrome_d1 (m : Nat) : d1 m ≠ (d1 m).reverse := by
  simp [d1, List.reverse_append, List.reverse_replicate]

theorem canonical_d2 (m : Nat) : DecimalDigits (d2 m) := by
  exact decimal_balanced [6, 8, 0, 8, 9] [8, 0, 8, 7, 1] (m+1) (by decide) (DecimalDigits.cons 8 _ (by decide) (DecimalDigits.cons 0 _ (by decide) (DecimalDigits.cons 8 _ (by decide) (DecimalDigits.cons 7 _ (by decide) (DecimalDigits.single 1 (by decide) (by decide))))))

theorem not_palindrome_d2 (m : Nat) : d2 m ≠ (d2 m).reverse := by
  simp [d2, List.reverse_append, List.reverse_replicate]

theorem canonical_d3 (m : Nat) : DecimalDigits (d3 m) := by
  exact decimal_balanced [7, 5, 9, 8, 7] [8, 9, 8, 5, 8] (m+1) (by decide) (DecimalDigits.cons 8 _ (by decide) (DecimalDigits.cons 9 _ (by decide) (DecimalDigits.cons 8 _ (by decide) (DecimalDigits.cons 5 _ (by decide) (DecimalDigits.single 8 (by decide) (by decide))))))

theorem not_palindrome_d3 (m : Nat) : d3 m ≠ (d3 m).reverse := by
  simp [d3, List.reverse_append, List.reverse_replicate]

theorem canonical_d4 (m : Nat) : DecimalDigits (d4 m) := by
  exact decimal_balanced [5, 1, 8, 8, 6, 9] [6, 8, 8, 1, 6, 1] (m) (by decide) (DecimalDigits.cons 6 _ (by decide) (DecimalDigits.cons 8 _ (by decide) (DecimalDigits.cons 8 _ (by decide) (DecimalDigits.cons 1 _ (by decide) (DecimalDigits.cons 6 _ (by decide) (DecimalDigits.single 1 (by decide) (by decide)))))))

theorem not_palindrome_d4 (m : Nat) : d4 m ≠ (d4 m).reverse := by
  simp [d4, List.reverse_append, List.reverse_replicate]

theorem canonical_d5 (m : Nat) : DecimalDigits (d5 m) := by
  exact decimal_balanced [6, 7, 9, 6, 5, 6] [6, 5, 7, 0, 8, 6] (m) (by decide) (DecimalDigits.cons 6 _ (by decide) (DecimalDigits.cons 5 _ (by decide) (DecimalDigits.cons 7 _ (by decide) (DecimalDigits.cons 0 _ (by decide) (DecimalDigits.cons 8 _ (by decide) (DecimalDigits.single 6 (by decide) (by decide)))))))

theorem not_palindrome_d5 (m : Nat) : d5 m ≠ (d5 m).reverse := by
  simp [d5, List.reverse_append, List.reverse_replicate]

/-- Numeric digit extraction and the list-level pair map coincide. -/
theorem pairWord_value {ds : List Nat} (h : DecimalDigits ds) :
    pairWord (value ds) = pair ds := by
  unfold pairWord
  rw [digits10_value h]
  rfl

theorem next_0 (m : Nat) : step (value (dSeed m)) = value (d0 m) := by
  rw [ordinary_step (canonical_dSeed m), seed_pair, norm0]

theorem next_1 (m : Nat) : step (value (d0 m)) = value (d1 m) := by
  rw [ordinary_step (canonical_d0 m), d0_pair, norm1]

theorem next_2 (m : Nat) : step (value (d1 m)) = value (d2 m) := by
  rw [ordinary_step (canonical_d1 m), d1_pair, norm2]

theorem next_3 (m : Nat) : step (value (d2 m)) = value (d3 m) := by
  rw [ordinary_step (canonical_d2 m), d2_pair, norm3]

theorem next_4 (m : Nat) : step (value (d3 m)) = value (d4 m) := by
  rw [ordinary_step (canonical_d3 m), d3_pair, norm4]

theorem next_5 (m : Nat) : step (value (d4 m)) = value (d5 m) := by
  rw [ordinary_step (canonical_d4 m), d4_pair, norm5]

theorem high_0 (m : Nat) : high (value (dSeed m)) = true := by
  simp [high, pairWord_value (canonical_dSeed m), seed_pair, q0]

theorem high_2 (m : Nat) : high (value (d1 m)) = true := by
  simp [high, pairWord_value (canonical_d1 m), d1_pair, q2]

theorem high_4 (m : Nat) : high (value (d3 m)) = true := by
  simp [high, pairWord_value (canonical_d3 m), d3_pair, q4]

theorem high_6 (m : Nat) : high (value (d5 m)) = true := by
  simp [high, pairWord_value (canonical_d5 m), d5_pair, q6]

theorem safe_0 (m : Nat) : palindrome (value (dSeed m)) = false := by
  simp [palindrome, digits10_value (canonical_dSeed m), not_palindrome_dSeed m]

theorem safe_1 (m : Nat) : palindrome (value (d0 m)) = false := by
  simp [palindrome, digits10_value (canonical_d0 m), not_palindrome_d0 m]

theorem safe_2 (m : Nat) : palindrome (value (d1 m)) = false := by
  simp [palindrome, digits10_value (canonical_d1 m), not_palindrome_d1 m]

theorem safe_3 (m : Nat) : palindrome (value (d2 m)) = false := by
  simp [palindrome, digits10_value (canonical_d2 m), not_palindrome_d2 m]

theorem safe_4 (m : Nat) : palindrome (value (d3 m)) = false := by
  simp [palindrome, digits10_value (canonical_d3 m), not_palindrome_d3 m]

theorem safe_5 (m : Nat) : palindrome (value (d4 m)) = false := by
  simp [palindrome, digits10_value (canonical_d4 m), not_palindrome_d4 m]

theorem safe_6 (m : Nat) : palindrome (value (d5 m)) = false := by
  simp [palindrome, digits10_value (canonical_d5 m), not_palindrome_d5 m]

def seed (m : Nat) : Nat := value (dSeed m)

/-- All four high-region memberships, at times 0,2,4,6. -/
theorem family_high_returns (m : Nat) :
    ∀ j : Fin 4, high (iterate (seed m) (2*j.val)) = true := by
  intro j
  have hj : j.val = 0 ∨ j.val = 1 ∨ j.val = 2 ∨ j.val = 3 := by omega
  rcases hj with h | h | h | h <;>
    simp [h, seed, iterate, next_0, next_1, next_2, next_3, next_4, next_5,
      high_0, high_2, high_4, high_6]

/-- No palindrome occurs at any time from 0 through 6. -/
theorem family_safe (m : Nat) :
    ∀ t : Fin 7, palindrome (iterate (seed m) t.val) = false := by
  intro t
  have ht : t.val = 0 ∨ t.val = 1 ∨ t.val = 2 ∨ t.val = 3 ∨
      t.val = 4 ∨ t.val = 5 ∨ t.val = 6 := by omega
  rcases ht with h | h | h | h | h | h | h <;>
    simp [h, seed, iterate, next_0, next_1, next_2, next_3, next_4, next_5,
      safe_0, safe_1, safe_2, safe_3, safe_4, safe_5, safe_6]

/-- Complete all-parameter finite-safe-return theorem on natural numbers. -/
theorem safe_three_returns_family (m : Nat) :
    0 < seed m ∧
    (∀ j : Fin 4, high (iterate (seed m) (2*j.val)) = true) ∧
    (∀ t : Fin 7, palindrome (iterate (seed m) t.val) = false) := by
  exact ⟨decimal_value_positive (canonical_dSeed m),
    family_high_returns m, family_safe m⟩

theorem value_append (xs ys : List Nat) :
    value (xs ++ ys) = value xs + 10^xs.length * value ys := by
  induction xs with
  | nil => simp [value]
  | cons x xs ih =>
      simp [value, ih, Nat.pow_succ, Nat.mul_add, Nat.mul_assoc, Nat.add_assoc, Nat.mul_left_comm]

theorem value_nines_add_one (m : Nat) :
    value (List.replicate m 9) + 1 = 10^m := by
  induction m with
  | zero => simp [value]
  | succ m ih =>
      simp only [List.replicate_succ, value, Nat.pow_succ]
      omega

theorem seed_digits (m : Nat) : dSeed m = List.replicate (m+7) 9 ++ [0,8] := by
  simp [dSeed, List.replicate_succ]

theorem seed_closed_form_add_one (m : Nat) : seed m + 1 = 81 * 10^(m+7) := by
  have hn := value_nines_add_one (m+7)
  simp only [seed, seed_digits, value_append, List.length_replicate, value]
  omega

/-- The explicit seeds are n=81*10^(m+7)-1, i.e. 80 followed by m+7 nines. -/
theorem seed_closed_form (m : Nat) : seed m = 81 * 10^(m+7) - 1 := by
  have h := seed_closed_form_add_one m
  omega

end SafeHighFamily
