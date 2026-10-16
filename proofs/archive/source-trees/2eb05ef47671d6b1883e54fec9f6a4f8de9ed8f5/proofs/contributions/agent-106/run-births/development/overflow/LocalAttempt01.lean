import Std

namespace RunBirths.Overflow

theorem adjacent_residues_zero_iff (x y a b d e : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18) (ha : a ≤ 1) (he : e ≤ 1)
    (hb : b = (x + a) / 10) (hd : d = (y + e) / 10) :
    (y + b) % 10 + (x + d) % 10 = 0 ↔
      (x = 0 ∧ y = 0) ∨
      (x = 9 ∧ y = 9 ∧ b = 1 ∧ d = 1) ∨
      (x = 9 ∧ y = 10 ∧ b = 0) ∨
      (x = 10 ∧ y = 9 ∧ d = 0) := by
  omega

theorem adjacent_residues_eighteen_iff (x y a b d e : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18) (ha : a ≤ 1) (he : e ≤ 1)
    (hb : b = (x + a) / 10) (hd : d = (y + e) / 10) :
    (y + b) % 10 + (x + d) % 10 = 18 ↔
      (x = 18 ∧ y = 18) ∨
      (x = 9 ∧ y = 9 ∧ b = 0 ∧ d = 0) ∨
      (x = 9 ∧ y = 8 ∧ b = 1) ∨
      (x = 8 ∧ y = 9 ∧ d = 1) := by
  omega

#print axioms adjacent_residues_zero_iff
#print axioms adjacent_residues_eighteen_iff
end RunBirths.Overflow
