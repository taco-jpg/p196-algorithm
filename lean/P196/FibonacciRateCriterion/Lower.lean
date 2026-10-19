import P196.InverseFiberGrowth.RationalEnvelopes

/-!
# A finite test for lower rational Fibonacci bounds

Agent #9. A positive defect in the quadratic certificate accumulates in a
weighted Fibonacci potential. This proves a finite detection horizon for
failure of the lower bound, without real analysis or an orbit assertion.
-/

namespace P196.FibonacciRateCriterion

open P196.Agent9.InverseFibers

private def lowerSeq (q n : Nat) : Nat := q ^ n * fib (n + 2)

private def lowerPotential (p q n : Nat) : Nat :=
  p * lowerSeq q (n + 1) + q ^ 2 * lowerSeq q n

private theorem potential_zero (p q : Nat) :
    lowerPotential p q 0 = p * q + p * q + q ^ 2 := by
  simp [lowerPotential, lowerSeq, fib, Nat.mul_two, Nat.mul_add]

private theorem potential_defect (p q d n : Nat)
    (h : p ^ 2 = p * q + q ^ 2 + d) :
    p * lowerPotential p q n =
      lowerPotential p q (n + 1) + d * lowerSeq q (n + 1) := by
  have hs : lowerSeq q (n + 2) =
      q * lowerSeq q (n + 1) + q ^ 2 * lowerSeq q n := by
    unfold lowerSeq
    rw [fib_succ_succ (n + 2)]
    simp only [Nat.pow_add, Nat.pow_one, Nat.pow_two, Nat.mul_add]
    ac_rfl
  calc
    p * lowerPotential p q n =
        p ^ 2 * lowerSeq q (n + 1) + p * q ^ 2 * lowerSeq q n := by
      simp only [lowerPotential, Nat.mul_add, Nat.pow_two]
      ac_rfl
    _ = (p * q + q ^ 2 + d) * lowerSeq q (n + 1) +
        p * q ^ 2 * lowerSeq q n := by rw [h]
    _ = p * (q * lowerSeq q (n + 1) + q ^ 2 * lowerSeq q n) +
        q ^ 2 * lowerSeq q (n + 1) + d * lowerSeq q (n + 1) := by
      simp only [Nat.add_mul, Nat.mul_add]
      ac_rfl
    _ = lowerPotential p q (n + 1) + d * lowerSeq q (n + 1) := by
      rw [← hs]
      rfl

private theorem potential_floor (p q n : Nat) :
    (p * q + q ^ 2) * lowerSeq q n ≤ lowerPotential p q n := by
  have hs : q * lowerSeq q n ≤ lowerSeq q (n + 1) := by
    have hm := Nat.mul_le_mul_left (q ^ (n + 1)) (fib_le_succ (n + 2))
    simpa [lowerSeq, Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm,
      Nat.mul_left_comm, Nat.add_assoc] using hm
  calc
    (p * q + q ^ 2) * lowerSeq q n =
        p * (q * lowerSeq q n) + q ^ 2 * lowerSeq q n := by
      simp only [Nat.add_mul, Nat.mul_assoc]
    _ ≤ p * lowerSeq q (n + 1) + q ^ 2 * lowerSeq q n :=
      Nat.add_le_add_right (Nat.mul_le_mul_left p hs) _
    _ = lowerPotential p q n := rfl

