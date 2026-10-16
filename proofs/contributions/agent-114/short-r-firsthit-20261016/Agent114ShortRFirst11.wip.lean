import DelayedOverlapGate

/-!
Agent #114: WIP kernel-checkable short-spacer first-eleven proposition.
These declarations have NOT been compiled in this author session. Source publication is
not LEAN-CHECKED, no axiom audit has been performed, and no infinite-time claim follows.
The original imports, Canonical, decimal step and pair-word semantics are unchanged.
Unlike the finite 3000-step Python experiment, these are proposed Lean proof scripts
for the first 11 positive steps, requiring Lean 4.19.0 compile and independent review.
-/

namespace Agent114.ShortR

open Lychrel196 DecimalDigits FoldedDecimal DelayedOverlapGate

set_option maxHeartbeats 10000000
set_option maxRecDepth 4096

/-- Reuses the ORIGINAL verified arithmetic bridge for every canonical splitting. -/
theorem common_first_step (r n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = DelayedOverlapGate.initial r 1 1 6 i) :
    Lychrel196.step n =
      DecimalDigits.value (DelayedOverlapGate.initial r 1 1 6) (2 * r + 7) :=
  FoldedDecimal.step_eq_word_value n d
    (DelayedOverlapGate.initial r 1 1 6) (2 * r + 7) hc hr

/-- Proposed universal r=1 first-eleven nonpalindromicity, NOT YET COMPILED.
Every input has the same positive tail after the common first reverse-add value. -/
theorem r1_first_eleven (n : Nat) (d : Nat → Nat)
    (hc : Canonical n d 9)
    (hr : ∀ i, i < 9 →
      columnSum d 9 i = DelayedOverlapGate.initial 1 1 1 6 i) :
    ∀ t : Nat, 1 ≤ t → t ≤ 11 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  intro t hpos htop
  have hstep : Lychrel196.step n = 111827111 := by
    rw [common_first_step 1 n d hc hr]
    decide
  obtain ⟨k, rfl⟩ :=
    Nat.exists_eq_succ_of_ne_zero (by omega : t ≠ 0)
  have hk : k < 11 := by omega
  have hcases : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 ∨ k = 7 ∨ k = 8 ∨ k = 9 ∨ k = 10 := by omega
  rw [← Lychrel196.orbit_from_step n k, hstep]
  rcases hcases with h | h | h | h | h | h | h | h | h | h | h
  all_goals
    subst k
    decide

/-- Proposed universal r=2 first-eleven nonpalindromicity, NOT YET COMPILED.
Every input has the same positive tail after the common first reverse-add value. -/
theorem r2_first_eleven (n : Nat) (d : Nat → Nat)
    (hc : Canonical n d 11)
    (hr : ∀ i, i < 11 →
      columnSum d 11 i = DelayedOverlapGate.initial 2 1 1 6 i) :
    ∀ t : Nat, 1 ≤ t → t ≤ 11 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  intro t hpos htop
  have hstep : Lychrel196.step n = 11018271011 := by
    rw [common_first_step 2 n d hc hr]
    decide
  obtain ⟨k, rfl⟩ :=
    Nat.exists_eq_succ_of_ne_zero (by omega : t ≠ 0)
  have hk : k < 11 := by omega
  have hcases : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 ∨ k = 7 ∨ k = 8 ∨ k = 9 ∨ k = 10 := by omega
  rw [← Lychrel196.orbit_from_step n k, hstep]
  rcases hcases with h | h | h | h | h | h | h | h | h | h | h
  all_goals
    subst k
    decide

/-- Proposed universal r=3 first-eleven nonpalindromicity, NOT YET COMPILED.
Every input has the same positive tail after the common first reverse-add value. -/
theorem r3_first_eleven (n : Nat) (d : Nat → Nat)
    (hc : Canonical n d 13)
    (hr : ∀ i, i < 13 →
      columnSum d 13 i = DelayedOverlapGate.initial 3 1 1 6 i) :
    ∀ t : Nat, 1 ≤ t → t ≤ 11 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  intro t hpos htop
  have hstep : Lychrel196.step n = 1100182710011 := by
    rw [common_first_step 3 n d hc hr]
    decide
  obtain ⟨k, rfl⟩ :=
    Nat.exists_eq_succ_of_ne_zero (by omega : t ≠ 0)
  have hk : k < 11 := by omega
  have hcases : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 ∨ k = 7 ∨ k = 8 ∨ k = 9 ∨ k = 10 := by omega
  rw [← Lychrel196.orbit_from_step n k, hstep]
  rcases hcases with h | h | h | h | h | h | h | h | h | h | h
  all_goals
    subst k
    decide

/-- Proposed universal r=4 first-eleven nonpalindromicity, NOT YET COMPILED.
Every input has the same positive tail after the common first reverse-add value. -/
theorem r4_first_eleven (n : Nat) (d : Nat → Nat)
    (hc : Canonical n d 15)
    (hr : ∀ i, i < 15 →
      columnSum d 15 i = DelayedOverlapGate.initial 4 1 1 6 i) :
    ∀ t : Nat, 1 ≤ t → t ≤ 11 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit n t) := by
  intro t hpos htop
  have hstep : Lychrel196.step n = 110001827100011 := by
    rw [common_first_step 4 n d hc hr]
    decide
  obtain ⟨k, rfl⟩ :=
    Nat.exists_eq_succ_of_ne_zero (by omega : t ≠ 0)
  have hk : k < 11 := by omega
  have hcases : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 ∨ k = 7 ∨ k = 8 ∨ k = 9 ∨ k = 10 := by omega
  rw [← Lychrel196.orbit_from_step n k, hstep]
  rcases hcases with h | h | h | h | h | h | h | h | h | h | h
  all_goals
    subst k
    decide

-- The longer r≥5 exact first-positive-hit time 11 belongs to Agent #2.
-- The four r≤4 tails after the finite horizon remain unknown; no IsLychrel theorem.
-- No use of sorry, admit, native_decide, custom axioms, or external oracles.

#print axioms Agent114.ShortR.common_first_step
#print axioms Agent114.ShortR.r1_first_eleven
#print axioms Agent114.ShortR.r2_first_eleven
#print axioms Agent114.ShortR.r3_first_eleven
#print axioms Agent114.ShortR.r4_first_eleven

end Agent114.ShortR
