import Agent1GroupIII

/-! Actual ordinary-integer realization of the Group III delayed repair.
All representations use the original canonical-digit and reverse-add definitions.
No infinite-time, first-hit, or recurrence claim is made. -/

namespace P196.Agent1.GroupIII

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DelayedOverlapGate

theorem numeric_middle (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r p u v i) :
    ∃ e, Canonical (orbit n 1) e (2*r+7) ∧
      ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = middle r p u v i := by
  have hw : nextWidth (DelayedOverlapGate.initial r p u v) (2*r+7) = 2*r+7 := by
    simp only [nextWidth, initial_no_overflow r p u v h, if_true]
  obtain ⟨e, he, herep⟩ := representation_next n d (DelayedOverlapGate.initial r p u v)
    (2*r+7) hc hrep
  rw [hw] at he herep
  exact ⟨e, he, fun i hi => (herep i hi).trans (initial_next r p u v h i hi)⟩

/-- Every canonical realization has the claimed entire pair word at time two. -/
theorem numeric_return (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r p u v i) :
    ∃ e, Canonical (orbit n 2) e (2*r+7) ∧
      ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = shiftOne (returnedComponent r p u v) i := by
  obtain ⟨e, he, herep⟩ := numeric_middle n d r p u v h hc hrep
  have hw : nextWidth (middle r p u v) (2*r+7) = 2*r+7 := by
    simp only [nextWidth, middle_no_overflow r p u v h, if_true]
  obtain ⟨f, hf, hfrep⟩ := representation_next (orbit n 1) e (middle r p u v)
    (2*r+7) he herep
  rw [hw] at hf hfrep
  exact ⟨f, hf, fun i hi => (hfrep i hi).trans (middle_next r p u v h i hi)⟩

/-- Both positive ordinary outputs are nonpalindromic, for every realization. -/
theorem numeric_two_step_safety (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r p u v i) :
    ¬ Palindrome (orbit n 1) ∧ ¬ Palindrome (orbit n 2) := by
  constructor
  · intro hp
    exact initial_not_bad r p u v h
      ((PairDelayBridge.palindrome_iff_bad n d (DelayedOverlapGate.initial r p u v)
        (2*r+7) hc hrep).mp hp)
  · obtain ⟨e, he, herep⟩ := numeric_middle n d r p u v h hc hrep
    intro hp
    exact middle_not_bad r p u v h
      ((PairDelayBridge.palindrome_iff_bad (orbit n 1) e (middle r p u v)
        (2*r+7) he herep).mp hp)

/-- All-realizations Group III delayed return, including both positive-time safety claims. -/
theorem numeric_delayed_return (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r p u v i) :
    ¬ Palindrome (orbit n 1) ∧ ¬ Palindrome (orbit n 2) ∧
      (∃ e, Canonical (orbit n 2) e (2*r+7) ∧
        ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = shiftOne (returnedComponent r p u v) i) := by
  have hs := numeric_two_step_safety n d r p u v h hc hrep
  exact ⟨hs.1, hs.2, numeric_return n d r p u v h hc hrep⟩

/-- Nonvacuous ordinary realization of every Group III parameter tuple. -/
theorem realized_safe_gate (r p u v : Nat) (h : Domain r p u v) :
    ∃ n d, 0 < n ∧ Canonical n d (2*r+7) ∧
      (∀ i, i < 2*r+7 → columnSum d (2*r+7) i = DelayedOverlapGate.initial r p u v i) ∧
      ¬ Palindrome (orbit n 1) ∧ ¬ Palindrome (orbit n 2) ∧
      (∃ e, Canonical (orbit n 2) e (2*r+7) ∧
        ∀ i, i < 2*r+7 → columnSum e (2*r+7) i = shiftOne (returnedComponent r p u v) i) := by
  have ha := initial_admissible r p u v h
  obtain ⟨n, d, hn, hc, hrep⟩ := valid_word_realizable (DelayedOverlapGate.initial r p u v)
    (2*r+7) ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  have hs := numeric_two_step_safety n d r p u v h hc hrep
  exact ⟨n, d, hn, hc, hrep, hs.1, hs.2, numeric_return n d r p u v h hc hrep⟩

end P196.Agent1.GroupIII
