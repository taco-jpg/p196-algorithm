import P196.OriginalStreamSuccessor.Coalescence
import P196.CompleteExteriorFibers.BoundaryFamily

/-!
# The boundary correction and irrecoverable initial carry

At phase eighteen the uncorrected sum of the original rational digit
prefixes can give the wrong successor. After the correction, the existing
boundary ambiguity families have identical exact futures. Their original
low and high stream histories agree at every time, while their initial
calculated carries remain different. This is not equality of an observation
predicate that additionally records the initial carry.
-/

namespace Agent5.OriginalStreamSuccessor

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.BoundedStreamCandidates Agent5.CompleteExteriorFibers
open Agent6.ExteriorCoordinates

/-- The literal uncorrected stream-sum formula fails at a valid phase
eighteen source, whose first high observation is improper. -/
theorem uncorrected_phase_eighteen_failure :
    let s : Outer := { c := 18, B := [8] }
    validOuter s = true ∧ originalHigh 2 s = [10, 0] ∧
      outerNext s ≠
        { c := bulkPhase 18,
          B := stripSuffix (bulkPhase 18)
            (List.zipWith (fun x y => x + y) (originalLow 2 s) (originalHigh 2 s)) } := by
  decide

/-- At both boundaries and every shared width at least three, distinct
valid sources with opposite actual carries have the same complete original
stream histories and all the same exact states after time zero. The
initial collision families are imported without a new construction. -/
theorem boundary_full_history_ambiguity (c m : Nat) (hc : c = 0 ∨ c = 18) :
    ∃ A B : List Nat,
      A.length = m + 3 ∧ B.length = m + 3 ∧
      validOuter { c := c, B := A } = true ∧
      validOuter { c := c, B := B } = true ∧ A ≠ B ∧
      actualCarry { c := c, B := A } = 0 ∧
      actualCarry { c := c, B := B } = 1 ∧
      (∀ t : Nat, sameStreams (outerIter t { c := c, B := A })
        (outerIter t { c := c, B := B })) ∧
      (∀ t : Nat, outerIter (t + 1) { c := c, B := B } =
        outerIter (t + 1) { c := c, B := A }) := by
  obtain ⟨A, B, hlenA, hlenB, hvA, hvB, hne, hgA, hgB, hstreams⟩ :=
    boundary_double_fiber c m hc
  have hcTen : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] := by
    rcases hc with rfl | rfl <;> decide
  have hfuture := outerIter_positive_eq_of_complete_streams
    { c := c, B := A } { c := c, B := B } hcTen hcTen
    (entries_le_of_valid c A hvA) (entries_le_of_valid c B hvB) hstreams
  refine ⟨A, B, hlenA, hlenB, hvA, hvB, hne, hgA, hgB, ?_, hfuture⟩
  intro t
  cases t with
  | zero => exact hstreams
  | succ t =>
    change sameStreams (outerIter (t + 1) { c := c, B := A })
      (outerIter (t + 1) { c := c, B := B })
    rw [hfuture t]
    intro cut
    exact ⟨rfl, rfl⟩

#print axioms uncorrected_phase_eighteen_failure
#print axioms boundary_full_history_ambiguity

end Agent5.OriginalStreamSuccessor
