import P196.OriginalStreamSuccessor.BoundaryHigh
import P196.OrdinaryExteriorHistories.Numeric
import P196.Agent5StreamAgreementWindow.StreamAgreementWindow

/-!
# Boundary observations with a coherent high readout

The phase-eighteen correction acts on a complete exterior window. A shorter
observation is read only after that correction. This retains the original
low stream and its separately computed terminal high carry, and gives the
high scan a consistent meaning at every requested cutoff.
-/

namespace Agent5.BoundaryOrdinaryStreams

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.BoundedStreamCandidates Agent5.OriginalStreamSuccessor

/-- Correct a full exterior high window before taking the requested prefix. -/
def coherentHigh (cut : Nat) (s : Outer) : List Nat :=
  let K := s.B.length + 1 + cut
  (correctedHigh s.c K (originalHigh K s)).take cut

/-- The original actual carry and low stream, with the coherent high scan. -/
def coherentObservation (cut : Nat) (s : Outer) :
    Nat × List Nat × List Nat :=
  (actualCarry s, originalLow cut s, coherentHigh cut s)

end Agent5.BoundaryOrdinaryStreams
