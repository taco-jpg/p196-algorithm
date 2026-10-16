import CertificateSaturation
import SaturationTheorem

/-!
Agent #215 — saturated temporal/column profile.

WIP target: strengthen the existing saturation theorem. The existing
potential argument already forces an 8-step clock progression in the
saturated case. The concrete eight clock states below form the resulting
temporal skeleton. This file deliberately does not label the global target
proved: the generic extraction from the clock recurrence and the saturation
count still needs a kernel-checked proof.

This is complementary to Agent #15's six-phase profile: this file is about
the stronger saturated eight-step temporal/column skeleton and the exact
input constraints on its eight concrete states.
-/

namespace Agent215.Saturated8

open P196.Agent4.Saturation

def cycleState : Nat → Prefix :=
  fun k =>
    match k % 8 with
    | 0 => ⟨8,12,9⟩
    | 1 => ⟨17,5,0⟩
    | 2 => ⟨8,13,5⟩
    | 3 => ⟨17,6,11⟩
    | 4 => ⟨8,14,8⟩
    | 5 => ⟨17,8,17⟩
    | 6 => ⟨8,16,16⟩
    | _ => ⟨17,13,14⟩

theorem edge0 : advance ⟨8,12,9⟩ 1 = (⟨17,5,0⟩, 0) := by decide
theorem edge1_0 : advance ⟨17,5,0⟩ 0 = (⟨8,13,5⟩, 1) := by decide
theorem edge1_1 : advance ⟨17,5,0⟩ 1 = (⟨8,13,5⟩, 1) := by decide
theorem edge2 : advance ⟨8,13,5⟩ 0 = (⟨17,6,11⟩, 0) := by decide
theorem edge3_0 : advance ⟨17,6,11⟩ 0 = (⟨8,14,8⟩, 1) := by decide
theorem edge3_1 : advance ⟨17,6,11⟩ 1 = (⟨8,14,8⟩, 1) := by decide
theorem edge4 : advance ⟨8,14,8⟩ 0 = (⟨17,8,17⟩, 0) := by decide
theorem edge5_0 : advance ⟨17,8,17⟩ 0 = (⟨8,16,16⟩, 1) := by decide
theorem edge5_1 : advance ⟨17,8,17⟩ 1 = (⟨8,16,16⟩, 1) := by decide
theorem edge6 : advance ⟨8,16,16⟩ 1 = (⟨17,13,14⟩, 0) := by decide
theorem edge7_0 : advance ⟨17,13,14⟩ 0 = (⟨8,12,9⟩, 1) := by decide
theorem edge7_1 : advance ⟨17,13,14⟩ 1 = (⟨8,12,9⟩, 1) := by decide

def ForcedOverflowPattern (e : Fin 8 → Nat) : Prop :=
  e 0 = 1 ∧ e 2 = 0 ∧ e 4 = 0 ∧ e 6 = 1

def EveryEdgeTight (s : Nat → Prefix) (e : Nat → Nat) (n : Nat) : Prop :=
  ∀ i < n,
    82 * (advance (s i) (e i)).2 + potential (s (i+1))
      = 41 + potential (s i)

def SaturatedEightCycleTarget : Prop :=
  ∀ (s : Nat → Prefix) (e : Nat → Nat) (n : Nat),
    (∀ i < n, Valid (s i)) →
    (∀ i < n, e i ≤ 1) →
    (∀ i < n, (advance (s i) (e i)).1 = s (i+1)) →
    s n = s 0 →
    2 * total (fun i => (advance (s i) (e i)).2) n = n →
    ∃ r : Fin 8,
      (∀ i < n, s i = cycleState (r.val + i)) ∧
      (∀ i < n, (i + r.val) % 8 = 0 → e i = 1) ∧
      (∀ i < n, (i + r.val) % 8 = 2 → e i = 0) ∧
      (∀ i < n, (i + r.val) % 8 = 4 → e i = 0) ∧
      (∀ i < n, (i + r.val) % 8 = 6 → e i = 1)

/-- The odd-position inputs are observationally irrelevant to the skeleton. -/
theorem edge1_any (e : Nat) (he : e ≤ 1) :
    advance ⟨17,5,0⟩ e = (⟨8,13,5⟩, 1) := by
  omega
theorem edge3_any (e : Nat) (he : e ≤ 1) :
    advance ⟨17,6,11⟩ e = (⟨8,14,8⟩, 1) := by
  omega
theorem edge5_any (e : Nat) (he : e ≤ 1) :
    advance ⟨17,8,17⟩ e = (⟨8,16,16⟩, 1) := by
  omega
theorem edge7_any (e : Nat) (he : e ≤ 1) :
    advance ⟨17,13,14⟩ e = (⟨8,12,9⟩, 1) := by
  omega

/-- Exact eight-edge overflow total once the skeleton is followed. -/
def skeletonInput (e1 e3 e5 e7 : Nat) : Nat → Nat
  | 0 => 1
  | 1 => e1
  | 2 => 0
  | 3 => e3
  | 4 => 0
  | 5 => e5
  | 6 => 1
  | _ => e7

def skeletonOverflow (e1 e3 e5 e7 : Nat) : Nat → Nat :=
  fun i => (advance (cycleState i) (skeletonInput e1 e3 e5 e7 i)).2

def OddInputBalance (e1 e3 e5 e7 : Nat) : Prop :=
  e1 + e3 + e5 + e7 = 2

def SaturatedBlockTarget : Prop :=
  ∀ e1 e3 e5 e7 : Nat,
    e1 ≤ 1 → e3 ≤ 1 → e5 ≤ 1 → e7 ≤ 1 →
    (2 * total (skeletonOverflow e1 e3 e5 e7) 8 = 8 ↔
      OddInputBalance e1 e3 e5 e7)

end Agent215.Saturated8
