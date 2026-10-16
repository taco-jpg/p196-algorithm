import Std
/- Finite graph certificates for the overflow-normalization reduction.
   The abstract path theorem below is kernel-checked. Connecting every
   normalized numeric orbit to this graph is justified in the companion
   mathematical note but is NOT yet a Lean theorem in this module. -/
namespace OverflowNormalizationCertificate
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
structure State where
  norm : Nat
  layers : List Nat
  bad : Bool
  deriving DecidableEq, Repr

def normEdges (s : Nat) : List (Nat × Nat) :=
  let a := s % 2
  let b := s / 2
  let reset := if b = 0 then [(0,0),(0,2)] else [(10,1),(10,3)]
  reset ++ if a = b then [] else [(9,s)]

def edge (s q h : Nat) : List (Nat × Nat) :=
  let a := s % 2
  let b := s / 2 % 2
  let t := s / 4
  [0,1].flatMap fun bn =>
    if (q+bn)/10 = b then
      let an := (q+a)/10
      let lo := (q+a)%10
      let hi := (q+bn)%10
      [(an+2*bn+(if h=1 then 4*hi else 0), if h=1 then lo+t else lo+hi)]
    else []

def feed : List Nat → Nat → List Nat → List (List Nat × Nat)
  | [], q, _ => [([],q)]
  | _::_, _, [] => []
  | s::ss, q, h::hs =>
    (edge s q h).flatMap fun (st,r) =>
      (feed ss r hs).map fun (tail,v) => (st::tail,v)

def finishFuel : Nat → List Nat → Option Nat → List Nat → Bool → List Bool
  | 0, _, _, _, _ => []
  | _+1, [], c, _, bad => [bad || match c with | none => false | some z => z > 9]
  | _+1, _::_, _, [], _ => []
  | fuel+1, s::ss, c, h::hs, bad =>
    let a := s%2
    let b := s/2%2
    let t := s/4
    match c with
    | none => if a=b then finishFuel fuel ss (if h=1 then some (2*t) else none) hs bad else []
    | some z =>
      if (z+a)/10=b then
        let r := (z+a)%10
        if h=1 then
          (feed ss (r+t) hs).flatMap fun (tail,v) => finishFuel fuel tail none hs (bad || v>9)
        else finishFuel fuel ss (some (2*r)) hs bad
      else []

def finish (layers : List Nat) (c : Option Nat) (hs : List Nat) (bad : Bool) : List Bool :=
  finishFuel (hs.length+1) layers c hs bad

def next (hs : List Nat) (st : State) : List State :=
  (normEdges st.norm).flatMap fun (q,ns) =>
    (feed st.layers q hs).map fun (tail,r) => ⟨ns,tail,st.bad || r>9⟩

def initials (first : Nat) (hs : List Nat) : List State :=
  let layers := hs.map fun h => 2*h + if h=1 then 4 else 0
  (normEdges 2).flatMap fun (q,ns) =>
    if q=first then
      (feed layers q hs).map fun (tail,r) => ⟨ns,tail,r>9⟩
    else []

def finals (hs : List Nat) (st : State) : List Bool :=
  let a := st.norm%2
  let b := st.norm/2
  let cs : List (Option Nat) := (if a=b then [none] else []) ++ [some (10*b)]
  cs.flatMap fun c => finish st.layers c hs st.bad

inductive Reach (first : Nat) (hs : List Nat) : State → Prop
  | initial {s} : s ∈ initials first hs → Reach first hs s
  | advance {s t} : Reach first hs s → t ∈ next hs s → Reach first hs t

theorem reach_subset (first : Nat) (hs : List Nat) (cert : List State)
    (hinit : ∀ s ∈ initials first hs, s ∈ cert)
    (hclosed : ∀ s ∈ cert, ∀ t ∈ next hs s, t ∈ cert) :
    ∀ s, Reach first hs s → s ∈ cert := by
  intro s hr
  induction hr with
  | initial h => exact hinit _ h
  | advance _ ht ih => exact hclosed _ ih _ ht

