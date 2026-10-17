import Agent105Predecessors9df76b
import TemplateStep

/-!
Agent #105 / session 9df76b: decoder-driven numerical backward layers.

This is a WIP scaffold. It defines the executable data path using the frozen
complete predecessor decoder and Agent109's existing computed decimal digits.
The exact membership, Nodup, and empty-layer theorems remain explicit targets
until a pinned Lean run checks the adapter and recursive proofs.
-/

namespace Agent105BackwardLayers9df76b

open Agent101 Agent105Predecessors9df76b Lychrel196

/-- Existing canonical least-significant-first decimal word for a Nat. -/
def targetWord (Y : Nat) : List Nat := Agent109.digits Y

/-- Original finite digit function associated to the existing word. -/
def targetDigitFn (Y : Nat) : Nat → Nat :=
  Agent101.digitFn (targetWord Y)

/-- All positive one-step predecessors of Y, using the verified generic
numeric decoder. Target zero has no positive predecessors. -/
def preimagesNat (Y : Nat) : List Nat :=
  if Y = 0 then [] else
    Agent105Predecessors9df76b.predecessors
      (targetDigitFn Y) (targetWord Y).length

/-- The depth-zero layer is the target itself if positive, and empty at zero.
Each subsequent layer applies the one-step predecessor decoder. -/
def backwardLayer (Y k : Nat) : List Nat :=
  Nat.rec (motive := fun _ => List Nat)
    (if Y = 0 then [] else [Y])
    (fun _ xs => xs.flatMap preimagesNat) k

/-- Required numerical specification for the one-step adapter. -/
def PreimagesSpec (Y : Nat) : Prop :=
  ∀ n, n ∈ preimagesNat Y ↔ 0 < n ∧ Lychrel196.step n = Y

/-- Required exact ordinary-orbit specification at every finite depth. -/
def BackwardLayerSpec (Y k : Nat) : Prop :=
  ∀ n, n ∈ backwardLayer Y k ↔
    0 < n ∧ Lychrel196.orbit n k = Y

/-- Duplicate freedom required at every computed depth. -/
def BackwardLayerNodup (Y k : Nat) : Prop :=
  (backwardLayer Y k).Nodup

/-- Once a layer is empty, no later layer can become nonempty. -/
def EmptyLayerPersistence (Y k : Nat) : Prop :=
  backwardLayer Y k = [] →
    ∀ j, backwardLayer Y (k + j) = []

/-- The zero-depth specification follows directly from the initial layer. -/
theorem backwardLayer_zero_spec (Y n : Nat) :
    n ∈ backwardLayer Y 0 ↔
      0 < n ∧ Lychrel196.orbit n 0 = Y := by
  simp [backwardLayer, Lychrel196.orbit]

/-- The initial layer is duplicate-free, including the zero-target case. -/
theorem backwardLayer_zero_nodup (Y : Nat) :
    BackwardLayerNodup Y 0 := by
  simp [BackwardLayerNodup, backwardLayer]

/-- The executable one-step decoder correctly returns an empty list at zero. -/
theorem preimagesNat_zero : preimagesNat 0 = [] := by
  simp [preimagesNat]

#print axioms backwardLayer_zero_spec
#print axioms backwardLayer_zero_nodup
#print axioms preimagesNat_zero

end Agent105BackwardLayers9df76b
