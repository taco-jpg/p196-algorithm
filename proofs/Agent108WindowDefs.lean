import Std

/-!
Agent #108, session b31b8818.
Literal complete, unpadded windows and the half-word family from
FOLDED_WEIGHT_OBSTRUCTION.md section 3 (original mathematical source).
The buffered arithmetic family is attributed to Agent #13.  These list
definitions do not assert any arithmetic transition or safety property.
-/

namespace Agent108.WindowWeights

def windows {α : Type} (d : Nat) : List α → List (List α)
  | [] => []
  | x :: xs =>
      if d ≤ (x :: xs).length then (x :: xs).take d :: windows d xs else []

def buffer (b : Nat) : List Nat := List.replicate b 9

def block : Bool → List Nat
  | false => [9, 9, 9, 9]
  | true => [14, 14, 4, 4]

def blocks (b : Nat) : List Bool → List Nat
  | [] => []
  | e :: es => block e ++ buffer b ++ blocks b es

/-- Here b = d - 1; the actual window width is always b+1. -/
def inputHalf (b k : Nat) (es : List Bool) : List Nat :=
  [5] ++ buffer b ++ blocks b es ++ [14] ++ List.replicate k 18

def targetHalf (b k r : Nat) : List Nat :=
  [11] ++ List.replicate (r * (b+4) + b+1) 9 ++ List.replicate k 18

def localBlock (b : Nat) (e : Bool) : List Nat :=
  buffer b ++ block e ++ buffer b

def endpoint (b k a : Nat) : List Nat :=
  buffer b ++ [a] ++ List.replicate k 18

def choices : Nat → List (List Bool)
  | 0 => [[]]
  | r+1 => (choices r).map (false :: ·) ++ (choices r).map (true :: ·)

end Agent108.WindowWeights
