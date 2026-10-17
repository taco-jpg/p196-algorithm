import P196.Agent5EvenBaseAbsorption.GeneralCarryMass

namespace P196.Agent5.General.Moment

def lengthSign : Nat → Int
  | 0 => 1
  | n + 1 => -lengthSign n

def wordSign (w : Word) : Int := lengthSign w.length

def altSum : Word → Int
  | [] => 0
  | x :: xs => x - altSum xs

def moment (c : Int) (w : Word) : Int := 2 * altSum w + wordSign w * c

theorem wordSign_cons (x : Int) (xs : Word) : wordSign (x :: xs) = -wordSign xs := rfl

theorem wordSign_bit (w : Word) : wordSign w = 1 ∨ wordSign w = -1 := by
  induction w with
  | nil => exact Or.inl rfl
  | cons x xs ih =>
    rw [wordSign_cons]
    rcases ih with h | h <;> simp [h]

theorem wordSign_append (a b : Word) : wordSign (a ++ b) = wordSign a * wordSign b := by
  induction a with
  | nil => simp [wordSign, lengthSign]
  | cons x xs ih =>
    simp only [List.cons_append, wordSign_cons, ih, Int.neg_mul]

theorem wordSign_reverse (w : Word) : wordSign w.reverse = wordSign w := by
  simp [wordSign]

theorem wordSign_normalize (m : Int) (w : Word) (e : Int) :
    wordSign (normalize m w e).1 = wordSign w := by
  simp [wordSign, normalize_length]

theorem altSum_append (a b : Word) :
    altSum (a ++ b) = altSum a + wordSign a * altSum b := by
  induction a with
  | nil => simp [altSum, wordSign, lengthSign]
  | cons x xs ih =>
    simp only [List.cons_append, altSum, ih, wordSign_cons, Int.neg_mul]
    omega

theorem altSum_reverse (w : Word) : altSum w.reverse = -wordSign w * altSum w := by
  induction w with
  | nil => simp [altSum]
  | cons x xs ih =>
    simp only [List.reverse_cons, altSum_append, ih, wordSign_reverse,
      altSum, Int.sub_zero, wordSign_cons, Int.neg_neg, Int.mul_sub, Int.neg_mul]
    omega

theorem altSum_zip_add (a b : Word) (h : a.length = b.length) :
    altSum (List.zipWith (· + ·) a b) = altSum a + altSum b := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => rfl
    | cons y ys => simp at h
  | cons x xs ih =>
    cases b with
    | nil => simp at h
    | cons y ys =>
      have hlen : xs.length = ys.length := by simpa using h
      have ht := ih ys hlen
      simp only [List.zipWith_cons_cons, altSum]
      omega

theorem stripPrefix_decomposition (c : Int) (w : Word) :
    w = List.replicate (stripPrefix c w).2 c ++ (stripPrefix c w).1 := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
    simp only [stripPrefix]
    split
    next h =>
      subst x
      simp only [List.replicate_succ, List.cons_append]
      exact congrArg (List.cons c) ih
    next h => rfl

theorem stripSuffix_decomposition (c : Int) (w : Word) :
    w = (stripSuffix c w).1 ++ List.replicate (stripSuffix c w).2 c := by
  have h := congrArg List.reverse (stripPrefix_decomposition c w.reverse)
  simpa [List.reverse_append, stripSuffix] using h

theorem moment_append_phase (c : Int) (w : Word) : moment c (w ++ [c]) = moment c w := by
  simp only [moment, altSum_append, wordSign_append, altSum,
    Int.sub_zero, show wordSign [c] = -1 from rfl]
  simp only [Int.mul_add, Int.mul_neg, Int.mul_one, Int.neg_mul]
  omega

