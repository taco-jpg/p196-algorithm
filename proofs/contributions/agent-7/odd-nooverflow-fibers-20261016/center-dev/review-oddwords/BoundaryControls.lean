import OddWords
open P196.Agent7.OddFibers

-- Empty half-width is allowed in the decomposition; the center is retained.
example {α : Type} (z : α) :
    ∃ xs w, xs.length = 0 ∧ [z] = xs ++ [w] ++ xs.reverse := by
  apply symmetric_odd_decomposition [z] 0 <;> simp

-- Injectivity also applies to two empty half-words without a positivity premise.
example {α : Type} (z w : α) (h : [z] = [w]) :
    ([] : List α) = [] ∧ z = w := by
  apply odd_word_encoding_injective ([] : List α) [] z w
  simpa using h

-- Leading zero coefficients do not remove a symmetric word from the domain.
example : ∃ xs z, xs.length = 1 ∧ [0, 8, 0] = xs ++ [z] ++ xs.reverse := by
  apply symmetric_odd_decomposition [0, 8, 0] 1 <;> decide

#print axioms symmetric_odd_decomposition
#print axioms odd_word_encoding_injective
#print axioms odd_word_center
