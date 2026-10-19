import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 80 through 99.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_four_05 :
    covered (extensions 0 3 16 ((triples.drop 80).take 20)) quadruples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 10, 17] ++ [a.val + 0], [17, 10, 16] ++ [a.val + 3]) ||
        !accepted ([17, 10, 17] ++ [a.val + 0], [17, 10, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 11, 1] ++ [a.val + 0], [17, 11, 0] ++ [a.val + 3]) ||
        !accepted ([17, 11, 1] ++ [a.val + 0], [17, 11, 0] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 11, 3] ++ [a.val + 0], [17, 11, 2] ++ [a.val + 3]) ||
        !accepted ([17, 11, 3] ++ [a.val + 0], [17, 11, 2] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 11, 5] ++ [a.val + 0], [17, 11, 4] ++ [a.val + 3]) ||
        !accepted ([17, 11, 5] ++ [a.val + 0], [17, 11, 4] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 11, 10] ++ [a.val + 0], [17, 11, 9] ++ [a.val + 3]) ||
        !accepted ([17, 11, 10] ++ [a.val + 0], [17, 11, 9] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 11, 12] ++ [a.val + 0], [17, 11, 11] ++ [a.val + 3]) ||
        !accepted ([17, 11, 12] ++ [a.val + 0], [17, 11, 11] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 11, 14] ++ [a.val + 0], [17, 11, 13] ++ [a.val + 3]) ||
        !accepted ([17, 11, 14] ++ [a.val + 0], [17, 11, 13] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 12, 8] ++ [a.val + 0], [17, 12, 7] ++ [a.val + 3]) ||
        !accepted ([17, 12, 8] ++ [a.val + 0], [17, 12, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 12, 17] ++ [a.val + 0], [17, 12, 16] ++ [a.val + 3]) ||
        !accepted ([17, 12, 17] ++ [a.val + 0], [17, 12, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 13, 6] ++ [a.val + 0], [17, 13, 5] ++ [a.val + 3]) ||
        !accepted ([17, 13, 6] ++ [a.val + 0], [17, 13, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 13, 15] ++ [a.val + 0], [17, 13, 14] ++ [a.val + 3]) ||
        !accepted ([17, 13, 15] ++ [a.val + 0], [17, 13, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 14, 7] ++ [a.val + 0], [17, 14, 6] ++ [a.val + 3]) ||
        !accepted ([17, 14, 7] ++ [a.val + 0], [17, 14, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 14, 16] ++ [a.val + 0], [17, 14, 15] ++ [a.val + 3]) ||
        !accepted ([17, 14, 16] ++ [a.val + 0], [17, 14, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 15, 18] ++ [a.val + 0], [17, 15, 17] ++ [a.val + 3]) ||
        !accepted ([17, 15, 18] ++ [a.val + 0], [17, 15, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 2] ++ [a.val + 0], [18, 0, 1] ++ [a.val + 3]) ||
        !accepted ([18, 0, 2] ++ [a.val + 0], [18, 0, 1] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 3] ++ [a.val + 0], [18, 0, 2] ++ [a.val + 3]) ||
        !accepted ([18, 0, 3] ++ [a.val + 0], [18, 0, 2] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 6] ++ [a.val + 0], [18, 0, 5] ++ [a.val + 3]) ||
        !accepted ([18, 0, 6] ++ [a.val + 0], [18, 0, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 7] ++ [a.val + 0], [18, 0, 6] ++ [a.val + 3]) ||
        !accepted ([18, 0, 7] ++ [a.val + 0], [18, 0, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 9] ++ [a.val + 0], [18, 0, 8] ++ [a.val + 3]) ||
        !accepted ([18, 0, 9] ++ [a.val + 0], [18, 0, 8] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 11] ++ [a.val + 0], [18, 0, 10] ++ [a.val + 3]) ||
        !accepted ([18, 0, 11] ++ [a.val + 0], [18, 0, 10] ++ [a.val + 3])) = true
    certify_fin16

#print axioms cover_four_05

end EightCarryMaximalWidth.Candidates