theorem moment_append_replicate (c : Int) (w : Word) (n : Nat) :
    moment c (w ++ List.replicate n c) = moment c w := by
  induction n generalizing w with
  | zero => simp
  | succ n ih =>
    have heq : w ++ List.replicate (n+1) c = (w ++ [c]) ++ List.replicate n c := by
      simp [List.replicate_succ]
    rw [heq, ih, moment_append_phase]

theorem moment_stripSuffix (c : Int) (w : Word) :
    moment c (stripSuffix c w).1 = moment c w := by
  conv => rhs; rw [stripSuffix_decomposition c w]
  exact (moment_append_replicate c (stripSuffix c w).1 (stripSuffix c w).2).symm

def alternatingCarry (m : Int) : Word → Int → Int
  | [], _ => 0
  | x :: xs, e =>
    let q := (x + e) / (m + 1)
    q - alternatingCarry m xs q

theorem normalize_alt_exact (m : Int) (w : Word) (e : Int) :
    altSum (normalize m w e).1 + wordSign w * (normalize m w e).2 =
      altSum w + e - (m + 2) * alternatingCarry m w e := by
  induction w generalizing e with
  | nil => simp [normalize, altSum, wordSign, lengthSign, alternatingCarry]
  | cons x xs ih =>
    have ht := ih ((x + e) / (m + 1))
    have hd := Int.emod_add_ediv (x + e) (m + 1)
    simp only [Int.add_mul, Int.one_mul] at hd
    simp only [normalize, altSum, wordSign_cons, alternatingCarry,
      Int.mul_sub, Int.add_mul, Int.neg_mul] at *
    omega

theorem raw_alt_no_overflow (m c : Int) (B : Word) (hg : exteriorOverflow m c B = 0) :
    altSum (rawExterior m c B) =
      2 * altSum B + wordSign B * (2 * c - 2 * (m + 1) * bulkCarry m c) +
        (m + 2) * (-alternatingCarry m B 0 +
          wordSign B * alternatingCarry m B.reverse (bulkCarry m c)) := by
  have hl := normalize_alt_exact m B 0
  have hh := normalize_alt_exact m B.reverse (bulkCarry m c)
  rw [altSum_reverse, wordSign_reverse] at hh
  have hn1 := normalize_length m B 0
  have hn2 := normalize_length m B.reverse (bulkCarry m c)
  simp only [List.length_reverse] at hn2
  simp only [exteriorOverflow] at hg
  simp only [rawExterior, hg, if_true]
  rw [altSum_zip_add]
  · simp only [altSum_append, altSum_reverse, wordSign_normalize, wordSign_reverse,
      altSum, Int.sub_zero]
    rcases wordSign_bit B with hs | hs <;>
      simp only [hs, hg, Int.one_mul, Int.neg_one_mul, Int.neg_neg, Int.mul_zero,
        Int.add_zero, Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul,
        Int.neg_mul, Int.mul_neg, Int.mul_one, Int.mul_assoc, Int.mul_left_comm m 2] at * <;>
      omega
  · simp [hn1, hn2]

theorem raw_alt_overflow (m c : Int) (B : Word) (hg : exteriorOverflow m c B = 1) :
    altSum (rawExterior m c B) =
      wordSign B * (c - m * bulkCarry m c) -
        (m + 2) * (alternatingCarry m B 0 +
          wordSign B * alternatingCarry m B.reverse (bulkCarry m c)) := by
  have hl := normalize_alt_exact m B 0
  have hh := normalize_alt_exact m B.reverse (bulkCarry m c)
  rw [altSum_reverse, wordSign_reverse] at hh
  have hn1 := normalize_length m B 0
  have hn2 := normalize_length m B.reverse (bulkCarry m c)
  simp only [List.length_reverse] at hn2
  simp only [exteriorOverflow] at hg
  simp only [rawExterior, hg]
  simp only [show (1 : Int) ≠ 0 by decide, if_false]
  rw [altSum_zip_add]
  · simp only [altSum_append, altSum_reverse, wordSign_normalize, wordSign_reverse,
      altSum, Int.sub_zero]
    rcases wordSign_bit B with hs | hs <;>
      simp only [hs, hg, Int.one_mul, Int.neg_one_mul, Int.neg_neg, Int.mul_zero,
        Int.add_zero, Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul,
        Int.neg_mul, Int.mul_neg, Int.mul_one, Int.mul_assoc] at * <;> omega
  · simp [hn1, hn2]


