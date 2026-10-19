import P196.BoundaryOrdinaryStreams.Realization
import P196.BoundaryOrdinaryStreams.Coherence

/-!
# Exact boundary controls for short high observations

These small kernel checks distinguish an original rational prefix from
the ordinary high digit. They also exhibit two positive ordinary seeds
whose prescribed boundary states have the same short original streams
and the same carry but different high digits in their actual successors.
-/

namespace Agent5.BoundaryOrdinaryStreams

open P196.Agent7.Finite Agent5.BoundedStreamCandidates
open Agent5.OriginalStreamSuccessor Agent5.OrdinaryExteriorHistories

/-- Correcting before reaching the complete exterior can change an already
correct leading digit. The extended correction preserves that digit. -/
theorem short_high_correction_failure :
    let s : Outer := ⟨18, [9]⟩
    validOuter s = true ∧ originalHigh 1 s = [1] ∧
      correctedHigh 18 1 (originalHigh 1 s) = [0] ∧
      coherentHigh 1 s = [1] := by decide

/-- Equal short original prefixes and equal actual carry need not determine
the coherent ordinary high digit, even at a shared valid boundary width. -/
theorem short_original_prefix_ambiguity :
    let s : Outer := ⟨18, [1, 8]⟩
    let q : Outer := ⟨18, [1, 9]⟩
    validOuter s = true ∧ validOuter q = true ∧
      actualCarry s = 0 ∧ actualCarry q = 0 ∧
      originalLow 1 s = originalLow 1 q ∧
      originalHigh 1 s = originalHigh 1 q ∧
      coherentHigh 1 s = [1] ∧ coherentHigh 1 q = [2] := by decide

/-- The short-prefix ambiguity occurs in actual positive ordinary seeds
with the prescribed protected pair words and different next high digits. -/
theorem ordinary_short_prefix_ambiguity :
    Agent109.pairWord 18999900 = P196.Agent6.surrounded [1, 8] 18 0 [] ∧
      Agent109.pairWord 19999900 = P196.Agent6.surrounded [1, 9] 18 0 [] ∧
      Lychrel196.step 18999900 = 19999881 ∧
      Lychrel196.step 19999900 = 20999891 ∧
      ordinaryObservation 1 18999900 0 = (0, [1], [1]) ∧
      ordinaryObservation 1 19999900 0 = (0, [1], [2]) := by decide

#print axioms short_high_correction_failure
#print axioms short_original_prefix_ambiguity
#print axioms ordinary_short_prefix_ambiguity

end Agent5.BoundaryOrdinaryStreams
