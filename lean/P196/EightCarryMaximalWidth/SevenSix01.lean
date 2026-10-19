import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 0 through 16.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_seven_six_01 :
    covered (extensions 6 0 13 ((sextuples.drop 0).take 17)) ([] : List Pair) = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 17 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 7, 2, 9, 0] ++ [a.val + 6], [18, 7, 6, 5, 4, 6] ++ [a.val + 0]) ||
        !accepted ([18, 7, 7, 2, 9, 0] ++ [a.val + 6], [18, 7, 6, 5, 4, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 7, 2, 18, 0] ++ [a.val + 6], [18, 7, 6, 5, 13, 6] ++ [a.val + 0]) ||
        !accepted ([18, 7, 7, 2, 18, 0] ++ [a.val + 6], [18, 7, 6, 5, 13, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 7, 2, 18, 9] ++ [a.val + 6], [18, 7, 6, 5, 13, 15] ++ [a.val + 0]) ||
        !accepted ([18, 7, 7, 2, 18, 9] ++ [a.val + 6], [18, 7, 6, 5, 13, 15] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 7, 11, 18, 0] ++ [a.val + 6], [18, 7, 6, 14, 13, 6] ++ [a.val + 0]) ||
        !accepted ([18, 7, 7, 11, 18, 0] ++ [a.val + 6], [18, 7, 6, 14, 13, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 7, 11, 18, 9] ++ [a.val + 6], [18, 7, 6, 14, 13, 15] ++ [a.val + 0]) ||
        !accepted ([18, 7, 7, 11, 18, 9] ++ [a.val + 6], [18, 7, 6, 14, 13, 15] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 16, 2, 9, 0] ++ [a.val + 6], [18, 7, 15, 5, 4, 6] ++ [a.val + 0]) ||
        !accepted ([18, 7, 16, 2, 9, 0] ++ [a.val + 6], [18, 7, 15, 5, 4, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 16, 2, 18, 0] ++ [a.val + 6], [18, 7, 15, 5, 13, 6] ++ [a.val + 0]) ||
        !accepted ([18, 7, 16, 2, 18, 0] ++ [a.val + 6], [18, 7, 15, 5, 13, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 16, 2, 18, 9] ++ [a.val + 6], [18, 7, 15, 5, 13, 15] ++ [a.val + 0]) ||
        !accepted ([18, 7, 16, 2, 18, 9] ++ [a.val + 6], [18, 7, 15, 5, 13, 15] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 16, 11, 18, 0] ++ [a.val + 6], [18, 7, 15, 14, 13, 6] ++ [a.val + 0]) ||
        !accepted ([18, 7, 16, 11, 18, 0] ++ [a.val + 6], [18, 7, 15, 14, 13, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 7, 16, 11, 18, 9] ++ [a.val + 6], [18, 7, 15, 14, 13, 15] ++ [a.val + 0]) ||
        !accepted ([18, 7, 16, 11, 18, 9] ++ [a.val + 6], [18, 7, 15, 14, 13, 15] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 8, 8, 6, 7, 0] ++ [a.val + 6], [18, 8, 7, 9, 2, 6] ++ [a.val + 0]) ||
        !accepted ([18, 8, 8, 6, 7, 0] ++ [a.val + 6], [18, 8, 7, 9, 2, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 8, 8, 15, 7, 0] ++ [a.val + 6], [18, 8, 7, 18, 2, 6] ++ [a.val + 0]) ||
        !accepted ([18, 8, 8, 15, 7, 0] ++ [a.val + 6], [18, 8, 7, 18, 2, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 8, 8, 15, 16, 0] ++ [a.val + 6], [18, 8, 7, 18, 11, 6] ++ [a.val + 0]) ||
        !accepted ([18, 8, 8, 15, 16, 0] ++ [a.val + 6], [18, 8, 7, 18, 11, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 8, 8, 15, 16, 9] ++ [a.val + 6], [18, 8, 7, 18, 11, 15] ++ [a.val + 0]) ||
        !accepted ([18, 8, 8, 15, 16, 9] ++ [a.val + 6], [18, 8, 7, 18, 11, 15] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 8, 17, 15, 7, 0] ++ [a.val + 6], [18, 8, 16, 18, 2, 6] ++ [a.val + 0]) ||
        !accepted ([18, 8, 17, 15, 7, 0] ++ [a.val + 6], [18, 8, 16, 18, 2, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 8, 17, 15, 16, 0] ++ [a.val + 6], [18, 8, 16, 18, 11, 6] ++ [a.val + 0]) ||
        !accepted ([18, 8, 17, 15, 16, 0] ++ [a.val + 6], [18, 8, 16, 18, 11, 6] ++ [a.val + 0])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (([] : List Pair).contains ([18, 8, 17, 15, 16, 9] ++ [a.val + 6], [18, 8, 16, 18, 11, 15] ++ [a.val + 0]) ||
        !accepted ([18, 8, 17, 15, 16, 9] ++ [a.val + 6], [18, 8, 16, 18, 11, 15] ++ [a.val + 0])) = true
    certify_fin13

#print axioms cover_seven_six_01

end EightCarryMaximalWidth.Candidates