private theorem accumulated_defect (p q d N : Nat)
    (hd : p ^ 2 = p * q + q ^ 2 + d)
    (hb : ∀ n, n ≤ N → p ^ n ≤ lowerSeq q n) :
    ∀ n, n ≤ N →
      lowerPotential p q n + n * d * p ^ n ≤ p ^ n * lowerPotential p q 0 := by
  intro n
  induction n with
  | zero => intro _; simp
  | succ n ih =>
    intro hn
    have hi := ih (by omega)
    have hnxt := hb (n + 1) hn
    calc
      lowerPotential p q (n + 1) + (n + 1) * d * p ^ (n + 1) =
          lowerPotential p q (n + 1) + d * p ^ (n + 1) + n * d * p ^ (n + 1) := by
        simp only [Nat.add_mul, Nat.one_mul]
        ac_rfl
      _ ≤ lowerPotential p q (n + 1) + d * lowerSeq q (n + 1) +
          n * d * p ^ (n + 1) :=
        Nat.add_le_add_right (Nat.add_le_add_left (Nat.mul_le_mul_left d hnxt) _) _
      _ = p * (lowerPotential p q n + n * d * p ^ n) := by
        rw [Nat.mul_add, potential_defect p q d n hd]
        simp only [Nat.pow_succ]
        ac_rfl
      _ ≤ p * (p ^ n * lowerPotential p q 0) := Nat.mul_le_mul_left p hi
      _ = p ^ (n + 1) * lowerPotential p q 0 := by
        simp only [Nat.pow_succ]
        ac_rfl

private theorem certificate_of_prefix (p q : Nat)
    (hb : ∀ n, n ≤ p * q + 1 → p ^ n ≤ lowerSeq q n) :
    p ^ 2 ≤ p * q + q ^ 2 := by
  by_cases hp : p = 0
  · simp [hp]
  have hp0 : 0 < p := by omega
  apply Nat.le_of_not_lt
  intro hlt
  let d := p ^ 2 - (p * q + q ^ 2)
  have hd0 : 0 < d := by dsimp [d]; omega
  have hd : p ^ 2 = p * q + q ^ 2 + d := by dsimp [d]; omega
  let N := p * q + 1
  have ha := accumulated_defect p q d N hd hb N (Nat.le_refl N)
  have hf : (p * q + q ^ 2) * p ^ N ≤ lowerPotential p q N :=
    Nat.le_trans (Nat.mul_le_mul_left (p * q + q ^ 2) (hb N (Nat.le_refl N)))
      (potential_floor p q N)
  have hm : p ^ N * (p * q + q ^ 2 + N * d) ≤ p ^ N * lowerPotential p q 0 := by
    calc
      p ^ N * (p * q + q ^ 2 + N * d) =
          (p * q + q ^ 2) * p ^ N + N * d * p ^ N := by
        simp only [Nat.mul_add, Nat.add_mul]
        ac_rfl
      _ ≤ lowerPotential p q N + N * d * p ^ N := Nat.add_le_add_right hf _
      _ ≤ p ^ N * lowerPotential p q 0 := ha
  have hc : p * q + q ^ 2 + N * d ≤ lowerPotential p q 0 :=
    Nat.le_of_mul_le_mul_left hm (Nat.pow_pos hp0)
  rw [potential_zero] at hc
  have hg : N ≤ N * d := by
    simpa using Nat.mul_le_mul_left N (show 1 ≤ d by omega)
  dsimp [N] at hc hg
  omega

/-- The quadratic lower certificate is equivalent to checking the bounds
through the explicit finite horizon `p * q + 1`, including zero parameters. -/
theorem lower_prefix_iff (p q : Nat) :
    (∀ n, n ≤ p * q + 1 → p ^ n ≤ q ^ n * fib (n + 2)) ↔
      p ^ 2 ≤ p * q + q ^ 2 := by
  constructor
  · exact certificate_of_prefix p q
  · intro h n _
    exact P196.InverseFiberGrowth.fib_lower p q n h

/-- The lower quadratic condition is necessary and sufficient at every index. -/
theorem lower_all_iff (p q : Nat) :
    (∀ n, p ^ n ≤ q ^ n * fib (n + 2)) ↔ p ^ 2 ≤ p * q + q ^ 2 := by
  constructor
  · intro h
    exact (lower_prefix_iff p q).mp (fun n _ => h n)
  · intro h n
    exact P196.InverseFiberGrowth.fib_lower p q n h

end P196.FibonacciRateCriterion