theorem wordSign_raw (m c : Int) (B : Word) :
    wordSign (rawExterior m c B) = -wordSign B := by
  simp [wordSign, rawExterior_length, lengthSign]

theorem moment_step_no_overflow_exact (m c : Int) (B : Word)
    (hg : exteriorOverflow m c B = 0) :
    moment (nextPhase m c) (nextExterior m c B) = 2 * moment c B +
      (2 * (m + 2)) * (-wordSign B * bulkCarry m c - alternatingCarry m B 0 +
        wordSign B * alternatingCarry m B.reverse (bulkCarry m c)) := by
  unfold nextExterior
  rw [moment_stripSuffix]
  simp only [moment, wordSign_raw, raw_alt_no_overflow m c B hg, nextPhase]
  rcases wordSign_bit B with hs | hs <;>
    simp only [hs, Int.one_mul, Int.neg_one_mul, Int.neg_neg,
      Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.mul_one,
      Int.neg_mul, Int.mul_neg, Int.mul_assoc, Int.mul_left_comm m 2] <;> omega

theorem moment_step_overflow_exact (m c : Int) (B : Word)
    (hg : exteriorOverflow m c B = 1) :
    moment (nextPhase m c) (nextExterior m c B) =
      (2 * (m + 2)) * (-alternatingCarry m B 0 -
        wordSign B * alternatingCarry m B.reverse (bulkCarry m c)) := by
  unfold nextExterior
  rw [moment_stripSuffix]
  simp only [moment, wordSign_raw, raw_alt_overflow m c B hg, nextPhase]
  rcases wordSign_bit B with hs | hs <;>
    simp only [hs, Int.one_mul, Int.neg_one_mul, Int.neg_neg,
      Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.mul_one,
      Int.neg_mul, Int.mul_neg, Int.mul_assoc, Int.mul_left_comm m 2] <;> omega

theorem moment_step_no_overflow (m c : Int) (B : Word)
    (hg : exteriorOverflow m c B = 0) :
    moment (nextPhase m c) (nextExterior m c B) % (2 * (m + 2)) =
      (2 * moment c B) % (2 * (m + 2)) := by
  rw [moment_step_no_overflow_exact m c B hg]
  exact Int.add_mul_emod_self_left _ _ _

theorem moment_step_overflow (m c : Int) (B : Word)
    (hg : exteriorOverflow m c B = 1) :
    moment (nextPhase m c) (nextExterior m c B) % (2 * (m + 2)) = 0 := by
  rw [moment_step_overflow_exact m c B hg]
  exact Int.mul_emod_right _ _

theorem moment_zero_preserved (m c : Int) (B : Word) (hm : 1 ≤ m)
    (hB : ∀ x ∈ B, 0 ≤ x ∧ x ≤ 2 * m)
    (hz : moment c B % (2 * (m + 2)) = 0) :
    moment (nextPhase m c) (nextExterior m c B) % (2 * (m + 2)) = 0 := by
  rcases exterior_overflow_bit m c B hm hB with hg | hg
  · rw [moment_step_no_overflow m c B hg, Int.mul_emod, hz]
    simp
  · exact moment_step_overflow m c B hg

