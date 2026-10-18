import P196.Drafts.D20261015ScalarClockFormalActualScalar.ActualScalar

/-! Scalar-clock arithmetic along the actual whole-word orbit, at arbitrary
start times and phases. No numerical graph bound is assumed as proved. -/

namespace ScalarOrbit

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

def widthAt (q : Nat → Nat) (L t : Nat) : Nat := (iterPairs q L t).1
def outerAt (q : Nat → Nat) (L t : Nat) : Nat := (iterPairs q L t).2 0
def controlAt (q : Nat → Nat) (L t : Nat) : Bool :=
  ActualScalar.actualControl (iterPairs q L t).2 (iterPairs q L t).1
def overflowAt (q : Nat → Nat) (L t : Nat) : Nat :=
  carry (iterPairs q L t).2 (iterPairs q L t).1

/-- Both endpoints are included. The prescribed phase is relative to a. -/
def ClockSegment (q : Nat → Nat) (L a s n : Nat) : Prop :=
  ∀ i, i ≤ n → outerAt q L (a+i) = ScalarClock.phase (s+i)

theorem widthAt_lower (q : Nat → Nat) (L t : Nat) : L ≤ widthAt q L t := by
  induction t with
  | zero => exact Nat.le_refl _
  | succ t ih =>
    change L ≤ nextWidth (iterPairs q L t).2 (iterPairs q L t).1
    unfold nextWidth
    change L ≤ (iterPairs q L t).1 at ih
    split <;> omega

theorem actual_step_at (q : Nat → Nat) (L t : Nat) (ha : Admissible L q) :
    (outerAt q L (t+1), overflowAt q L t) =
      ScalarClock.step (outerAt q L t) (controlAt q L t) :=
  ActualScalar.actual_scalar_step (iterPairs q L t).2 (iterPairs q L t).1
    (iterPairs_admissible q L t ha)

theorem overflow_at_of_phase (q : Nat → Nat) (L t s : Nat)
    (ha : Admissible L q) (hp : outerAt q L t = ScalarClock.phase s) :
    overflowAt q L t = ScalarClock.overflow s :=
  ActualScalar.overflow_of_phase (iterPairs q L t).2 (iterPairs q L t).1 s
    (iterPairs_admissible q L t ha) hp

theorem follows_phase_iff_actual_control (q : Nat → Nat) (L t s : Nat)
    (ha : Admissible L q) (hp : outerAt q L t = ScalarClock.phase s) :
    outerAt q L (t+1) = ScalarClock.phase (s+1) ↔
      ScalarClock.allowed s (controlAt q L t) :=
  ActualScalar.next_phase_iff_actual_control (iterPairs q L t).2
    (iterPairs q L t).1 s (iterPairs_admissible q L t ha) hp

theorem widthAt_succ (q : Nat → Nat) (L t : Nat) (ha : Admissible L q) :
    widthAt q L (t+1) = widthAt q L t + overflowAt q L t := by
  have had := iterPairs_admissible q L t ha
  have hb := carry_bounded (iterPairs q L t).2 (iterPairs q L t).1 had.2.2.1
    (iterPairs q L t).1 (Nat.le_refl _)
  change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 =
    (iterPairs q L t).1 + carry (iterPairs q L t).2 (iterPairs q L t).1
  unfold nextWidth
  split <;> omega

/-- The exact scalar clock increases actual width by three in every
seven-step rotation, at any time offset. -/
theorem seven_width_of_clock (q : Nat → Nat) (L a s : Nat)
    (ha : Admissible L q) (hc : ClockSegment q L a s 7) :
    widthAt q L (a+7) = widthAt q L a + 3 := by
  have hh : ∀ i, i < 7 → widthAt q L (a+(i+1)) =
      widthAt q L (a+i) + ScalarClock.overflow (s+i) := by
    intro i hi
    have h := widthAt_succ q L (a+i) ha
    rw [overflow_at_of_phase q L (a+i) (s+i) ha (hc i (by omega))] at h
    simpa only [Nat.add_assoc] using h
  have h0 := hh 0 (by decide)
  have h1 := hh 1 (by decide)
  have h2 := hh 2 (by decide)
  have h3 := hh 3 (by decide)
  have h4 := hh 4 (by decide)
  have h5 := hh 5 (by decide)
  have h6 := hh 6 (by decide)
  have hs := ScalarClock.seven_overflow_sum s
  simp only [Nat.add_zero, Nat.reduceAdd] at h0 h1 h2 h3 h4 h5 h6
  omega

