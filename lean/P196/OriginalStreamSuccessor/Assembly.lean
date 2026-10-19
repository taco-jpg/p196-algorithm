import P196.OriginalStreamSuccessor.BoundaryHigh
import P196.Agent5ExactDigitStreams.CoordinateStreams

/-!
# Assemble the original exterior successor

The published stream formula already reconstructs every interior-phase
successor. At the two boundary phases, the low formula and the corrected
high formula recover the same two scan words used by the original map.
Their equal constant tails disappear under the existing suffix-removal
identity. No normalization or successor-padding induction is needed.
-/

namespace Agent5.OriginalStreamSuccessor

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.BoundedStreamCandidates
open Agent5.CompleteExteriorFibers

private theorem boundary_from_corrected_prefixes (c q : Nat) (B : List Nat)
    (hc : c = 0 ∨ c = 18) (hB : ∀ x ∈ B, x ≤ 18) :
    outerNext { c := c, B := B } =
      { c := bulkPhase c,
        B := stripSuffix (bulkPhase c)
          (List.zipWith (fun x y => x + y)
            (originalLow (B.length + 1 + q) { c := c, B := B })
            (correctedHigh c (B.length + 1 + q)
              (originalHigh (B.length + 1 + q) { c := c, B := B }))) } := by
  have hcTen : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] := by
    rcases hc with rfl | rfl <;> decide
  have hlow :
      originalLow (B.length + 1 + q) { c := c, B := B } =
        (normalize B 0).1 ++
          [c + (normalize B 0).2 - 10 * (if 10 ≤ c then 1 else 0)] ++
          List.replicate q (c - 9 * (if 10 ≤ c then 1 else 0)) :=
    low_prefix_even_phase c B q hcTen hB
  have hhigh := boundary_high_reconstruction c q B hc hB
  dsimp only at hhigh
  have hlength :
      ((normalize B 0).1 ++
        [c + (normalize B 0).2 - 10 * (if 10 ≤ c then 1 else 0)]).length =
      (if (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 == 0 then
        (normalize B.reverse (if 10 ≤ c then 1 else 0)).1.reverse ++
          [c - 9 * (if 10 ≤ c then 1 else 0)]
       else [1] ++ (normalize B.reverse (if 10 ≤ c then 1 else 0)).1.reverse).length := by
    by_cases hg : (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 = 0 <;>
      simp [hg, normalize_length, Nat.add_comm]
  rw [hlow, hhigh]
  unfold bulkPhase
  rw [strip_zip_append_replicate _ _ _ _ hlength]
  rfl

/-- Every cutoff containing the boundary term reconstructs the original
successor at all ten even phases. The high correction is needed only at
phase eighteen; each original high prefix retains its own calculated carry
and denominator. Empty, zero-head, and untrimmed words are included. -/
theorem outerNext_from_corrected_prefixes (c cut : Nat) (B : List Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hB : ∀ x ∈ B, x ≤ 18) (hcut : B.length + 1 ≤ cut) :
    outerNext { c := c, B := B } =
      { c := bulkPhase c,
        B := stripSuffix (bulkPhase c)
          (List.zipWith (fun x y => x + y)
            (originalLow cut { c := c, B := B })
            (correctedHigh c cut (originalHigh cut { c := c, B := B }))) } := by
  by_cases hcInterior : nonneutralPhase c
  · have hcEighteen : c ≠ 18 := by
      simp only [nonneutralPhase, List.mem_cons, List.mem_nil_iff, or_false] at hcInterior
      omega
    simpa only [originalLow, originalHigh, actualCarry, correctedHigh,
      if_neg hcEighteen] using
      outerNext_from_streams_of_cutoff c B cut hcInterior hB hcut
  have hcBoundary : c = 0 ∨ c = 18 := by
    simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc
    simp only [nonneutralPhase, List.mem_cons, List.mem_nil_iff, or_false] at hcInterior
    omega
  have hlength : B.length + 1 + (cut - (B.length + 1)) = cut :=
    Nat.add_sub_of_le hcut
  simpa only [hlength] using
    boundary_from_corrected_prefixes c (cut - (B.length + 1)) B hcBoundary hB

#print axioms outerNext_from_corrected_prefixes

end Agent5.OriginalStreamSuccessor
