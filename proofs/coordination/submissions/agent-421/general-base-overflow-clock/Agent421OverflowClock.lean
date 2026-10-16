import Agent421OverflowNormalization

namespace Agent421Overflow
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd Agent11HighBase Agent421NoOverflow

/-- Total indexed view of an existing finite list; out-of-range values are unused. -/
def seq (xs : List Int) (i : Nat) : Int := xs[i]?.getD 0

theorem seq_get (xs : List Int) (i : Nat) (hi : i < xs.length) :
    seq xs i = xs[i] := by
  simp only [seq, List.getElem?_eq_getElem hi, Option.getD_some]

theorem word_seq (xs : List Int) : word (seq xs) xs.length = xs := by
  apply List.ext_getElem (by simp)
  intro i hi hj
  rw [word_get (seq xs) xs.length i hj, seq_get xs i hj]

theorem seq_symmetric (xs : List Int) (hs : xs.reverse = xs) :
    ∀ i, i < xs.length → seq xs i = seq xs (xs.length-1-i) := by
  intro i hi
  have hm : xs.length-1-i < xs.length := by omega
  rw [seq_get xs i hi, seq_get xs (xs.length-1-i) hm]
  have hh : xs.reverse[i]'(by simpa using hi) = xs[i] := by
    simp only [hs]
  rw [List.getElem_reverse] at hh
  exact hh.symm

/-- The computed final carry determines the real output width, including its
new leading one. This uses the existing actualDigits implementation. -/
theorem normalize_overflow (b : Int) (q : Nat → Int) (L : Nat)
    (hc : carry b q L = 1) :
    normalize b (word q L) = word (output b q) L ++ [1] := by
  simp only [normalize, actualDigits, atActualWidth, tags_ordinary,
    terminal_word, hc, Int.reduceEq, ↓reduceIte, placed_body_terminal, body_word]

theorem normalize_overflow_length (b : Int) (q : Nat → Int) (L : Nat)
    (hc : carry b q L = 1) : (normalize b (word q L)).length = L+1 := by
  rw [normalize_overflow b q L hc]
  simp

theorem normalize_overflow_bounds (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hc : carry b q L = 1) : DigitBounds b (normalize b (word q L)) := by
  rw [normalize_overflow b q L hc]
  intro d hd
  rcases List.mem_append.mp hd with hd | hd
  · obtain ⟨i, hi, rfl⟩ := (word_mem (output b q) L d).mp hd
    exact ⟨Int.emod_nonneg _ (by omega), Int.emod_lt_of_pos _ (by omega)⟩
  · have he : d = 1 := by simpa using hd
    subst d; omega

theorem normalize_overflow_positive_last (b : Int) (q : Nat → Int) (L : Nat)
    (hc : carry b q L = 1) : PositiveLast (normalize b (word q L)) := by
  exact ⟨word (output b q) L, 1, normalize_overflow b q L hc, by omega⟩

/-- Not an abstract update: this is exactly the repository's existing nextPairs. -/
def nextSeq (b : Int) (q : Nat → Int) (L : Nat) : Nat → Int :=
  seq (nextPairs b (word q L))

theorem nextSeq_word (b : Int) (q : Nat → Int) (L : Nat)
    (hc : carry b q L = 1) :
    word (nextSeq b q L) (L+1) = nextPairs b (word q L) := by
  have hl : (nextPairs b (word q L)).length = L+1 := by
    simp only [nextPairs, pairs_length, normalize_overflow_length b q L hc]
  simpa only [hl] using word_seq (nextPairs b (word q L))