theorem periods_width_of_clock (q : Nat → Nat) (L a s R : Nat)
    (ha : Admissible L q) (hc : ClockSegment q L a s (7*R)) :
    widthAt q L (a+7*R) = widthAt q L a + 3*R := by
  induction R with
  | zero => simp
  | succ R ih =>
    have hshort : ClockSegment q L a s (7*R) := fun i hi => hc i (by omega)
    have hi := ih hshort
    have hblock : ClockSegment q L (a+7*R) (s+7*R) 7 := by
      intro i ht
      have h := hc (7*R+i) (by omega)
      simpa only [Nat.add_assoc] using h
    have hb := seven_width_of_clock q L (a+7*R) (s+7*R) ha hblock
    have he : a+7*(R+1) = (a+7*R)+7 := by omega
    rw [he, hb, hi]
    omega

theorem initial_periods_width (q : Nat → Nat) (L s R : Nat)
    (ha : Admissible L q) (hc : ClockSegment q L 0 s (7*R)) :
    widthAt q L (7*R) = L + 3*R := by
  have h := periods_width_of_clock q L 0 s R ha hc
  simpa only [Nat.zero_add] using h

/-- Complete periods needed to reach width fourteen, with truncated Nat subtraction. -/
def warmup (L : Nat) : Nat := (14-L+2)/3

theorem warmup_at_most_four (L : Nat) (hL : 2 ≤ L) : warmup L ≤ 4 := by
  unfold warmup
  omega

theorem warmup_width_arithmetic (L : Nat) : 14 ≤ L + 3*warmup L := by
  unfold warmup
  omega

theorem warmup_reaches_fourteen (q : Nat → Nat) (L s : Nat)
    (ha : Admissible L q) (hc : ClockSegment q L 0 s (7*warmup L)) :
    14 ≤ widthAt q L (7*warmup L) := by
  rw [initial_periods_width q L s (warmup L) ha hc]
  exact warmup_width_arithmetic L

/-- Conditional transfer of an independently supplied wide-word bound.
The wide-word numerical graph theorem remains an explicit premise. -/
theorem period_bound_after_warmup (q : Nat → Nat) (L s R B : Nat)
    (ha : Admissible L q) (hc : ClockSegment q L 0 s (7*R))
    (hwide : ∀ a phase periods, 14 ≤ widthAt q L a →
      ClockSegment q L a phase (7*periods) → periods ≤ B) :
    R ≤ B + warmup L := by
  by_cases hr : R < warmup L
  · omega
  · have hshort : ClockSegment q L 0 s (7*warmup L) :=
      fun i hi => hc i (by omega)
    have hw := warmup_reaches_fourteen q L s ha hshort
    have htail : ClockSegment q L (7*warmup L) (s+7*warmup L)
        (7*(R-warmup L)) := by
      intro i hi
      have h := hc (7*warmup L+i) (by omega)
      simpa only [Nat.zero_add, Nat.add_assoc] using h
    have hb := hwide (7*warmup L) (s+7*warmup L) (R-warmup L) hw htail
    omega

theorem uniform_period_bound_of_wide_bound (q : Nat → Nat) (L s R B : Nat)
    (hL : 2 ≤ L) (ha : Admissible L q) (hc : ClockSegment q L 0 s (7*R))
    (hwide : ∀ a phase periods, 14 ≤ widthAt q L a →
      ClockSegment q L a phase (7*periods) → periods ≤ B) : R ≤ B+4 := by
  have hb := period_bound_after_warmup q L s R B ha hc hwide
  have hk := warmup_at_most_four L hL
  omega

/-- Canonical decimal digits supply the actual-word hypotheses for the
exact width formula; no graph bound is introduced. -/
theorem periods_width_of_canonical (n : Nat) (d q : Nat → Nat) (L s R : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hclock : ClockSegment q L 0 s (7*R)) : widthAt q L (7*R) = L+3*R := by
  have ha : Admissible L q := NormalizationBridge.admissible_congr _ _ _
    (NormalizationBridge.canonical_admissible n d L hc) hrep
  exact initial_periods_width q L s R ha hclock

/-- The width formula is the exact decimal length of the actual numeric
iterate represented by the canonical initial digits. -/
theorem decimalLength_of_clock (n : Nat) (d q : Nat → Nat) (L s R : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hclock : ClockSegment q L 0 s (7*R)) :
    DecimalQuantitativeMass.decimalLength (Lychrel196.orbit n (7*R)) = L+3*R := by
  obtain ⟨e, he, _⟩ := iterPairs_representation n d q L (7*R) hc hrep
  have hw := periods_width_of_canonical n d q L s R hc hrep hclock
  change (iterPairs q L (7*R)).1 = L+3*R at hw
  rw [hw] at he
  exact DecimalQuantitativeMass.decimalLength_of_canonical _ e _ he

end ScalarOrbit