def cert10 : List State := [
  ⟨0, [0, 0], false⟩,
  ⟨0, [0, 2], false⟩,
  ⟨0, [0, 1], false⟩,
  ⟨0, [0, 3], false⟩,
  ⟨0, [6, 0], false⟩,
  ⟨0, [6, 2], false⟩,
  ⟨0, [6, 1], false⟩,
  ⟨0, [6, 3], false⟩,
  ⟨2, [0, 0], false⟩,
  ⟨2, [0, 2], false⟩,
  ⟨2, [0, 1], false⟩,
  ⟨2, [0, 3], false⟩,
  ⟨2, [36, 0], true⟩,
  ⟨2, [36, 2], false⟩,
  ⟨2, [36, 1], false⟩,
  ⟨2, [36, 1], true⟩,
  ⟨2, [36, 3], false⟩,
  ⟨2, [36, 3], true⟩,
  ⟨2, [2, 1], false⟩,
  ⟨2, [2, 3], false⟩,
  ⟨2, [6, 0], false⟩,
  ⟨2, [6, 2], false⟩,
  ⟨2, [6, 1], false⟩,
  ⟨2, [6, 3], false⟩,
  ⟨1, [1, 0], false⟩,
  ⟨1, [1, 2], false⟩,
  ⟨1, [37, 0], false⟩,
  ⟨1, [37, 0], true⟩,
  ⟨1, [37, 2], false⟩,
  ⟨1, [3, 0], false⟩,
  ⟨1, [3, 2], false⟩,
  ⟨1, [7, 0], false⟩,
  ⟨1, [7, 2], false⟩,
  ⟨3, [1, 0], false⟩,
  ⟨3, [1, 2], false⟩,
  ⟨3, [7, 0], false⟩,
  ⟨3, [7, 2], false⟩
]

