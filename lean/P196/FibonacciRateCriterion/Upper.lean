import P196.InverseFiberGrowth.RationalEnvelopes

/-
Agent #9. Necessary and sufficient upper Fibonacci rate certificates.
A failed quadratic condition creates a positive defect in a weighted
potential. The existing lower envelope makes that defect accumulate until
one of the two indices p*q and p*q+1 violates the proposed upper envelope.
-/
namespace P196.FibonacciRateCriterion

open P196.Agent9.InverseFibers

/-- Two consecutive indices decide whether the rational upper envelope holds.
All parameters are natural numbers, including zero. -/
theorem upper_pair_iff (p q : Nat) :
    (q ^ (p * q) * fib (p * q + 1) ≤ p ^ (p * q) ∧
      q ^ (p * q + 1) * fib (p * q + 2) ≤ p ^ (p * q + 1)) ↔
    p * q + q ^ 2 ≤ p ^ 2 := by
  constructor
  · intro hb
    by_cases hp0 : p = 0
    · subst p
      have hq0 : q = 0 := by simpa [fib] using hb.2
      simp [hq0]
    have hp : 0 < p := by omega
    apply Nat.le_of_not_lt
    intro hfail
    obtain ⟨δ, heq⟩ := Nat.exists_eq_add_of_le (Nat.le_of_lt hfail)
    have hδ : 0 < δ := by omega
    let A (n : Nat) : Nat := q ^ n * fib (n + 1)
    let E (n : Nat) : Nat := p * A (n + 1) + q ^ 2 * A n
    have he0 : E 0 = p * q + q ^ 2 := by simp [E, A, fib]
    have hrec (n : Nat) : E (n + 1) = p * E n + δ * A (n + 1) := by
      calc
        E (n + 1) = (p * q + q ^ 2) * A (n + 1) + p * q ^ 2 * A n := by
          dsimp [E, A]
          simp only [Nat.pow_add, Nat.pow_one, Nat.pow_two, Nat.mul_add, Nat.add_mul]
          ac_rfl
        _ = (p ^ 2 + δ) * A (n + 1) + p * q ^ 2 * A n := by rw [heq]
        _ = p * E n + δ * A (n + 1) := by
          dsimp [E]
          simp only [Nat.pow_two, Nat.mul_add, Nat.add_mul]
          ac_rfl
    have ha (n : Nat) : q * p ^ n ≤ A (n + 1) := by
      have hm := Nat.mul_le_mul_left q
        (P196.InverseFiberGrowth.fib_lower p q n (Nat.le_of_lt hfail))
      simpa only [A, Nat.pow_add, Nat.pow_one, Nat.add_assoc,
        Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using hm
    have hacc (n : Nat) : p ^ n * (p * E 0 + n * δ * q) ≤ p * E n := by
      induction n with
      | zero => simp
      | succ n ih =>
        change p ^ (n + 1) * (p * E 0 + (n + 1) * δ * q) ≤ p * E (n + 1)
        calc
          p ^ (n + 1) * (p * E 0 + (n + 1) * δ * q) =
              p * (p ^ n * (p * E 0 + n * δ * q)) + p * δ * (q * p ^ n) := by
            simp only [Nat.pow_add, Nat.pow_one, Nat.mul_add, Nat.add_mul, Nat.one_mul]
            ac_rfl
          _ ≤ p * (p * E n) + p * δ * A (n + 1) :=
            Nat.add_le_add (Nat.mul_le_mul_left p ih)
              (Nat.mul_le_mul_left (p * δ) (ha n))
          _ = p * E (n + 1) := by
            rw [hrec n]
            simp only [Nat.mul_add]
            ac_rfl
    have hb0 : A (p * q) ≤ p ^ (p * q) := hb.1
    have hb1 : A (p * q + 1) ≤ p ^ (p * q + 1) := hb.2
    have hbound : E (p * q) ≤ p ^ (p * q) * (p ^ 2 + q ^ 2) := by
      calc
        E (p * q) = p * A (p * q + 1) + q ^ 2 * A (p * q) := rfl
        _ ≤ p * p ^ (p * q + 1) + q ^ 2 * p ^ (p * q) :=
          Nat.add_le_add (Nat.mul_le_mul_left p hb1)
            (Nat.mul_le_mul_left (q ^ 2) hb0)
        _ = p ^ (p * q) * (p ^ 2 + q ^ 2) := by
          simp only [Nat.pow_add, Nat.pow_one, Nat.pow_two, Nat.mul_add]
          ac_rfl
    have hc := Nat.le_trans (hacc (p * q)) (Nat.mul_le_mul_left p hbound)
    have hc' : p * E 0 + (p * q) * δ * q ≤ p * (p ^ 2 + q ^ 2) := by
      apply Nat.le_of_mul_le_mul_left (c := p ^ (p * q)) _ (Nat.pow_pos hp)
      simpa only [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using hc
    have hc'' : E 0 + δ * q ^ 2 ≤ p ^ 2 + q ^ 2 := by
      apply Nat.le_of_mul_le_mul_left (c := p) _ hp
      calc
        p * (E 0 + δ * q ^ 2) = p * E 0 + (p * q) * δ * q := by
          simp only [Nat.mul_add, Nat.pow_two]
          ac_rfl
        _ ≤ p * (p ^ 2 + q ^ 2) := hc'
    rw [he0, heq] at hc''
    have hm : q ^ 2 ≤ δ * q ^ 2 := by
      simpa only [Nat.one_mul] using
        Nat.mul_le_mul_right (q ^ 2) (show 1 ≤ δ by omega)
    omega
  · intro h
    constructor
    · exact P196.InverseFiberGrowth.fib_upper p q (p * q) h
    · exact P196.InverseFiberGrowth.fib_upper p q (p * q + 1) h

/-- The quadratic condition exactly characterizes all-index upper envelopes. -/
theorem upper_all_iff (p q : Nat) :
    (∀ n : Nat, q ^ n * fib (n + 1) ≤ p ^ n) ↔
    p * q + q ^ 2 ≤ p ^ 2 := by
  constructor
  · intro h
    exact (upper_pair_iff p q).mp ⟨h (p * q), h (p * q + 1)⟩
  · intro h n
    exact P196.InverseFiberGrowth.fib_upper p q n h

#print axioms upper_pair_iff
#print axioms upper_all_iff

end P196.FibonacciRateCriterion
