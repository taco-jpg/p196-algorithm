import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 0 through 15.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_six_01 :
    covered (extensions 0 6 13 ((quintuples.drop 0).take 16)) sextuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 16 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 4, 5, 6] ++ [a.val + 0], [13, 6, 3, 8, 1] ++ [a.val + 6]) ||
        !accepted ([13, 6, 4, 5, 6] ++ [a.val + 0], [13, 6, 3, 8, 1] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 4, 5, 9] ++ [a.val + 0], [13, 6, 3, 8, 4] ++ [a.val + 6]) ||
        !accepted ([13, 6, 4, 5, 9] ++ [a.val + 0], [13, 6, 3, 8, 4] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 4, 5, 15] ++ [a.val + 0], [13, 6, 3, 8, 10] ++ [a.val + 6]) ||
        !accepted ([13, 6, 4, 5, 15] ++ [a.val + 0], [13, 6, 3, 8, 10] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 4, 5, 18] ++ [a.val + 0], [13, 6, 3, 8, 13] ++ [a.val + 6]) ||
        !accepted ([13, 6, 4, 5, 18] ++ [a.val + 0], [13, 6, 3, 8, 13] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 4, 14, 6] ++ [a.val + 0], [13, 6, 3, 17, 1] ++ [a.val + 6]) ||
        !accepted ([13, 6, 4, 14, 6] ++ [a.val + 0], [13, 6, 3, 17, 1] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 4, 14, 15] ++ [a.val + 0], [13, 6, 3, 17, 10] ++ [a.val + 6]) ||
        !accepted ([13, 6, 4, 14, 15] ++ [a.val + 0], [13, 6, 3, 17, 10] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 4, 14, 18] ++ [a.val + 0], [13, 6, 3, 17, 13] ++ [a.val + 6]) ||
        !accepted ([13, 6, 4, 14, 18] ++ [a.val + 0], [13, 6, 3, 17, 13] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 13, 5, 6] ++ [a.val + 0], [13, 6, 12, 8, 1] ++ [a.val + 6]) ||
        !accepted ([13, 6, 13, 5, 6] ++ [a.val + 0], [13, 6, 12, 8, 1] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 13, 5, 9] ++ [a.val + 0], [13, 6, 12, 8, 4] ++ [a.val + 6]) ||
        !accepted ([13, 6, 13, 5, 9] ++ [a.val + 0], [13, 6, 12, 8, 4] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 13, 5, 15] ++ [a.val + 0], [13, 6, 12, 8, 10] ++ [a.val + 6]) ||
        !accepted ([13, 6, 13, 5, 15] ++ [a.val + 0], [13, 6, 12, 8, 10] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 13, 5, 18] ++ [a.val + 0], [13, 6, 12, 8, 13] ++ [a.val + 6]) ||
        !accepted ([13, 6, 13, 5, 18] ++ [a.val + 0], [13, 6, 12, 8, 13] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 13, 14, 6] ++ [a.val + 0], [13, 6, 12, 17, 1] ++ [a.val + 6]) ||
        !accepted ([13, 6, 13, 14, 6] ++ [a.val + 0], [13, 6, 12, 17, 1] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 13, 14, 15] ++ [a.val + 0], [13, 6, 12, 17, 10] ++ [a.val + 6]) ||
        !accepted ([13, 6, 13, 14, 15] ++ [a.val + 0], [13, 6, 12, 17, 10] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 6, 13, 14, 18] ++ [a.val + 0], [13, 6, 12, 17, 13] ++ [a.val + 6]) ||
        !accepted ([13, 6, 13, 14, 18] ++ [a.val + 0], [13, 6, 12, 17, 13] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 15, 4, 5, 6] ++ [a.val + 0], [13, 15, 3, 8, 1] ++ [a.val + 6]) ||
        !accepted ([13, 15, 4, 5, 6] ++ [a.val + 0], [13, 15, 3, 8, 1] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([13, 15, 4, 5, 9] ++ [a.val + 0], [13, 15, 3, 8, 4] ++ [a.val + 6]) ||
        !accepted ([13, 15, 4, 5, 9] ++ [a.val + 0], [13, 15, 3, 8, 4] ++ [a.val + 6])) = true
    certify_fin13

#print axioms cover_six_01

end EightCarryMaximalWidth.Candidates
