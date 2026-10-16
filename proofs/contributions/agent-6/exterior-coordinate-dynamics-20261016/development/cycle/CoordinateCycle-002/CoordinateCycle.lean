import CoordinateDynamics

/-!
Finite telescopes for the literal exterior transition.  The statements include
the empty path and do not assert that a closed orbit exists.  Overflow counting
uses the indicator of nonzero final carry, not the carry's numerical value, so
the identities do not require a bound on the input coefficients.
-/

namespace Agent6.ExteriorCoordinates

open P196.Agent7.Finite Agent115.ExteriorFactorization

/-- The state after exactly `n` applications of `outerNext`. -/
def outerIter : Nat → Outer → Outer
  | 0, s => s
  | n + 1, s => outerNext (outerIter n s)

/-- Sum a signed state observable over the first `n` states of an orbit. -/
def orbitSum (f : Outer → Int) (s : Outer) : Nat → Int
  | 0 => 0
  | n + 1 => orbitSum f s n + f (outerIter n s)

/-- The total signed high-side contribution over a finite orbit segment. -/
def contributionSum (s : Outer) (n : Nat) : Int :=
  orbitSum (fun q => highContribution q.c q.B) s n

@[simp] theorem outerIter_zero (s : Outer) : outerIter 0 s = s := rfl

@[simp] theorem outerIter_succ (s : Outer) (n : Nat) :
    outerIter (n + 1) s = outerNext (outerIter n s) := rfl

@[simp] theorem orbitSum_zero (f : Outer → Int) (s : Outer) :
    orbitSum f s 0 = 0 := rfl

theorem orbitSum_succ (f : Outer → Int) (s : Outer) (n : Nat) :
    orbitSum f s (n + 1) = orbitSum f s n + f (outerIter n s) := rfl

@[simp] theorem contributionSum_zero (s : Outer) :
    contributionSum s 0 = 0 := rfl

theorem contributionSum_succ (s : Outer) (n : Nat) :
    contributionSum s (n + 1) = contributionSum s n +
      highContribution (outerIter n s).c (outerIter n s).B := rfl

/-- A generic finite telescope, independent of exterior arithmetic. -/
theorem orbitSum_telescope (a f : Outer → Int)
    (hstep : ∀ q, a (outerNext q) = a q + f q) (s : Outer) (n : Nat) :
    a (outerIter n s) = a s + orbitSum f s n := by
  induction n with
  | zero => simp only [outerIter_zero, orbitSum_zero, Int.add_zero]
  | succ n ih =>
    rw [outerIter_succ, hstep, ih, orbitSum_succ]
    omega

/-- A supplied finite transition chain agrees with the canonical iterate. -/
theorem outerIter_eq_chain (q : Nat → Outer) (n : Nat)
    (hstep : ∀ i, i < n → q (i + 1) = outerNext (q i)) :
    outerIter n (q 0) = q n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [outerIter_succ, ih (by intro i hi; exact hstep i (by omega))]
    exact (hstep n (by omega)).symm

/-- A nonnegative finite sum equal to zero has only zero summands. -/
theorem orbitSum_eq_zero_of_nonneg (f : Outer → Int) (s : Outer) (n : Nat)
    (hnonneg : ∀ i, i < n → 0 ≤ f (outerIter i s))
    (hsum : orbitSum f s n = 0) :
    ∀ i, i < n → f (outerIter i s) = 0 := by
  have hsum_nonneg : ∀ m, m ≤ n → 0 ≤ orbitSum f s m := by
    intro m hm
    induction m with
    | zero => simp only [orbitSum_zero, Int.le_refl]
    | succ m ih =>
      rw [orbitSum_succ]
      have := ih (by omega)
      have := hnonneg m (by omega)
      omega
  induction n with
  | zero => intro i hi; omega
  | succ n ih =>
    rw [orbitSum_succ] at hsum
    have hlast := hnonneg n (by omega)
    have hprior := hsum_nonneg n (by omega)
    have hzero : orbitSum f s n = 0 := by omega
    intro i hi
    by_cases hin : i < n
    · exact ih (by intro j hj; exact hnonneg j (by omega)) hzero
        (by intro m hm; exact hsum_nonneg m (by omega)) i hin
    · have : i = n := by omega
      subst i
      omega

/-- A nonpositive finite sum equal to zero has only zero summands. -/
theorem orbitSum_eq_zero_of_nonpos (f : Outer → Int) (s : Outer) (n : Nat)
    (hnonpos : ∀ i, i < n → f (outerIter i s) ≤ 0)
    (hsum : orbitSum f s n = 0) :
    ∀ i, i < n → f (outerIter i s) = 0 := by
  have hsum_nonpos : ∀ m, m ≤ n → orbitSum f s m ≤ 0 := by
    intro m hm
    induction m with
    | zero => simp only [orbitSum_zero, Int.le_refl]
    | succ m ih =>
      rw [orbitSum_succ]
      have := ih (by omega)
      have := hnonpos m (by omega)
      omega
  induction n with
  | zero => intro i hi; omega
  | succ n ih =>
    rw [orbitSum_succ] at hsum
    have hlast := hnonpos n (by omega)
    have hprior := hsum_nonpos n (by omega)
    have hzero : orbitSum f s n = 0 := by omega
    intro i hi
    by_cases hin : i < n
    · exact ih (by intro j hj; exact hnonpos j (by omega)) hzero
        (by intro m hm; exact hsum_nonpos m (by omega)) i hin
    · have : i = n := by omega
      subst i
      omega

