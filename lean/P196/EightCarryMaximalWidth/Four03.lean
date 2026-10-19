import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 40 through 59.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_four_03 :
    covered (extensions 0 3 16 ((triples.drop 40).take 20)) quadruples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 7, 13] ++ [a.val + 0], [14, 7, 12] ++ [a.val + 3]) ||
        !accepted ([14, 7, 13] ++ [a.val + 0], [14, 7, 12] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 7, 16] ++ [a.val + 0], [14, 7, 15] ++ [a.val + 3]) ||
        !accepted ([14, 7, 16] ++ [a.val + 0], [14, 7, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 7, 18] ++ [a.val + 0], [14, 7, 17] ++ [a.val + 3]) ||
        !accepted ([14, 7, 18] ++ [a.val + 0], [14, 7, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 16, 4] ++ [a.val + 0], [14, 16, 3] ++ [a.val + 3]) ||
        !accepted ([14, 16, 4] ++ [a.val + 0], [14, 16, 3] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 16, 7] ++ [a.val + 0], [14, 16, 6] ++ [a.val + 3]) ||
        !accepted ([14, 16, 7] ++ [a.val + 0], [14, 16, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 16, 13] ++ [a.val + 0], [14, 16, 12] ++ [a.val + 3]) ||
        !accepted ([14, 16, 13] ++ [a.val + 0], [14, 16, 12] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 16, 16] ++ [a.val + 0], [14, 16, 15] ++ [a.val + 3]) ||
        !accepted ([14, 16, 16] ++ [a.val + 0], [14, 16, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([14, 16, 18] ++ [a.val + 0], [14, 16, 17] ++ [a.val + 3]) ||
        !accepted ([14, 16, 18] ++ [a.val + 0], [14, 16, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([15, 6, 8] ++ [a.val + 0], [15, 6, 7] ++ [a.val + 3]) ||
        !accepted ([15, 6, 8] ++ [a.val + 0], [15, 6, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([15, 6, 17] ++ [a.val + 0], [15, 6, 16] ++ [a.val + 3]) ||
        !accepted ([15, 6, 17] ++ [a.val + 0], [15, 6, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([15, 15, 8] ++ [a.val + 0], [15, 15, 7] ++ [a.val + 3]) ||
        !accepted ([15, 15, 8] ++ [a.val + 0], [15, 15, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([15, 15, 17] ++ [a.val + 0], [15, 15, 16] ++ [a.val + 3]) ||
        !accepted ([15, 15, 17] ++ [a.val + 0], [15, 15, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 1, 2] ++ [a.val + 0], [17, 1, 1] ++ [a.val + 3]) ||
        !accepted ([17, 1, 2] ++ [a.val + 0], [17, 1, 1] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 1, 4] ++ [a.val + 0], [17, 1, 3] ++ [a.val + 3]) ||
        !accepted ([17, 1, 4] ++ [a.val + 0], [17, 1, 3] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 1, 7] ++ [a.val + 0], [17, 1, 6] ++ [a.val + 3]) ||
        !accepted ([17, 1, 7] ++ [a.val + 0], [17, 1, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 1, 8] ++ [a.val + 0], [17, 1, 7] ++ [a.val + 3]) ||
        !accepted ([17, 1, 8] ++ [a.val + 0], [17, 1, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 1, 11] ++ [a.val + 0], [17, 1, 10] ++ [a.val + 3]) ||
        !accepted ([17, 1, 11] ++ [a.val + 0], [17, 1, 10] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 1, 13] ++ [a.val + 0], [17, 1, 12] ++ [a.val + 3]) ||
        !accepted ([17, 1, 13] ++ [a.val + 0], [17, 1, 12] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 1, 16] ++ [a.val + 0], [17, 1, 15] ++ [a.val + 3]) ||
        !accepted ([17, 1, 16] ++ [a.val + 0], [17, 1, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([17, 1, 17] ++ [a.val + 0], [17, 1, 16] ++ [a.val + 3]) ||
        !accepted ([17, 1, 17] ++ [a.val + 0], [17, 1, 16] ++ [a.val + 3])) = true
    certify_fin16

#print axioms cover_four_03

end EightCarryMaximalWidth.Candidates
