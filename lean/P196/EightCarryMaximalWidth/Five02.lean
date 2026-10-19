import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 20 through 39.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_five_02 :
    covered (extensions 5 0 14 ((quadruples.drop 20).take 20)) quintuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 3, 8, 2] ++ [a.val + 5], [17, 3, 7, 5] ++ [a.val + 0]) ||
        !accepted ([17, 3, 8, 2] ++ [a.val + 5], [17, 3, 7, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 3, 8, 11] ++ [a.val + 5], [17, 3, 7, 14] ++ [a.val + 0]) ||
        !accepted ([17, 3, 8, 11] ++ [a.val + 5], [17, 3, 7, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 3, 17, 2] ++ [a.val + 5], [17, 3, 16, 5] ++ [a.val + 0]) ||
        !accepted ([17, 3, 17, 2] ++ [a.val + 5], [17, 3, 16, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 3, 17, 11] ++ [a.val + 5], [17, 3, 16, 14] ++ [a.val + 0]) ||
        !accepted ([17, 3, 17, 11] ++ [a.val + 5], [17, 3, 16, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 6, 9, 2] ++ [a.val + 5], [17, 6, 8, 5] ++ [a.val + 0]) ||
        !accepted ([17, 6, 9, 2] ++ [a.val + 5], [17, 6, 8, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 6, 9, 6] ++ [a.val + 5], [17, 6, 8, 9] ++ [a.val + 0]) ||
        !accepted ([17, 6, 9, 6] ++ [a.val + 5], [17, 6, 8, 9] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 6, 18, 2] ++ [a.val + 5], [17, 6, 17, 5] ++ [a.val + 0]) ||
        !accepted ([17, 6, 18, 2] ++ [a.val + 5], [17, 6, 17, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 6, 18, 11] ++ [a.val + 5], [17, 6, 17, 14] ++ [a.val + 0]) ||
        !accepted ([17, 6, 18, 11] ++ [a.val + 5], [17, 6, 17, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 6, 18, 15] ++ [a.val + 5], [17, 6, 17, 18] ++ [a.val + 0]) ||
        !accepted ([17, 6, 18, 15] ++ [a.val + 5], [17, 6, 17, 18] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 11, 1, 1] ++ [a.val + 5], [17, 11, 0, 4] ++ [a.val + 0]) ||
        !accepted ([17, 11, 1, 1] ++ [a.val + 5], [17, 11, 0, 4] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 11, 1, 5] ++ [a.val + 5], [17, 11, 0, 8] ++ [a.val + 0]) ||
        !accepted ([17, 11, 1, 5] ++ [a.val + 5], [17, 11, 0, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 11, 1, 10] ++ [a.val + 5], [17, 11, 0, 13] ++ [a.val + 0]) ||
        !accepted ([17, 11, 1, 10] ++ [a.val + 5], [17, 11, 0, 13] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 11, 1, 14] ++ [a.val + 5], [17, 11, 0, 17] ++ [a.val + 0]) ||
        !accepted ([17, 11, 1, 14] ++ [a.val + 5], [17, 11, 0, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 11, 10, 10] ++ [a.val + 5], [17, 11, 9, 13] ++ [a.val + 0]) ||
        !accepted ([17, 11, 10, 10] ++ [a.val + 5], [17, 11, 9, 13] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 11, 10, 14] ++ [a.val + 5], [17, 11, 9, 17] ++ [a.val + 0]) ||
        !accepted ([17, 11, 10, 14] ++ [a.val + 5], [17, 11, 9, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 12, 8, 2] ++ [a.val + 5], [17, 12, 7, 5] ++ [a.val + 0]) ||
        !accepted ([17, 12, 8, 2] ++ [a.val + 5], [17, 12, 7, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 12, 8, 11] ++ [a.val + 5], [17, 12, 7, 14] ++ [a.val + 0]) ||
        !accepted ([17, 12, 8, 11] ++ [a.val + 5], [17, 12, 7, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 12, 17, 2] ++ [a.val + 5], [17, 12, 16, 5] ++ [a.val + 0]) ||
        !accepted ([17, 12, 17, 2] ++ [a.val + 5], [17, 12, 16, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 12, 17, 11] ++ [a.val + 5], [17, 12, 16, 14] ++ [a.val + 0]) ||
        !accepted ([17, 12, 17, 11] ++ [a.val + 5], [17, 12, 16, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 15, 18, 2] ++ [a.val + 5], [17, 15, 17, 5] ++ [a.val + 0]) ||
        !accepted ([17, 15, 18, 2] ++ [a.val + 5], [17, 15, 17, 5] ++ [a.val + 0])) = true
    certify_fin14

#print axioms cover_five_02

end EightCarryMaximalWidth.Candidates
