import P196.Agent1GroupIIIHandoff.Agent1GroupIIIHandoff
import P196.Agent1GroupIII.Agent1GroupIIINumeric

/-! Ordinary-integer interpretation of the sharp Group III second repair.
The original canonical digits, palindrome predicate, and reverse-add orbit
are unchanged. All claims concern the stated finite four-step horizon. -/

namespace P196.Agent1.GroupIIIHandoff

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DelayedOverlapGate

theorem numeric_time_two (n : Nat) (d : Nat → Nat) (r : Nat)
    (hr : 1 ≤ r) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r 1 10 6 i) :
    ∃ e, Canonical (orbit n 2) e (2*r+7) ∧
      ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = wholeTwo r i := by
  exact GroupIII.numeric_return n d r 1 10 6 (first_domain r hr) hc hrep

theorem numeric_time_three (n : Nat) (d : Nat → Nat) (r : Nat)
    (hr : 1 ≤ r) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r 1 10 6 i) :
    ∃ e, Canonical (orbit n 3) e (2*r+7) ∧
      ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = wholeThree r i := by
  obtain ⟨e, he, herep⟩ := iterPairs_representation n d (DelayedOverlapGate.initial r 1 10 6)
    (2*r+7) 3 hc hrep
  have hs := whole_time_three r hr
  rw [hs.1] at he herep
  exact ⟨e, he, fun i hi => (herep i hi).trans (hs.2 i hi)⟩

/-- Exact whole pair word and canonical width for every ordinary realization. -/
theorem numeric_time_four (n : Nat) (d : Nat → Nat) (r : Nat)
    (hr : 2 ≤ r) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r 1 10 6 i) :
    ∃ e, Canonical (orbit n 4) e (2*r+7) ∧
      ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = shiftOne (componentFour r) i := by
  obtain ⟨e, he, herep⟩ := iterPairs_representation n d (DelayedOverlapGate.initial r 1 10 6)
    (2*r+7) 4 hc hrep
  have hs := whole_time_four r hr
  rw [hs.1] at he herep
  exact ⟨e, he, fun i hi => (herep i hi).trans (hs.2 i hi)⟩

/-- The spacer threshold is exact also for the canonical ordinary time-four output. -/
theorem numeric_time_four_iff (n : Nat) (d : Nat → Nat) (r : Nat)
    (hr : 1 ≤ r) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r 1 10 6 i) :
    (∃ e, Canonical (orbit n 4) e (2*r+7) ∧
      ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = shiftOne (componentFour r) i) ↔ 2 ≤ r := by
  constructor
  · rintro ⟨e, he, heq⟩
    by_cases hn : 2 ≤ r
    · exact hn
    · have h1 : r=1 := by omega
      subst r
      have hb := columnSum_bounded e 9 he.2.1 1 (by decide)
      have hcol := heq 1 (by decide)
      have hbad : shiftOne (componentFour 1) 1 = 24 := by decide
      rw [hcol, hbad] at hb
      omega
  · intro hr2
    exact numeric_time_four n d r hr2 hc hrep

theorem numeric_four_step_safety (n : Nat) (d : Nat → Nat) (r : Nat)
    (hr : 2 ≤ r) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r 1 10 6 i) :
    ∀ t, 1 ≤ t → t ≤ 4 → ¬ Palindrome (orbit n t) := by
  have hs := GroupIII.numeric_two_step_safety n d r 1 10 6 (first_domain r (by omega)) hc hrep
  have h3 : ¬ Palindrome (orbit n 3) := by
    obtain ⟨e, he, herep⟩ := numeric_time_two n d r (by omega) hc hrep
    intro hp
    exact wholeTwo_not_bad r (by omega)
      ((PairDelayBridge.palindrome_iff_bad (orbit n 2) e (wholeTwo r) (2*r+7) he herep).mp hp)
  have h4 : ¬ Palindrome (orbit n 4) := by
    obtain ⟨e, he, herep⟩ := numeric_time_three n d r (by omega) hc hrep
    intro hp
    exact wholeThree_not_bad r (by omega)
      ((PairDelayBridge.palindrome_iff_bad (orbit n 3) e (wholeThree r) (2*r+7) he herep).mp hp)
  intro t ht htle
  have hcases : t=1 ∨ t=2 ∨ t=3 ∨ t=4 := by omega
  rcases hcases with rfl | rfl | rfl | rfl
  · exact hs.1
  · exact hs.2
  · exact h3
  · exact h4

theorem numeric_safe_handoff (n : Nat) (d : Nat → Nat) (r : Nat)
    (hr : 2 ≤ r) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r 1 10 6 i) :
    (∀ t, 1 ≤ t → t ≤ 4 → ¬ Palindrome (orbit n t)) ∧
      (∃ e, Canonical (orbit n 4) e (2*r+7) ∧
        ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = shiftOne (componentFour r) i) :=
  ⟨numeric_four_step_safety n d r hr hc hrep, numeric_time_four n d r hr hc hrep⟩

/-- Every permitted spacer has a positive ordinary realization of the safe handoff. -/
theorem realized_safe_handoff (r : Nat) (hr : 2 ≤ r) :
    ∃ n d, 0 < n ∧ Canonical n d (2*r+7) ∧
      (∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r 1 10 6 i) ∧
      (∀ t, 1 ≤ t → t ≤ 4 → ¬ Palindrome (orbit n t)) ∧
      (∃ e, Canonical (orbit n 4) e (2*r+7) ∧
        ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = shiftOne (componentFour r) i) := by
  obtain ⟨n, d, hn, hc, hrep, _⟩ := GroupIII.realized_safe_gate r 1 10 6 (first_domain r (by omega))
  exact ⟨n, d, hn, hc, hrep, numeric_safe_handoff n d r hr hc hrep⟩

end P196.Agent1.GroupIIIHandoff
