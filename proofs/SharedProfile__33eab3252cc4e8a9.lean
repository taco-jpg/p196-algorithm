import LychrelDigitSums

/-!
Concrete, nonsymmetric decimal half-line profiles.  Every normalization
retains its terminal forward carry.  There is no assumed dynamics axiom.
-/

namespace DecimalProfile

open DecimalDigits DecimalMass

abbrev State := Nat × (Nat → Nat)

/-- Exact support width, positive anchor, and the decimal pair-coefficient bound. -/
def Valid (L : Nat) (q : Nat → Nat) : Prop :=
  0 < L ∧ 0 < q 0 ∧ (∀ i, q i ≤ 18) ∧
    (∀ i, L ≤ i → q i = 0) ∧ 0 < q (L - 1)

/-- Reflection padded with zeros outside the specified finite width. -/
def reflect (q : Nat → Nat) (L i : Nat) : Nat :=
  if i < L then q (L - 1 - i) else 0

/-- Backward carries computed independently of the forward carries. -/
def backCarry (q : Nat → Nat) (L i : Nat) : Nat :=
  carry (reflect q L) (L - i)

/-- Backward normalized digits, with an exact zero tail. -/
def backOutput (q : Nat → Nat) (L i : Nat) : Nat :=
  if i < L then output (reflect q L) (L - 1 - i) else 0

/-- The actual nonsymmetric half-line map from the written proof. -/
def phi (q : Nat → Nat) (L i : Nat) : Nat :=
  if backCarry q L 0 = 0 then output q i + backOutput q L i
  else if i = 0 then output q 0 + 1
  else output q i + backOutput q L (i - 1)

/-- Detached-component update; the branch is selected by the left component. -/
def bulk (q : Nat → Nat) (L h i : Nat) : Nat :=
  if h = 0 then output q i + backOutput q L i
  else output q i + if i = 0 then 0 else backOutput q L (i - 1)

/-- Either end can add a last coefficient in a nonsymmetric profile. -/
def nextLen (q : Nat → Nat) (L : Nat) : Nat :=
  if carry q L = 0 ∧ backCarry q L 0 = 0 then L else L + 1

def step (s : State) : State := (nextLen s.2 s.1, phi s.2 s.1)

def iter (s : State) : Nat → State
  | 0 => s
  | t + 1 => step (iter s t)

def mass (s : State) : Nat := wordSum s.2 s.1

end DecimalProfile
