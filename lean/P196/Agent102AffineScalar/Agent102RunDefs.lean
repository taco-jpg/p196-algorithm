import Std

/-!
Agent #102: literal run words and integer affine endpoint data.
These definitions do not replace the repository's decimal reverse-add operation.
`word` expands every run using `List.replicate` and concatenation.
-/

namespace Agent102

structure Affine where
  slope : Int
  intercept : Int
  deriving DecidableEq, Repr

namespace Affine

def eval (f : Affine) (k : Nat) : Int := f.slope * (k : Int) + f.intercept

def zero : Affine := ⟨0, 0⟩

def add (f g : Affine) : Affine := ⟨f.slope + g.slope, f.intercept + g.intercept⟩

def cutoff (f : Affine) : Nat := f.intercept.natAbs + 1

/-- The affine expression representing the eventual nonnegative part. -/
def positivePart (f : Affine) : Affine :=
  if f.slope < 0 ∨ (f.slope = 0 ∧ f.intercept < 0) then zero else f

end Affine

structure Run where
  digit : Nat
  count : Nat
  deriving DecidableEq, Repr

def word (rs : List Run) : List Nat :=
  rs.flatMap (fun r => List.replicate r.count r.digit)

structure Span where
  digit : Nat
  lo : Nat
  hi : Nat
  deriving DecidableEq, Repr

def spansFrom (start : Nat) : List Run → List Span
  | [] => []
  | r :: rs => ⟨r.digit, start, start + r.count⟩ :: spansFrom (start + r.count) rs

def spans (rs : List Run) : List Span := spansFrom 0 rs

def Span.covers (s : Span) (i : Nat) : Prop := s.lo ≤ i ∧ i < s.hi

/-- Positive intersection; a zero-length run never intersects another run. -/
def Span.overlaps (s t : Span) : Prop := max s.lo t.lo < min s.hi t.hi

structure RunSpec where
  digit : Nat
  length : Affine
  deriving DecidableEq, Repr

def runsAt (rs : List RunSpec) (k : Nat) : List Run :=
  rs.map (fun r => ⟨r.digit, (r.length.eval k).toNat⟩)

def wordAt (rs : List RunSpec) (k : Nat) : List Nat := word (runsAt rs k)

end Agent102
