import P196.EightCarryMaximalWidth.CertificateTools

/-!
Complete extension coverage for parent positions 120 through 139.
Each literal coefficient pair is checked separately by the kernel.
-/

set_option maxHeartbeats 0
set_option maxRecDepth 100000

namespace EightCarryMaximalWidth.Candidates

theorem cover_four_07 :
    covered (extensions 0 3 16 ((triples.drop 120).take 20)) quadruples = true := by
  apply extensions_cover_of_indices
  intro i
  rcases i with ⟨i, hi⟩
  change i < 20 at hi
  have hiCases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 ∨ i = 8 ∨ i = 9 ∨ i = 10 ∨ i = 11 ∨ i = 12 ∨ i = 13 ∨ i = 14 ∨ i = 15 ∨ i = 16 ∨ i = 17 ∨ i = 18 ∨ i = 19 := by omega
  rcases hiCases with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 9, 15] ++ [a.val + 0], [18, 9, 14] ++ [a.val + 3]) ||
        !accepted ([18, 9, 15] ++ [a.val + 0], [18, 9, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 9, 16] ++ [a.val + 0], [18, 9, 15] ++ [a.val + 3]) ||
        !accepted ([18, 9, 16] ++ [a.val + 0], [18, 9, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 9, 18] ++ [a.val + 0], [18, 9, 17] ++ [a.val + 3]) ||
        !accepted ([18, 9, 18] ++ [a.val + 0], [18, 9, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 16, 6] ++ [a.val + 0], [18, 16, 5] ++ [a.val + 3]) ||
        !accepted ([18, 16, 6] ++ [a.val + 0], [18, 16, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 16, 7] ++ [a.val + 0], [18, 16, 6] ++ [a.val + 3]) ||
        !accepted ([18, 16, 7] ++ [a.val + 0], [18, 16, 6] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 16, 15] ++ [a.val + 0], [18, 16, 14] ++ [a.val + 3]) ||
        !accepted ([18, 16, 15] ++ [a.val + 0], [18, 16, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 16, 16] ++ [a.val + 0], [18, 16, 15] ++ [a.val + 3]) ||
        !accepted ([18, 16, 16] ++ [a.val + 0], [18, 16, 15] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 16, 18] ++ [a.val + 0], [18, 16, 17] ++ [a.val + 3]) ||
        !accepted ([18, 16, 18] ++ [a.val + 0], [18, 16, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 17, 2] ++ [a.val + 0], [18, 17, 1] ++ [a.val + 3]) ||
        !accepted ([18, 17, 2] ++ [a.val + 0], [18, 17, 1] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 17, 6] ++ [a.val + 0], [18, 17, 5] ++ [a.val + 3]) ||
        !accepted ([18, 17, 6] ++ [a.val + 0], [18, 17, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 17, 8] ++ [a.val + 0], [18, 17, 7] ++ [a.val + 3]) ||
        !accepted ([18, 17, 8] ++ [a.val + 0], [18, 17, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 17, 11] ++ [a.val + 0], [18, 17, 10] ++ [a.val + 3]) ||
        !accepted ([18, 17, 11] ++ [a.val + 0], [18, 17, 10] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 17, 15] ++ [a.val + 0], [18, 17, 14] ++ [a.val + 3]) ||
        !accepted ([18, 17, 15] ++ [a.val + 0], [18, 17, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 17, 17] ++ [a.val + 0], [18, 17, 16] ++ [a.val + 3]) ||
        !accepted ([18, 17, 17] ++ [a.val + 0], [18, 17, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 17, 18] ++ [a.val + 0], [18, 17, 17] ++ [a.val + 3]) ||
        !accepted ([18, 17, 18] ++ [a.val + 0], [18, 17, 17] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 18, 6] ++ [a.val + 0], [18, 18, 5] ++ [a.val + 3]) ||
        !accepted ([18, 18, 6] ++ [a.val + 0], [18, 18, 5] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 18, 8] ++ [a.val + 0], [18, 18, 7] ++ [a.val + 3]) ||
        !accepted ([18, 18, 8] ++ [a.val + 0], [18, 18, 7] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 18, 15] ++ [a.val + 0], [18, 18, 14] ++ [a.val + 3]) ||
        !accepted ([18, 18, 15] ++ [a.val + 0], [18, 18, 14] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 18, 17] ++ [a.val + 0], [18, 18, 16] ++ [a.val + 3]) ||
        !accepted ([18, 18, 17] ++ [a.val + 0], [18, 18, 16] ++ [a.val + 3])) = true
    certify_fin16
  · change ∀ a : Fin 16,
      (quadruples.contains ([18, 18, 18] ++ [a.val + 0], [18, 18, 17] ++ [a.val + 3]) ||
        !accepted ([18, 18, 18] ++ [a.val + 0], [18, 18, 17] ++ [a.val + 3])) = true
    certify_fin16

#print axioms cover_four_07

end EightCarryMaximalWidth.Candidates
