import P196.Drafts.Agent106CongruenceCarryBudget.Agent106CarryBudget

set_option autoImplicit false

/-!
# Unbounded outgoing carry counts on ordinary decimal orbits

The numerical count below is proved equal to the existing sum of the actual
outgoing carries, including the terminal carry, for every canonical decimal
representation. It is not a count of the times at which the width increases.

If the digit sum exceeds 9 * B + 9 at a state of width L, some one-step carry
count exceeds B in the first 2 * L + 3 steps. Combining this with the existing
finite digit-sum escape theorem gives a computable carry-count escape window
after every starting time on every positive ordinary orbit, including 196.

The ordinary orbit continues after a palindrome. No palindrome-avoidance,
Lychrel-existence, optimal-window, or carry-density conclusion is claimed.
-/

namespace CarryCountGrowth

open Lychrel196 DecimalDigits DecimalMass DecimalQuantitativeMass

/-- Number of outgoing decimal carry positions in one reverse-and-add step.
The identification with the literal column count is proved below. -/
def outgoingCarryCount (n : Nat) : Nat :=
  (2 * digitSum n - digitSum (step n)) / 9

theorem outgoingCarryCount_zero : outgoingCarryCount 0 = 0 := by
  simp [outgoingCarryCount, step, reverse10, reverseFuel, digitSum_zero]

/-- The numerical count agrees with every canonical column representation;
in particular, it counts the terminal outgoing carry when one is present. -/
theorem outgoingCarryCount_of_canonical
    (n : Nat) (d : Nat → Nat) (L : Nat) (hc : Canonical n d L) :
    outgoingCarryCount n = carryCount (columnSum d L) L := by
  have hb := digitSum_step_balance d L hc.2.1 (Or.inr hc.2.2.1)
  rw [hc.2.2.2] at hb
  unfold outgoingCarryCount
  omega

/-- Exact numerical mass balance, including the zero state. -/
theorem outgoingCarryCount_balance (n : Nat) :
    digitSum (step n) + 9 * outgoingCarryCount n = 2 * digitSum n := by
  by_cases hn : n = 0
  · subst n
    simp [step, reverse10, reverseFuel, digitSum_zero, outgoingCarryCount_zero]
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    have hb := digitSum_step_balance d L hc.2.1 (Or.inr hc.2.2.1)
    rw [hc.2.2.2] at hb
    rw [outgoingCarryCount_of_canonical n d L hc]
    exact hb

/-- There is at most one outgoing carry per input digit. -/
theorem outgoingCarryCount_le_decimalLength (n : Nat) :
    outgoingCarryCount n ≤ decimalLength n := by
  by_cases hn : n = 0
  · subst n
    simp [outgoingCarryCount_zero, decimalLength_zero]
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    rw [outgoingCarryCount_of_canonical n d L hc,
      decimalLength_of_canonical n d L hc]
    exact Agent106.CongruenceBudget.carryCount_le_width (columnSum d L) L
      (columnSum_bounded d L hc.2.1)

/-- A direct digit-sum consequence of the existing upper bound on actual
canonical width. The starting width, rather than a guessed width, is used. -/
theorem digitSum_twice_upper_bound_of_canonical
    (n : Nat) (d : Nat → Nat) (L t : Nat) (hc : Canonical n d L) :
    2 * digitSum (orbit n t) ≤ 18 * L + 9 * t + 27 := by
  obtain ⟨e, W, he, _, hwidth⟩ :=
    DecimalWidthGrowth.numeric_width_bounds n d L t hc
  have hsum := Agent106.CongruenceBudget.wordSum_le_constant e W 9 he.2.1
  have hdigit : digitSum (orbit n t) = wordSum e W := by
    rw [← he.2.2.2, digitSum_value e W he.2.1]
  rw [← hdigit] at hsum
  omega

/-- A large digit sum forces a carry-count escape within a finite interval.
The interval bounds the input time of the step whose carries are counted. -/
theorem outgoingCarryCount_escape_of_large_digitSum
    (n : Nat) (d : Nat → Nat) (L B : Nat)
    (hc : Canonical n d L) (hlarge : 9 * B + 9 < digitSum n) :
    ∃ t, t < 2 * L + 3 ∧ B < outgoingCarryCount (orbit n t) := by
  apply Classical.byContradiction
  intro hnone
  have hcount : ∀ t, t < 2 * L + 3 → outgoingCarryCount (orbit n t) ≤ B := by
    intro t ht
    exact Nat.le_of_not_gt (fun hgt => hnone ⟨t, ht, hgt⟩)
  have hlower : ∀ t, t ≤ 2 * L + 3 →
      digitSum n + 10 * t ≤ digitSum (orbit n t) := by
    intro t
    induction t with
    | zero =>
        intro _
        simp [orbit]
    | succ t ih =>
        intro ht
        have hprev := ih (by omega)
        have hcarries := hcount t (by omega)
        have hbalance := outgoingCarryCount_balance (orbit n t)
        change digitSum (orbit n (t + 1)) +
          9 * outgoingCarryCount (orbit n t) = 2 * digitSum (orbit n t) at hbalance
        omega
  have hlow := hlower (2 * L + 3) (by omega)
  have hupp := digitSum_twice_upper_bound_of_canonical n d L (2 * L + 3) hc
  omega

