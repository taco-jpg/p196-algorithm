import P196.Agent1Pr104Repair.DelayedOverlapGate

/-!
Agent #114 / independent session s2124Z. WIP Lean 4.19.0 candidate.
UNCOMPILED, UNAUDITED. No theorem here is accepted unless it actually builds
with the original project sources and the transitive axiom audit passes.

Previously recorded finite observation: renewal_pass/tails/STATUS.md (u,v,r)=(1,7,3).
No mathematical novelty claim is attached to its rediscovery.

The numerical scripts verify exact finite arithmetic; they do not certify Lean.
The proof attempt retains original Lychrel196.step/orbit/Palindrome and
FoldedDecimal.Canonical, and uses the proven original numeric pair-sum bridge.
-/
namespace Agent114.Core17R3

open Lychrel196 DecimalDigits FoldedDecimal DelayedOverlapGate DecimalDelayBridge

set_option maxHeartbeats 10000000
set_option maxRecDepth 4096

/-- Target: the fixed r=3 case, every original 13-digit canonical realization. -/
def UniversalFirstHit11 : Prop :=
  ∀ (n : Nat) (d : Nat → Nat), Canonical n d 13 →
    (∀ i, i < 13 → columnSum d 13 i = DelayedOverlapGate.initial 3 1 1 7 i) →
    FirstPositiveHit n 11

/-- Proposed concrete kernel proof. One verified numeric first image gives
    the entire common positive tail, independently of the digit split. -/
theorem universal_first_hit_11 (n : Nat) (d : Nat → Nat)
    (hc : Canonical n d 13)
    (hr : ∀ i, i < 13 →
      columnSum d 13 i = DelayedOverlapGate.initial 3 1 1 7 i) :
    FirstPositiveHit n 11 := by
  have hstep : Lychrel196.step n = 1100194810011 := by
    rw [FoldedDecimal.step_eq_word_value n d
      (DelayedOverlapGate.initial 3 1 1 7) 13 hc hr]
    decide
  refine ⟨by decide, ?_, ?_⟩
  · rw [← Lychrel196.orbit_from_step n 10, hstep]
    decide
  · intro k hk0 hk11
    obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : k ≠ 0)
    have hj : j < 10 := by omega
    have cases :
      j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 ∨
      j = 5 ∨ j = 6 ∨ j = 7 ∨ j = 8 ∨ j = 9 := by omega
    rw [← Lychrel196.orbit_from_step n j, hstep]
    rcases cases with h | h | h | h | h | h | h | h | h | h
    all_goals
      subst j
      decide

/-- Proposed concrete existence via the ORIGINAL gate's positive realizability.
    This is a new conclusion about core(1,7), not an infinite-safe family. -/
theorem exists_realized_first_hit_11 :
    ∃ n d, 0 < n ∧ Canonical n d 13 ∧
      (∀ i, i < 13 → columnSum d 13 i =
        DelayedOverlapGate.initial 3 1 1 7 i) ∧
      FirstPositiveHit n 11 := by
  have hd : DelayedOverlapGate.Domain 3 1 1 7 := by
    unfold DelayedOverlapGate.Domain
    omega
  obtain ⟨n, d, hn, hc, hr, _⟩ :=
    DelayedOverlapGate.realized_safe_gate 3 1 1 7 hd
  exact ⟨n, d, hn, hc, hr, universal_first_hit_11 n d hc hr⟩

-- Source is intentionally WIP outside the accepted build until a real
-- Lean4.19.0 author rebuild, source-hash lock and independent axiom audit.
#print axioms Agent114.Core17R3.universal_first_hit_11
#print axioms Agent114.Core17R3.exists_realized_first_hit_11

end Agent114.Core17R3
