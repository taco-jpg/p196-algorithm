import P196.Foundations.LychrelDigitSums

/-!
Actual arbitrary-size simultaneous births of coefficients 0 and 18.
For k,r >= 1, the admissible full-width word
  (1,9^k,1,10,9^(2r),10,1,9^k,1)
contains no 0 or 18 and its actual no-overflow successor is
  (2,18^k,3,1,0^(2r),1,3,18^k,2).
The formulas also cover empty bands, k=0 or r=0. This is one exact step;
no recurrence, infinite safety, or assertion about the orbit of 196 follows.
-/

namespace RunBirths.UnboundedBirths

open DecimalDigits FoldedDecimal

def width (k r : Nat) : Nat := 2 * k + 2 * r + 6

/-- The positive source coefficients; values beyond the width are irrelevant. -/
def source (k r i : Nat) : Nat :=
  if i = 0 ∨ i = k + 1 ∨ i = k + 2 * r + 4 ∨ i = 2 * k + 2 * r + 5 then 1
  else if i = k + 2 ∨ i = k + 2 * r + 3 then 10
  else if i < width k r then 9 else 0

/-- The exact candidate carry interval, later identified with recursive carry. -/
def incoming (k r i : Nat) : Nat :=
  if k + 3 ≤ i ∧ i ≤ k + 2 * r + 4 then 1 else 0

/-- Actual normalized digits (1,9^k,1,0,0^(2r),1,2,9^k,1). -/
def normalized (k r i : Nat) : Nat :=
  if i = 0 ∨ i = k + 1 ∨ i = k + 2 * r + 3 ∨ i = 2 * k + 2 * r + 5 then 1
  else if (1 ≤ i ∧ i ≤ k) ∨ (k + 2 * r + 5 ≤ i ∧ i < 2 * k + 2 * r + 5) then 9
  else if i = k + 2 * r + 4 then 2 else 0

/-- Target coefficients with two exterior 18 bands and a central zero band. -/
def target (k r i : Nat) : Nat :=
  if i = 0 ∨ i = 2 * k + 2 * r + 5 then 2
  else if i = k + 1 ∨ i = k + 2 * r + 4 then 3
  else if i = k + 2 ∨ i = k + 2 * r + 3 then 1
  else if (1 ≤ i ∧ i ≤ k) ∨ (k + 2 * r + 5 ≤ i ∧ i < 2 * k + 2 * r + 5) then 18
  else 0

theorem source_bounded (k r i : Nat) : source k r i ≤ 18 := by
  unfold source
  repeat first | omega | split

theorem normalized_bounded (k r i : Nat) : normalized k r i ≤ 9 := by
  unfold normalized
  repeat first | omega | split

theorem incoming_zero (k r : Nat) : incoming k r 0 = 0 := by
  unfold incoming
  split <;> omega

theorem incoming_terminal (k r : Nat) : incoming k r (width k r) = 0 := by
  unfold incoming width
  split <;> omega

set_option maxHeartbeats 1000000 in
theorem exact_column_equation (k r i : Nat) :
    normalized k r i + 10 * incoming k r (i + 1) = source k r i + incoming k r i := by
  have hcases : i = 0 ∨ (1 ≤ i ∧ i ≤ k) ∨ i = k + 1 ∨ i = k + 2 ∨
      (k + 3 ≤ i ∧ i < k + 2 * r + 3) ∨ i = k + 2 * r + 3 ∨ i = k + 2 * r + 4 ∨
      (k + 2 * r + 5 ≤ i ∧ i < 2 * k + 2 * r + 5) ∨ i = 2 * k + 2 * r + 5 ∨
      width k r ≤ i := by unfold width; omega
  rcases hcases with h | h | h | h | h | h | h | h | h | h
  all_goals (try subst i)
  all_goals simp (disch := omega) [normalized, incoming, source, width]
  all_goals (repeat first | omega | split)

theorem actual_carry (k r i : Nat) : carry (source k r) i = incoming k r i := by
  induction i with
  | zero => exact (incoming_zero k r).symm
  | succ i ih =>
    have he := exact_column_equation k r i
    have hd := normalized_bounded k r i
    simp only [carry, ih]
    omega

theorem actual_output (k r i : Nat) : output (source k r) i = normalized k r i := by
  have he := exact_column_equation k r i
  have hd := normalized_bounded k r i
  simp only [output, actual_carry]
  omega