theorem moment_zero_path (m : Int) (c : Nat → Int) (B : Nat → Word) (n : Nat)
    (hm : 1 ≤ m) (hB : ∀ i, i < n → ∀ x ∈ B i, 0 ≤ x ∧ x ≤ 2 * m)
    (hstep : ∀ i, i < n → c (i+1) = nextPhase m (c i) ∧
      B (i+1) = nextExterior m (c i) (B i))
    (hz : moment (c 0) (B 0) % (2 * (m + 2)) = 0) :
    moment (c n) (B n) % (2 * (m + 2)) = 0 := by
  induction n with
  | zero => exact hz
  | succ n ih =>
    have hp := ih (fun i hi => hB i (by omega)) (fun i hi => hstep i (by omega))
    rw [(hstep n (by omega)).1, (hstep n (by omega)).2]
    exact moment_zero_preserved m (c n) (B n) hm (hB n (by omega)) hp

theorem moment_zero_after_overflow (m : Int) (c : Nat → Int) (B : Nat → Word) (n : Nat)
    (hm : 1 ≤ m) (hB : ∀ i, i < n → ∀ x ∈ B i, 0 ≤ x ∧ x ≤ 2 * m)
    (hstep : ∀ i, i < n → c (i+1) = nextPhase m (c i) ∧
      B (i+1) = nextExterior m (c i) (B i))
    (hover : ∃ i, i < n ∧ exteriorOverflow m (c i) (B i) = 1) :
    moment (c n) (B n) % (2 * (m + 2)) = 0 := by
  induction n with
  | zero => obtain ⟨i, hi, _⟩ := hover; omega
  | succ n ih =>
    obtain ⟨i, hi, hg⟩ := hover
    by_cases hil : i < n
    · have hp := ih (fun j hj => hB j (by omega))
        (fun j hj => hstep j (by omega)) ⟨i, hil, hg⟩
      rw [(hstep n (by omega)).1, (hstep n (by omega)).2]
      exact moment_zero_preserved m (c n) (B n) hm (hB n (by omega)) hp
    · have hieq : i = n := by omega
      subst i
      rw [(hstep n (by omega)).1, (hstep n (by omega)).2]
      exact moment_step_overflow m (c n) (B n) hg

theorem closed_exterior_moment_zero (m : Int) (c : Nat → Int) (B : Nat → Word) (n : Nat)
    (hm : 1 ≤ m) (hB : ∀ i, i < n → ∀ x ∈ B i, 0 ≤ x ∧ x ≤ 2 * m)
    (hstep : ∀ i, i < n → c (i+1) = nextPhase m (c i) ∧
      B (i+1) = nextExterior m (c i) (B i))
    (closeC : c n = c 0) (closeB : B n = B 0)
    (hover : ∃ i, i < n ∧ exteriorOverflow m (c i) (B i) = 1) :
    ∀ i, i ≤ n → moment (c i) (B i) % (2 * (m + 2)) = 0 := by
  have hz := moment_zero_after_overflow m c B n hm hB hstep hover
  rw [closeC, closeB] at hz
  intro i hi
  exact moment_zero_path m c B i hm (fun j hj => hB j (by omega))
    (fun j hj => hstep j (by omega)) hz

#print axioms wordSign_cons
#print axioms wordSign_bit
#print axioms wordSign_append
#print axioms wordSign_reverse
#print axioms wordSign_normalize
#print axioms altSum_append
#print axioms altSum_reverse
#print axioms altSum_zip_add
#print axioms stripPrefix_decomposition
#print axioms stripSuffix_decomposition
#print axioms moment_append_phase
#print axioms moment_append_replicate
#print axioms moment_stripSuffix
#print axioms normalize_alt_exact
#print axioms raw_alt_no_overflow
#print axioms raw_alt_overflow
#print axioms wordSign_raw
#print axioms moment_step_no_overflow_exact
#print axioms moment_step_overflow_exact
#print axioms moment_step_no_overflow
#print axioms moment_step_overflow
#print axioms moment_zero_preserved
#print axioms moment_zero_path
#print axioms moment_zero_after_overflow
#print axioms closed_exterior_moment_zero

end P196.Agent5.General.Moment
