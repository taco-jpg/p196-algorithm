import P196.Drafts.Agent4GeneralBaseNormalization.SharpnessSupport

/-! Agent #4: all representatives of the source's sharp carry class. -/
namespace P196.Agent4.GeneralBase

def sharpCarry (k : Nat) : Nat := if k ≤ 2 then 0 else 1

def sharpPair (b r : Nat) : Nat → Nat
  | 0 => b - 1
  | 1 => b - 1
  | 2 => b + 2 * r
  | 3 => b - 1
  | 4 => b - 1
  | _ => 0

/-- Characterizes every genuine digit word, not only the exhibited witness. -/
theorem sharp_class_pair_characterization (b : Nat) (d : Nat → Nat)
    (hb : 10 ≤ b) (hbe : b % 2 = 0) (hd : CanonicalDigits b 5 d)
    (hc : ∀ k ≤ 5, arithmeticCarry b (pairCoeff 5 d) k = sharpCarry k) :
    ∃ r : Nat, r < b / 2 ∧ ∀ i < 5, pairCoeff 5 d i = sharpPair b r i := by
  have h0 : arithmeticCarry b (pairCoeff 5 d) 0 = 0 := rfl
  have h1 : arithmeticCarry b (pairCoeff 5 d) 1 = 0 := by
    simpa [sharpCarry] using hc 1 (by decide)
  have h2 : arithmeticCarry b (pairCoeff 5 d) 2 = 0 := by
    simpa [sharpCarry] using hc 2 (by decide)
  have h3 : arithmeticCarry b (pairCoeff 5 d) 3 = 1 := by
    simpa [sharpCarry] using hc 3 (by decide)
  have h4 : arithmeticCarry b (pairCoeff 5 d) 4 = 1 := by
    simpa [sharpCarry] using hc 4 (by decide)
  have h5 : arithmeticCarry b (pairCoeff 5 d) 5 = 1 := by
    simpa [sharpCarry] using hc 5 (by decide)
  have c0 := arithmetic_column_bounds b (pairCoeff 5 d) 0 (by omega)
  have c1 := arithmetic_column_bounds b (pairCoeff 5 d) 1 (by omega)
  have c2 := arithmetic_column_bounds b (pairCoeff 5 d) 2 (by omega)
  have c3 := arithmetic_column_bounds b (pairCoeff 5 d) 3 (by omega)
  have c4 := arithmetic_column_bounds b (pairCoeff 5 d) 4 (by omega)
  simp only [h0, h1, h2, h3, h4, h5, Nat.zero_mul, Nat.one_mul,
    Nat.add_zero, Nat.zero_add] at c0 c1 c2 c3 c4
  simp [pairCoeff] at c0 c1 c2 c3 c4
  have hd2 := hd.2.1 2 (by decide)
  have heven := Nat.mod_add_div b 2
  rw [hbe] at heven
  refine ⟨d 2 - b / 2, by omega, ?_⟩
  intro i hi
  have cases5 : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases cases5 with rfl | rfl | rfl | rfl | rfl <;>
    simp [pairCoeff, sharpPair] <;> omega

/-- The same class cannot contain an initial palindrome when the base is even. -/
theorem sharp_class_initial_nonpalindrome (b : Nat) (d : Nat → Nat)
    (hb : 10 ≤ b) (hbe : b % 2 = 0) (hd : CanonicalDigits b 5 d)
    (hc : ∀ k ≤ 5, arithmeticCarry b (pairCoeff 5 d) k = sharpCarry k) :
    reverseAtWidth b 5 (value b d 5) ≠ value b d 5 := by
  obtain ⟨r, _, hpairs⟩ := sharp_class_pair_characterization b d hb hbe hd hc
  have hpair := hpairs 0 (by decide)
  simp [pairCoeff, sharpPair] at hpair
  have heven := Nat.mod_add_div b 2
  rw [hbe] at heven
  apply numeric_nonpalindrome_of_mismatch b 5 d (by omega) hd.2.1 0 (by decide)
  change d 0 ≠ d 4
  intro h
  omega

end P196.Agent4.GeneralBase

#print axioms P196.Agent4.GeneralBase.sharp_class_pair_characterization
#print axioms P196.Agent4.GeneralBase.sharp_class_initial_nonpalindrome
