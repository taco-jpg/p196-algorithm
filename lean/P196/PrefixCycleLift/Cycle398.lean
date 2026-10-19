import P196.PrefixCycleLift.NumericBridge
import P196.Agent117RemainingCycles.Cycle398_k7

/-!
# A three-step obstruction inside the displayed prefix-398 cycle

Four rows of the existing seven-column backward cycle are selected from
its original packed data and put in forward time order. No eighth-column
extension passes all three steps. Thus this precise four-row trace cannot
occur in any ordinary reverse-and-add orbit whose state at the start of
this trace has width at least eight. This does not exclude the palindrome-prefix 398
class and does not invalidate the existing seven-column cycle theorem.
-/

namespace PrefixCycleLift.Cycle398

open SevenColumnProjection DecimalDigits FoldedDecimal Lychrel196
open Agent105WidthSupport9df76b

/-- The original backward-cycle row 32, first in the forward trace. -/
def row0 : Word :=
  (Agent117.unpack 7 (Agent117.Cycle398_k7.cycleData[31]?.getD 0)).1

/-- The original backward-cycle row 31. -/
def row1 : Word :=
  (Agent117.unpack 7 (Agent117.Cycle398_k7.cycleData[30]?.getD 0)).1

/-- The original backward-cycle row 30. -/
def row2 : Word :=
  (Agent117.unpack 7 (Agent117.Cycle398_k7.cycleData[29]?.getD 0)).1

/-- The original backward-cycle row 29, last in the forward trace. -/
def row3 : Word :=
  (Agent117.unpack 7 (Agent117.Cycle398_k7.cycleData[28]?.getD 0)).1

def forwardRows : List Word := [row0, row1, row2, row3]

/-- The source slice is reversed because the existing witness is backward. -/
theorem forwardRows_from_cycle :
    forwardRows =
      (((Agent117.Cycle398_k7.cycleData.drop 28).take 4).map
        (fun packed => (Agent117.unpack 7 packed).1)).reverse := by
  decide +kernel

theorem forwardRows_value : forwardRows =
    [[10, 13, 9, 17, 2, 9, 17],
     [1, 5, 4, 8, 10, 12, 7],
     [2, 10, 8, 17, 1, 5, 15],
     [5, 0, 18, 14, 3, 11, 10]] := by
  decide +kernel

/-- Both possible high boundary carries are considered on every edge. -/
theorem first_candidates :
    advance row0 row1 (List.range 19) = List.range' 7 11 := by
  decide +kernel

