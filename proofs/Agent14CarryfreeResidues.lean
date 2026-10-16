import Std

/-!
# Constructive residue parameters for carry-free decimal witnesses

This Std-only module supplies the arithmetic parameters for Theorem 3 of
`proofs/research/astra_spectral_carry_quotient.md` at source-map commit
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, source blob
`eac5b8f61385a615d9cc3e7796a4d698c66b716b`.

The odd-width parameter construction uses division with remainder. It does
not enumerate the 99 residue pairs. Actual canonical digits, computed
carries, and palindromic successors are proved in separate modules.
-/

namespace Agent14.Carryfree

/-- Every pair of physical odd-width residue classes has the parameters
used in the original three-digit carry-free construction. -/
theorem residue_parameters (s r : Nat) (hs : s < 9) (hr : r < 11) :
    ∃ u b : Nat, 1 ≤ u ∧ u ≤ 10 ∧ b ≤ 9 ∧
      (u + b) % 9 = s ∧ (u + 10 * b) % 11 = r := by
  let t : Nat := (55 * s + 45 * r) % 99
  have ht : t < 99 := by dsimp [t]; omega
  have ht9 : t % 9 = s := by dsimp [t]; omega
  have ht11 : t % 11 = r := by dsimp [t]; omega
  let x : Nat := if t = 0 then 99 else t
  have hx : 1 ≤ x ∧ x ≤ 99 ∧ x % 9 = s ∧ x % 11 = r := by
    by_cases h : t = 0
    · have hs0 : s = 0 := by omega
      have hr0 : r = 0 := by omega
      simp [x, h, hs0, hr0]
    · simp only [x, h, if_false]
      omega
  rcases hx with ⟨hx1, hx99, hx9, hx11⟩
  let u : Nat := (x - 1) % 10 + 1
  let b : Nat := (x - 1) / 10
  have hu1 : 1 ≤ u := by dsimp [u]; omega
  have hu10 : u ≤ 10 := by dsimp [u]; omega
  have hb : b ≤ 9 := by dsimp [b]; omega
  have hvalue : u + 10 * b = x := by dsimp [u, b]; omega
  refine ⟨u, b, hu1, hu10, hb, ?_, ?_⟩
  · omega
  · rw [hvalue]
    exact hx11

/-- Every physical even-width class has a nonzero one-digit parameter. -/
theorem even_residue_parameters (s : Nat) (hs : s < 9) :
    ∃ a : Nat, 1 ≤ a ∧ a ≤ 9 ∧ a % 9 = s := by
  by_cases h : s = 0
  · refine ⟨9, by omega, by omega, ?_⟩
    omega
  · exact ⟨s, by omega, by omega, by omega⟩

/-- The original `AstraModular.ten_pow_mod99` arithmetic lemma, retained
here with its elementary proof to keep this helper independent of the
standalone decimal core. This is a reused supporting fact. -/
theorem ten_pow_mod99 (k : Nat) :
    10 ^ k % 99 = if k % 2 = 0 then 1 else 10 := by
  induction k with
  | zero => decide
  | succ k ih =>
      rw [Nat.pow_succ, Nat.mul_mod, ih]
      by_cases h : k % 2 = 0
      · have hs : (k + 1) % 2 ≠ 0 := by omega
        simp [h, hs]
      · have hs : (k + 1) % 2 = 0 := by omega
        simp [h, hs]

/-- The three high positions of an odd-width witness retain the source
residue `a + 10*b + c`. Coefficient bounds are unnecessary here. -/
theorem odd_three_digit_mod99 (L a b c : Nat)
    (hL : 5 ≤ L) (hodd : L % 2 = 1) :
    (a * 10 ^ (L - 1) + b * 10 ^ (L - 2) + c * 10 ^ (L - 3)) % 99 =
      (a + 10 * b + c) % 99 := by
  have h1 : (L - 1) % 2 = 0 := by omega
  have h2 : (L - 2) % 2 ≠ 0 := by omega
  have h3 : (L - 3) % 2 = 0 := by omega
  have hp1 : 10 ^ (L - 1) % 99 = 1 := by simp [ten_pow_mod99, h1]
  have hp2 : 10 ^ (L - 2) % 99 = 10 := by simp [ten_pow_mod99, h2]
  have hp3 : 10 ^ (L - 3) % 99 = 1 := by simp [ten_pow_mod99, h3]
  have ha : (a * 10 ^ (L - 1)) % 99 = a % 99 := by
    rw [Nat.mul_mod, hp1]
    omega
  have hb : (b * 10 ^ (L - 2)) % 99 = (10 * b) % 99 := by
    rw [Nat.mul_mod b (10 ^ (L - 2)) 99, hp2, Nat.mul_mod 10 b 99]
    omega
  have hc : (c * 10 ^ (L - 3)) % 99 = c % 99 := by
    rw [Nat.mul_mod, hp3]
    omega
  omega

#print axioms residue_parameters
#print axioms even_residue_parameters
#print axioms ten_pow_mod99
#print axioms odd_three_digit_mod99

end Agent14.Carryfree
