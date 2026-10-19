import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 0 through 19.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_four_01 :
    covered (extensions 0 3 16 ((triples.drop 0).take 20)) quadruples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 16,
      (quadruples.contains ([9, 0, 1] ++ [a.val + 0], [9, 0, 0] ++ [a.val + 3]) ||
        !accepted ([9, 0, 1] ++ [a.val + 0], [9, 0, 0] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([9, 0, 3] ++ [a.val + 0], [9, 0, 2] ++ [a.val + 3]) ||
        !accepted ([9, 0, 3] ++ [a.val + 0], [9, 0, 2] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([9, 0, 6] ++ [a.val + 0], [9, 0, 5] ++ [a.val + 3]) ||
        !accepted ([9, 0, 6] ++ [a.val + 0], [9, 0, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([9, 0, 8] ++ [a.val + 0], [9, 0, 7] ++ [a.val + 3]) ||
        !accepted ([9, 0, 8] ++ [a.val + 0], [9, 0, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([9, 4, 16] ++ [a.val + 0], [9, 4, 15] ++ [a.val + 3]) ||
        !accepted ([9, 4, 16] ++ [a.val + 0], [9, 4, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([9, 4, 18] ++ [a.val + 0], [9, 4, 17] ++ [a.val + 3]) ||
        !accepted ([9, 4, 18] ++ [a.val + 0], [9, 4, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 5, 6] ++ [a.val + 0], [13, 5, 5] ++ [a.val + 3]) ||
        !accepted ([13, 5, 6] ++ [a.val + 0], [13, 5, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 5, 8] ++ [a.val + 0], [13, 5, 7] ++ [a.val + 3]) ||
        !accepted ([13, 5, 8] ++ [a.val + 0], [13, 5, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 5, 15] ++ [a.val + 0], [13, 5, 14] ++ [a.val + 3]) ||
        !accepted ([13, 5, 15] ++ [a.val + 0], [13, 5, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 5, 17] ++ [a.val + 0], [13, 5, 16] ++ [a.val + 3]) ||
        !accepted ([13, 5, 17] ++ [a.val + 0], [13, 5, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 6, 2] ++ [a.val + 0], [13, 6, 1] ++ [a.val + 3]) ||
        !accepted ([13, 6, 2] ++ [a.val + 0], [13, 6, 1] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 6, 4] ++ [a.val + 0], [13, 6, 3] ++ [a.val + 3]) ||
        !accepted ([13, 6, 4] ++ [a.val + 0], [13, 6, 3] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 6, 11] ++ [a.val + 0], [13, 6, 10] ++ [a.val + 3]) ||
        !accepted ([13, 6, 11] ++ [a.val + 0], [13, 6, 10] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 6, 13] ++ [a.val + 0], [13, 6, 12] ++ [a.val + 3]) ||
        !accepted ([13, 6, 13] ++ [a.val + 0], [13, 6, 12] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 8, 3] ++ [a.val + 0], [13, 8, 2] ++ [a.val + 3]) ||
        !accepted ([13, 8, 3] ++ [a.val + 0], [13, 8, 2] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 8, 5] ++ [a.val + 0], [13, 8, 4] ++ [a.val + 3]) ||
        !accepted ([13, 8, 5] ++ [a.val + 0], [13, 8, 4] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 8, 7] ++ [a.val + 0], [13, 8, 6] ++ [a.val + 3]) ||
        !accepted ([13, 8, 7] ++ [a.val + 0], [13, 8, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 8, 9] ++ [a.val + 0], [13, 8, 8] ++ [a.val + 3]) ||
        !accepted ([13, 8, 9] ++ [a.val + 0], [13, 8, 8] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 8, 12] ++ [a.val + 0], [13, 8, 11] ++ [a.val + 3]) ||
        !accepted ([13, 8, 12] ++ [a.val + 0], [13, 8, 11] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([13, 8, 14] ++ [a.val + 0], [13, 8, 13] ++ [a.val + 3]) ||
        !accepted ([13, 8, 14] ++ [a.val + 0], [13, 8, 13] ++ [a.val + 3])) = true
    certify_fin16

#print axioms cover_four_01

end EightCarryMaximalWidth.Candidates
