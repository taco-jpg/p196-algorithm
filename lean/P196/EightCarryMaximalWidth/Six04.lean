import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 48 through 63.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_six_04 :
    covered (extensions 0 6 13 ((quintuples.drop 48).take 16)) sextuples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 16 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 2, 1, 10, 16] ++ [a.val + 0], [17, 2, 0, 13, 11] ++ [a.val + 6]) ||
        !accepted ([17, 2, 1, 10, 16] ++ [a.val + 0], [17, 2, 0, 13, 11] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 2, 1, 10, 17] ++ [a.val + 0], [17, 2, 0, 13, 12] ++ [a.val + 6]) ||
        !accepted ([17, 2, 1, 10, 17] ++ [a.val + 0], [17, 2, 0, 13, 12] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 2, 1, 14, 18] ++ [a.val + 0], [17, 2, 0, 17, 13] ++ [a.val + 6]) ||
        !accepted ([17, 2, 1, 14, 18] ++ [a.val + 0], [17, 2, 0, 17, 13] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 6, 9, 6, 5] ++ [a.val + 0], [17, 6, 8, 9, 0] ++ [a.val + 6]) ||
        !accepted ([17, 6, 9, 6, 5] ++ [a.val + 0], [17, 6, 8, 9, 0] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 6, 9, 6, 6] ++ [a.val + 0], [17, 6, 8, 9, 1] ++ [a.val + 6]) ||
        !accepted ([17, 6, 9, 6, 6] ++ [a.val + 0], [17, 6, 8, 9, 1] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 6, 18, 15, 5] ++ [a.val + 0], [17, 6, 17, 18, 0] ++ [a.val + 6]) ||
        !accepted ([17, 6, 18, 15, 5] ++ [a.val + 0], [17, 6, 17, 18, 0] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 6, 18, 15, 6] ++ [a.val + 0], [17, 6, 17, 18, 1] ++ [a.val + 6]) ||
        !accepted ([17, 6, 18, 15, 6] ++ [a.val + 0], [17, 6, 17, 18, 1] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 6, 18, 15, 14] ++ [a.val + 0], [17, 6, 17, 18, 9] ++ [a.val + 6]) ||
        !accepted ([17, 6, 18, 15, 14] ++ [a.val + 0], [17, 6, 17, 18, 9] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 6, 18, 15, 15] ++ [a.val + 0], [17, 6, 17, 18, 10] ++ [a.val + 6]) ||
        !accepted ([17, 6, 18, 15, 15] ++ [a.val + 0], [17, 6, 17, 18, 10] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 11, 1, 1, 7] ++ [a.val + 0], [17, 11, 0, 4, 2] ++ [a.val + 6]) ||
        !accepted ([17, 11, 1, 1, 7] ++ [a.val + 0], [17, 11, 0, 4, 2] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 11, 1, 1, 8] ++ [a.val + 0], [17, 11, 0, 4, 3] ++ [a.val + 6]) ||
        !accepted ([17, 11, 1, 1, 8] ++ [a.val + 0], [17, 11, 0, 4, 3] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 11, 1, 1, 16] ++ [a.val + 0], [17, 11, 0, 4, 11] ++ [a.val + 6]) ||
        !accepted ([17, 11, 1, 1, 16] ++ [a.val + 0], [17, 11, 0, 4, 11] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 11, 1, 1, 17] ++ [a.val + 0], [17, 11, 0, 4, 12] ++ [a.val + 6]) ||
        !accepted ([17, 11, 1, 1, 17] ++ [a.val + 0], [17, 11, 0, 4, 12] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 11, 1, 5, 9] ++ [a.val + 0], [17, 11, 0, 8, 4] ++ [a.val + 6]) ||
        !accepted ([17, 11, 1, 5, 9] ++ [a.val + 0], [17, 11, 0, 8, 4] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 11, 1, 5, 18] ++ [a.val + 0], [17, 11, 0, 8, 13] ++ [a.val + 6]) ||
        !accepted ([17, 11, 1, 5, 18] ++ [a.val + 0], [17, 11, 0, 8, 13] ++ [a.val + 6])) = true
    certify_fin13
  · change ∀ a : Fin 13,
      (sextuples.contains ([17, 11, 1, 10, 7] ++ [a.val + 0], [17, 11, 0, 13, 2] ++ [a.val + 6]) ||
        !accepted ([17, 11, 1, 10, 7] ++ [a.val + 0], [17, 11, 0, 13, 2] ++ [a.val + 6])) = true
    certify_fin13

#print axioms cover_six_04

end EightCarryMaximalWidth.Candidates
