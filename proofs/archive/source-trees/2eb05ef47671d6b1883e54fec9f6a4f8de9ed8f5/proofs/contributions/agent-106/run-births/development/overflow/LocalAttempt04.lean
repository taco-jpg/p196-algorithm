import Std

namespace RunBirths.Overflow

private theorem residue_zero_iff (x a : Nat) (hx : x ≤ 18) (ha : a ≤ 1) :
    (x + a) % 10 = 0 ↔
      (x = 0 ∧ a = 0) ∨ (x = 10 ∧ a = 0) ∨ (x = 9 ∧ a = 1) := by
  have hd : (x + a) / 10 = 0 ∨ (x + a) / 10 = 1 := by omega
  rcases hd with hd | hd <;> omega

private theorem residue_nine_iff (x a : Nat) (hx : x ≤ 18) (ha : a ≤ 1) :
    (x + a) % 10 = 9 ↔
      (x = 9 ∧ a = 0) ∨ (x = 8 ∧ a = 1) ∨ (x = 18 ∧ a = 1) := by
  have hd : (x + a) / 10 = 0 ∨ (x + a) / 10 = 1 := by omega
  rcases hd with hd | hd <;> omega

theorem adjacent_residues_zero_iff (x y a b d e : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18) (ha : a ≤ 1) (he : e ≤ 1)
    (hb : b = (x + a) / 10) (hd : d = (y + e) / 10) :
    (y + b) % 10 + (x + d) % 10 = 0 ↔
      (x = 0 ∧ y = 0) ∨
      (x = 9 ∧ y = 9 ∧ b = 1 ∧ d = 1) ∨
      (x = 9 ∧ y = 10 ∧ b = 0) ∨
      (x = 10 ∧ y = 9 ∧ d = 0) := by
  have hb' : b ≤ 1 := by omega
  have hd' : d ≤ 1 := by omega
  have hz : (y + b) % 10 + (x + d) % 10 = 0 ↔
      (y + b) % 10 = 0 ∧ (x + d) % 10 = 0 := by omega
  rw [hz, residue_zero_iff y b hy hb', residue_zero_iff x d hx hd']
  omega

theorem adjacent_residues_eighteen_iff (x y a b d e : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18) (ha : a ≤ 1) (he : e ≤ 1)
    (hb : b = (x + a) / 10) (hd : d = (y + e) / 10) :
    (y + b) % 10 + (x + d) % 10 = 18 ↔
      (x = 18 ∧ y = 18) ∨
      (x = 9 ∧ y = 9 ∧ b = 0 ∧ d = 0) ∨
      (x = 9 ∧ y = 8 ∧ b = 1) ∨
      (x = 8 ∧ y = 9 ∧ d = 1) := by
  have hb' : b ≤ 1 := by omega
  have hd' : d ≤ 1 := by omega
  have hz : (y + b) % 10 + (x + d) % 10 = 18 ↔
      (y + b) % 10 = 9 ∧ (x + d) % 10 = 9 := by omega
  rw [hz, residue_nine_iff y b hy hb', residue_nine_iff x d hx hd']
  omega

#print axioms adjacent_residues_zero_iff
#print axioms adjacent_residues_eighteen_iff
end RunBirths.Overflow
