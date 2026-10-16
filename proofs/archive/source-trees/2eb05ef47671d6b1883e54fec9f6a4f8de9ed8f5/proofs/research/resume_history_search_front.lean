import Std

/- Exact local-front certificate. This is a theorem about the explicitly
   defined decimal suffix update, not a theorem asserting a Lychrel seed.
   The suffix is followed by an infinite uniform nonneutral q tail.
   The incoming carry from the omitted left portion may be arbitrary. -/
namespace CarryFront

structure Suffix where
  word : List Nat
  uniform : Nat
  displacement : Int
  deriving DecidableEq, Repr

def addDigits : List Nat → Nat → List Nat
  | [], _ => []
  | q :: qs, c => (q + c) % 10 :: addDigits qs ((q + c) / 10)

def step (overflow incoming : Bool) (s : Suffix) : Suffix := Id.run do
  let h := if overflow then 1 else 0
  let cs := s.word ++ List.replicate 3 s.uniform
  let low := addDigits cs (if incoming then 1 else 0)
  let high := (addDigits cs.reverse (if s.uniform ≥ 10 then 1 else 0)).reverse
  let output := (List.range (cs.length - 1 - h)).map fun j =>
    low[j+h]! + high[j]!
  let u := 2 * ((s.uniform + if s.uniform ≥ 10 then 1 else 0) % 10)
  let trimmed := (output.reverse.dropWhile (fun x => x == u)).reverse
  return ⟨trimmed, u,
    s.displacement + (trimmed.length : Int) + (h : Int) - (s.word.length : Int)⟩

def six (a b c d e f : Bool) : Suffix :=
  step true f (step false e (step true d (step false c
    (step true b (step false a ⟨[8], 6, 0⟩)))))

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem terminal_eight_front_renews :
    ∀ a b c d e f : Bool,
      (six a b c d e f).word.getLast? = some 8 ∧
      (six a b c d e f).word.length = 2 ∧
      (six a b c d e f).uniform = 6 ∧
      (six a b c d e f).displacement = 4 := by
  decide

#print axioms terminal_eight_front_renews
end CarryFront

namespace CarryFront

def centerStep (overflow incoming : Bool) (q : List Nat) : List Nat :=
  let ds := addDigits q (if incoming then 1 else 0)
  if overflow then
    (List.range (q.length - 1)).map fun j => ds[j+1]! + ds[q.length-1-j]!
  else ds.zipWith (· + ·) ds.reverse

def centerSix (m : Nat) (a b c d e f : Bool) : List Nat :=
  centerStep true f (centerStep false e (centerStep true d (centerStep false c
    (centerStep true b (centerStep false a ([8] ++ List.replicate m 6 ++ [8]))))))

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem gap_four_collision :
    ∀ a b c d e f : Bool,
      (centerSix 4 a b c d e f).length = 3 ∧
      (centerSix 4 a b c d e f)[1]! = 10 ∧
      (centerSix 4 a b c d e f)[0]! = (centerSix 4 a b c d e f)[2]! := by
  decide

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem gap_five_contact :
    ∀ a b c d e f : Bool,
      (centerSix 5 a b c d e f).length = 4 ∧
      (centerSix 5 a b c d e f)[1]! = 8 ∧
      (centerSix 5 a b c d e f)[2]! = 8 := by
  decide

#print axioms gap_four_collision
#print axioms gap_five_contact
end CarryFront
