import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 40 through 59.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_five_03 :
    covered (extensions 5 0 14 ((quadruples.drop 40).take 20)) quintuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 15, 18, 11] ++ [a.val + 5], [17, 15, 17, 14] ++ [a.val + 0]) ||
        !accepted ([17, 15, 18, 11] ++ [a.val + 5], [17, 15, 17, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([17, 15, 18, 15] ++ [a.val + 5], [17, 15, 17, 18] ++ [a.val + 0]) ||
        !accepted ([17, 15, 18, 15] ++ [a.val + 5], [17, 15, 17, 18] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 2, 3] ++ [a.val + 5], [18, 0, 1, 6] ++ [a.val + 0]) ||
        !accepted ([18, 0, 2, 3] ++ [a.val + 5], [18, 0, 1, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 2, 12] ++ [a.val + 5], [18, 0, 1, 15] ++ [a.val + 0]) ||
        !accepted ([18, 0, 2, 12] ++ [a.val + 5], [18, 0, 1, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 3, 3] ++ [a.val + 5], [18, 0, 2, 6] ++ [a.val + 0]) ||
        !accepted ([18, 0, 3, 3] ++ [a.val + 5], [18, 0, 2, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 3, 4] ++ [a.val + 5], [18, 0, 2, 7] ++ [a.val + 0]) ||
        !accepted ([18, 0, 3, 4] ++ [a.val + 5], [18, 0, 2, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 3, 12] ++ [a.val + 5], [18, 0, 2, 15] ++ [a.val + 0]) ||
        !accepted ([18, 0, 3, 12] ++ [a.val + 5], [18, 0, 2, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 3, 13] ++ [a.val + 5], [18, 0, 2, 16] ++ [a.val + 0]) ||
        !accepted ([18, 0, 3, 13] ++ [a.val + 5], [18, 0, 2, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 6, 4] ++ [a.val + 5], [18, 0, 5, 7] ++ [a.val + 0]) ||
        !accepted ([18, 0, 6, 4] ++ [a.val + 5], [18, 0, 5, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 6, 13] ++ [a.val + 5], [18, 0, 5, 16] ++ [a.val + 0]) ||
        !accepted ([18, 0, 6, 13] ++ [a.val + 5], [18, 0, 5, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 7, 5] ++ [a.val + 5], [18, 0, 6, 8] ++ [a.val + 0]) ||
        !accepted ([18, 0, 7, 5] ++ [a.val + 5], [18, 0, 6, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 7, 14] ++ [a.val + 5], [18, 0, 6, 17] ++ [a.val + 0]) ||
        !accepted ([18, 0, 7, 14] ++ [a.val + 5], [18, 0, 6, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 11, 3] ++ [a.val + 5], [18, 0, 10, 6] ++ [a.val + 0]) ||
        !accepted ([18, 0, 11, 3] ++ [a.val + 5], [18, 0, 10, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 11, 12] ++ [a.val + 5], [18, 0, 10, 15] ++ [a.val + 0]) ||
        !accepted ([18, 0, 11, 12] ++ [a.val + 5], [18, 0, 10, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 12, 3] ++ [a.val + 5], [18, 0, 11, 6] ++ [a.val + 0]) ||
        !accepted ([18, 0, 12, 3] ++ [a.val + 5], [18, 0, 11, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 12, 4] ++ [a.val + 5], [18, 0, 11, 7] ++ [a.val + 0]) ||
        !accepted ([18, 0, 12, 4] ++ [a.val + 5], [18, 0, 11, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 12, 12] ++ [a.val + 5], [18, 0, 11, 15] ++ [a.val + 0]) ||
        !accepted ([18, 0, 12, 12] ++ [a.val + 5], [18, 0, 11, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 12, 13] ++ [a.val + 5], [18, 0, 11, 16] ++ [a.val + 0]) ||
        !accepted ([18, 0, 12, 13] ++ [a.val + 5], [18, 0, 11, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 15, 4] ++ [a.val + 5], [18, 0, 14, 7] ++ [a.val + 0]) ||
        !accepted ([18, 0, 15, 4] ++ [a.val + 5], [18, 0, 14, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 15, 13] ++ [a.val + 5], [18, 0, 14, 16] ++ [a.val + 0]) ||
        !accepted ([18, 0, 15, 13] ++ [a.val + 5], [18, 0, 14, 16] ++ [a.val + 0])) = true
    certify_fin14

#print axioms cover_five_03

end EightCarryMaximalWidth.Candidates