theorem no_overflow (k r : Nat) : carry (source k r) (width k r) = 0 := by
  rw [actual_carry, incoming_terminal]

theorem actual_width (k r : Nat) : nextWidth (source k r) (width k r) = width k r := by
  simp only [nextWidth, no_overflow, if_true]

theorem source_symmetric (k r i : Nat) (hi : i < width k r) :
    source k r i = source k r (width k r - 1 - i) := by
  let j := width k r - 1 - i
  have hj : j = 2 * k + 2 * r + 5 - i := by simp [j, width]
  have hib : i < 2 * k + 2 * r + 6 := hi
  have hjb : j < width k r := by unfold width; omega
  have h1 : (i = 0 ∨ i = k + 1 ∨ i = k + 2 * r + 4 ∨ i = 2 * k + 2 * r + 5) ↔
      (j = 0 ∨ j = k + 1 ∨ j = k + 2 * r + 4 ∨ j = 2 * k + 2 * r + 5) := by omega
  have h10 : (i = k + 2 ∨ i = k + 2 * r + 3) ↔
      (j = k + 2 ∨ j = k + 2 * r + 3) := by omega
  change source k r i = source k r j
  simp only [source, h1, h10, hi, hjb, if_true]

/-- The width is even, so no forbidden odd central coefficient is hidden. -/
theorem source_admissible (k r : Nat) : Admissible (width k r) (source k r) := by
  refine ⟨by unfold width; omega, by simp [source],
    (fun i _ => source_bounded k r i), source_symmetric k r, ?_⟩
  intro i hi heq
  unfold width at hi heq
  omega

set_option maxHeartbeats 1000000 in
theorem exact_pair_equation (k r i : Nat) (hi : i < width k r) :
    columnSum (normalized k r) (width k r) i = target k r i := by
  have hib : i < 2 * k + 2 * r + 6 := hi
  have hcases : i = 0 ∨ (1 ≤ i ∧ i ≤ k) ∨ i = k + 1 ∨ i = k + 2 ∨
      (k + 3 ≤ i ∧ i < k + 2 * r + 3) ∨ i = k + 2 * r + 3 ∨ i = k + 2 * r + 4 ∨
      (k + 2 * r + 5 ≤ i ∧ i < 2 * k + 2 * r + 5) ∨ i = 2 * k + 2 * r + 5 := by omega
  rcases hcases with h | h | h | h | h | h | h | h | h
  all_goals (try subst i)
  all_goals simp (disch := omega) [columnSum, reflected, normalized, target, width]
  all_goals (repeat first | omega | split)

/-- Exact full-width formula for the actual successor, with no guessed carry. -/
theorem actual_update (k r i : Nat) (hi : i < width k r) :
    nextColumns (source k r) (width k r) i = target k r i := by
  simp only [nextColumns, no_overflow, if_true, columnSum, reflected, actual_output]
  exact exact_pair_equation k r i hi

theorem target_admissible (k r : Nat) : Admissible (width k r) (target k r) := by
  have ha := NormalizationBridge.admissible_next (source k r) (width k r) (source_admissible k r)
  rw [actual_width] at ha
  exact NormalizationBridge.admissible_congr _ _ _ ha (actual_update k r)

/-- Every source position avoids both extreme coefficients. -/
theorem source_no_extremes (k r i : Nat) (hi : i < width k r) :
    source k r i ≠ 0 ∧ source k r i ≠ 18 := by
  unfold source
  repeat first | omega | split

/-- The entire central band consists of newly born zeros from old nines. -/
theorem new_zero_band (k r i : Nat) (hlo : k + 3 ≤ i) (hhi : i < k + 2 * r + 3) :
    source k r i = 9 ∧ nextColumns (source k r) (width k r) i = 0 := by
  have hi : i < width k r := by unfold width; omega
  rw [actual_update k r i hi]
  unfold source target
  repeat first | omega | split

/-- Each exterior band consists of newly born 18s from old nines. -/
theorem new_eighteen_bands (k r i : Nat)
    (hb : (1 ≤ i ∧ i ≤ k) ∨ (k + 2 * r + 5 ≤ i ∧ i < 2 * k + 2 * r + 5)) :
    source k r i = 9 ∧ nextColumns (source k r) (width k r) i = 18 := by
  have hi : i < width k r := by unfold width; omega
  rw [actual_update k r i hi]
  unfold source target
  repeat first | omega | split

