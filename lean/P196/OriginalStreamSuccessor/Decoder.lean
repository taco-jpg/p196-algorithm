import P196.OriginalStreamSuccessor.Assembly

/-!
# Recovering the original successor without a supplied phase

The last low term identifies the phase once the observation includes one
term beyond the boundary digit. The corrected assembly formula then gives
the exact original successor. No validity or calculated carry is supplied.
-/

namespace Agent5.OriginalStreamSuccessor

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.BoundedStreamCandidates

/-- Two original prefixes reaching beyond the boundary digit determine the
exact exterior successor at every even phase from zero through eighteen.
Empty, zero-head and untrimmed coefficient words are allowed. -/
theorem successorFromPrefixes_correct (c cut : Nat) (B : List Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hB : ∀ x ∈ B, x ≤ 18) (hcut : B.length + 2 ≤ cut) :
    successorFromPrefixes cut
      (originalLow cut { c := c, B := B })
      (originalHigh cut { c := c, B := B }) =
      outerNext { c := c, B := B } := by
  have hphase : phaseFromLow (originalLow cut { c := c, B := B }) = c := by
    have h := phaseFromLow_correct (cut - 2) c B hc hB (by omega)
    simpa only [show cut - 2 + 2 = cut by omega] using h
  unfold successorFromPrefixes
  rw [hphase]
  exact (outerNext_from_corrected_prefixes c cut B hc hB (by omega)).symm

#print axioms successorFromPrefixes_correct

end Agent5.OriginalStreamSuccessor
