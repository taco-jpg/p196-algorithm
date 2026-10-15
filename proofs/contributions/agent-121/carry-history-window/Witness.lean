import Targets

namespace Agent121.CarryWindow
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- Pair sums of the canonical decimal number 917. -/
def leftWord (i : Nat) : Nat := if i = 1 then 2 else 16

/-- Pair sums of the canonical decimal number 908. -/
def rightWord (i : Nat) : Nat := if i = 1 then 0 else 17

def leftDigits (i : Nat) : Nat := if i = 0 then 7 else if i = 1 then 1 else 9
def rightDigits (i : Nat) : Nat := if i = 0 then 8 else if i = 1 then 0 else 9

theorem left_admissible : Admissible 3 leftWord := by
  refine ⟨by decide, by decide, ?_, ?_, ?_⟩
  · intro i hi
    unfold leftWord
    split <;> omega
  · intro i hi
    have h : i = 0 ∨ i = 1 ∨ i = 2 := by omega
    rcases h with rfl | rfl | rfl <;> decide
  · intro i hi hm
    have h : i = 1 := by omega
    subst i
    decide

theorem right_admissible : Admissible 3 rightWord := by
  refine ⟨by decide, by decide, ?_, ?_, ?_⟩
  · intro i hi
    unfold rightWord
    split <;> omega
  · intro i hi
    have h : i = 0 ∨ i = 1 ∨ i = 2 := by omega
    rcases h with rfl | rfl | rfl <;> decide
  · intro i hi hm
    have h : i = 1 := by omega
    subst i
    decide

theorem left_canonical : Canonical 917 leftDigits 3 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  unfold leftDigits
  split <;> (try split) <;> omega

theorem right_canonical : Canonical 908 rightDigits 3 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  unfold rightDigits
  split <;> (try split) <;> omega

theorem left_realization : ∀ i, i < 3 → columnSum leftDigits 3 i = leftWord i := by
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 := by omega
  rcases h with rfl | rfl | rfl <;> decide

theorem right_realization : ∀ i, i < 3 → columnSum rightDigits 3 i = rightWord i := by
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 := by omega
  rcases h with rfl | rfl | rfl <;> decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 100000000 in
theorem witness_widths : ∀ t : Fin 6, (iterPairs leftWord 3 t.val).1 < 7 := by decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 100000000 in
theorem witness_carry_table : ∀ t : Fin 6, ∀ i : Fin 7,
    i.val ≤ (iterPairs leftWord 3 t.val).1 →
      carry (iterPairs leftWord 3 t.val).2 i.val =
        carry (iterPairs rightWord 3 t.val).2 i.val := by decide

theorem six_equal_carry_words : ∀ t, t < 6 → ∀ i,
    i ≤ (iterPairs leftWord 3 t).1 →
      carry (iterPairs leftWord 3 t).2 i = carry (iterPairs rightWord 3 t).2 i := by
  intro t ht i hi
  have hw := witness_widths ⟨t, ht⟩
  exact witness_carry_table ⟨t, ht⟩ ⟨i, by omega⟩ hi

/-- A valid all-width reconstruction window must contain at least seven
complete carry words. This is not a claim that seven always suffice. -/
theorem reconstruction_requires_seven (k : Nat) (h : ReconstructionWindow k) : 7 ≤ k := by
  by_contra hn
  have hk : k ≤ 6 := by omega
  have he := h leftWord rightWord 3 left_admissible right_admissible
    (fun t ht i hi => six_equal_carry_words t (by omega) i hi)
  have hz : 16 = 17 := he 0 (by decide)
  omega

#print axioms left_admissible
#print axioms right_admissible
#print axioms left_canonical
#print axioms right_canonical
#print axioms left_realization
#print axioms right_realization
#print axioms witness_widths
#print axioms witness_carry_table
#print axioms six_equal_carry_words
#print axioms reconstruction_requires_seven
end Agent121.CarryWindow
