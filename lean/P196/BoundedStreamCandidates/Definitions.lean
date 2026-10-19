import P196.CompleteExteriorFibers.LowTail
import P196.BidirectionalWordDecoder.Numeric

/-!
# Executable candidates for bounded original stream observations

The input consists of two literal lists and an upper bound on the original
word width. The actual carry is not an input. Two carry guesses feed the
published positional decoder; a decidable filter checks the original
observations, phase, validity, width, and each guess's calculated carry.
All functions are total, including on malformed observation lists.
-/

namespace Agent5.BoundedStreamCandidates

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- The calculated high carry of the original exterior state. -/
def actualCarry (s : Outer) : Nat :=
  (normalize s.B.reverse (if 10 ≤ s.c then 1 else 0)).2

/-- The original low prefix, with no change to its numerator. -/
def originalLow (cut : Nat) (s : Outer) : List Nat :=
  adicNumeratorDigits cut (zValue s.c s.B - (s.c : Int))

/-- The original high prefix retains its own width and actual carry. -/
def originalHigh (cut : Nat) (s : Outer) : List Nat :=
  fractionDigits cut (rhoNum s.c s.B)
    (9 * 10 ^ s.B.length * 10 ^ actualCarry s)

/-- Exact compatibility with both entire input lists at the stated width
bound. No consistency or length assumptions are imposed on the inputs. -/
def boundedPrefixMatch
    (N : Nat) (low high : List Nat) (s : Outer) : Prop :=
  s.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] ∧
  validOuter s = true ∧
  s.B.length ≤ N ∧
  originalLow (N + 2) s = low ∧
  originalHigh (N + 2) s = high

instance (N : Nat) (low high : List Nat) (s : Outer) :
    Decidable (boundedPrefixMatch N low high s) := by
  unfold boundedPrefixMatch
  infer_instance

/-- For a correct input, the last low term is the eventual phase digit.
The zero default only makes this function total on an empty input. -/
def phaseFromLow (low : List Nat) : Nat :=
  let t := low.getLast?.getD 0
  if t % 2 = 0 then t else t + 9

/-- Select the low positional value from its two possible lifts. -/
def restoreLow (M R H : Nat) : Nat :=
  if R % 9 = H % 9 then R else R + 10 ^ M

/-- Reconstruct one word at a supplied phase and carry guess. The known
width bound is padded to the positive width N+1 before suffix removal. -/
def candidateAtCarry
    (N c g : Nat) (low high : List Nat) : Outer :=
  let M := N + 1
  let R := lowValue (low.take M)
  let H := highValue (high.take (M + g)) - c / 9
  { c := c, B := stripSuffix c
      (Agent5.BidirectionalWordDecoder.decodeValues M (restoreLow M R H) H) }

/-- Retain a guess only when the original state satisfies every input
condition and its actual calculated carry equals this guess. -/
def checkedGuess (N : Nat) (low high : List Nat) (g : Nat) : Option Outer :=
  let s := candidateAtCarry N (phaseFromLow low) g low high
  if boundedPrefixMatch N low high s ∧ actualCarry s = g then some s else none

/-- The complete candidate list tests exactly the two possible carries. -/
def decodeCandidates (N : Nat) (low high : List Nat) : List Outer :=
  [0, 1].filterMap (checkedGuess N low high)

end Agent5.BoundedStreamCandidates
