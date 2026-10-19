import P196.Drafts.Agent3TwoHistory.InverseFibers

/-
Agent #9. Rational exponential envelopes for the existing Fibonacci sequence.
The proofs use only natural-number arithmetic and paired induction. The
quadratic hypotheses include all zero-parameter boundary cases; no division,
real algebra, or asymptotic theorem is assumed.
-/
namespace P196.InverseFiberGrowth

open P196.Agent9.InverseFibers

private theorem upper_base (p q : Nat) (h : p * q + q ^ 2 ≤ p ^ 2) :
    q ≤ p := by
  apply Nat.le_of_not_lt
  intro hpq
  have hq : 0 < q := by omega
  have hs : p * p < q * q :=
    Nat.lt_of_le_of_lt (Nat.mul_le_mul_left p (Nat.le_of_lt hpq))
      (Nat.mul_lt_mul_of_pos_right hpq hq)
  have hh : p * q + q * q ≤ p * p := by
    simpa only [Nat.pow_two] using h
  omega

private theorem lower_base (p q : Nat) (h : p ^ 2 ≤ p * q + q ^ 2) :
    p ≤ 2 * q := by
  by_cases hp : p = 0
  · simp [hp]
  by_cases hqp : q ≤ p
  · have hqq : q * q ≤ p * q := Nat.mul_le_mul_right q hqp
    have hh : p * p ≤ p * (q + q) := by
      calc
        p * p ≤ p * q + q * q := by simpa only [Nat.pow_two] using h
        _ ≤ p * q + p * q := Nat.add_le_add_left hqq (p * q)
        _ = p * (q + q) := (Nat.mul_add p q q).symm
    have hb : p ≤ q + q := Nat.le_of_mul_le_mul_left hh (by omega)
    omega
  · omega

private theorem weighted_fib_step (q n k : Nat) :
    q ^ (n + 2) * fib (n + k + 2) =
      q * (q ^ (n + 1) * fib (n + k + 1)) +
      q ^ 2 * (q ^ n * fib (n + k)) := by
  rw [fib_succ_succ (n + k)]
  simp only [Nat.pow_add, Nat.pow_one, Nat.pow_two, Nat.mul_add]
  ac_rfl

/-- An upper quadratic certificate bounds the shifted Fibonacci sequence.
The condition alone implies `q ≤ p`; positive parameters are not required. -/
theorem fib_upper (p q n : Nat) (h : p * q + q ^ 2 ≤ p ^ 2) :
    q ^ n * fib (n + 1) ≤ p ^ n := by
  have hpair : q ^ n * fib (n + 1) ≤ p ^ n ∧
      q ^ (n + 1) * fib (n + 2) ≤ p ^ (n + 1) := by
    induction n with
    | zero =>
      constructor
      · simp [fib]
      · simpa [fib] using upper_base p q h
    | succ n ih =>
      constructor
      · exact ih.2
      · change q ^ (n + 2) * fib (n + 3) ≤ p ^ (n + 2)
        calc
          q ^ (n + 2) * fib (n + 3) =
              q * (q ^ (n + 1) * fib (n + 2)) +
              q ^ 2 * (q ^ n * fib (n + 1)) := by
            simpa only [Nat.add_assoc] using weighted_fib_step q n 1
          _ ≤ q * p ^ (n + 1) + q ^ 2 * p ^ n :=
            Nat.add_le_add (Nat.mul_le_mul_left q ih.2)
              (Nat.mul_le_mul_left (q ^ 2) ih.1)
          _ = p ^ n * (p * q + q ^ 2) := by
            simp only [Nat.pow_add, Nat.pow_one, Nat.mul_add]
            ac_rfl
          _ ≤ p ^ n * p ^ 2 := Nat.mul_le_mul_left (p ^ n) h
          _ = p ^ (n + 2) := (Nat.pow_add p n 2).symm
  exact hpair.1

/-- A lower quadratic certificate bounds the twice-shifted Fibonacci sequence.
The condition alone implies `p ≤ 2 * q`; positive parameters are not required. -/
theorem fib_lower (p q n : Nat) (h : p ^ 2 ≤ p * q + q ^ 2) :
    p ^ n ≤ q ^ n * fib (n + 2) := by
  have hpair : p ^ n ≤ q ^ n * fib (n + 2) ∧
      p ^ (n + 1) ≤ q ^ (n + 1) * fib (n + 3) := by
    induction n with
    | zero =>
      constructor
      · simp [fib]
      · simpa [fib, Nat.mul_comm] using lower_base p q h
    | succ n ih =>
      constructor
      · exact ih.2
      · change p ^ (n + 2) ≤ q ^ (n + 2) * fib (n + 4)
        calc
          p ^ (n + 2) = p ^ n * p ^ 2 := Nat.pow_add p n 2
          _ ≤ p ^ n * (p * q + q ^ 2) := Nat.mul_le_mul_left (p ^ n) h
          _ = q * p ^ (n + 1) + q ^ 2 * p ^ n := by
            simp only [Nat.pow_add, Nat.pow_one, Nat.mul_add]
            ac_rfl
          _ ≤ q * (q ^ (n + 1) * fib (n + 3)) +
              q ^ 2 * (q ^ n * fib (n + 2)) :=
            Nat.add_le_add (Nat.mul_le_mul_left q ih.2)
              (Nat.mul_le_mul_left (q ^ 2) ih.1)
          _ = q ^ (n + 2) * fib (n + 4) := by
            simpa only [Nat.add_assoc] using (weighted_fib_step q n 2).symm
  exact hpair.1

#print axioms fib_upper
#print axioms fib_lower

end P196.InverseFiberGrowth
