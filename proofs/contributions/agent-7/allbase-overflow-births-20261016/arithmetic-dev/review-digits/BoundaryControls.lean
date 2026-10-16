import OverflowDigits

/-!
Independent exact controls for the actual overflow index bridge.
These small closed instances are reduced by the Lean kernel. They exercise
width boundaries, both old-width parities, reset-tag erasure, changed mirror
indices, and list defaults. They do not replace the generic bridge proof.
-/
namespace P196.Agent7.AllBaseOverflow.ReviewDigits

open ResetNormalization PhysicalWidth ReverseAdd ActualBaseBirths

def one : List (Int × Bool) := [(2, true)]
def evenTwo : List (Int × Bool) := [(10, false), (10, true)]
def oddThree : List (Int × Bool) := [(1, true), (2, false), (1, true)]
def asymmetric : List (Int × Bool) := [(12, true), (9, false), (10, true)]
def wideCarry : List (Int × Bool) := [(10, false), (1, false)]

/-- The empty source cannot supply the bridge's computed terminal-one premise. -/
theorem empty_boundary :
    terminal 2 0 (ordinaryTags []) = 0 ∧
      terminal 2 0 (ordinaryTags []) ≠ 1 := by decide

/-- Old width one has two true output endpoints and no interior index.
The following index is absent, so its getD value really is the chosen default. -/
theorem width_one_endpoints_and_defaults :
    terminal 2 0 (ordinaryTags one) = 1 ∧
    actualDigits 2 one = [0, 1] ∧
    pairs (actualDigits 2 one) = [1, 1] ∧
    (pairs (actualDigits 2 one)).getD 1 37 = 1 ∧
    (pairs (actualDigits 2 one)).getD 2 0 = 0 ∧
    (pairs (actualDigits 2 one)).getD 2 37 = 37 ∧
    one.getD 1 (37, true) = (37, true) := by decide

/-- With old width two the new middle is at index one. Using the old
reflection carry index zero would give one, whereas the true pair is two. -/
theorem even_width_shift :
    terminal 10 0 (ordinaryTags evenTwo) = 1 ∧
    actualDigits 10 evenTwo = [0, 1, 1] ∧
    pairs (actualDigits 10 evenTwo) = [1, 2, 1] ∧
    (pairs (actualDigits 10 evenTwo)).getD 1 0 = 2 ∧
    ((evenTwo.getD 1 (0, false)).1 + incoming 10 evenTwo 1) % 10 +
      ((evenTwo.getD 0 (0, false)).1 + incoming 10 evenTwo 0) % 10 = 1 := by decide

/-- Actual carrying erases the source reset flags. The old reflection's
carry index one would give one at index one, while the actual output is zero. -/
theorem odd_width_shift_and_actual_carries :
    terminal 2 0 oddThree = 0 ∧
    terminal 2 0 (ordinaryTags oddThree) = 1 ∧
    (List.range 4).map (incoming 2 oddThree) = [0, 0, 1, 1] ∧
    actualDigits 2 oddThree = [1, 0, 0, 1] ∧
    pairs (actualDigits 2 oddThree) = [2, 0, 0, 2] ∧
    (pairs (actualDigits 2 oddThree)).getD 1 0 = 0 ∧
    ((oddThree.getD 1 (0, false)).1 + incoming 2 oddThree 1) % 2 +
      ((oddThree.getD 0 (0, false)).1 + incoming 2 oddThree 1) % 2 = 1 := by decide

/-- The endpoint theorem intentionally does not require source symmetry. -/
theorem asymmetric_endpoints :
    (asymmetric.map Prod.fst).reverse ≠ asymmetric.map Prod.fst ∧
    terminal 10 0 (ordinaryTags asymmetric) = 1 ∧
    actualDigits 10 asymmetric = [2, 0, 1, 1] ∧
    (pairs (actualDigits 10 asymmetric)).getD 0 0 = 3 ∧
    (pairs (actualDigits 10 asymmetric)).getD asymmetric.length 0 = 3 := by decide

/-- The shape bridge does not assume carry-bit bounds: those are separate
premises of downstream arithmetic. This source has an intermediate carry three. -/
theorem unbounded_shape_control :
    incoming 3 wideCarry 1 = 3 ∧
    terminal 3 0 (ordinaryTags wideCarry) = 1 ∧
    actualDigits 3 wideCarry = [1, 1, 1] ∧
    (actualDigits 3 wideCarry).length = wideCarry.length + 1 := by decide

/-- Instantiate the reviewed interior getD API at both old-width parities. -/
theorem reviewed_interior_api_instances :
    (pairs (actualDigits 10 evenTwo)).getD 1 0 =
      ((evenTwo.getD 1 (0, false)).1 + incoming 10 evenTwo 1) % 10 +
        ((evenTwo.getD 0 (0, false)).1 + incoming 10 evenTwo 1) % 10 ∧
    (pairs (actualDigits 2 oddThree)).getD 1 0 =
      ((oddThree.getD 1 (0, false)).1 + incoming 2 oddThree 1) % 2 +
        ((oddThree.getD 0 (0, false)).1 + incoming 2 oddThree 2) % 2 := by
  constructor
  · exact actual_overflow_pair_getD 10 evenTwo 1 (by decide) (by decide)
      (by decide) (by decide)
  · exact actual_overflow_pair_getD 2 oddThree 1 (by decide) (by decide)
      (by decide) (by decide)

/-- The reviewed carry APIs include the final old boundary and its reflected
predecessor, with exactly the incoming carries of the ordinary prefix. -/
theorem reviewed_carry_api_instances :
    incoming 2 oddThree 3 =
      ((oddThree[2]'(by decide)).1 + incoming 2 oddThree 2) / 2 ∧
    incoming 2 oddThree 2 =
      ((oddThree[1]'(by decide)).1 + incoming 2 oddThree 1) / 2 := by
  constructor
  · exact incoming_predecessor 2 oddThree 3 (by decide) (by decide)
  · exact incoming_mirror_predecessor 2 oddThree 1 (by decide) (by decide) (by decide)

#print axioms empty_boundary
#print axioms width_one_endpoints_and_defaults
#print axioms even_width_shift
#print axioms odd_width_shift_and_actual_carries
#print axioms asymmetric_endpoints
#print axioms unbounded_shape_control
#print axioms reviewed_interior_api_instances
#print axioms reviewed_carry_api_instances

end P196.Agent7.AllBaseOverflow.ReviewDigits
