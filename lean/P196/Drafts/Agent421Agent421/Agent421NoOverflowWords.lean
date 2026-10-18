import P196.Drafts.Agent421Agent421.Agent421NoOverflowLocal

namespace Agent421NoOverflow
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd Agent11HighBase

/-- Indexed view of one ordinary carry chain; the list bridge below is exact. -/
def carry (b : Int) (q : Nat → Int) : Nat → Int
  | 0 => 0
  | i+1 => (q i + carry b q i) / b

def output (b : Int) (q : Nat → Int) (i : Nat) : Int :=
  (q i + carry b q i) % b

def segment (q : Nat → Int) (k : Nat) : Nat → List Int
  | 0 => []
  | n+1 => q k :: segment q (k+1) n

def word (q : Nat → Int) (n : Nat) : List Int := segment q 0 n

@[simp] theorem segment_length (q : Nat → Int) (k n : Nat) :
    (segment q k n).length = n := by
  induction n generalizing k with
  | zero => rfl
  | succ n ih => simp [segment, ih]

@[simp] theorem word_length (q : Nat → Int) (n : Nat) : (word q n).length = n :=
  segment_length q 0 n

theorem segment_get (q : Nat → Int) (k n i : Nat) (hi : i < n) :
    (segment q k n)[i]'(by simpa using hi) = q (k+i) := by
  induction n generalizing k i with
  | zero => omega
  | succ n ih =>
    cases i with
    | zero => simp [segment]
    | succ i =>
      simpa [segment, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
        ih (k+1) i (by omega)

@[simp] theorem word_get (q : Nat → Int) (n i : Nat) (hi : i < n) :
    (word q n)[i]'(by simpa using hi) = q i := by
  simpa [word] using segment_get q 0 n i hi

theorem segment_mem (q : Nat → Int) (k n : Nat) (a : Int) :
    a ∈ segment q k n ↔ ∃ i, i < n ∧ q (k+i) = a := by
  induction n generalizing k with
  | zero => simp [segment]
  | succ n ih =>
    simp only [segment, List.mem_cons, ih]
    constructor
    · intro h
      rcases h with h | ⟨i, hi, he⟩
      · exact ⟨0, by omega, by simpa using h.symm⟩
      · exact ⟨i+1, by omega, by simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using he⟩
    · rintro ⟨i, hi, he⟩
      cases i with
      | zero => exact Or.inl (by simpa using he.symm)
      | succ i => exact Or.inr ⟨i, by omega, by simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using he⟩

theorem word_mem (q : Nat → Int) (n : Nat) (a : Int) :
    a ∈ word q n ↔ ∃ i, i < n ∧ q i = a := by
  simpa [word] using segment_mem q 0 n a

theorem word_ext (q r : Nat → Int) (n : Nat) (h : ∀ i, i < n → q i = r i) :
    word q n = word r n := by
  apply List.ext_getElem (by simp)
  intro i hi hj
  simp only [word_length] at hi hj
  rw [word_get q n i hi, word_get r n i hj]
  exact h i hi

theorem word_symmetric (q : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → q i = q (n-1-i)) : (word q n).reverse = word q n := by
  apply List.ext_getElem (by simp)
  intro i hi hj
  have hn : i < n := by simpa using hj
  simp only [List.getElem_reverse, word_length]
  rw [word_get q n (n-1-i) (by omega), word_get q n i hn]
  exact (h i hn).symm

theorem pairs_word (q : Nat → Int) (n : Nat) :
    pairs (word q n) = word (fun i => q i + q (n-1-i)) n := by
  apply List.ext_getElem (by simp [pairs])
  intro i hi hj
  have hn : i < n := by simpa using hj
  simp only [pairs, List.getElem_zipWith, List.getElem_reverse, word_length]
  rw [word_get q n i hn, word_get q n (n-1-i) (by omega),
    word_get (fun i => q i + q (n-1-i)) n i hn]

theorem segment_snoc (q : Nat → Int) (k n : Nat) :
    segment q k (n+1) = segment q k n ++ [q (k+n)] := by
  induction n generalizing k with
  | zero => simp [segment]
  | succ n ih =>
    change q k :: segment q (k+1) (n+1) = q k :: (segment q (k+1) n ++ [q (k+(n+1))])
    rw [ih]
    have he : k+1+n = k+(n+1) := by omega
    rw [he]

theorem word_positiveLast (q : Nat → Int) (n : Nat) (hn : 0 < n)
    (hp : 0 < q (n-1)) : PositiveLast (word q n) := by
  refine ⟨word q (n-1), q (n-1), ?_, hp⟩
  have he : n = (n-1)+1 := by omega
  calc
    word q n = word q ((n-1)+1) := congrArg (word q) he
    _ = word q (n-1) ++ [q (n-1)] := by simpa only [word, Nat.zero_add] using segment_snoc q 0 (n-1)

theorem carry_bounded (b : Int) (q : Nat → Int) (n : Nat) (hb : 2 ≤ b)
    (hq : ∀ i, i < n → 0 ≤ q i ∧ q i ≤ 2*b-2) :
    ∀ i, i ≤ n → 0 ≤ carry b q i ∧ carry b q i ≤ 1 := by
  intro i
  induction i with
  | zero => intro _; simp [carry]
  | succ i ih =>
    intro hi
    have hc := carry_bit b (q i) (carry b q i) hb (hq i (by omega)) (ih (by omega))
    change 0 ≤ (q i + carry b q i)/b ∧ (q i + carry b q i)/b ≤ 1
    omega

theorem terminal_segment (b : Int) (q : Nat → Int) (k n : Nat) :
    terminal b (carry b q k) (tags (segment q k n)) = carry b q (k+n) := by
  induction n generalizing k with
  | zero => simp [segment, tags, terminal]
  | succ n ih =>
    change terminal b ((q k + carry b q k)/b) (tags (segment q (k+1) n)) = carry b q (k+(n+1))
    change terminal b (carry b q (k+1)) (tags (segment q (k+1) n)) = carry b q (k+(n+1))
    simpa only [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using ih (k+1)

theorem body_segment (b : Int) (q : Nat → Int) (k n : Nat) :
    body b (carry b q k) (tags (segment q k n)) = segment (output b q) k n := by
  induction n generalizing k with
  | zero => rfl
  | succ n ih =>
    simp only [segment, tags, List.map_cons, body, Bool.false_eq_true,
      ↓reduceIte, Int.add_zero]
    change output b q k :: body b (carry b q (k+1)) (tags (segment q (k+1) n)) =
      output b q k :: segment (output b q) (k+1) n
    rw [ih]

theorem terminal_word (b : Int) (q : Nat → Int) (n : Nat) :
    terminal b 0 (tags (word q n)) = carry b q n := by
  simpa only [word, carry, Nat.zero_add] using terminal_segment b q 0 n

theorem body_word (b : Int) (q : Nat → Int) (n : Nat) :
    body b 0 (tags (word q n)) = word (output b q) n := by
  simpa only [word, carry] using body_segment b q 0 n

/-- No padding slot survives the actual-width normalization. -/
theorem normalize_nooverflow (b : Int) (q : Nat → Int) (n : Nat)
    (hc : carry b q n = 0) : normalize b (word q n) = word (output b q) n := by
  simp only [normalize, actualDigits, atActualWidth, tags_ordinary,
    terminal_word, hc, ↓reduceIte, body_word]

#print axioms normalize_nooverflow
#print axioms pairs_word
end Agent421NoOverflow
