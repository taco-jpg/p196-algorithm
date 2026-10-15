import Std

/-!
Exact finite checks for the complementary-band OUTER projection.
No state-table axiom or native evaluator is used. The all-width connection
between this projection and ordinary reverse-and-add is stated separately.
-/
namespace P196.Agent7.Finite
set_option maxRecDepth 100000
set_option maxHeartbeats 0

structure Outer where
  c : Nat
  B : List Nat
  deriving Repr, DecidableEq

def normalize : List Nat → Nat → List Nat × Nat
  | [], carry => ([], carry)
  | x :: xs, carry =>
      let rest := normalize xs ((x + carry) / 10)
      ((x + carry) % 10 :: rest.1, rest.2)

def bulkPhase (c : Nat) : Nat := 2 * (c - 9 * (if 10 ≤ c then 1 else 0))

def stripSuffix (c : Nat) (w : List Nat) : List Nat :=
  (w.reverse.dropWhile (fun x => x == c)).reverse

def outerNext (s : Outer) : Outer :=
  let k := if 10 ≤ s.c then 1 else 0
  let t := s.c - 9 * k
  let left := normalize s.B 0
  let right := normalize s.B.reverse k
  let u := s.c + left.2 - 10 * k
  let other := if right.2 == 0 then right.1.reverse ++ [t]
               else [1] ++ right.1.reverse
  let raw := List.zipWith (fun x y => x + y) (left.1 ++ [u]) other
  { c := 2 * t, B := stripSuffix (2 * t) raw }

-- The finite domain includes all words of length at most two, including
-- invalid leading-zero/nontrimmed words, which are rejected by validOuter.
def decodeWord (k : Nat) : List Nat :=
  if k == 0 then []
  else if k ≤ 19 then [k - 1]
  else [(k - 20) / 19, (k - 20) % 19]

def encoded (p : Fin 8) (k : Fin 381) : Outer :=
  { c := 2 * (p.val + 1), B := decodeWord k.val }

def validOuter (s : Outer) : Bool :=
  (s.B.all (fun x => x ≤ 18)) &&
  (match s.B with
   | [] => true
   | a :: _ => decide (0 < a)) &&
  (match s.B.getLast? with
   | none => true
   | some a => !(a == s.c))

-- Inclusive convention: staysSmall n means n+1 states at times 0,...,n
-- all have |B|<=2. A false value allows an exit at any time in that range.
def staysSmall : Nat → Outer → Bool
  | 0, s => decide (s.B.length ≤ 2)
  | n + 1, s => decide (s.B.length ≤ 2) && staysSmall n (outerNext s)

theorem cap2_exits_by_seven :
    ∀ (p : Fin 8) (k : Fin 381),
      validOuter (encoded p k) = true →
      staysSmall 7 (encoded p k) = false := by
  decide +kernel

def sharpStart : Outer := { c := 14, B := [2, 17] }

theorem cap2_sharp_six : staysSmall 6 sharpStart = true := by decide

theorem cap2_sharp_seven : staysSmall 7 sharpStart = false := by decide

#print axioms cap2_exits_by_seven
#print axioms cap2_sharp_six
#print axioms cap2_sharp_seven
end P196.Agent7.Finite
