import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 100 through 119.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_five_06 :
    covered (extensions 5 0 14 ((quadruples.drop 100).take 20)) quintuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 15, 4] ++ [a.val + 5], [18, 16, 14, 7] ++ [a.val + 0]) ||
        !accepted ([18, 16, 15, 4] ++ [a.val + 5], [18, 16, 14, 7] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 15, 12] ++ [a.val + 5], [18, 16, 14, 15] ++ [a.val + 0]) ||
        !accepted ([18, 16, 15, 12] ++ [a.val + 5], [18, 16, 14, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 15, 13] ++ [a.val + 5], [18, 16, 14, 16] ++ [a.val + 0]) ||
        !accepted ([18, 16, 15, 13] ++ [a.val + 5], [18, 16, 14, 16] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 16, 2] ++ [a.val + 5], [18, 16, 15, 5] ++ [a.val + 0]) ||
        !accepted ([18, 16, 16, 2] ++ [a.val + 5], [18, 16, 15, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 16, 16, 11] ++ [a.val + 5], [18, 16, 15, 14] ++ [a.val + 0]) ||
        !accepted ([18, 16, 16, 11] ++ [a.val + 5], [18, 16, 15, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 17, 8, 6] ++ [a.val + 5], [18, 17, 7, 9] ++ [a.val + 0]) ||
        !accepted ([18, 17, 8, 6] ++ [a.val + 5], [18, 17, 7, 9] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 17, 8, 15] ++ [a.val + 5], [18, 17, 7, 18] ++ [a.val + 0]) ||
        !accepted ([18, 17, 8, 15] ++ [a.val + 5], [18, 17, 7, 18] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 17, 17, 15] ++ [a.val + 5], [18, 17, 16, 18] ++ [a.val + 0]) ||
        !accepted ([18, 17, 17, 15] ++ [a.val + 5], [18, 17, 16, 18] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 17, 18, 2] ++ [a.val + 5], [18, 17, 17, 5] ++ [a.val + 0]) ||
        !accepted ([18, 17, 18, 2] ++ [a.val + 5], [18, 17, 17, 5] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 17, 18, 3] ++ [a.val + 5], [18, 17, 17, 6] ++ [a.val + 0]) ||
        !accepted ([18, 17, 18, 3] ++ [a.val + 5], [18, 17, 17, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 17, 18, 11] ++ [a.val + 5], [18, 17, 17, 14] ++ [a.val + 0]) ||
        !accepted ([18, 17, 18, 11] ++ [a.val + 5], [18, 17, 17, 14] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 17, 18, 12] ++ [a.val + 5], [18, 17, 17, 15] ++ [a.val + 0]) ||
        !accepted ([18, 17, 18, 12] ++ [a.val + 5], [18, 17, 17, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 18, 6, 3] ++ [a.val + 5], [18, 18, 5, 6] ++ [a.val + 0]) ||
        !accepted ([18, 18, 6, 3] ++ [a.val + 5], [18, 18, 5, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 18, 6, 12] ++ [a.val + 5], [18, 18, 5, 15] ++ [a.val + 0]) ||
        !accepted ([18, 18, 6, 12] ++ [a.val + 5], [18, 18, 5, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 18, 8, 3] ++ [a.val + 5], [18, 18, 7, 6] ++ [a.val + 0]) ||
        !accepted ([18, 18, 8, 3] ++ [a.val + 5], [18, 18, 7, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 18, 8, 12] ++ [a.val + 5], [18, 18, 7, 15] ++ [a.val + 0]) ||
        !accepted ([18, 18, 8, 12] ++ [a.val + 5], [18, 18, 7, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 18, 15, 3] ++ [a.val + 5], [18, 18, 14, 6] ++ [a.val + 0]) ||
        !accepted ([18, 18, 15, 3] ++ [a.val + 5], [18, 18, 14, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 18, 15, 12] ++ [a.val + 5], [18, 18, 14, 15] ++ [a.val + 0]) ||
        !accepted ([18, 18, 15, 12] ++ [a.val + 5], [18, 18, 14, 15] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 18, 17, 3] ++ [a.val + 5], [18, 18, 16, 6] ++ [a.val + 0]) ||
        !accepted ([18, 18, 17, 3] ++ [a.val + 5], [18, 18, 16, 6] ++ [a.val + 0])) = true
    certify_fin14
  · change ∀ a : Fin 14,
      (quintuples.contains ([18, 18, 17, 12] ++ [a.val + 5], [18, 18, 16, 15] ++ [a.val + 0]) ||
        !accepted ([18, 18, 17, 12] ++ [a.val + 5], [18, 18, 16, 15] ++ [a.val + 0])) = true
    certify_fin14

#print axioms cover_five_06

end EightCarryMaximalWidth.Candidates
