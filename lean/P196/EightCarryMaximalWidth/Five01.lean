import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 0 through 19.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_five_01 :
    covered (extensions 5 0 14 ((quadruples.drop 0).take 20)) quintuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 14,
      (quintuples.contains ([13, 6, 4, 5] ++ [a.val + 5], [13, 6, 3, 8] ++ [a.val + 0]) ||
        !accepted ([13, 6, 4, 5] ++ [a.val + 5], [13, 6, 3, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([13, 6, 4, 14] ++ [a.val + 5], [13, 6, 3, 17] ++ [a.val + 0]) ||
        !accepted ([13, 6, 4, 14] ++ [a.val + 5], [13, 6, 3, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([13, 6, 13, 5] ++ [a.val + 5], [13, 6, 12, 8] ++ [a.val + 0]) ||
        !accepted ([13, 6, 13, 5] ++ [a.val + 5], [13, 6, 12, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([13, 6, 13, 14] ++ [a.val + 5], [13, 6, 12, 17] ++ [a.val + 0]) ||
        !accepted ([13, 6, 13, 14] ++ [a.val + 5], [13, 6, 12, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([13, 15, 4, 5] ++ [a.val + 5], [13, 15, 3, 8] ++ [a.val + 0]) ||
        !accepted ([13, 15, 4, 5] ++ [a.val + 5], [13, 15, 3, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([13, 15, 4, 14] ++ [a.val + 5], [13, 15, 3, 17] ++ [a.val + 0]) ||
        !accepted ([13, 15, 4, 14] ++ [a.val + 5], [13, 15, 3, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([13, 15, 13, 5] ++ [a.val + 5], [13, 15, 12, 8] ++ [a.val + 0]) ||
        !accepted ([13, 15, 13, 5] ++ [a.val + 5], [13, 15, 12, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([13, 15, 13, 14] ++ [a.val + 5], [13, 15, 12, 17] ++ [a.val + 0]) ||
        !accepted ([13, 15, 13, 14] ++ [a.val + 5], [13, 15, 12, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([14, 7, 4, 5] ++ [a.val + 5], [14, 7, 3, 8] ++ [a.val + 0]) ||
        !accepted ([14, 7, 4, 5] ++ [a.val + 5], [14, 7, 3, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([14, 7, 4, 14] ++ [a.val + 5], [14, 7, 3, 17] ++ [a.val + 0]) ||
        !accepted ([14, 7, 4, 14] ++ [a.val + 5], [14, 7, 3, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([14, 7, 13, 5] ++ [a.val + 5], [14, 7, 12, 8] ++ [a.val + 0]) ||
        !accepted ([14, 7, 13, 5] ++ [a.val + 5], [14, 7, 12, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([14, 7, 13, 14] ++ [a.val + 5], [14, 7, 12, 17] ++ [a.val + 0]) ||
        !accepted ([14, 7, 13, 14] ++ [a.val + 5], [14, 7, 12, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([14, 16, 4, 5] ++ [a.val + 5], [14, 16, 3, 8] ++ [a.val + 0]) ||
        !accepted ([14, 16, 4, 5] ++ [a.val + 5], [14, 16, 3, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([14, 16, 4, 14] ++ [a.val + 5], [14, 16, 3, 17] ++ [a.val + 0]) ||
        !accepted ([14, 16, 4, 14] ++ [a.val + 5], [14, 16, 3, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([14, 16, 13, 5] ++ [a.val + 5], [14, 16, 12, 8] ++ [a.val + 0]) ||
        !accepted ([14, 16, 13, 5] ++ [a.val + 5], [14, 16, 12, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([14, 16, 13, 14] ++ [a.val + 5], [14, 16, 12, 17] ++ [a.val + 0]) ||
        !accepted ([14, 16, 13, 14] ++ [a.val + 5], [14, 16, 12, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 2, 1, 1] ++ [a.val + 5], [17, 2, 0, 4] ++ [a.val + 0]) ||
        !accepted ([17, 2, 1, 1] ++ [a.val + 5], [17, 2, 0, 4] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 2, 1, 5] ++ [a.val + 5], [17, 2, 0, 8] ++ [a.val + 0]) ||
        !accepted ([17, 2, 1, 5] ++ [a.val + 5], [17, 2, 0, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 2, 1, 10] ++ [a.val + 5], [17, 2, 0, 13] ++ [a.val + 0]) ||
        !accepted ([17, 2, 1, 10] ++ [a.val + 5], [17, 2, 0, 13] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 2, 1, 14] ++ [a.val + 5], [17, 2, 0, 17] ++ [a.val + 0]) ||
        !accepted ([17, 2, 1, 14] ++ [a.val + 5], [17, 2, 0, 17] ++ [a.val + 0])) = true
    certify_fin14

#print axioms cover_five_01

end EightCarryMaximalWidth.Candidates
