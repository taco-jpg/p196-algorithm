import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 80 through 99.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_five_05 :
    covered (extensions 5 0 14 ((quadruples.drop 80).take 20)) quintuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 18, 3] ++ [a.val + 5], [18, 8, 17, 6] ++ [a.val + 0]) ||
        !accepted ([18, 8, 18, 3] ++ [a.val + 5], [18, 8, 17, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 18, 11] ++ [a.val + 5], [18, 8, 17, 14] ++ [a.val + 0]) ||
        !accepted ([18, 8, 18, 11] ++ [a.val + 5], [18, 8, 17, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 8, 18, 12] ++ [a.val + 5], [18, 8, 17, 15] ++ [a.val + 0]) ||
        !accepted ([18, 8, 18, 12] ++ [a.val + 5], [18, 8, 17, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 11, 3] ++ [a.val + 5], [18, 9, 10, 6] ++ [a.val + 0]) ||
        !accepted ([18, 9, 11, 3] ++ [a.val + 5], [18, 9, 10, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 11, 12] ++ [a.val + 5], [18, 9, 10, 15] ++ [a.val + 0]) ||
        !accepted ([18, 9, 11, 12] ++ [a.val + 5], [18, 9, 10, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 12, 3] ++ [a.val + 5], [18, 9, 11, 6] ++ [a.val + 0]) ||
        !accepted ([18, 9, 12, 3] ++ [a.val + 5], [18, 9, 11, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 12, 4] ++ [a.val + 5], [18, 9, 11, 7] ++ [a.val + 0]) ||
        !accepted ([18, 9, 12, 4] ++ [a.val + 5], [18, 9, 11, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 12, 12] ++ [a.val + 5], [18, 9, 11, 15] ++ [a.val + 0]) ||
        !accepted ([18, 9, 12, 12] ++ [a.val + 5], [18, 9, 11, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 12, 13] ++ [a.val + 5], [18, 9, 11, 16] ++ [a.val + 0]) ||
        !accepted ([18, 9, 12, 13] ++ [a.val + 5], [18, 9, 11, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 15, 4] ++ [a.val + 5], [18, 9, 14, 7] ++ [a.val + 0]) ||
        !accepted ([18, 9, 15, 4] ++ [a.val + 5], [18, 9, 14, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 15, 13] ++ [a.val + 5], [18, 9, 14, 16] ++ [a.val + 0]) ||
        !accepted ([18, 9, 15, 13] ++ [a.val + 5], [18, 9, 14, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 16, 5] ++ [a.val + 5], [18, 9, 15, 8] ++ [a.val + 0]) ||
        !accepted ([18, 9, 16, 5] ++ [a.val + 5], [18, 9, 15, 8] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 9, 16, 14] ++ [a.val + 5], [18, 9, 15, 17] ++ [a.val + 0]) ||
        !accepted ([18, 9, 16, 14] ++ [a.val + 5], [18, 9, 15, 17] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 6, 3] ++ [a.val + 5], [18, 16, 5, 6] ++ [a.val + 0]) ||
        !accepted ([18, 16, 6, 3] ++ [a.val + 5], [18, 16, 5, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 6, 4] ++ [a.val + 5], [18, 16, 5, 7] ++ [a.val + 0]) ||
        !accepted ([18, 16, 6, 4] ++ [a.val + 5], [18, 16, 5, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 6, 12] ++ [a.val + 5], [18, 16, 5, 15] ++ [a.val + 0]) ||
        !accepted ([18, 16, 6, 12] ++ [a.val + 5], [18, 16, 5, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 6, 13] ++ [a.val + 5], [18, 16, 5, 16] ++ [a.val + 0]) ||
        !accepted ([18, 16, 6, 13] ++ [a.val + 5], [18, 16, 5, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 7, 2] ++ [a.val + 5], [18, 16, 6, 5] ++ [a.val + 0]) ||
        !accepted ([18, 16, 7, 2] ++ [a.val + 5], [18, 16, 6, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 7, 11] ++ [a.val + 5], [18, 16, 6, 14] ++ [a.val + 0]) ||
        !accepted ([18, 16, 7, 11] ++ [a.val + 5], [18, 16, 6, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 15, 3] ++ [a.val + 5], [18, 16, 14, 6] ++ [a.val + 0]) ||
        !accepted ([18, 16, 15, 3] ++ [a.val + 5], [18, 16, 14, 6] ++ [a.val + 0])) = true
    certify_fin14

#print axioms cover_five_05

end EightCarryMaximalWidth.Candidates
