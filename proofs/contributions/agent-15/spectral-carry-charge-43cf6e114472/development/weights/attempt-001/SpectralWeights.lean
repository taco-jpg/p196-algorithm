import Std

/-!
# Integer weights for the original spectral carry charge

The original `carry_coordinates` definition uses U with initial values 0, 1
and S with initial values 1, 21. Both satisfy X(n+2) = 20*X(n+1) - X(n).
Odd carry differences use U(n+1), while even carry differences use S(n).

Source snapshot: 5ff4f607535587d572fbc9e95ba9501d1fbe5fc5.
Original notes blob: cb1c355fa05916a770816a4d5ef680e54079cccb.
Original script blob: 730acd722bf017b6bf1e51e5a0411169a7804da4.
This module formalizes the original weights, without a novelty claim.
-/

namespace P196.Agent15.SpectralCarry

/-- The exact integer recurrence used by the original coordinate script. -/
def recurrence (a b : Int) : Nat → Int
  | 0 => a
  | 1 => b
  | n + 2 => 20 * recurrence a b (n + 1) - recurrence a b n

@[simp] theorem recurrence_zero (a b : Int) : recurrence a b 0 = a := rfl

@[simp] theorem recurrence_one (a b : Int) : recurrence a b 1 = b := rfl

theorem recurrence_step (a b : Int) (n : Nat) :
    recurrence a b (n + 2) =
      20 * recurrence a b (n + 1) - recurrence a b n := rfl

/-- Odd-width carry sequence; its zero term is not a used charge weight. -/
def U : Nat → Int := recurrence 0 1

/-- Even-width carry sequence. -/
def S : Nat → Int := recurrence 1 21

@[simp] theorem U_zero : U 0 = 0 := rfl

@[simp] theorem U_one : U 1 = 1 := rfl

theorem U_step (n : Nat) : U (n + 2) = 20 * U (n + 1) - U n := rfl

@[simp] theorem S_zero : S 0 = 1 := rfl

@[simp] theorem S_one : S 1 = 21 := rfl

theorem S_step (n : Nat) : S (n + 2) = 20 * S (n + 1) - S n := rfl

/-- The positive odd-width charge weights start at U(1). -/
def oddWeight (n : Nat) : Int := U (n + 1)

/-- The positive even-width charge weights start at S(0). -/
def evenWeight (n : Nat) : Int := S n

@[simp] theorem oddWeight_zero : oddWeight 0 = 1 := rfl

@[simp] theorem oddWeight_one : oddWeight 1 = 20 := rfl

theorem oddWeight_step (n : Nat) :
    oddWeight (n + 2) = 20 * oddWeight (n + 1) - oddWeight n := rfl

@[simp] theorem evenWeight_zero : evenWeight 0 = 1 := rfl

@[simp] theorem evenWeight_one : evenWeight 1 = 21 := rfl

theorem evenWeight_step (n : Nat) :
    evenWeight (n + 2) = 20 * evenWeight (n + 1) - evenWeight n := rfl

/-- Sum of the n weights preceding the weight at index n. -/
def weightSum (w : Nat → Int) : Nat → Int
  | 0 => 0
  | n + 1 => weightSum w n + w n

@[simp] theorem weightSum_zero (w : Nat → Int) : weightSum w 0 = 0 := rfl

@[simp] theorem weightSum_succ (w : Nat → Int) (n : Nat) :
    weightSum w (n + 1) = weightSum w n + w n := rfl

private theorem positive_and_growth (w : Nat → Int)
    (hzero : 0 < w 0) (hone : 19 * w 0 ≤ w 1)
    (hstep : ∀ n, w (n + 2) = 20 * w (n + 1) - w n) :
    ∀ n, 0 < w n ∧ 19 * w n ≤ w (n + 1) := by
  intro n
  induction n with
  | zero => exact ⟨hzero, hone⟩
  | succ n ih =>
      have hs := hstep n
      constructor <;> omega

theorem oddWeight_pos (n : Nat) : 0 < oddWeight n := by
  have h := positive_and_growth oddWeight (by simp) (by simp) oddWeight_step n
  exact h.1

theorem evenWeight_pos (n : Nat) : 0 < evenWeight n := by
  have h := positive_and_growth evenWeight (by simp) (by simp) evenWeight_step n
  exact h.1

theorem oddWeight_growth (n : Nat) : 19 * oddWeight n ≤ oddWeight (n + 1) := by
  have h := positive_and_growth oddWeight (by simp) (by simp) oddWeight_step n
  exact h.2

theorem evenWeight_growth (n : Nat) : 19 * evenWeight n ≤ evenWeight (n + 1) := by
  have h := positive_and_growth evenWeight (by simp) (by simp) evenWeight_step n
  exact h.2

private theorem sum_lt_of_growth (w : Nat → Int)
    (hpos : ∀ n, 0 < w n) (hgrowth : ∀ n, 19 * w n ≤ w (n + 1)) :
    ∀ n, weightSum w n < w n := by
  intro n
  induction n with
  | zero => exact hpos 0
  | succ n ih =>
      have hp := hpos n
      have hg := hgrowth n
      rw [weightSum_succ]
      omega

/-- Every used odd weight exceeds the sum of all preceding used odd weights. -/
theorem oddWeight_superincreasing (n : Nat) :
    weightSum oddWeight n < oddWeight n :=
  sum_lt_of_growth oddWeight oddWeight_pos oddWeight_growth n

/-- Every used even weight exceeds the sum of all preceding used even weights. -/
theorem evenWeight_superincreasing (n : Nat) :
    weightSum evenWeight n < evenWeight n :=
  sum_lt_of_growth evenWeight evenWeight_pos evenWeight_growth n

end P196.Agent15.SpectralCarry
