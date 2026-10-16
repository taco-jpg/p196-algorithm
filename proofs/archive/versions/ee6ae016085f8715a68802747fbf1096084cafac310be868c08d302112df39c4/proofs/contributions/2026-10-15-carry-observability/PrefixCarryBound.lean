import Std

/-!
Two-column necessary transition and an exact finite carry-count bound.

This file certifies the finite graph and its generic path consequence.
The connection from the actual all-width reverse-add map to this graph is
proved separately in METHOD_AND_PROOF.md, not asserted by this module.
No imported project assumptions and no native_decide are used.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace CarryObservability

abbrev State := Nat × Nat

def innerBit (v : Bool) : Nat := if v then 1 else 0

def overflow (s : State) (v : Bool) : Nat :=
  (s.1 + (s.2 + innerBit v) / 10) / 10

def cost (s : State) (v : Bool) : Nat :=
  1 - overflow s v

def next (s : State) (v : Bool) : State :=
  let p := s.1
  let q := s.2
  let a := p / 10
  let u := (q + innerBit v) / 10
  let b := (q + a) / 10
  let h := (p + u) / 10
  if h = 0 then
    (2 * p + u - 10 * a, 2 * q + a + innerBit v - 10 * (b + u))
  else
    (p - 10 * a + 1, p + q + a + u - 10 * (b + h))

def minCost : Nat → State → Nat
  | 0, _ => 0
  | n + 1, s =>
    min (cost s false + minCost n (next s false))
        (cost s true + minCost n (next s true))

def pathCost : State → List Bool → Nat
  | _, [] => 0
  | s, v :: vs => cost s v + pathCost (next s v) vs

theorem minCost_step_le (n : Nat) (s : State) (v : Bool) :
    minCost (n + 1) s ≤ cost s v + minCost n (next s v) := by
  cases v
  · exact Nat.min_le_left _ _
  · exact Nat.min_le_right _ _

theorem minCost_le_pathCost (s : State) (vs : List Bool) :
    minCost vs.length s ≤ pathCost s vs := by
  induction vs generalizing s with
  | nil => exact Nat.le_refl 0
  | cons v vs ih =>
    exact Nat.le_trans (minCost_step_le vs.length s v)
      (Nat.add_le_add_left (ih (next s v)) (cost s v))

/-- A necessary-graph certificate, not a quantified numeric-orbit theorem. -/
theorem nine_step_minimum :
    ∀ p : Fin 18, ∀ q : Fin 19,
      4 ≤ minCost 9 (p.val + 1, q.val) := by
  decide

/-- Every nine-edge path in the stated two-column graph has at least four
nonoverflow edges. Actual-orbit inclusion remains a separate proof obligation. -/
theorem nine_step_path_bound (p q : Nat) (hp : 1 ≤ p) (hp' : p ≤ 18)
    (hq : q ≤ 18) (vs : List Bool) (hlen : vs.length = 9) :
    4 ≤ pathCost (p, q) vs := by
  have hi : p - 1 < 18 := by omega
  have hj : q < 19 := by omega
  have h := nine_step_minimum ⟨p - 1, hi⟩ ⟨q, hj⟩
  have heq : p - 1 + 1 = p := by omega
  change 4 ≤ minCost 9 (p - 1 + 1, q) at h
  rw [heq] at h
  have hpath := minCost_le_pathCost (p, q) vs
  rw [hlen] at hpath
  exact Nat.le_trans h hpath

/-- The graph bound cannot be shortened to eight edges by carry counting alone. -/
theorem eight_step_counting_obstruction : minCost 8 (13, 6) = 3 := by
  decide

#print axioms minCost_step_le
#print axioms minCost_le_pathCost
#print axioms nine_step_minimum
#print axioms nine_step_path_bound
#print axioms eight_step_counting_obstruction

end CarryObservability
