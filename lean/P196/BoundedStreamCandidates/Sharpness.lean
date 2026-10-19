import P196.BoundedStreamCandidates.Candidates
import P196.CompleteExteriorFibers.BoundaryFamily

/-!
# Both candidates are needed at either boundary phase

The already proved boundary families have identical complete original
streams and distinct valid words of every width at least three. Exact
finite candidate membership therefore puts both words in the decoder's
list. Its unconditional length bound makes that list have exactly two
elements. The existing collisions are imported, not reproved here.
-/

namespace Agent5.BoundedStreamCandidates

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

private theorem two_le_length_of_distinct_mem {L : List Outer} {a b : Outer}
    (ha : a ∈ L) (hb : b ∈ L) (hne : a ≠ b) : 2 ≤ L.length := by
  cases L with
  | nil => simp at ha
  | cons x xs =>
      cases xs with
      | nil =>
          simp only [List.mem_cons, List.mem_nil_iff, or_false] at ha hb
          exact False.elim (hne (ha.trans hb.symm))
      | cons y ys => simp

/-- At either boundary phase and every width bound at least three, some
valid word of exactly that width produces a list of exactly two candidates. -/
theorem boundary_candidates_length_two (c N : Nat)
    (hc : c = 0 ∨ c = 18) (hN : 3 ≤ N) :
    ∃ A : List Nat,
      A.length = N ∧ validOuter { c := c, B := A } = true ∧
      (decodeCandidates N
        (originalLow (N + 2) { c := c, B := A })
        (originalHigh (N + 2) { c := c, B := A })).length = 2 := by
  obtain ⟨A, B, hAlen, hBlen, hvA, hvB, hne, _, _, hstreams⟩ :=
    Agent5.CompleteExteriorFibers.boundary_double_fiber c (N - 3) hc
  have hwidth : N - 3 + 3 = N := by omega
  rw [hwidth] at hAlen hBlen
  have hcEven : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] := by
    rcases hc with rfl | rfl <;> simp
  let low := originalLow (N + 2) { c := c, B := A }
  let high := originalHigh (N + 2) { c := c, B := A }
  have hmemA : { c := c, B := A } ∈ decodeCandidates N low high := by
    apply (mem_decodeCandidates N low high _).mpr
    exact ⟨hcEven, hvA, by change A.length ≤ N; omega, rfl, rfl⟩
  have hmemB : { c := c, B := B } ∈ decodeCandidates N low high := by
    apply (mem_decodeCandidates N low high _).mpr
    exact ⟨hcEven, hvB, by change B.length ≤ N; omega,
      (hstreams (N + 2)).1, (hstreams (N + 2)).2⟩
  have hstates : ({ c := c, B := A } : Outer) ≠ { c := c, B := B } := by
    intro h
    exact hne (congrArg Outer.B h)
  have htwo := two_le_length_of_distinct_mem hmemA hmemB hstates
  exact ⟨A, hAlen, hvA, Nat.le_antisymm (decodeCandidates_length N low high) htwo⟩

#print axioms boundary_candidates_length_two

end Agent5.BoundedStreamCandidates
