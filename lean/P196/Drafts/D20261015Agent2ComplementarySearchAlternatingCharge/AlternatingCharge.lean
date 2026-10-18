import P196.Agent2SaturatedProfile.ExteriorCharge

namespace Agent2Exterior

/-- Alternating sign of a word length. -/
def paritySign : Nat → Int
  | 0 => 1
  | n + 1 => -paritySign n

/-- Evaluation of the coefficient polynomial at minus one. -/
def alternatingSum : List Nat → Int
  | [] => 0
  | a :: as => (a : Int) - alternatingSum as

theorem paritySign_cases (n : Nat) : paritySign n = 1 ∨ paritySign n = -1 := by
  induction n with
  | zero => exact Or.inl rfl
  | succ n ih => simp only [paritySign]; omega

theorem alternatingSum_append (A B : List Nat) :
    alternatingSum (A ++ B) = alternatingSum A + paritySign A.length * alternatingSum B := by
  induction A with
  | nil => simp [alternatingSum, paritySign]
  | cons a as ih =>
      simp only [List.cons_append, alternatingSum, List.length_cons, paritySign, ih,
        Int.neg_mul]
      omega

theorem alternatingSum_reverse (A : List Nat) :
    alternatingSum A.reverse = -paritySign A.length * alternatingSum A := by
  induction A with
  | nil => simp [alternatingSum, paritySign]
  | cons a as ih =>
      simp only [List.reverse_cons, alternatingSum_append, List.length_reverse,
        alternatingSum, List.length_cons, paritySign, ih,
        Int.sub_zero, Int.neg_neg, Int.mul_sub, Int.neg_mul]
      omega

theorem alternatingSum_zip_add (A B : List Nat) (h : A.length = B.length) :
    alternatingSum (List.zipWith (· + ·) A B) = alternatingSum A + alternatingSum B := by
  induction A generalizing B with
  | nil => cases B <;> simp_all [alternatingSum]
  | cons a as ih =>
      cases B with
      | nil => simp at h
      | cons b bs =>
          have ht : as.length = bs.length := by simpa using h
          simp only [List.zipWith_cons_cons, alternatingSum, Int.ofNat_add, ih bs ht]
          omega

theorem normalize_alternating_mod11 (A : List Nat) (e : Nat) :
    (alternatingSum (normalize A e).1 + paritySign A.length * ((normalize A e).2 : Int)) % 11 =
      (alternatingSum A + (e : Int)) % 11 := by
  induction A generalizing e with
  | nil => simp [normalize, alternatingSum, paritySign]
  | cons a as ih =>
      have h := ih ((a+e)/10)
      have hd := Nat.mod_add_div (a+e) 10
      simp only [normalize, alternatingSum, List.length_cons, paritySign, Int.neg_mul]
      omega

/-- This is unchanged by appending or removing a suffix of the bulk phase. -/
def alternatingCharge (c : Nat) (B : List Nat) : Int :=
  2 * alternatingSum B + paritySign B.length * (c : Int)

@[simp] theorem alternatingCharge_nil (c : Nat) : alternatingCharge c [] = c := by
  simp [alternatingCharge, alternatingSum, paritySign]

theorem alternatingCharge_cons (c a : Nat) (B : List Nat) :
    alternatingCharge c (a :: B) = 2*(a : Int) - alternatingCharge c B := by
  simp only [alternatingCharge, alternatingSum, List.length_cons, paritySign,
    Int.mul_sub, Int.neg_mul]
  omega

theorem alternatingCharge_trimSuffix (c : Nat) (B : List Nat) :
    alternatingCharge c (trimSuffix c B) = alternatingCharge c B := by
  induction B with
  | nil => rfl
  | cons a as ih =>
      simp only [trimSuffix]
      split
      · rename_i h
        have ht : alternatingCharge c as = c := by rw [← ih, h.1]; simp
        rw [alternatingCharge_nil, alternatingCharge_cons, h.2, ht]
        omega
      · rw [alternatingCharge_cons, ih, alternatingCharge_cons]

theorem raw_alternating_nooverflow (c : Nat) (B : List Nat)
    (hg : overflow c B = 0) :
    alternatingCharge (phase c) (rawExterior c B) % 11 =
      (2 * alternatingCharge c B) % 11 := by
  have hD := normalize_alternating_mod11 B 0
  have hR := normalize_alternating_mod11 B.reverse (c/10)
  have hnum := Nat.mod_add_div c 10
  have hs := paritySign_cases B.length
  simp only [List.length_reverse, alternatingSum_reverse] at hR
  unfold overflow at hg
  unfold alternatingCharge
  rw [rawExterior_length]
  simp only [paritySign]
  unfold rawExterior
  dsimp only
  rw [hg]
  simp only [if_true]
  rw [alternatingSum_zip_add]
  · simp only [alternatingSum_append, alternatingSum_reverse, normalize_length,
      List.length_reverse, alternatingSum, Int.sub_zero, phase]
    rcases hs with hp | hp <;> simp only [hp, Int.one_mul,
      Int.neg_mul, Int.one_mul, Int.neg_neg, Int.ofNat_zero, Int.add_zero,
      hg, Int.mul_zero] at * <;> omega
  · simp