theorem second_candidates :
    advance row1 row2 (List.range' 7 11) = List.range' 14 5 := by
  decide +kernel

theorem third_candidates :
    advance row2 row3 (List.range' 14 5) = [] := by
  decide +kernel

/-- The complete finite trace certificate has an empty reachable set. -/
theorem certificate : run forwardRows (List.range 19) = [] := by
  change advance row2 row3
    (advance row1 row2 (advance row0 row1 (List.range 19))) = []
  rw [first_candidates, second_candidates, third_candidates]

theorem no_eighth_column_lift {x z : Nat} (hx : x < 19) :
    ¬ Lift forwardRows x z :=
  checked_no_lift certificate hx

/-- No ordinary integer orbit has this four-row prefix trace. Only the
width at time `t` is constrained; subsequent widths may increase normally. -/
theorem no_cycle398_integer_orbit_trace
    (n t : Nat) (width : Nat → Nat) (digits : Nat → Nat → Nat)
    (hcan : ∀ i, i ≤ 3 →
      Canonical (orbit n (t + i)) (digits i) (width i))
    (hwidth : 8 ≤ width 0) :
    [wordPrefix (columnSum (digits 0) (width 0)) 7,
     wordPrefix (columnSum (digits 1) (width 1)) 7,
     wordPrefix (columnSum (digits 2) (width 2)) 7,
     wordPrefix (columnSum (digits 3) (width 3)) 7]
      ≠ forwardRows := by
  intro htrace
  let q : Nat → Nat → Nat := fun i => columnSum (digits i) (width i)
  have hc0 := hcan 0 (by decide)
  have hc1 := hcan 1 (by decide)
  have hc2 := hcan 2 (by decide)
  have hc3 := hcan 3 (by decide)
  have hs0 : Canonical (step (orbit n (t + 0))) (digits 1) (width 1) := by
    change Canonical (orbit n ((t + 0) + 1)) (digits 1) (width 1)
    simpa only [Nat.add_assoc] using hc1
  have hs1 : Canonical (step (orbit n (t + 1))) (digits 2) (width 2) := by
    change Canonical (orbit n ((t + 1) + 1)) (digits 2) (width 2)
    simpa only [Nat.add_assoc] using hc2
  have hs2 : Canonical (step (orbit n (t + 2))) (digits 3) (width 3) := by
    change Canonical (orbit n ((t + 2) + 1)) (digits 3) (width 3)
    simpa only [Nat.add_assoc] using hc3
  have hw01 := canonical_step_width hc0 hs0
  have hw12 := canonical_step_width hc1 hs1
  have hw23 := canonical_step_width hc2 hs2
  have hw1 : 8 ≤ width 1 := by omega
  have hw2 : 8 ≤ width 2 := by omega
  have hw3 : 8 ≤ width 3 := by omega
  have hx0 : q 0 7 < 19 := by
    have h := columnSum_bounded (digits 0) (width 0) hc0.2.1 7 (by omega)
    change columnSum (digits 0) (width 0) 7 < 19
    omega
  have hx1 : q 1 7 < 19 := by
    have h := columnSum_bounded (digits 1) (width 1) hc1.2.1 7 (by omega)
    change columnSum (digits 1) (width 1) 7 < 19
    omega
  have hx2 : q 2 7 < 19 := by
    have h := columnSum_bounded (digits 2) (width 2) hc2.2.1 7 (by omega)
    change columnSum (digits 2) (width 2) 7 < 19
    omega
  have hx3 : q 3 7 < 19 := by
    have h := columnSum_bounded (digits 3) (width 3) hc3.2.1 7 (by omega)
    change columnSum (digits 3) (width 3) 7 < 19
    omega
  have he01 := canonical_step_lift 7 hc0 hs0 (by omega)
  have he12 := canonical_step_lift 7 hc1 hs1 (by omega)
  have he23 := canonical_step_lift 7 hc2 hs2 (by omega)
  change ForwardAdmitted (wordPrefix (q 0) 7 ++ [q 0 7])
    (wordPrefix (q 1) 7 ++ [q 1 7]) at he01
  change ForwardAdmitted (wordPrefix (q 1) 7 ++ [q 1 7])
    (wordPrefix (q 2) 7 ++ [q 2 7]) at he12
  change ForwardAdmitted (wordPrefix (q 2) 7 ++ [q 2 7])
    (wordPrefix (q 3) 7 ++ [q 3 7]) at he23
  have hp0 := congrArg (fun rows : List Word => rows[0]?.getD []) htrace
  have hp1 := congrArg (fun rows : List Word => rows[1]?.getD []) htrace
  have hp2 := congrArg (fun rows : List Word => rows[2]?.getD []) htrace
  have hp3 := congrArg (fun rows : List Word => rows[3]?.getD []) htrace
  change wordPrefix (q 0) 7 = row0 at hp0
  change wordPrefix (q 1) 7 = row1 at hp1
  change wordPrefix (q 2) 7 = row2 at hp2
  change wordPrefix (q 3) 7 = row3 at hp3
  have e01 : ForwardAdmitted (row0 ++ [q 0 7]) (row1 ++ [q 1 7]) := by
    simpa only [hp0, hp1] using he01
  have e12 : ForwardAdmitted (row1 ++ [q 1 7]) (row2 ++ [q 2 7]) := by
    simpa only [hp1, hp2] using he12
  have e23 : ForwardAdmitted (row2 ++ [q 2 7]) (row3 ++ [q 3 7]) := by
    simpa only [hp2, hp3] using he23
  apply no_eighth_column_lift hx0
  exact Lift.step e01 hx1
    (Lift.step e12 hx2 (Lift.step e23 hx3 (Lift.single row3 (q 3 7))))

end PrefixCycleLift.Cycle398
