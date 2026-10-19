import P196.OddPredecessorTargetSparsity.Counts

/-!
# Quadratic sparsity at decimal cutoffs

Agent #6: the exact cumulative counts give a uniform quadratic bound.
Squaring their linear estimates and cancelling the positive factor
eighty-one leaves a fixed numerical comparison at each width parity.
-/

set_option autoImplicit false

namespace OddPredecessorTargetSparsity

private theorem quadratic_of_count
    (S c k m : Nat) (hcount : 9 * S + 29 = c * 10 ^ k)
    (hconstant : c ^ 2 ≤ 81 * 5 * 10 ^ m) :
    S ^ 2 ≤ 5 * 10 ^ (2 * k + m) := by
  have hlinear : 9 * S ≤ c * 10 ^ k := by omega
  have hsquare := Nat.pow_le_pow_left hlinear 2
  simp only [Nat.mul_pow] at hsquare
  have hnine : (9 : Nat) ^ 2 = 81 := by decide
  rw [hnine] at hsquare
  have hscaled := Nat.mul_le_mul_right ((10 ^ k) ^ 2) hconstant
  have hbound : 81 * S ^ 2 ≤ 81 * (5 * 10 ^ (2 * k + m)) := by
    calc
      81 * S ^ 2 ≤ c ^ 2 * (10 ^ k) ^ 2 := hsquare
      _ ≤ (81 * 5 * 10 ^ m) * (10 ^ k) ^ 2 := hscaled
      _ = 81 * (5 * 10 ^ (2 * k + m)) := by
        rw [Nat.pow_add 10 (2 * k) m, Nat.pow_mul' 10 2 k]
        simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
  exact Nat.le_of_mul_le_mul_left hbound (by decide)

/-- The number of positive targets below a decimal power with odd complete
predecessor cardinality has square at most five times that cutoff. -/
theorem belowPower_quadratic (W : Nat) :
    (belowPower W).length ^ 2 ≤ 5 * 10 ^ W := by
  match W with
  | 0 => rw [length_belowPower_zero]; decide
  | 1 => rw [length_belowPower_one]; decide
  | 2 => rw [length_belowPower_two]; decide
  | n + 3 =>
    rcases Nat.mod_two_eq_zero_or_one n with heven | hodd
    · have hindex : n + 3 = 2 * (n / 2) + 3 := by omega
      rw [hindex]
      exact quadratic_of_count _ 605 (n / 2) 3
        (belowPower_count_odd (n / 2)) (by decide)
    · have hindex : n + 3 = 2 * ((n - 1) / 2) + 4 := by omega
      rw [hindex]
      exact quadratic_of_count _ 1505 ((n - 1) / 2) 4
        (belowPower_count_even ((n - 1) / 2)) (by decide)

/-- The integer constant four already fails at the three-digit cutoff,
so the uniform integer constant five cannot be decreased. -/
theorem belowPower_four_fails :
    ¬ ∀ W : Nat, (belowPower W).length ^ 2 ≤ 4 * 10 ^ W := by
  intro h
  have hthree := h 3
  rw [length_belowPower_three] at hthree
  exact (by decide : ¬ ((64 : Nat) ^ 2 ≤ 4 * 10 ^ 3)) hthree

#print axioms belowPower_quadratic
#print axioms belowPower_four_fails

end OddPredecessorTargetSparsity