def cert9 : List State := [
  ⟨0, [0, 0, 0], false⟩,
  ⟨0, [0, 0, 2], false⟩,
  ⟨0, [0, 4, 0], false⟩,
  ⟨0, [0, 4, 2], false⟩,
  ⟨0, [0, 6, 0], false⟩,
  ⟨0, [0, 6, 2], false⟩,
  ⟨0, [0, 10, 0], false⟩,
  ⟨0, [0, 10, 2], false⟩,
  ⟨0, [0, 1, 0], false⟩,
  ⟨0, [0, 1, 2], false⟩,
  ⟨0, [0, 7, 0], false⟩,
  ⟨0, [0, 7, 2], false⟩,
  ⟨0, [6, 0, 0], false⟩,
  ⟨0, [6, 0, 2], false⟩,
  ⟨0, [6, 4, 0], false⟩,
  ⟨0, [6, 4, 2], false⟩,
  ⟨0, [6, 6, 0], false⟩,
  ⟨0, [6, 6, 2], false⟩,
  ⟨0, [6, 10, 0], false⟩,
  ⟨0, [6, 10, 2], false⟩,
  ⟨0, [6, 1, 0], false⟩,
  ⟨0, [6, 1, 2], false⟩,
  ⟨0, [6, 7, 0], false⟩,
  ⟨0, [6, 7, 2], false⟩,
  ⟨2, [0, 0, 0], false⟩,
  ⟨2, [0, 0, 2], false⟩,
  ⟨2, [0, 4, 0], false⟩,
  ⟨2, [0, 4, 2], false⟩,
  ⟨2, [0, 6, 0], false⟩,
  ⟨2, [0, 6, 2], false⟩,
  ⟨2, [0, 10, 0], false⟩,
  ⟨2, [0, 10, 2], false⟩,
  ⟨2, [0, 1, 0], false⟩,
  ⟨2, [0, 1, 2], false⟩,
  ⟨2, [0, 7, 0], false⟩,
  ⟨2, [0, 7, 2], false⟩,
  ⟨2, [36, 36, 0], true⟩,
  ⟨2, [36, 36, 2], false⟩,
  ⟨2, [36, 36, 1], false⟩,
  ⟨2, [36, 36, 3], false⟩,
  ⟨2, [36, 2, 1], false⟩,
  ⟨2, [36, 2, 3], false⟩,
  ⟨2, [36, 33, 0], true⟩,
  ⟨2, [36, 33, 2], false⟩,
  ⟨2, [36, 33, 2], true⟩,
  ⟨2, [36, 33, 1], true⟩,
  ⟨2, [36, 33, 3], true⟩,
  ⟨2, [36, 37, 0], false⟩,
  ⟨2, [36, 37, 2], false⟩,
  ⟨2, [36, 3, 0], false⟩,
  ⟨2, [36, 3, 2], false⟩,
  ⟨2, [36, 39, 0], true⟩,
  ⟨2, [36, 39, 2], false⟩,
  ⟨2, [36, 39, 2], true⟩,
  ⟨2, [36, 39, 1], true⟩,
  ⟨2, [36, 39, 3], true⟩,
  ⟨2, [2, 1, 0], false⟩,
  ⟨2, [2, 1, 2], false⟩,
  ⟨2, [2, 37, 0], false⟩,
  ⟨2, [2, 37, 0], true⟩,
  ⟨2, [2, 37, 2], false⟩,
  ⟨2, [2, 3, 0], false⟩,
  ⟨2, [2, 3, 2], false⟩,
  ⟨2, [2, 7, 0], false⟩,
  ⟨2, [2, 7, 2], false⟩,
  ⟨2, [6, 0, 0], false⟩,
  ⟨2, [6, 0, 2], false⟩,
  ⟨2, [6, 4, 0], false⟩,
  ⟨2, [6, 4, 2], false⟩,
  ⟨2, [6, 6, 0], false⟩,
  ⟨2, [6, 6, 2], false⟩,
  ⟨2, [6, 10, 0], false⟩,
  ⟨2, [6, 10, 2], false⟩,
  ⟨2, [6, 1, 0], false⟩,
  ⟨2, [6, 1, 2], false⟩,
  ⟨2, [6, 7, 0], false⟩,
  ⟨2, [6, 7, 2], false⟩,
  ⟨1, [1, 0, 0], false⟩,
  ⟨1, [1, 0, 2], false⟩,
  ⟨1, [1, 0, 1], false⟩,
  ⟨1, [1, 0, 3], false⟩,
  ⟨1, [1, 4, 0], false⟩,
  ⟨1, [1, 4, 2], false⟩,
  ⟨1, [1, 8, 0], false⟩,
  ⟨1, [1, 8, 2], false⟩,
  ⟨1, [1, 6, 0], false⟩,
  ⟨1, [1, 6, 2], false⟩,
  ⟨1, [1, 6, 1], false⟩,
  ⟨1, [1, 6, 3], false⟩,
  ⟨1, [1, 10, 0], false⟩,
  ⟨1, [1, 10, 2], false⟩,
  ⟨1, [1, 14, 0], false⟩,
  ⟨1, [1, 14, 2], false⟩,
  ⟨1, [37, 0, 0], false⟩,
  ⟨1, [37, 0, 2], false⟩,
  ⟨1, [37, 36, 0], true⟩,
  ⟨1, [37, 36, 2], false⟩,
  ⟨1, [37, 36, 1], true⟩,
  ⟨1, [37, 36, 3], true⟩,
  ⟨1, [37, 2, 1], false⟩,
  ⟨1, [37, 2, 3], false⟩,
  ⟨1, [37, 6, 0], false⟩,
  ⟨1, [37, 6, 2], false⟩,
  ⟨1, [3, 0, 0], false⟩,
  ⟨1, [3, 0, 2], false⟩,
  ⟨1, [3, 4, 0], false⟩,
  ⟨1, [3, 4, 2], false⟩,
  ⟨1, [3, 6, 0], false⟩,
  ⟨1, [3, 6, 2], false⟩,
  ⟨1, [3, 10, 0], false⟩,
  ⟨1, [3, 10, 2], false⟩,
  ⟨1, [7, 0, 0], false⟩,
  ⟨1, [7, 0, 2], false⟩,
  ⟨1, [7, 0, 1], false⟩,
  ⟨1, [7, 0, 3], false⟩,
  ⟨1, [7, 4, 0], false⟩,
  ⟨1, [7, 4, 2], false⟩,
  ⟨1, [7, 8, 0], false⟩,
  ⟨1, [7, 8, 2], false⟩,
  ⟨1, [7, 6, 0], false⟩,
  ⟨1, [7, 6, 2], false⟩,
  ⟨1, [7, 6, 1], false⟩,
  ⟨1, [7, 6, 3], false⟩,
  ⟨1, [7, 10, 0], false⟩,
  ⟨1, [7, 10, 2], false⟩,
  ⟨1, [7, 14, 0], false⟩,
  ⟨1, [7, 14, 2], false⟩,
  ⟨3, [1, 0, 0], false⟩,
  ⟨3, [1, 0, 2], false⟩,
  ⟨3, [1, 0, 1], false⟩,
  ⟨3, [1, 0, 3], false⟩,
  ⟨3, [1, 4, 0], false⟩,
  ⟨3, [1, 4, 2], false⟩,
  ⟨3, [1, 8, 0], false⟩,
  ⟨3, [1, 8, 2], false⟩,
  ⟨3, [1, 6, 0], false⟩,
  ⟨3, [1, 6, 2], false⟩,
  ⟨3, [1, 6, 1], false⟩,
  ⟨3, [1, 6, 3], false⟩,
  ⟨3, [1, 10, 0], false⟩,
  ⟨3, [1, 10, 2], false⟩,
  ⟨3, [1, 14, 0], false⟩,
  ⟨3, [1, 14, 2], false⟩,
  ⟨3, [7, 0, 0], false⟩,
  ⟨3, [7, 0, 2], false⟩,
  ⟨3, [7, 0, 1], false⟩,
  ⟨3, [7, 0, 3], false⟩,
  ⟨3, [7, 4, 0], false⟩,
  ⟨3, [7, 4, 2], false⟩,
  ⟨3, [7, 8, 0], false⟩,
  ⟨3, [7, 8, 2], false⟩,
  ⟨3, [7, 6, 0], false⟩,
  ⟨3, [7, 6, 2], false⟩,
  ⟨3, [7, 6, 1], false⟩,
  ⟨3, [7, 6, 3], false⟩,
  ⟨3, [7, 10, 0], false⟩,
  ⟨3, [7, 10, 2], false⟩,
  ⟨3, [7, 14, 0], false⟩,
  ⟨3, [7, 14, 2], false⟩
]

