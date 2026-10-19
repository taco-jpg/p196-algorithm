import P196.Agent5ExactDigitStreams.CoordinateStreams

/-!
# Concrete obstructions without terminal trimming

Agent #5. At phases eight and ten, distinct bounded positive-head words can
share the first n low digits and the first n+1 high digits. The second word
ends in its phase in each example. These kernel-checked identities show why
the trimming condition matters for the asymmetric recovery theorem.
-/

namespace Agent5.TrimmedStreamObservation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- A width-four collision at phase eight. Both heads are positive and all
coefficients are bounded; the second word fails only terminal trimming. -/
theorem untrimmed_phase_eight_collision :
    let A : List Nat := [1, 0, 18, 17]
    let B : List Nat := [11, 9, 7, 8]
    A ≠ B ∧ nonneutralPhase 8 ∧
      validOuter { c := 8, B := A } = true ∧
      B.all (fun x => x ≤ 18) = true ∧ B.head? = some 11 ∧
      B.getLast? = some 8 ∧
      adicNumeratorDigits 4 (zValue 8 A - (8 : Int)) = [1, 0, 8, 8] ∧
      adicNumeratorDigits 4 (zValue 8 B - (8 : Int)) = [1, 0, 8, 8] ∧
      fractionDigits 5 (rhoNum 8 A)
        (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 0).2) = [1, 1, 9, 7, 8] ∧
      fractionDigits 5 (rhoNum 8 B)
        (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 0).2) = [1, 1, 9, 7, 8] := by
  dsimp only
  simp only [nonneutralPhase, List.mem_cons, List.not_mem_nil, or_false]
  decide

/-- A width-two collision at phase ten, again with bounded positive-head
words and an otherwise valid first word. -/
theorem untrimmed_phase_ten_collision :
    let A : List Nat := [1, 1]
    let B : List Nat := [11, 10]
    A ≠ B ∧ nonneutralPhase 10 ∧
      validOuter { c := 10, B := A } = true ∧
      B.all (fun x => x ≤ 18) = true ∧ B.head? = some 11 ∧
      B.getLast? = some 10 ∧
      adicNumeratorDigits 2 (zValue 10 A - (10 : Int)) = [1, 1] ∧
      adicNumeratorDigits 2 (zValue 10 B - (10 : Int)) = [1, 1] ∧
      fractionDigits 3 (rhoNum 10 A)
        (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 1).2) = [1, 2, 1] ∧
      fractionDigits 3 (rhoNum 10 B)
        (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 1).2) = [1, 2, 1] := by
  dsimp only
  simp only [nonneutralPhase, List.mem_cons, List.not_mem_nil, or_false]
  decide

#print axioms untrimmed_phase_eight_collision
#print axioms untrimmed_phase_ten_collision

/-- With unknown width, even terminal-trimmed valid words can share the low
prefix at their maximum width and every high observation. The next low digit
distinguishes them. Thus the reduced low cutoff cannot simply be transferred
from the shared-width theorem to the arbitrary-width setting. -/
theorem unequal_width_mixed_collision :
    let A : List Nat := [1, 1]
    let B : List Nat := [11]
    A.length = 2 ∧ B.length = 1 ∧ A ≠ B ∧
      validOuter { c := 10, B := A } = true ∧
      validOuter { c := 10, B := B } = true ∧
      adicNumeratorDigits 2 (zValue 10 A - (10 : Int)) =
        adicNumeratorDigits 2 (zValue 10 B - (10 : Int)) ∧
      (∀ highCut : Nat,
        fractionDigits highCut (rhoNum 10 A)
          (9 * 10 ^ A.length * 10 ^ (normalize A.reverse 1).2) =
        fractionDigits highCut (rhoNum 10 B)
          (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 1).2)) ∧
      adicNumeratorDigits 3 (zValue 10 A - (10 : Int)) ≠
        adicNumeratorDigits 3 (zValue 10 B - (10 : Int)) := by
  dsimp only
  refine ⟨rfl, rfl, by decide, by decide, by decide, by decide, ?_, by decide⟩
  intro highCut
  change fractionDigits highCut 109 900 = fractionDigits highCut 109 900
  rfl

#print axioms unequal_width_mixed_collision

end Agent5.TrimmedStreamObservation