theorem nextSeq_bounds (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hc : carry b q L = 1) :
    ∀ i, i < L+1 → 0 ≤ nextSeq b q L i ∧ nextSeq b q L i ≤ 2*b-2 := by
  intro i hi
  have hl : (nextPairs b (word q L)).length = L+1 := by
    simp only [nextPairs, pairs_length, normalize_overflow_length b q L hc]
  have hi' : i < (nextPairs b (word q L)).length := by omega
  change 0 ≤ seq (nextPairs b (word q L)) i ∧ seq (nextPairs b (word q L)) i ≤ 2*b-2
  rw [seq_get _ i hi']
  exact pairs_bounds b _ (normalize_overflow_bounds b q L hb hc) _ (List.getElem_mem hi')

theorem nextSeq_symmetric (b : Int) (q : Nat → Int) (L : Nat)
    (hc : carry b q L = 1) :
    ∀ i, i < L+1 → nextSeq b q L i = nextSeq b q L ((L+1)-1-i) := by
  have hl : (nextPairs b (word q L)).length = L+1 := by
    simp only [nextPairs, pairs_length, normalize_overflow_length b q L hc]
  simpa only [hl] using seq_symmetric (nextPairs b (word q L)) (pairs_symmetric _)

/-- The new outer pair is the old low-end digit plus the actual leading one. -/
theorem nextSeq_outer (b : Int) (q : Nat → Int) (L : Nat)
    (hL : 0 < L) (hc : carry b q L = 1) :
    nextSeq b q L 0 = q 0 % b + 1 := by
  unfold nextSeq nextPairs
  rw [normalize_overflow b q L hc]
  cases L with
  | zero => omega
  | succ L =>
    simp [seq, pairs, word, segment, List.reverse_append, output, carry]

theorem terminal_of_outer_low (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (ho : q 0 < b-1) :
    carry b q L = 0 := by
  have hc := carry_bounded b q L hb hq (L-1) (by omega)
  have hlast : q (L-1) = q 0 := by simpa using (hsym 0 hL).symm
  have hq0 := hq 0 hL
  have he : L = (L-1)+1 := by omega
  calc
    carry b q L = (q (L-1) + carry b q (L-1))/b := by rw [show L = (L-1)+1 from he]; rfl
    _ = 0 := (low_divmod b _ (by omega) (by omega)).1

theorem terminal_of_outer_high (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (ho : b ≤ q 0) :
    carry b q L = 1 := by
  have hc := carry_bounded b q L hb hq (L-1) (by omega)
  have hlast : q (L-1) = q 0 := by simpa using (hsym 0 hL).symm
  have hq0 := hq 0 hL
  have he : L = (L-1)+1 := by omega
  calc
    carry b q L = (q (L-1) + carry b q (L-1))/b := by rw [show L = (L-1)+1 from he]; rfl
    _ = 1 := (high_divmod b _ hb (by omega)).1

/-- Starting with alpha, exactly one overflow is followed by non-overflow. -/
theorem alpha_schedule (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 3 ≤ b) (hs : 1 ≤ s ∧ s ≤ b-2) (hL : 0 < L)
    (hc : carry b q L = 1) (ho : q 0 = b+s-1) :
    nextSeq b q L 0 = s ∧ carry b (nextSeq b q L) (L+1) = 0 := by
  have he := nextSeq_outer b q L hL hc
  have hd := high_divmod b (b+s-1) (by omega) (by omega)
  rw [ho, hd.2] at he
  have he' : nextSeq b q L 0 = s := by omega
  refine ⟨he', terminal_of_outer_low b (nextSeq b q L) (L+1) (by omega) (by omega)
    (nextSeq_bounds b q L (by omega) hc) (nextSeq_symmetric b q L hc) ?_⟩
  omega

/-- Starting with b-1, exactly two overflows are followed by non-overflow. -/
theorem neutral_schedule (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 3 ≤ b) (hL : 0 < L) (hc : carry b q L = 1) (ho : q 0 = b-1) :
    nextSeq b q L 0 = b ∧ carry b (nextSeq b q L) (L+1) = 1 ∧
    nextSeq b (nextSeq b q L) (L+1) 0 = 1 ∧
    carry b (nextSeq b (nextSeq b q L) (L+1)) (L+2) = 0 := by
  have he := nextSeq_outer b q L hL hc
  rw [ho, (low_divmod b (b-1) (by omega) (by omega)).2] at he
  have he' : nextSeq b q L 0 = b := by omega
  have hc' := terminal_of_outer_high b (nextSeq b q L) (L+1) (by omega) (by omega)
    (nextSeq_bounds b q L (by omega) hc) (nextSeq_symmetric b q L hc) (by omega)
  have he2 := nextSeq_outer b (nextSeq b q L) (L+1) (by omega) hc'
  rw [he', Int.emod_self, Int.zero_add] at he2
  refine ⟨he', hc', he2, ?_⟩
  exact terminal_of_outer_low b (nextSeq b (nextSeq b q L) (L+1)) (L+2)
    (by omega) (by omega) (nextSeq_bounds b _ _ (by omega) hc')
    (nextSeq_symmetric b _ _ hc') (by omega)

/-- Complete outer-clock disjunction for the source's overflow-normalized word.
No protected-run closure or low-bound propagation is smuggled into a premise. -/
theorem normalized_outer_clock (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 3 ≤ b) (hs : 1 ≤ s ∧ s ≤ b-2) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hc : carry b q L = 1) :
    let r := normalized b s q L
    carry b r L = 1 ∧
    ((r 0 = b+s-1 ∧ nextSeq b r L 0 = s ∧ carry b (nextSeq b r L) (L+1) = 0) ∨
     (r 0 = b-1 ∧ nextSeq b r L 0 = b ∧ carry b (nextSeq b r L) (L+1) = 1 ∧
      nextSeq b (nextSeq b r L) (L+1) 0 = 1 ∧
      carry b (nextSeq b (nextSeq b r L) (L+1)) (L+2) = 0)) := by
  dsimp
  have hcn := (normalized_preserves_carry b s q L (by omega) (by omega) hq hsym L (by omega)).trans hc
  refine ⟨hcn, ?_⟩
  rcases normalized_outer_cases b s q L (by omega) hL hq hc with ha | hn
  · exact Or.inl ⟨ha, alpha_schedule b s _ L hb hs hL hcn ha⟩
  · exact Or.inr ⟨hn, neutral_schedule b _ L hb hL hcn hn⟩

#print axioms normalize_overflow
#print axioms normalized_outer_clock
end Agent421Overflow
