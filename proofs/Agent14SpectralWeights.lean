import Std

/-!
Integer recurrence weights from `creative_global_spectral_notes.md` at
source commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.

The odd coordinate uses the central weight one followed by `T 1`, `T 2`,
and the later `T` weights. The even coordinate uses `R 0`, `R 1`, and the
later `R` weights. Strict domination of all smaller weights is the finite
arithmetic fact needed to recover coefficients bounded by eighteen.
-/

namespace Agent14.Spectral

def T : Nat → Nat
  | 0 => 2
  | 1 => 20
  | n + 2 => 20 * T (n + 1) - T n

def R : Nat → Nat
  | 0 => 1
  | 1 => 19
  | n + 2 => 20 * R (n + 1) - R n

@[simp] theorem T_zero : T 0 = 2 := rfl
@[simp] theorem T_one : T 1 = 20 := rfl
@[simp] theorem R_zero : R 0 = 1 := rfl
@[simp] theorem R_one : R 1 = 19 := rfl

theorem T_monotone_step (n : Nat) : T n ≤ T (n + 1) := by
  induction n with
  | zero => decide
  | succ n ih =>
      change T (n + 1) ≤ 20 * T (n + 1) - T n
      omega

theorem R_monotone_step (n : Nat) : R n ≤ R (n + 1) := by
  induction n with
  | zero => decide
  | succ n ih =>
      change R (n + 1) ≤ 20 * R (n + 1) - R n
      omega

/-- The defining natural subtraction gives the exact integer recurrence. -/
theorem T_recurrence_exact (n : Nat) :
    T (n + 2) + T n = 20 * T (n + 1) := by
  have hm := T_monotone_step n
  change 20 * T (n + 1) - T n + T n = 20 * T (n + 1)
  omega

/-- The defining natural subtraction gives the exact integer recurrence. -/
theorem R_recurrence_exact (n : Nat) :
    R (n + 2) + R n = 20 * R (n + 1) := by
  have hm := R_monotone_step n
  change 20 * R (n + 1) - R n + R n = 20 * R (n + 1)
  omega

theorem T_positive (n : Nat) : 0 < T n := by
  induction n with
  | zero => decide
  | succ n ih =>
      have hm := T_monotone_step n
      omega

theorem R_positive (n : Nat) : 0 < R n := by
  induction n with
  | zero => decide
  | succ n ih =>
      have hm := R_monotone_step n
      omega

/-- The comparison begins at `T 1`, the first noncentral odd weight. -/
theorem T_growth_from_one (n : Nat) :
    19 * T (n + 1) ≤ T (n + 2) := by
  have hm := T_monotone_step n
  have he := T_recurrence_exact n
  omega

theorem R_growth (n : Nat) : 19 * R n ≤ R (n + 1) := by
  cases n with
  | zero => decide
  | succ n =>
      change 19 * R (n + 1) ≤ R (n + 2)
      have hm := R_monotone_step n
      have he := R_recurrence_exact n
      omega

def oddWeight (n : Nat) : Nat := if n = 0 then 1 else T n

@[simp] theorem oddWeight_zero : oddWeight 0 = 1 := rfl

@[simp] theorem oddWeight_succ (n : Nat) : oddWeight (n + 1) = T (n + 1) := by
  simp [oddWeight]

theorem oddWeight_positive (n : Nat) : 0 < oddWeight n := by
  cases n with
  | zero => decide
  | succ n =>
      rw [oddWeight_succ]
      exact T_positive (n + 1)

theorem oddWeight_growth (n : Nat) :
    19 * oddWeight n ≤ oddWeight (n + 1) := by
  cases n with
  | zero => decide
  | succ n =>
      rw [oddWeight_succ, oddWeight_succ]
      exact T_growth_from_one n

def prefixSum (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => prefixSum f n + f n

@[simp] theorem prefixSum_zero (f : Nat → Nat) : prefixSum f 0 = 0 := rfl

@[simp] theorem prefixSum_succ (f : Nat → Nat) (n : Nat) :
    prefixSum f (n + 1) = prefixSum f n + f n := rfl

/-- A nineteenfold step dominates eighteen times the entire earlier sum. -/
theorem dominates_of_nineteen_growth (f : Nat → Nat)
    (hzero : 0 < f 0) (hgrowth : ∀ n, 19 * f n ≤ f (n + 1))
    (n : Nat) : 18 * prefixSum f n < f n := by
  induction n with
  | zero => simpa only [prefixSum, Nat.mul_zero] using hzero
  | succ n ih =>
      have hg := hgrowth n
      rw [prefixSum_succ]
      omega

theorem oddWeight_dominates (n : Nat) :
    18 * prefixSum oddWeight n < oddWeight n :=
  dominates_of_nineteen_growth oddWeight (by decide) oddWeight_growth n

theorem R_dominates (n : Nat) : 18 * prefixSum R n < R n :=
  dominates_of_nineteen_growth R (by decide) R_growth n

theorem initial_weight_values :
    T 2 = 398 ∧ R 2 = 379 ∧ oddWeight 0 = 1 ∧ oddWeight 1 = 20 := by
  decide

#print axioms T_recurrence_exact
#print axioms R_recurrence_exact
#print axioms T_positive
#print axioms R_positive
#print axioms T_growth_from_one
#print axioms R_growth
#print axioms oddWeight_growth
#print axioms dominates_of_nineteen_growth
#print axioms oddWeight_dominates
#print axioms R_dominates
#print axioms initial_weight_values

end Agent14.Spectral
