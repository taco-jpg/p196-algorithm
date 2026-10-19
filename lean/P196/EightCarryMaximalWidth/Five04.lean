import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 60 through 79.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_five_04 :
    covered (extensions 5 0 14 ((quadruples.drop 60).take 20)) quintuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 16, 5] ++ [a.val + 5], [18, 0, 15, 8] ++ [a.val + 0]) ||
        !accepted ([18, 0, 16, 5] ++ [a.val + 5], [18, 0, 15, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 0, 16, 14] ++ [a.val + 5], [18, 0, 15, 17] ++ [a.val + 0]) ||
        !accepted ([18, 0, 16, 14] ++ [a.val + 5], [18, 0, 15, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 6, 3] ++ [a.val + 5], [18, 7, 5, 6] ++ [a.val + 0]) ||
        !accepted ([18, 7, 6, 3] ++ [a.val + 5], [18, 7, 5, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 6, 4] ++ [a.val + 5], [18, 7, 5, 7] ++ [a.val + 0]) ||
        !accepted ([18, 7, 6, 4] ++ [a.val + 5], [18, 7, 5, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 6, 12] ++ [a.val + 5], [18, 7, 5, 15] ++ [a.val + 0]) ||
        !accepted ([18, 7, 6, 12] ++ [a.val + 5], [18, 7, 5, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 6, 13] ++ [a.val + 5], [18, 7, 5, 16] ++ [a.val + 0]) ||
        !accepted ([18, 7, 6, 13] ++ [a.val + 5], [18, 7, 5, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 7, 2] ++ [a.val + 5], [18, 7, 6, 5] ++ [a.val + 0]) ||
        !accepted ([18, 7, 7, 2] ++ [a.val + 5], [18, 7, 6, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 7, 11] ++ [a.val + 5], [18, 7, 6, 14] ++ [a.val + 0]) ||
        !accepted ([18, 7, 7, 11] ++ [a.val + 5], [18, 7, 6, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 15, 3] ++ [a.val + 5], [18, 7, 14, 6] ++ [a.val + 0]) ||
        !accepted ([18, 7, 15, 3] ++ [a.val + 5], [18, 7, 14, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 15, 4] ++ [a.val + 5], [18, 7, 14, 7] ++ [a.val + 0]) ||
        !accepted ([18, 7, 15, 4] ++ [a.val + 5], [18, 7, 14, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 15, 12] ++ [a.val + 5], [18, 7, 14, 15] ++ [a.val + 0]) ||
        !accepted ([18, 7, 15, 12] ++ [a.val + 5], [18, 7, 14, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 15, 13] ++ [a.val + 5], [18, 7, 14, 16] ++ [a.val + 0]) ||
        !accepted ([18, 7, 15, 13] ++ [a.val + 5], [18, 7, 14, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 16, 2] ++ [a.val + 5], [18, 7, 15, 5] ++ [a.val + 0]) ||
        !accepted ([18, 7, 16, 2] ++ [a.val + 5], [18, 7, 15, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 7, 16, 11] ++ [a.val + 5], [18, 7, 15, 14] ++ [a.val + 0]) ||
        !accepted ([18, 7, 16, 11] ++ [a.val + 5], [18, 7, 15, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 8, 6] ++ [a.val + 5], [18, 8, 7, 9] ++ [a.val + 0]) ||
        !accepted ([18, 8, 8, 6] ++ [a.val + 5], [18, 8, 7, 9] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 8, 15] ++ [a.val + 5], [18, 8, 7, 18] ++ [a.val + 0]) ||
        !accepted ([18, 8, 8, 15] ++ [a.val + 5], [18, 8, 7, 18] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 9, 2] ++ [a.val + 5], [18, 8, 8, 5] ++ [a.val + 0]) ||
        !accepted ([18, 8, 9, 2] ++ [a.val + 5], [18, 8, 8, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 9, 3] ++ [a.val + 5], [18, 8, 8, 6] ++ [a.val + 0]) ||
        !accepted ([18, 8, 9, 3] ++ [a.val + 5], [18, 8, 8, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 17, 15] ++ [a.val + 5], [18, 8, 16, 18] ++ [a.val + 0]) ||
        !accepted ([18, 8, 17, 15] ++ [a.val + 5], [18, 8, 16, 18] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 18, 2] ++ [a.val + 5], [18, 8, 17, 5] ++ [a.val + 0]) ||
        !accepted ([18, 8, 18, 2] ++ [a.val + 5], [18, 8, 17, 5] ++ [a.val + 0])) = true
    certify_fin14

#print axioms cover_five_04

end EightCarryMaximalWidth.Candidates