/-- A finite zero sum containing a nonzero summand contains both signs. -/
theorem orbitSum_zero_both_signs (f : Outer → Int) (s : Outer) (n : Nat)
    (hsum : orbitSum f s n = 0)
    (hnonzero : ∃ i, i < n ∧ f (outerIter i s) ≠ 0) :
    (∃ i, i < n ∧ 0 < f (outerIter i s)) ∧
      (∃ j, j < n ∧ f (outerIter j s) < 0) := by
  constructor
  · apply Classical.byContradiction
    intro hpos
    have hnonpos : ∀ i, i < n → f (outerIter i s) ≤ 0 := by
      intro i hi
      have : ¬ 0 < f (outerIter i s) := fun h => hpos ⟨i, hi, h⟩
      omega
    obtain ⟨i, hi, hne⟩ := hnonzero
    exact hne (orbitSum_eq_zero_of_nonpos f s n hnonpos hsum i hi)
  · apply Classical.byContradiction
    intro hneg
    have hnonneg : ∀ i, i < n → 0 ≤ f (outerIter i s) := by
      intro i hi
      have : ¬ f (outerIter i s) < 0 := fun h => hneg ⟨i, hi, h⟩
      omega
    obtain ⟨i, hi, hne⟩ := hnonzero
    exact hne (orbitSum_eq_zero_of_nonneg f s n hnonneg hsum i hi)

/-- Indicator of a nonzero final high-side carry. -/
def overflowBit (s : Outer) : Nat :=
  if (highValue s.B + (if 10 ≤ s.c then 1 else 0)) / 10 ^ s.B.length = 0
    then 0 else 1

/-- The scale used in the high-side contribution: one or ten. -/
def carryScale (s : Outer) : Int :=
  if (highValue s.B + (if 10 ≤ s.c then 1 else 0)) / 10 ^ s.B.length = 0
    then 1 else 10

/-- The reversed high value, multiplied by its overflow-dependent scale. -/
def weightedReverse (s : Outer) : Int :=
  carryScale s * (revN s.B.length (highValue s.B + (if 10 ≤ s.c then 1 else 0)) : Int)

/-- The phase contribution, multiplied by its overflow-dependent scale. -/
def weightedPhase (s : Outer) : Int :=
  carryScale s * ((s.c - 9 * (if 10 ≤ s.c then 1 else 0) : Nat) : Int) *
    (10 : Int) ^ s.B.length

/-- Count steps with a nonzero final high-side carry. -/
def overflowCount (s : Outer) : Nat → Nat
  | 0 => 0
  | n + 1 => overflowCount s n + overflowBit (outerIter n s)

@[simp] theorem overflowCount_zero (s : Outer) : overflowCount s 0 = 0 := rfl

theorem overflowCount_succ (s : Outer) (n : Nat) :
    overflowCount s (n + 1) = overflowCount s n + overflowBit (outerIter n s) := rfl

theorem highContribution_eq_weighted (s : Outer) :
    highContribution s.c s.B =
      9 * weightedReverse s - weightedPhase s + 9 * (overflowBit s : Int) := by
  unfold highContribution weightedReverse weightedPhase carryScale overflowBit
  dsimp only
  by_cases hcarry :
      (highValue s.B + (if 10 ≤ s.c then 1 else 0)) / 10 ^ s.B.length = 0
  · simp only [hcarry, if_true, Int.natCast_zero,
      Int.mul_zero, Int.one_mul, Int.add_zero]
  · simp only [hcarry, if_false, Int.natCast_one, Int.mul_one, ← Int.mul_assoc]
    omega

/-- The explicit weighted balance, with a finite overflow count. -/
theorem contributionSum_eq_weighted (s : Outer) (n : Nat) :
    contributionSum s n = 9 * orbitSum weightedReverse s n -
      orbitSum weightedPhase s n + 9 * (overflowCount s n : Int) := by
  induction n with
  | zero => simp only [contributionSum_zero, orbitSum_zero, overflowCount_zero,
      Int.natCast_zero, Int.mul_zero, Int.sub_zero, Int.add_zero]
  | succ n ih =>
    rw [contributionSum_succ, ih, highContribution_eq_weighted,
      orbitSum_succ, orbitSum_succ, overflowCount_succ, Int.natCast_add]
    simp only [Int.mul_add]
    omega

end Agent6.ExteriorCoordinates
