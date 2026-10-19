import P196.BoundedStreamCandidates.Phase
import P196.Agent5ExactDigitStreams.CoordinateStreams

/-!
# Executable reconstruction of an original exterior successor

The high coordinate at phase eighteen uses a terminating decimal expansion.
The original exterior scan uses the equivalent expansion with a trailing
band of nines. Subtracting one from the value of the whole finite high
prefix and reading the same number of places recovers that scan window.
The correction is applied only after recovering the phase from the low
prefix. These functions remain total on arbitrary input lists.
-/

namespace Agent5.OriginalStreamSuccessor

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.BoundedStreamCandidates

/-- Restore the high scan window at phase eighteen by a finite borrow. -/
def correctedHigh (c cut : Nat) (high : List Nat) : List Nat :=
  if c = 18 then fractionDigits cut (highValue high - 1) (10 ^ cut)
  else high

/-- Recover the phase, sum the low and corrected high windows, and remove
the new constant band. Correctness requires sufficiently long observations
of a bounded-coefficient source, as stated in the decoder theorem. -/
def successorFromPrefixes (cut : Nat) (low high : List Nat) : Outer :=
  let c := phaseFromLow low
  { c := bulkPhase c,
    B := stripSuffix (bulkPhase c)
      (List.zipWith (fun x y => x + y) low (correctedHigh c cut high)) }

end Agent5.OriginalStreamSuccessor
