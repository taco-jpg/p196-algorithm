import Agent102RunDefs

/-!
Agent #102: finite unions of exact natural-parameter intervals.
An upper endpoint of `none` denotes infinity. Degenerate/reversed intervals
are allowed and contain no point; the algorithms never enumerate their points.
-/

namespace Agent102.ParameterSets

structure Interval where
  lo : Nat
  hi : Option Nat
  deriving DecidableEq, Repr

def Interval.Contains (I : Interval) (k : Nat) : Prop :=
  I.lo ≤ k ∧ match I.hi with
    | none => True
    | some h => k < h

instance (I : Interval) (k : Nat) : Decidable (I.Contains k) := by
  unfold Interval.Contains
  cases I.hi <;> dsimp <;> infer_instance

def Interval.empty : Interval := ⟨0, some 0⟩

def Interval.univ : Interval := ⟨0, none⟩

def Interval.inter (I J : Interval) : Interval :=
  ⟨max I.lo J.lo, match I.hi, J.hi with
    | none, h => h
    | h, none => h
    | some h, some j => some (min h j)⟩

def Interval.complement (I : Interval) : List Interval :=
  ⟨0, some I.lo⟩ :: (match I.hi with
    | none => []
    | some h => [⟨h, none⟩])

abbrev Region := List Interval

def holds (R : Region) (k : Nat) : Prop := ∃ I ∈ R, I.Contains k

def empty : Region := []

def univ : Region := [Interval.univ]

def union (R S : Region) : Region := R ++ S

def inter (R S : Region) : Region :=
  R.flatMap (fun I => S.map (fun J => I.inter J))

def complement (R : Region) : Region :=
  R.foldr (fun I acc => inter I.complement acc) univ

def unionAll (Rs : List Region) : Region := Rs.flatten

def interAll (Rs : List Region) : Region := Rs.foldr inter univ

def test (R : Region) (k : Nat) : Bool :=
  R.any (fun I => decide (I.Contains k))

def inhabited (R : Region) : Bool :=
  R.any (fun I => match I.hi with
    | none => true
    | some h => decide (I.lo < h))

end Agent102.ParameterSets
