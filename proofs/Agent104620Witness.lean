import Agent124PrefixK

/-!
# A concrete twelve-step 620 witness (Agent #104)

The seed was discovered by a bounded bit-vector search. That search is not a
proof premise: all numerical facts below are reduced by the Lean kernel using
the unchanged ordinary decimal reverse-add operation. This module proves a
lower bound on any uniform ancestry bound; the separate 620 certificate supplies
the matching upper bound. No minimal seed or minimal width claim is made.
-/

namespace Agent104.Prefix620Witness

open Lychrel196 DecimalDigits Agent124.PrefixK

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def seed : Nat := 19014942070
def target : Nat := 62003033030026
def targetDigit (i : Nat) : Nat := (target / 10 ^ i) % 10

/-- Every iterate, including the time-zero seed, is checked in the kernel. -/
theorem exact_trajectory :
    (List.range 13).map (orbit seed) =
      [19014942070, 26039883161, 42178776223, 74446563347,
       148783127794, 646504515635, 1183019921281, 3004319025092,
       5909528159095, 11819046418190, 21000510510001,
       31002012010013, 62003033030026] := by
  decide +kernel

theorem twelve_steps : orbit seed 12 = target := by
  decide +kernel

/-- The fourteen-digit target has the actual canonical decimal representation. -/
theorem target_canonical : Canonical target targetDigit 14 := by
  refine ⟨by decide +kernel, ?_, by decide +kernel, by decide +kernel⟩
  intro i _hi
  unfold targetDigit
  have h := Nat.mod_lt (target / 10 ^ i) (by decide : 0 < 10)
  omega

/-- This is the same unchanged prefix predicate used by the upper-bound theorem. -/
theorem target_mem_family : PalStarts3 6 2 0 target := by
  refine ⟨by decide +kernel, targetDigit, 14, target_canonical,
    by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel⟩

/-- The displayed trajectory first reaches any palindrome at time twelve. -/
theorem first_hit_twelve :
    Palindrome (orbit seed 12) ∧ ∀ t, t < 12 → ¬ Palindrome (orbit seed t) := by
  have checked : ∀ t : Fin 12, ¬ Palindrome (orbit seed t.val) := by
    decide +kernel
  refine ⟨?_, fun t ht => checked ⟨t, ht⟩⟩
  rw [twelve_steps]
  exact target_mem_family.1

/-- A positive finite ordinary seed really attains the twelve-step target. -/
theorem realized_depth12 :
    ∃ A, 0 < A ∧ PalStarts3 6 2 0 (orbit A 12) := by
  refine ⟨seed, by decide +kernel, ?_⟩
  rw [twelve_steps]
  exact target_mem_family

/-- Every uniform bound for this exact target family is at least twelve. -/
theorem any_uniform_bound_ge12 (B : Nat)
    (hB : ∀ A P t, 0 < A → PalStarts3 6 2 0 P → orbit A t = P → t ≤ B) :
    12 ≤ B :=
  hB seed target 12 (by decide +kernel) target_mem_family twelve_steps

#print axioms exact_trajectory
#print axioms twelve_steps
#print axioms target_canonical
#print axioms target_mem_family
#print axioms first_hit_twelve
#print axioms realized_depth12
#print axioms any_uniform_bound_ge12

end Agent104.Prefix620Witness