theorem cert10_initial : ∀ s ∈ initials 10 [1,0], s ∈ cert10 := by decide
theorem cert10_closed : ∀ s ∈ cert10, ∀ t ∈ next [1,0] s, t ∈ cert10 := by decide
theorem cert10_safe : ∀ s ∈ cert10, ∀ b ∈ finals [1,0] s, b = false := by decide

theorem cert9_initial : ∀ s ∈ initials 9 [1,1,0], s ∈ cert9 := by decide
theorem cert9_closed : ∀ s ∈ cert9, ∀ t ∈ next [1,1,0] s, t ∈ cert9 := by decide
theorem cert9_safe : ∀ s ∈ cert9, ∀ b ∈ finals [1,1,0] s, b = false := by decide

theorem normalized10_graph_safe (s : State) (hr : Reach 10 [1,0] s) :
    ∀ b ∈ finals [1,0] s, b = false :=
  cert10_safe s (reach_subset 10 [1,0] cert10 cert10_initial cert10_closed s hr)

theorem normalized9_graph_safe (s : State) (hr : Reach 9 [1,1,0] s) :
    ∀ b ∈ finals [1,1,0] s, b = false :=
  cert9_safe s (reach_subset 9 [1,1,0] cert9 cert9_initial cert9_closed s hr)

#print axioms normalized10_graph_safe
#print axioms normalized9_graph_safe
end OverflowNormalizationCertificate
