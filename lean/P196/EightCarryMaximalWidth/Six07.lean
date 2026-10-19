import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 96 through 111.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_six_07 :
    covered (extensions 0 6 13 ((quintuples.drop 96).take 16)) sextuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 16 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 9, 3, 17] ++ [a.val + 0], [18, 8, 8, 6, 12] ++ [a.val + 6]) ||
        !accepted ([18, 8, 9, 3, 17] ++ [a.val + 0], [18, 8, 8, 6, 12] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 17, 15, 7] ++ [a.val + 0], [18, 8, 16, 18, 2] ++ [a.val + 6]) ||
        !accepted ([18, 8, 17, 15, 7] ++ [a.val + 0], [18, 8, 16, 18, 2] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 17, 15, 16] ++ [a.val + 0], [18, 8, 16, 18, 11] ++ [a.val + 6]) ||
        !accepted ([18, 8, 17, 15, 16] ++ [a.val + 0], [18, 8, 16, 18, 11] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 18, 2, 5] ++ [a.val + 0], [18, 8, 17, 5, 0] ++ [a.val + 6]) ||
        !accepted ([18, 8, 18, 2, 5] ++ [a.val + 0], [18, 8, 17, 5, 0] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 18, 3, 8] ++ [a.val + 0], [18, 8, 17, 6, 3] ++ [a.val + 6]) ||
        !accepted ([18, 8, 18, 3, 8] ++ [a.val + 0], [18, 8, 17, 6, 3] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 18, 3, 17] ++ [a.val + 0], [18, 8, 17, 6, 12] ++ [a.val + 6]) ||
        !accepted ([18, 8, 18, 3, 17] ++ [a.val + 0], [18, 8, 17, 6, 12] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 18, 11, 5] ++ [a.val + 0], [18, 8, 17, 14, 0] ++ [a.val + 6]) ||
        !accepted ([18, 8, 18, 11, 5] ++ [a.val + 0], [18, 8, 17, 14, 0] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 18, 11, 14] ++ [a.val + 0], [18, 8, 17, 14, 9] ++ [a.val + 6]) ||
        !accepted ([18, 8, 18, 11, 14] ++ [a.val + 0], [18, 8, 17, 14, 9] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 18, 12, 8] ++ [a.val + 0], [18, 8, 17, 15, 3] ++ [a.val + 6]) ||
        !accepted ([18, 8, 18, 12, 8] ++ [a.val + 0], [18, 8, 17, 15, 3] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 8, 18, 12, 17] ++ [a.val + 0], [18, 8, 17, 15, 12] ++ [a.val + 6]) ||
        !accepted ([18, 8, 18, 12, 17] ++ [a.val + 0], [18, 8, 17, 15, 12] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 9, 15, 4, 8] ++ [a.val + 0], [18, 9, 14, 7, 3] ++ [a.val + 6]) ||
        !accepted ([18, 9, 15, 4, 8] ++ [a.val + 0], [18, 9, 14, 7, 3] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 9, 15, 4, 17] ++ [a.val + 0], [18, 9, 14, 7, 12] ++ [a.val + 6]) ||
        !accepted ([18, 9, 15, 4, 17] ++ [a.val + 0], [18, 9, 14, 7, 12] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 9, 15, 13, 8] ++ [a.val + 0], [18, 9, 14, 16, 3] ++ [a.val + 6]) ||
        !accepted ([18, 9, 15, 13, 8] ++ [a.val + 0], [18, 9, 14, 16, 3] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 9, 15, 13, 17] ++ [a.val + 0], [18, 9, 14, 16, 12] ++ [a.val + 6]) ||
        !accepted ([18, 9, 15, 13, 17] ++ [a.val + 0], [18, 9, 14, 16, 12] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 16, 7, 2, 9] ++ [a.val + 0], [18, 16, 6, 5, 4] ++ [a.val + 6]) ||
        !accepted ([18, 16, 7, 2, 9] ++ [a.val + 0], [18, 16, 6, 5, 4] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([18, 16, 7, 2, 18] ++ [a.val + 0], [18, 16, 6, 5, 13] ++ [a.val + 6]) ||
        !accepted ([18, 16, 7, 2, 18] ++ [a.val + 0], [18, 16, 6, 5, 13] ++ [a.val + 6])) = true
    certify_fin13

#print axioms cover_six_07

end EightCarryMaximalWidth.Candidates
