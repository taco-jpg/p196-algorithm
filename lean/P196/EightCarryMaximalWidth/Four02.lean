import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 20 through 39.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_four_02 :
    covered (extensions 0 3 16 ((triples.drop 20).take 20)) quadruples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 8, 16] ++ [a.val + 0], [13, 8, 15] ++ [a.val + 3]) ||
        !accepted ([13, 8, 16] ++ [a.val + 0], [13, 8, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 8, 18] ++ [a.val + 0], [13, 8, 17] ++ [a.val + 3]) ||
        !accepted ([13, 8, 18] ++ [a.val + 0], [13, 8, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 14, 6] ++ [a.val + 0], [13, 14, 5] ++ [a.val + 3]) ||
        !accepted ([13, 14, 6] ++ [a.val + 0], [13, 14, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 14, 8] ++ [a.val + 0], [13, 14, 7] ++ [a.val + 3]) ||
        !accepted ([13, 14, 8] ++ [a.val + 0], [13, 14, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 14, 15] ++ [a.val + 0], [13, 14, 14] ++ [a.val + 3]) ||
        !accepted ([13, 14, 15] ++ [a.val + 0], [13, 14, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 14, 17] ++ [a.val + 0], [13, 14, 16] ++ [a.val + 3]) ||
        !accepted ([13, 14, 17] ++ [a.val + 0], [13, 14, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 15, 2] ++ [a.val + 0], [13, 15, 1] ++ [a.val + 3]) ||
        !accepted ([13, 15, 2] ++ [a.val + 0], [13, 15, 1] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 15, 4] ++ [a.val + 0], [13, 15, 3] ++ [a.val + 3]) ||
        !accepted ([13, 15, 4] ++ [a.val + 0], [13, 15, 3] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 15, 11] ++ [a.val + 0], [13, 15, 10] ++ [a.val + 3]) ||
        !accepted ([13, 15, 11] ++ [a.val + 0], [13, 15, 10] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 15, 13] ++ [a.val + 0], [13, 15, 12] ++ [a.val + 3]) ||
        !accepted ([13, 15, 13] ++ [a.val + 0], [13, 15, 12] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 17, 3] ++ [a.val + 0], [13, 17, 2] ++ [a.val + 3]) ||
        !accepted ([13, 17, 3] ++ [a.val + 0], [13, 17, 2] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 17, 5] ++ [a.val + 0], [13, 17, 4] ++ [a.val + 3]) ||
        !accepted ([13, 17, 5] ++ [a.val + 0], [13, 17, 4] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 17, 7] ++ [a.val + 0], [13, 17, 6] ++ [a.val + 3]) ||
        !accepted ([13, 17, 7] ++ [a.val + 0], [13, 17, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 17, 12] ++ [a.val + 0], [13, 17, 11] ++ [a.val + 3]) ||
        !accepted ([13, 17, 12] ++ [a.val + 0], [13, 17, 11] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 17, 14] ++ [a.val + 0], [13, 17, 13] ++ [a.val + 3]) ||
        !accepted ([13, 17, 14] ++ [a.val + 0], [13, 17, 13] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 17, 16] ++ [a.val + 0], [13, 17, 15] ++ [a.val + 3]) ||
        !accepted ([13, 17, 16] ++ [a.val + 0], [13, 17, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 17, 18] ++ [a.val + 0], [13, 17, 17] ++ [a.val + 3]) ||
        !accepted ([13, 17, 18] ++ [a.val + 0], [13, 17, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 7, 4] ++ [a.val + 0], [14, 7, 3] ++ [a.val + 3]) ||
        !accepted ([14, 7, 4] ++ [a.val + 0], [14, 7, 3] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 7, 7] ++ [a.val + 0], [14, 7, 6] ++ [a.val + 3]) ||
        !accepted ([14, 7, 7] ++ [a.val + 0], [14, 7, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 7, 9] ++ [a.val + 0], [14, 7, 8] ++ [a.val + 3]) ||
        !accepted ([14, 7, 9] ++ [a.val + 0], [14, 7, 8] ++ [a.val + 3])) = true
    certify_fin16

#print axioms cover_four_02

end EightCarryMaximalWidth.Candidates