theorem raw_alternating_overflow (c : Nat) (B : List Nat)
    (hg : overflow c B = 1) :
    alternatingCharge (phase c) (rawExterior c B) % 11 = 0 := by
  have hD := normalize_alternating_mod11 B 0
  have hR := normalize_alternating_mod11 B.reverse (c/10)
  have hnum := Nat.mod_add_div c 10
  have hs := paritySign_cases B.length
  simp only [List.length_reverse, alternatingSum_reverse] at hR
  unfold overflow at hg
  unfold alternatingCharge
  rw [rawExterior_length]
  simp only [paritySign]
  unfold rawExterior
  dsimp only
  rw [hg]
  simp only [Nat.one_ne_zero, if_false]
  rw [alternatingSum_zip_add]
  · simp only [alternatingSum_append, alternatingSum_reverse, normalize_length,
      List.length_reverse, alternatingSum, Int.sub_zero, phase]
    rcases hs with hp | hp <;> simp only [hp, Int.one_mul,
      Int.neg_mul, Int.one_mul, Int.neg_neg, Int.ofNat_zero, Int.add_zero,
      hg, Int.ofNat_one, Int.mul_one] at * <;> omega
  · simp


theorem exterior_alternating_nooverflow (c : Nat) (B : List Nat)
    (hg : overflow c B = 0) :
    alternatingCharge (phase c) (exterior c B) % 11 =
      (2 * alternatingCharge c B) % 11 := by
  unfold exterior
  rw [alternatingCharge_trimSuffix]
  exact raw_alternating_nooverflow c B hg

theorem exterior_alternating_overflow (c : Nat) (B : List Nat)
    (hg : overflow c B = 1) :
    alternatingCharge (phase c) (exterior c B) % 11 = 0 := by
  unfold exterior
  rw [alternatingCharge_trimSuffix]
  exact raw_alternating_overflow c B hg

/-- Overflow resets this residue; the zero residue is then forward invariant. -/
theorem exterior_alternating_step (c : Nat) (B : List Nat)
    (hc : c ≤ 18) (hB : ∀ a ∈ B, a ≤ 18) :
    alternatingCharge (phase c) (exterior c B) % 11 =
      (if overflow c B = 0 then 2 * alternatingCharge c B else 0) % 11 := by
  by_cases h0 : overflow c B = 0
  · simp only [h0, if_true]
    exact exterior_alternating_nooverflow c B h0
  · have hr : ∀ a ∈ B.reverse, a ≤ 18 := by
      intro a ha
      exact hB a (by simpa using ha)
    have hb := normalize_carry_bit B.reverse (c/10) hr (by omega)
    have h1 : overflow c B = 1 := by unfold overflow at *; omega
    simp only [h0, if_false, Int.zero_emod]
    exact exterior_alternating_overflow c B h1

theorem reset_after_positive_step (k : Nat → Int) (g : Nat → Nat) (n : Nat)
    (hs : ∀ i, i < n → k (i+1) % 11 = (if g i = 0 then 2*k i else 0) % 11)
    (hw : ∃ i, i < n ∧ g i ≠ 0) : k n % 11 = 0 := by
  induction n with
  | zero => rcases hw with ⟨i, hi, _⟩; omega
  | succ n ih =>
      have hn := hs n (by omega)
      by_cases h0 : g n = 0
      · have hpw : ∃ i, i < n ∧ g i ≠ 0 := by
          rcases hw with ⟨i, hi, hg⟩
          have hne : i ≠ n := by intro h; subst i; exact hg h0
          exact ⟨i, by omega, hg⟩
        have hp := ih (by intro i hi; exact hs i (by omega)) hpw
        simp only [h0, if_true] at hn
        omega
      · simpa [h0] using hn

theorem closed_exterior_alternating_zero (s : Nat → ExteriorState) (n : Nat)
    (hv : ∀ i, i < n → (s i).c ≤ 18 ∧ (∀ a ∈ (s i).B, a ≤ 18))
    (hs : ∀ i, i < n → s (i+1) = nextState (s i))
    (hr : s n = s 0)
    (hw : ∃ i, i < n ∧ overflow (s i).c (s i).B ≠ 0) :
    alternatingCharge (s 0).c (s 0).B % 11 = 0 := by
  have hz := reset_after_positive_step
    (fun i => alternatingCharge (s i).c (s i).B)
    (fun i => overflow (s i).c (s i).B) n (by
      intro i hi
      dsimp only
      rw [hs i hi]
      exact exterior_alternating_step (s i).c (s i).B (hv i hi).1 (hv i hi).2) hw
  simpa [hr] using hz

#print axioms paritySign_cases
#print axioms alternatingSum_append
#print axioms alternatingSum_reverse
#print axioms alternatingSum_zip_add
#print axioms normalize_alternating_mod11
#print axioms alternatingCharge_nil
#print axioms alternatingCharge_cons
#print axioms alternatingCharge_trimSuffix
#print axioms raw_alternating_nooverflow
#print axioms raw_alternating_overflow
#print axioms exterior_alternating_nooverflow
#print axioms exterior_alternating_overflow
#print axioms exterior_alternating_step
#print axioms reset_after_positive_step
#print axioms closed_exterior_alternating_zero

end Agent2Exterior