/-- A computable carry-count escape horizon depending on the current actual
width and the requested count threshold. The digit-sum horizon is unchanged. -/
def outgoingCarryEscapeBound (L B : Nat) : Nat :=
  2 * L + 2 * DecimalQuantitativeMass.escapeBound L (9 * B + 9) + 6

/-- Every canonical positive seed exceeds a prescribed carry-count threshold
within the displayed finite horizon, without an initial digit-sum premise. -/
theorem outgoingCarryCount_escape_of_canonical
    (n : Nat) (d : Nat → Nat) (L B : Nat) (hc : Canonical n d L) :
    ∃ t, t < outgoingCarryEscapeBound L B ∧
      B < outgoingCarryCount (orbit n t) := by
  obtain ⟨j, hj, hlarge⟩ :=
    DecimalQuantitativeMass.digitSum_escape_of_canonical n d L (9 * B + 9) hc
  obtain ⟨e, W, he, _, hwidth⟩ :=
    DecimalWidthGrowth.numeric_width_bounds n d L j hc
  obtain ⟨k, hk, hcarry⟩ := outgoingCarryCount_escape_of_large_digitSum
    (orbit n j) e W B he hlarge
  refine ⟨j + k, ?_, ?_⟩
  · unfold outgoingCarryEscapeBound
    omega
  · rw [LychrelCertificates.orbit_add]
    exact hcarry

/-- A fully numerical version of the finite carry-count escape theorem. -/
theorem outgoingCarryCount_escape (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t < outgoingCarryEscapeBound (decimalLength n) B ∧
      B < outgoingCarryCount (orbit n t) := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  rw [decimalLength_of_canonical n d L hc]
  exact outgoingCarryCount_escape_of_canonical n d L B hc

/-- The finite horizon restarts at any requested orbit time and uses the
actual decimal width at that time. -/
theorem outgoingCarryCount_window
    (n : Nat) (hn : 0 < n) (B start : Nat) :
    ∃ t, start ≤ t ∧
      t < start + outgoingCarryEscapeBound (decimalLength (orbit n start)) B ∧
      B < outgoingCarryCount (orbit n t) := by
  obtain ⟨k, hk, hcarry⟩ := outgoingCarryCount_escape
    (orbit n start) (orbit_positive n hn start) B
  refine ⟨start + k, by omega, by omega, ?_⟩
  rw [LychrelCertificates.orbit_add]
  exact hcarry

/-- Every positive ordinary decimal orbit has arbitrarily large one-step
carry counts after every starting time. -/
theorem outgoingCarryCount_unbounded_after
    (n : Nat) (hn : 0 < n) (B start : Nat) :
    ∃ t, start ≤ t ∧ B < outgoingCarryCount (orbit n t) := by
  obtain ⟨t, ht, _, hcarry⟩ := outgoingCarryCount_window n hn B start
  exact ⟨t, ht, hcarry⟩

/-- A positive ordinary orbit cannot eventually impose a fixed upper bound
on the number of outgoing carry positions in each step. -/
theorem not_eventually_bounded_outgoingCarryCount (n : Nat) (hn : 0 < n) :
    ¬ ∃ start B, ∀ t, start ≤ t → outgoingCarryCount (orbit n t) ≤ B := by
  rintro ⟨start, B, hbound⟩
  obtain ⟨t, ht, hlarge⟩ := outgoingCarryCount_unbounded_after n hn B start
  have hsmall := hbound t ht
  omega

/-- The actual orbit of 196 has arbitrarily large one-step carry counts,
independently of whether a palindrome ever appears. -/
theorem outgoingCarryCount_196_unbounded_after (B start : Nat) :
    ∃ t, start ≤ t ∧ B < outgoingCarryCount (orbit 196 t) :=
  outgoingCarryCount_unbounded_after 196 (by decide) B start

end CarryCountGrowth

#print axioms CarryCountGrowth.outgoingCarryCount_of_canonical
#print axioms CarryCountGrowth.outgoingCarryCount_balance
#print axioms CarryCountGrowth.outgoingCarryCount_le_decimalLength
#print axioms CarryCountGrowth.digitSum_twice_upper_bound_of_canonical
#print axioms CarryCountGrowth.outgoingCarryCount_escape_of_large_digitSum
#print axioms CarryCountGrowth.outgoingCarryCount_escape_of_canonical
#print axioms CarryCountGrowth.outgoingCarryCount_escape
#print axioms CarryCountGrowth.outgoingCarryCount_window
#print axioms CarryCountGrowth.outgoingCarryCount_unbounded_after
#print axioms CarryCountGrowth.not_eventually_bounded_outgoingCarryCount
#print axioms CarryCountGrowth.outgoingCarryCount_196_unbounded_after
