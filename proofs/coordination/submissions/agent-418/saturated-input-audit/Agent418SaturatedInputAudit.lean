import Lean.Elab.Tactic.Omega

/-!
Agent #418: independent audit of Agent #215, PR #71 at
0a22e6278bd63554d3f7cf5b19122553de5cc0a7.

`Prefix` and `advance` below are the exact definitions (namespace changed)
from P196.Agent4.Saturation in PrefixModel.lean, Git blob
28eaab767b15fd81f73f2dcfc3dfff307eb02307, source commit
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5. `total` is the exact definition
from SaturationTheorem.lean, blob f4f8f7da5f2e87f3f0d99503e8f76e6aee4b5f6f.
No potential certificate or actual-orbit theorem is assumed here.

This is an exact-model standalone proof, not a full rebuild of PR #71.
All conclusions concern the abstract three-column relation. They supply
no ordinary-integer lift, ReturnCertificate instance, or P196 conclusion.
-/
namespace Agent418.SaturatedInputAudit

structure Prefix where
  a : Nat
  b : Nat
  c : Nat
  deriving DecidableEq, Repr

def advance (s : Prefix) (e : Nat) : Prefix × Nat :=
  let l1 := s.a / 10
  let l2 := (s.b + l1) / 10
  let d0 := s.a % 10
  let d1 := (s.b + l1) % 10
  let d2 := (s.c + l2) % 10
  let r2 := (s.c + e) / 10
  let r1 := (s.b + r2) / 10
  let gamma := (s.a + r1) / 10
  let h0 := (s.a + r1) % 10
  let h1 := (s.b + r2) % 10
  let h2 := (s.c + e) % 10
  if gamma = 0 then (⟨d0+h0, d1+h1, d2+h2⟩, gamma)
  else (⟨d0+1, d1+h0, d2+h1⟩, gamma)

def total (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n+1 => total f n + f n

-- Exact state and block definitions from Agent #215's audited source.
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

-- This is the exact closed counterexample to the proposed equivalence.
theorem zero_inputs_counterexample :
    2 * total (skeletonOverflow 0 0 0 0) 8 = 8 ∧
      ¬ OddInputBalance 0 0 0 0 := by
  unfold OddInputBalance
  decide

theorem not_saturatedBlockTarget : ¬ SaturatedBlockTarget := by
  intro h
  have wrong := (h 0 0 0 0 (by decide) (by decide) (by decide) (by decide)).mp
    zero_inputs_counterexample.1
  exact zero_inputs_counterexample.2 wrong

-- Correct universal statement: output overflows are independent of odd inputs.
theorem odd_edge_table : ∀ e : Fin 2,
    advance ⟨17,5,0⟩ e.val = (⟨8,13,5⟩, 1) ∧
    advance ⟨17,6,11⟩ e.val = (⟨8,14,8⟩, 1) ∧
    advance ⟨17,8,17⟩ e.val = (⟨8,16,16⟩, 1) ∧
    advance ⟨17,13,14⟩ e.val = (⟨8,12,9⟩, 1) := by decide

theorem every_block_overflow_four_fin : ∀ e1 e3 e5 e7 : Fin 2,
    total (skeletonOverflow e1.val e3.val e5.val e7.val) 8 = 4 := by decide

theorem every_block_overflow_four (e1 e3 e5 e7 : Nat)
    (h1 : e1 ≤ 1) (h3 : e3 ≤ 1) (h5 : e5 ≤ 1) (h7 : e7 ≤ 1) :
    total (skeletonOverflow e1 e3 e5 e7) 8 = 4 :=
  every_block_overflow_four_fin ⟨e1, by omega⟩ ⟨e3, by omega⟩
    ⟨e5, by omega⟩ ⟨e7, by omega⟩

theorem every_block_saturated (e1 e3 e5 e7 : Nat)
    (h1 : e1 ≤ 1) (h3 : e3 ≤ 1) (h5 : e5 ≤ 1) (h7 : e7 ≤ 1) :
    2 * total (skeletonOverflow e1 e3 e5 e7) 8 = 8 := by
  rw [every_block_overflow_four e1 e3 e5 e7 h1 h3 h5 h7]

-- The full transition, not only its overflow output, follows the same skeleton.
theorem every_block_edge : ∀ e1 e3 e5 e7 : Fin 2, ∀ i : Fin 8,
    advance (cycleState i.val)
      (skeletonInput e1.val e3.val e5.val e7.val i.val) =
      (cycleState (i.val + 1), i.val % 2) := by decide

-- Every proposed odd-input sum from zero through four really occurs.
def bits : List Nat := [0, 1]
def schedules : List (Nat × Nat × Nat × Nat) :=
  bits.flatMap fun a => bits.flatMap fun b =>
    bits.flatMap fun c => bits.map fun d => (a,b,c,d)
def inputSum (s : Nat × Nat × Nat × Nat) : Nat :=
  s.1 + s.2.1 + s.2.2.1 + s.2.2.2

def balancedSchedules := schedules.filter fun s => inputSum s == 2

theorem schedule_count : schedules.length = 16 := by decide
theorem balanced_schedule_count : balancedSchedules.length = 6 := by decide

#print axioms zero_inputs_counterexample
#print axioms not_saturatedBlockTarget
#print axioms odd_edge_table
#print axioms every_block_overflow_four_fin
#print axioms every_block_overflow_four
#print axioms every_block_saturated
#print axioms every_block_edge
#print axioms schedule_count
#print axioms balanced_schedule_count

end Agent418.SaturatedInputAudit
