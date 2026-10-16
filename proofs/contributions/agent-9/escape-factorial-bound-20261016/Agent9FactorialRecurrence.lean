import Std

/-!
The algebraic factorial estimate from strengthening_notes.txt, section 5,
equation (9), at source commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5.
The recurrence is a hypothesis. No general-base dynamics are introduced.
Lean 4.19.0 Std supplies no factorial definition, so its ordinary natural
recursion is defined in this contribution's namespace.
-/

namespace P196.Agent9.FactorialEscape

/-- Ordinary factorial, with `0! = 1`. -/
def factorial : Nat → Nat
  | 0 => 1
  | m + 1 => (m + 1) * factorial m

@[simp] theorem factorial_zero : factorial 0 = 1 := rfl

@[simp] theorem factorial_succ (m : Nat) :
    factorial (m + 1) = (m + 1) * factorial m := rfl

theorem factorial_pos (m : Nat) : 0 < factorial m := by
  induction m with
  | zero => decide
  | succ m ih => exact Nat.mul_pos (Nat.succ_pos m) ih

/-- The positive margin in the manuscript's induction. -/
theorem recurrence_step_bound (i C : Nat) (hC : 1 ≤ C) :
    (i + 2) + (i + 1) * (2 * C + 1) ≤ 4 * (i + 2) * C := by
  have hsmall : i + 2 ≤ (i + 2) * C := by
    simpa only [Nat.mul_one] using Nat.mul_le_mul_left (i + 2) hC
  have hthree : 2 * C + 1 ≤ 3 * C := by omega
  calc
    (i + 2) + (i + 1) * (2 * C + 1) ≤
        (i + 2) * C + (i + 1) * (3 * C) :=
      Nat.add_le_add hsmall (Nat.mul_le_mul_left (i + 1) hthree)
    _ = ((i + 2) + 3 * (i + 1)) * C := by
      simp only [Nat.add_mul, Nat.mul_add, Nat.mul_assoc, Nat.mul_left_comm,
        Nat.mul_comm, Nat.add_assoc]
    _ ≤ 4 * (i + 2) * C :=
      Nat.mul_le_mul_right C (by omega)

/-- Shifted induction form; no value of `E 0` is assumed or used. -/
theorem recurrence_factorial_bound_succ (κ : Nat) (hκ : 0 < κ)
    (E : Nat → Nat) (h1 : E 1 = 1)
    (hrec : ∀ i, E (i + 2) =
      κ * ((i + 2) + (i + 1) * (2 * E (i + 1) + 1)))
    (i : Nat) :
    E (i + 1) ≤ (4 * κ) ^ i * factorial (i + 1) := by
  induction i with
  | zero => simp [h1, factorial]
  | succ i ih =>
    let C := (4 * κ) ^ i * factorial (i + 1)
    have hC : 1 ≤ C :=
      Nat.mul_pos (Nat.pow_pos (by omega)) (factorial_pos (i + 1))
    have hEC : E (i + 1) ≤ C := ih
    calc
      E (i + 1 + 1) =
          κ * ((i + 2) + (i + 1) * (2 * E (i + 1) + 1)) := hrec i
      _ ≤ κ * ((i + 2) + (i + 1) * (2 * C + 1)) :=
        Nat.mul_le_mul_left κ (Nat.add_le_add_left
          (Nat.mul_le_mul_left (i + 1)
            (Nat.add_le_add_right (Nat.mul_le_mul_left 2 hEC) 1)) (i + 2))
      _ ≤ κ * (4 * (i + 2) * C) :=
        Nat.mul_le_mul_left κ (recurrence_step_bound i C hC)
      _ = (4 * κ) ^ (i + 1) * factorial (i + 2) := by
        simp only [C, Nat.pow_succ, factorial_succ,
          Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]

/-- Equation (9) for the exact recurrence, for every positive mass index.
The unconstrained value `E 0` is deliberately outside this conclusion. -/
theorem recurrence_factorial_bound (κ : Nat) (hκ : 0 < κ)
    (E : Nat → Nat) (h1 : E 1 = 1)
    (hrec : ∀ i, E (i + 2) =
      κ * ((i + 2) + (i + 1) * (2 * E (i + 1) + 1)))
    (M : Nat) (hM : 1 ≤ M) :
    E M ≤ (4 * κ) ^ (M - 1) * factorial M := by
  cases M with
  | zero => omega
  | succ i =>
    simpa using recurrence_factorial_bound_succ κ hκ E h1 hrec i

#print axioms factorial
#print axioms factorial_zero
#print axioms factorial_succ
#print axioms factorial_pos
#print axioms recurrence_step_bound
#print axioms recurrence_factorial_bound_succ
#print axioms recurrence_factorial_bound

end P196.Agent9.FactorialEscape
