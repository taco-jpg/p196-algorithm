import P196.Foundations.LychrelDigitSums
import P196.Drafts.D20261015ScalarClockFormalScalarClock.ScalarClock

/-! Exact one-coefficient transition of an admissible whole decimal pair
word. Width one and overlapping windows are included. -/

namespace ActualScalar

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

def actualControl (q : Nat → Nat) (L : Nat) : Bool :=
  decide (carry q (L - 1) = 1)

theorem actualControl_exact (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    carry q (L - 1) = (actualControl q L).toNat := by
  have hb := carry_bounded q L ha.2.2.1 (L - 1) (by omega)
  by_cases hc : carry q (L - 1) = 1
  · simp [actualControl, hc]
  · have hz : carry q (L - 1) = 0 := by omega
    simp [actualControl, hz]

theorem actualControl_false_iff (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    actualControl q L = false ↔ carry q (L - 1) = 0 := by
  have hb := carry_bounded q L ha.2.2.1 (L - 1) (by omega)
  simp only [actualControl, decide_eq_false_iff_not]
  omega

theorem actualControl_true_iff (q : Nat → Nat) (L : Nat) :
    actualControl q L = true ↔ carry q (L - 1) = 1 := by
  simp [actualControl]

/-- Exact scalar step for the actual incoming high-column carry. -/
theorem scalar_step_exact (q : Nat → Nat) (L : Nat) (c : Bool)
    (ha : Admissible L q) (hc : carry q (L - 1) = c.toNat) :
    (nextColumns q L 0, carry q L) = ScalarClock.step (q 0) c := by
  have hL : 0 < L := ha.1
  have hs : q (L - 1) = q 0 := by
    simpa only [Nat.sub_zero] using (ha.2.2.2.1 0 hL).symm
  have he : carry q L = (q 0 + c.toNat) / 10 := by
    have hi : L = (L - 1) + 1 := by omega
    calc
      carry q L = carry q ((L - 1) + 1) := congrArg (carry q) hi
      _ = _ := by rw [carry, hs, hc]
  have hh : output q (L - 1) = (q 0 + c.toNat) % 10 := by
    simp only [output, hs, hc]
  have hl : output q 0 = q 0 % 10 := by simp [output, carry]
  simp only [ScalarClock.step, ← he, ← hh, ← hl]
  by_cases hz : carry q L = 0
  · simp only [hz, if_true, nextColumns, columnSum, reflected, Nat.sub_zero]
  · have hone : carry q L = 1 := by
      have hb := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
      omega
    simp only [hz, if_false, nextColumns, columnSum, reflected,
      Nat.add_sub_cancel, Nat.sub_zero, extended, hL, Nat.lt_irrefl,
      if_true, if_false, hone]

theorem actual_scalar_step (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    (nextColumns q L 0, carry q L) = ScalarClock.step (q 0) (actualControl q L) :=
  scalar_step_exact q L (actualControl q L) ha (actualControl_exact q L ha)

/-- Merely occupying a scalar-clock phase already determines the overflow. -/
theorem overflow_of_phase (q : Nat → Nat) (L s : Nat)
    (ha : Admissible L q) (hp : q 0 = ScalarClock.phase s) :
    carry q L = ScalarClock.overflow s := by
  have he := congrArg Prod.snd (actual_scalar_step q L ha)
  rw [hp] at he
  exact he.trans (ScalarClock.step_overflow_phase s (actualControl q L))

/-- Following the next scalar phase is equivalent to a condition on the
actual whole-word carry, not a freely selected Boolean input. -/
theorem next_phase_iff_actual_control (q : Nat → Nat) (L s : Nat)
    (ha : Admissible L q) (hp : q 0 = ScalarClock.phase s) :
    nextColumns q L 0 = ScalarClock.phase (s+1) ↔
      ScalarClock.allowed s (actualControl q L) := by
  have he := congrArg Prod.fst (actual_scalar_step q L ha)
  rw [hp] at he
  simp only [Prod.fst] at he
  rw [he]
  exact ScalarClock.step_follows_phase_iff s (actualControl q L)

end ActualScalar
