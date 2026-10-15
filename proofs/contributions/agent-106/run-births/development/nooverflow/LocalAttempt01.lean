import Std

namespace RunBirths.NoOverflow

theorem residues_eighteen_iff (x a b : Nat)
    (hx : x ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    (x + a) % 10 + (x + b) % 10 = 18 ↔
      ((x = 8 ∨ x = 18) ∧ a + b = 2) ∨ (x = 9 ∧ a + b = 0) := by
  omega

theorem residues_zero_iff (x a b : Nat)
    (hx : x ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    (x + a) % 10 + (x + b) % 10 = 0 ↔
      ((x = 0 ∨ x = 10) ∧ a + b = 0) ∨ (x = 9 ∧ a + b = 2) := by
  omega

#print axioms residues_eighteen_iff
#print axioms residues_zero_iff
end RunBirths.NoOverflow
