import InverseFibers

/-!
The restricted three-layer zero-overflow prefix machine. The fixed first
coefficient is 14; later coefficients are 5 or 14. Its arithmetic interface
is the original P196.Agent9.InverseFibers.Local relation.

Original Local source blob: cade8ace6359fe8246a29ec781859e3a39b00e11.
Historical generator: c41f16d9853adf8320db54564385d1b3fe8fde99.
Later clock000/y5 generator: d845edd9a114bd61ff379d0184cae36ce6f3d379.
The machine is a prefix condition; it does not assert center sufficiency.
-/

namespace P196.Agent3.PrefixContraction

open P196.Agent9.InverseFibers

abbrev Triple := State × State × State

def coefficient (bit : Bool) : Symbol := if bit then 14 else 5

/-- Choose the unique carry successor away from target coefficient nine.
At nine this selects one valid successor; coverage is used only away from nine. -/
def nextCarry (s : Symbol) (p : State) : Option State :=
  if s.val % 2 = 1 then
    match p.val with
    | 0 => some 1
    | 1 => some 3
    | 2 => some 0
    | _ => some 2
  else
    match p.val with
    | 0 => some 0
    | 1 => if s.val = 18 then none else some 2
    | 2 => if s.val = 0 then none else some 1
    | _ => some 3

/-- The two remainder equations determine the emitted coefficient. -/
def emitted (s : Symbol) (p q : State) : Symbol :=
  ⟨((s.val + 10 * (low q + high p) - low p - high q) / 2) % 19,
    Nat.mod_lt _ (by decide)⟩

def oneStep (s : Symbol) (p : State) : Option (State × Symbol) :=
  (nextCarry s p).map (fun q => (q, emitted s p q))

def machineStep (bit : Bool) (p : Triple) : Option Triple := do
  let (q₁, x) ← oneStep (coefficient bit) p.1
  let (q₂, y) ← oneStep x p.2.1
  let (q₃, _) ← oneStep y p.2.2
  pure (q₁, q₂, q₃)

def advance (p : Option Triple) (bit : Bool) : Option Triple :=
  p.bind (machineStep bit)

def prefixRun (p : Option Triple) (bits : List Bool) : Option Triple :=
  bits.foldl advance p

@[simp] theorem coefficient_false : coefficient false = 5 := rfl
@[simp] theorem coefficient_true : coefficient true = 14 := rfl

theorem machineStep_initial : machineStep true (0, 0, 0) = some (0, 1, 1) := by
  decide

end P196.Agent3.PrefixContraction
