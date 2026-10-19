import Std

/-!
Local folded carry states for two consecutive decimal normalizations.
The first layer reads a symmetric coefficient pair. The second layer
reads the resulting low digit together with the previous high digit.
The two equalities in `Local` encode the high carry equations, while
its last equality encodes antisymmetry of the normalized digit defect.

These definitions are a local arithmetic model. Their realization by
ordinary decimal coefficient words is proved in the scan module.
-/

set_option autoImplicit false

namespace P196.CommonOverflowRigidity

structure Layer where
  qLow : Nat
  qHigh : Nat
  sLow : Nat
  sHigh : Nat
  deriving DecidableEq

structure State where
  first : Layer
  second : Layer
  qPrevious : Nat
  sPrevious : Nat
  deriving DecidableEq

def LayerBounded (t : Layer) : Prop :=
  t.qLow ≤ 1 ∧ t.qHigh ≤ 1 ∧ t.sLow ≤ 1 ∧ t.sHigh ≤ 1

def Bounded (t : State) : Prop :=
  LayerBounded t.first ∧ LayerBounded t.second ∧
    t.qPrevious ≤ 9 ∧ t.sPrevious ≤ 9

def Diagonal (t : State) : Prop :=
  t.first.qLow = t.first.sLow ∧ t.first.qHigh = t.first.sHigh ∧
    t.second.qLow = t.second.sLow ∧ t.second.qHigh = t.second.sHigh ∧
    t.qPrevious = t.sPrevious

def Local (t : Layer) (a b rq rs : Nat) : Prop :=
  (a + rq) / 10 = t.qHigh ∧ (b + rs) / 10 = t.sHigh ∧
    (a + t.qLow) % 10 + (a + rq) % 10 =
      (b + t.sLow) % 10 + (b + rs) % 10

def advanceLayer (t : Layer) (a b rq rs : Nat) : Layer :=
  ⟨(a + t.qLow) / 10, rq, (b + t.sLow) / 10, rs⟩

def Transition (t : State) (a b rq rs tq ts : Nat) : Prop :=
  let A := (a + t.first.qLow) % 10 + t.qPrevious
  let B := (b + t.first.sLow) % 10 + t.sPrevious
  Local t.first a b rq rs ∧ Local t.second A B tq ts

def advance (t : State) (a b rq rs tq ts : Nat) : State :=
  let A := (a + t.first.qLow) % 10 + t.qPrevious
  let B := (b + t.first.sLow) % 10 + t.sPrevious
  ⟨advanceLayer t.first a b rq rs, advanceLayer t.second A B tq ts,
    (a + rq) % 10, (b + rs) % 10⟩

/-- The twelve exceptional states of the local closure invariant. -/
def badStates : List State :=
  [⟨⟨0, 0, 1, 0⟩, ⟨1, 0, 0, 0⟩, 4, 9⟩,
   ⟨⟨0, 0, 1, 0⟩, ⟨1, 1, 0, 1⟩, 4, 9⟩,
   ⟨⟨0, 1, 1, 0⟩, ⟨0, 1, 0, 0⟩, 5, 9⟩,
   ⟨⟨0, 1, 1, 0⟩, ⟨1, 1, 1, 0⟩, 0, 4⟩,
   ⟨⟨0, 1, 1, 1⟩, ⟨1, 0, 0, 0⟩, 0, 5⟩,
   ⟨⟨0, 1, 1, 1⟩, ⟨1, 1, 0, 1⟩, 0, 5⟩,
   ⟨⟨1, 0, 0, 0⟩, ⟨0, 0, 1, 0⟩, 9, 4⟩,
   ⟨⟨1, 0, 0, 0⟩, ⟨0, 1, 1, 1⟩, 9, 4⟩,
   ⟨⟨1, 0, 0, 1⟩, ⟨0, 0, 0, 1⟩, 9, 5⟩,
   ⟨⟨1, 0, 0, 1⟩, ⟨1, 0, 1, 1⟩, 4, 0⟩,
   ⟨⟨1, 1, 0, 1⟩, ⟨0, 0, 1, 0⟩, 5, 0⟩,
   ⟨⟨1, 1, 0, 1⟩, ⟨0, 1, 1, 1⟩, 5, 0⟩]

def Bad (t : State) : Prop := t ∈ badStates

end P196.CommonOverflowRigidity
