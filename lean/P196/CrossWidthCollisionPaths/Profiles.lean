import P196.CrossWidthCollisionStates.StateSpace

/-!
# Coefficient words reconstructed from reflected collision paths

A closed reflected path determines two bounded symmetric coefficient
words of adjacent widths. The two center conditions in `Valid` make both
words admissible for ordinary decimal reverse-and-add sources.
-/

set_option autoImplicit false

namespace CrossWidthCollisionPaths

open DecimalDigits FoldedDecimal CrossWidthCollisionStates

/-- Reflection exchanges the two encoded carry differences. -/
def flip (s : State) : State := ⟨s.x, s.v, s.u⟩

/-- The shorter coefficient word is read from successive states. -/
def shortWord (f : Nat → State) (i : Nat) : Nat := (f (i + 1)).x

/-- The longer word has outer coefficients one and inner coefficients
determined by consecutive states. -/
def longWord (L : Nat) (f : Nat → State) (i : Nat) : Nat :=
  if i = 0 ∨ i = L then 1
  else (f i).x + (f (i + 1)).v + 9 - 10 * (f i).v

/-- A closed reflected path over the full shorter-source interval. -/
structure Closed (L : Nat) (f : Nat → State) : Prop where
  length : 2 ≤ L
  first : f 1 = initial
  last : f L = initial
  edge : ∀ i, 1 ≤ i → i < L → Edge (f i) (f (i + 1))
  reflection : ∀ i, 1 ≤ i → i ≤ L → f (L + 1 - i) = flip (f i)

/-- The center conditions needed for both reconstructed words to be
coefficient words of ordinary positive decimal sources. -/
structure Valid (L : Nat) (f : Nat → State) : Prop extends Closed L f where
  short_center : ∀ i, i < L → i = L - 1 - i → shortWord f i % 2 = 0
  long_center : ∀ i, i < L + 1 → i = L - i → longWord L f i % 2 = 0

/-- The two local column identities, with the reflected identity first.
The edge inequalities make the natural subtraction exact. -/
theorem closed_columns {L : Nat} {f : Nat → State} (h : Closed L f)
    {i : Nat} (hi : 1 ≤ i) (hiL : i < L) :
    (longWord L f i + 10 * (f i).v = (f i).x + (f (i + 1)).v + 9) ∧
    (shortWord f i + (f i).u + 9 =
      longWord L f i + 10 * (f (i + 1)).u) := by
  obtain ⟨_, _, _, _, _, _, hlo, _, heq⟩ := h.edge i hi hiL
  have hz : ¬ (i = 0 ∨ i = L) := by omega
  have hw : longWord L f i =
      (f i).x + (f (i + 1)).v + 9 - 10 * (f i).v := by
    simp only [longWord, if_neg hz]
  simp only [hw, shortWord]
  constructor <;> omega

private theorem closed_state_bounds {L : Nat} {f : Nat → State}
    (h : Closed L f) {i : Nat} (hi : 1 ≤ i) (hiL : i ≤ L) :
    (f i).x ≤ 18 ∧ (f i).u ≤ 2 ∧ (f i).v ≤ 2 := by
  by_cases hilast : i = L
  · rw [hilast, h.last]
    decide +kernel
  · have he := h.edge i hi (by omega)
    exact ⟨he.1, he.2.1, he.2.2.1⟩

/-- The reconstructed words have the forced outer coefficients and are
bounded and symmetric on their respective active intervals. -/
theorem closed_word_properties {L : Nat} {f : Nat → State} (h : Closed L f) :
    shortWord f 0 = 11 ∧ longWord L f 0 = 1 ∧ longWord L f L = 1 ∧
    (∀ i, i < L → shortWord f i ≤ 18) ∧
    (∀ i, i < L + 1 → longWord L f i ≤ 18) ∧
    (∀ i, i < L → shortWord f i = shortWord f (L - 1 - i)) ∧
    (∀ i, i < L + 1 → longWord L f i = longWord L f (L - i)) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp [shortWord, h.first, initial]
  · simp [longWord]
  · simp [longWord]
  · intro i hi
    exact (closed_state_bounds h (i := i + 1) (by omega) (by omega)).1
  · intro i hi
    by_cases hz : i = 0 ∨ i = L
    · simp only [longWord, if_pos hz]
      decide
    · have hi0 : 1 ≤ i := by omega
      have hiL : i < L := by omega
      have hhigh := (closed_columns h hi0 hiL).1
      obtain ⟨_, _, _, _, _, _, _, hupper, _⟩ := h.edge i hi0 hiL
      omega
  · intro i hi
    have href := h.reflection (i + 1) (by omega) (by omega)
    have hindex : L + 1 - (i + 1) = (L - 1 - i) + 1 := by omega
    have hx := congrArg State.x href
    simpa only [shortWord, flip, hindex] using hx.symm
  · intro i hi
    by_cases hz : i = 0
    · subst i
      simp [longWord]
    by_cases hend : i = L
    · subst i
      simp [longWord]
    have hi0 : 1 ≤ i := by omega
    have hiL : i < L := by omega
    have hleft : f (L - i) = flip (f (i + 1)) := by
      have href := h.reflection (i + 1) (by omega) (by omega)
      have hindex : L + 1 - (i + 1) = L - i := by omega
      simpa only [hindex] using href
    have hright : f (L - i + 1) = flip (f i) := by
      have href := h.reflection i hi0 (by omega)
      have hindex : L + 1 - i = L - i + 1 := by omega
      simpa only [hindex] using href
    have hhigh := (closed_columns h (i := L - i) (by omega) (by omega)).1
    have hlow := (closed_columns h hi0 hiL).2
    rw [hleft, hright] at hhigh
    dsimp only [flip] at hhigh
    dsimp only [shortWord] at hlow
    omega

/-- The two center conditions complete admissibility of the shorter and
longer reconstructed coefficient words. -/
theorem valid_words {L : Nat} {f : Nat → State} (h : Valid L f) :
    Admissible L (shortWord f) ∧ Admissible (L + 1) (longWord L f) := by
  have hL := h.toClosed.length
  obtain ⟨hq0, hr0, _, hqb, hrb, hqs, hrs⟩ := closed_word_properties h.toClosed
  constructor
  · exact ⟨by omega, by omega, hqb, hqs, h.short_center⟩
  · refine ⟨by omega, by omega, hrb, ?_, ?_⟩
    · simpa only [Nat.add_sub_cancel] using hrs
    · simpa only [Nat.add_sub_cancel] using h.long_center

end CrossWidthCollisionPaths

#print axioms CrossWidthCollisionPaths.flip
#print axioms CrossWidthCollisionPaths.shortWord
#print axioms CrossWidthCollisionPaths.longWord
#print axioms CrossWidthCollisionPaths.Closed
#print axioms CrossWidthCollisionPaths.Valid
#print axioms CrossWidthCollisionPaths.closed_columns
#print axioms CrossWidthCollisionPaths.closed_word_properties
#print axioms CrossWidthCollisionPaths.valid_words