/-- Exact classification of the new extrema, excluding extra unlisted sites. -/
theorem exact_extreme_positions (k r i : Nat) (hi : i < width k r) :
    (nextColumns (source k r) (width k r) i = 0 ↔ k + 3 ≤ i ∧ i < k + 2 * r + 3) ∧
    (nextColumns (source k r) (width k r) i = 18 ↔
      (1 ≤ i ∧ i ≤ k) ∨ (k + 2 * r + 5 ≤ i ∧ i < 2 * k + 2 * r + 5)) := by
  have hib : i < 2 * k + 2 * r + 6 := hi
  rw [actual_update k r i hi]
  constructor <;> unfold target <;> repeat first | omega | split

theorem birth_band_lengths (k r : Nat) :
    (k + 1) - 1 = k ∧ (2 * k + 2 * r + 5) - (k + 2 * r + 5) = k ∧
    (k + 2 * r + 3) - (k + 3) = 2 * r := by omega

/-- Positive finite decimal realizations exist for every pair of parameters. -/
theorem family_realized (k r : Nat) :
    ∃ n d, 0 < n ∧ Canonical n d (width k r) ∧
      (∀ i, i < width k r → columnSum d (width k r) i = source k r i) := by
  obtain ⟨hL, ho, hb, hs, hm⟩ := source_admissible k r
  exact valid_word_realizable (source k r) (width k r) hL ho hb hs hm

/-- The exact target is also realized by the actual numeric successor. -/
theorem numeric_family_realized (k r : Nat) :
    ∃ n d e, 0 < n ∧ Canonical n d (width k r) ∧
      (∀ i, i < width k r → columnSum d (width k r) i = source k r i) ∧
      Canonical (Lychrel196.step n) e (width k r) ∧
      (∀ i, i < width k r → columnSum e (width k r) i = target k r i) := by
  obtain ⟨n, d, hp, hc, hr⟩ := family_realized k r
  obtain ⟨e, he, hn⟩ := representation_next n d (source k r) (width k r) hc hr
  rw [actual_width] at he hn
  refine ⟨n, d, e, hp, hc, hr, he, ?_⟩
  intro i hi
  exact (hn i hi).trans (actual_update k r i hi)

/-- For every B there are simultaneously B+1 consecutive new zeros and
B+1 consecutive new 18s, although the whole source has neither extreme.
The bound concerns a single actual step of a finite admissible word. -/
theorem arbitrarily_long_birth_bands (B : Nat) :
    ∃ L q a b, Admissible L q ∧
      (∀ i, i < L → q i ≠ 0 ∧ q i ≠ 18) ∧
      carry q L = 0 ∧ a + (B + 1) ≤ L ∧ b + (B + 1) ≤ L ∧
      (∀ j, j < B + 1 →
        q (a + j) = 9 ∧ nextColumns q L (a + j) = 0 ∧
        q (b + j) = 9 ∧ nextColumns q L (b + j) = 18) := by
  refine ⟨width (B + 1) (B + 1), source (B + 1) (B + 1), B + 4, 1,
    source_admissible _ _, source_no_extremes _ _, no_overflow _ _, ?_, ?_, ?_⟩
  · unfold width
    omega
  · unfold width
    omega
  · intro j hj
    have h0 := new_zero_band (B + 1) (B + 1) (B + 4 + j) (by omega) (by omega)
    have h18 := new_eighteen_bands (B + 1) (B + 1) (1 + j)
      (Or.inl ⟨by omega, by omega⟩)
    exact ⟨h0.1, h0.2, h18.1, h18.2⟩

#print axioms source_bounded
#print axioms normalized_bounded
#print axioms incoming_zero
#print axioms incoming_terminal
#print axioms exact_column_equation
#print axioms actual_carry
#print axioms actual_output
#print axioms no_overflow
#print axioms actual_width
#print axioms source_symmetric
#print axioms source_admissible
#print axioms exact_pair_equation
#print axioms actual_update
#print axioms target_admissible
#print axioms source_no_extremes
#print axioms new_zero_band
#print axioms new_eighteen_bands
#print axioms exact_extreme_positions
#print axioms birth_band_lengths
#print axioms family_realized
#print axioms numeric_family_realized
#print axioms arbitrarily_long_birth_bands

end RunBirths.UnboundedBirths
