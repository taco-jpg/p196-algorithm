import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 60 through 79.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_four_04 :
    covered (extensions 0 3 16 ((triples.drop 60).take 20)) quadruples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 2, 1] ++ [a.val + 0], [17, 2, 0] ++ [a.val + 3]) ||
        !accepted ([17, 2, 1] ++ [a.val + 0], [17, 2, 0] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 2, 3] ++ [a.val + 0], [17, 2, 2] ++ [a.val + 3]) ||
        !accepted ([17, 2, 3] ++ [a.val + 0], [17, 2, 2] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 2, 5] ++ [a.val + 0], [17, 2, 4] ++ [a.val + 3]) ||
        !accepted ([17, 2, 5] ++ [a.val + 0], [17, 2, 4] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 2, 12] ++ [a.val + 0], [17, 2, 11] ++ [a.val + 3]) ||
        !accepted ([17, 2, 12] ++ [a.val + 0], [17, 2, 11] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 2, 14] ++ [a.val + 0], [17, 2, 13] ++ [a.val + 3]) ||
        !accepted ([17, 2, 14] ++ [a.val + 0], [17, 2, 13] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 3, 8] ++ [a.val + 0], [17, 3, 7] ++ [a.val + 3]) ||
        !accepted ([17, 3, 8] ++ [a.val + 0], [17, 3, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 3, 17] ++ [a.val + 0], [17, 3, 16] ++ [a.val + 3]) ||
        !accepted ([17, 3, 17] ++ [a.val + 0], [17, 3, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 4, 6] ++ [a.val + 0], [17, 4, 5] ++ [a.val + 3]) ||
        !accepted ([17, 4, 6] ++ [a.val + 0], [17, 4, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 4, 15] ++ [a.val + 0], [17, 4, 14] ++ [a.val + 3]) ||
        !accepted ([17, 4, 15] ++ [a.val + 0], [17, 4, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 5, 7] ++ [a.val + 0], [17, 5, 6] ++ [a.val + 3]) ||
        !accepted ([17, 5, 7] ++ [a.val + 0], [17, 5, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 5, 16] ++ [a.val + 0], [17, 5, 15] ++ [a.val + 3]) ||
        !accepted ([17, 5, 16] ++ [a.val + 0], [17, 5, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 6, 9] ++ [a.val + 0], [17, 6, 8] ++ [a.val + 3]) ||
        !accepted ([17, 6, 9] ++ [a.val + 0], [17, 6, 8] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 6, 18] ++ [a.val + 0], [17, 6, 17] ++ [a.val + 3]) ||
        !accepted ([17, 6, 18] ++ [a.val + 0], [17, 6, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 10, 2] ++ [a.val + 0], [17, 10, 1] ++ [a.val + 3]) ||
        !accepted ([17, 10, 2] ++ [a.val + 0], [17, 10, 1] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 10, 4] ++ [a.val + 0], [17, 10, 3] ++ [a.val + 3]) ||
        !accepted ([17, 10, 4] ++ [a.val + 0], [17, 10, 3] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 10, 7] ++ [a.val + 0], [17, 10, 6] ++ [a.val + 3]) ||
        !accepted ([17, 10, 7] ++ [a.val + 0], [17, 10, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 10, 8] ++ [a.val + 0], [17, 10, 7] ++ [a.val + 3]) ||
        !accepted ([17, 10, 8] ++ [a.val + 0], [17, 10, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 10, 11] ++ [a.val + 0], [17, 10, 10] ++ [a.val + 3]) ||
        !accepted ([17, 10, 11] ++ [a.val + 0], [17, 10, 10] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 10, 13] ++ [a.val + 0], [17, 10, 12] ++ [a.val + 3]) ||
        !accepted ([17, 10, 13] ++ [a.val + 0], [17, 10, 12] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 10, 16] ++ [a.val + 0], [17, 10, 15] ++ [a.val + 3]) ||
        !accepted ([17, 10, 16] ++ [a.val + 0], [17, 10, 15] ++ [a.val + 3])) = true
    certify_fin16

#print axioms cover_four_04

end EightCarryMaximalWidth.Candidates
