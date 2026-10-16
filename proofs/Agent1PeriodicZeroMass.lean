import Agent1PeriodicValidity

/-!
Exact finite mass of a periodic word with zero period. The arithmetic link
uses the original DecimalMass.wordSum_columns and digitSum_value theorems.
This module supplies no transition, cycle, or orbit-existence assertion.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

private theorem wordSum_list (W : Word) :
    DecimalMass.wordSum (fun i => (W[i]?).getD 0) W.length = W.sum := by
  induction W with
  | nil => rfl
  | cons a W ih =>
    rw [List.length_cons, DecimalMass.wordSum_shift]
    simpa only [List.getElem?_cons_zero, List.getElem?_cons_succ,
      Option.getD_some, List.sum_cons] using congrArg (fun n => a + n) ih

private theorem sum_append (A B : Word) : (A ++ B).sum = A.sum + B.sum := by
  induction A with
  | nil => simp only [List.nil_append, List.sum_nil, Nat.zero_add]
  | cons a A ih =>
    simp only [List.cons_append, List.sum_cons, ih, Nat.add_assoc]

private theorem sum_reverse (W : Word) : W.reverse.sum = W.sum := by
  induction W with
  | nil => rfl
  | cons a W ih =>
    simp only [List.reverse_cons, sum_append, List.sum_cons, List.sum_nil, ih]
    omega

private theorem pow_zero_sum (k : Nat) :
    (pow [0, 0, 0, 0] k).sum = 0 := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [pow, sum_append, List.sum_cons, List.sum_nil, Nat.zero_add, ih]

/-- Zero bulk contributes no mass, at every exponent including zero.
No boundedness, symmetry, positivity, or validity assumption is required. -/
theorem zero_period_wordSum (B H : Word) (k : Nat) :
    DecimalMass.wordSum
      (fun i => ((periodicWord B H [0, 0, 0, 0] k)[i]?).getD 0)
      (periodicWord B H [0, 0, 0, 0] k).length = 2 * B.sum + H.sum := by
  rw [wordSum_list]
  have hz : ([0, 0, 0, 0] : Word).reverse = [0, 0, 0, 0] := rfl
  simp only [periodicWord, sum_append, hz, pow_zero_sum, sum_reverse]
  omega

/-- Every canonical ordinary realization of the zero-period template has
twice its digit sum equal to the fixed exterior-and-center mass. -/
theorem zero_period_digitSum (B H : Word) (k n : Nat) (d : Nat → Nat)
    (hc : DecimalDigits.Canonical n d (periodicWord B H [0, 0, 0, 0] k).length)
    (hrep : ∀ i, i < (periodicWord B H [0, 0, 0, 0] k).length →
      DecimalDigits.columnSum d (periodicWord B H [0, 0, 0, 0] k).length i =
        ((periodicWord B H [0, 0, 0, 0] k)[i]?).getD 0) :
    2 * DecimalMass.digitSum n = 2 * B.sum + H.sum := by
  calc
    2 * DecimalMass.digitSum n =
        2 * DecimalMass.wordSum d (periodicWord B H [0, 0, 0, 0] k).length := by
      rw [← hc.2.2.2, DecimalMass.digitSum_value d _ hc.2.1]
    _ = DecimalMass.wordSum
        (DecimalDigits.columnSum d (periodicWord B H [0, 0, 0, 0] k).length)
        (periodicWord B H [0, 0, 0, 0] k).length :=
      (DecimalMass.wordSum_columns _ _).symm
    _ = DecimalMass.wordSum
        (fun i => ((periodicWord B H [0, 0, 0, 0] k)[i]?).getD 0)
        (periodicWord B H [0, 0, 0, 0] k).length :=
      DecimalMass.wordSum_congr _ _ _ hrep
    _ = 2 * B.sum + H.sum := zero_period_wordSum B H k

/-- A bound on the finite interface mass bounds every actual digit sum
represented by that zero-period template, independently of its exponent. -/
theorem zero_period_digitSum_le (B H : Word) (k n : Nat) (d : Nat → Nat) (M : Nat)
    (hc : DecimalDigits.Canonical n d (periodicWord B H [0, 0, 0, 0] k).length)
    (hrep : ∀ i, i < (periodicWord B H [0, 0, 0, 0] k).length →
      DecimalDigits.columnSum d (periodicWord B H [0, 0, 0, 0] k).length i =
        ((periodicWord B H [0, 0, 0, 0] k)[i]?).getD 0)
    (hmass : 2 * B.sum + H.sum ≤ M) : DecimalMass.digitSum n ≤ M := by
  have hm := zero_period_digitSum B H k n d hc hrep
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.zero_period_wordSum
#print axioms Agent1.Periodic.zero_period_digitSum
#print axioms Agent1.Periodic.zero_period_digitSum_le
