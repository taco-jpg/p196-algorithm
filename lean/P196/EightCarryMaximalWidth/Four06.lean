import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 100 through 119.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_four_06 :
    covered (extensions 0 3 16 ((triples.drop 100).take 20)) quadruples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 12] ++ [a.val + 0], [18, 0, 11] ++ [a.val + 3]) ||
        !accepted ([18, 0, 12] ++ [a.val + 0], [18, 0, 11] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 15] ++ [a.val + 0], [18, 0, 14] ++ [a.val + 3]) ||
        !accepted ([18, 0, 15] ++ [a.val + 0], [18, 0, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 16] ++ [a.val + 0], [18, 0, 15] ++ [a.val + 3]) ||
        !accepted ([18, 0, 16] ++ [a.val + 0], [18, 0, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 0, 18] ++ [a.val + 0], [18, 0, 17] ++ [a.val + 3]) ||
        !accepted ([18, 0, 18] ++ [a.val + 0], [18, 0, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 7, 6] ++ [a.val + 0], [18, 7, 5] ++ [a.val + 3]) ||
        !accepted ([18, 7, 6] ++ [a.val + 0], [18, 7, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 7, 7] ++ [a.val + 0], [18, 7, 6] ++ [a.val + 3]) ||
        !accepted ([18, 7, 7] ++ [a.val + 0], [18, 7, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 7, 9] ++ [a.val + 0], [18, 7, 8] ++ [a.val + 3]) ||
        !accepted ([18, 7, 9] ++ [a.val + 0], [18, 7, 8] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 7, 15] ++ [a.val + 0], [18, 7, 14] ++ [a.val + 3]) ||
        !accepted ([18, 7, 15] ++ [a.val + 0], [18, 7, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 7, 16] ++ [a.val + 0], [18, 7, 15] ++ [a.val + 3]) ||
        !accepted ([18, 7, 16] ++ [a.val + 0], [18, 7, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 7, 18] ++ [a.val + 0], [18, 7, 17] ++ [a.val + 3]) ||
        !accepted ([18, 7, 18] ++ [a.val + 0], [18, 7, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 8, 2] ++ [a.val + 0], [18, 8, 1] ++ [a.val + 3]) ||
        !accepted ([18, 8, 2] ++ [a.val + 0], [18, 8, 1] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 8, 6] ++ [a.val + 0], [18, 8, 5] ++ [a.val + 3]) ||
        !accepted ([18, 8, 6] ++ [a.val + 0], [18, 8, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 8, 8] ++ [a.val + 0], [18, 8, 7] ++ [a.val + 3]) ||
        !accepted ([18, 8, 8] ++ [a.val + 0], [18, 8, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 8, 9] ++ [a.val + 0], [18, 8, 8] ++ [a.val + 3]) ||
        !accepted ([18, 8, 9] ++ [a.val + 0], [18, 8, 8] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 8, 11] ++ [a.val + 0], [18, 8, 10] ++ [a.val + 3]) ||
        !accepted ([18, 8, 11] ++ [a.val + 0], [18, 8, 10] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 8, 15] ++ [a.val + 0], [18, 8, 14] ++ [a.val + 3]) ||
        !accepted ([18, 8, 15] ++ [a.val + 0], [18, 8, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 8, 17] ++ [a.val + 0], [18, 8, 16] ++ [a.val + 3]) ||
        !accepted ([18, 8, 17] ++ [a.val + 0], [18, 8, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 8, 18] ++ [a.val + 0], [18, 8, 17] ++ [a.val + 3]) ||
        !accepted ([18, 8, 18] ++ [a.val + 0], [18, 8, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 9, 11] ++ [a.val + 0], [18, 9, 10] ++ [a.val + 3]) ||
        !accepted ([18, 9, 11] ++ [a.val + 0], [18, 9, 10] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 9, 12] ++ [a.val + 0], [18, 9, 11] ++ [a.val + 3]) ||
        !accepted ([18, 9, 12] ++ [a.val + 0], [18, 9, 11] ++ [a.val + 3])) = true
    certify_fin16

#print axioms cover_four_06

end EightCarryMaximalWidth.Candidates
