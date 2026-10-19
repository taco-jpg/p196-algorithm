import P196.CompleteStreamDecoder.Prefixes
import P196.CompleteStreamDecoder.Width
import P196.CompleteStreamDecoder.Sharpness
import P196.BoundedStreamCandidates.Candidates

/-!
# Complete fibers from finite observations of a bounded source

A complete competitor of a valid source is at most one coefficient wider.
The existing candidate decoder therefore needs only that one extra place.
The finite-to-complete bridge proves that every retained word has both
complete original streams in common with the source. The resulting exact
membership theorem imposes no width bound on a competing state.
-/

namespace Agent5.CompleteStreamDecoder

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams
open Agent5.BoundedStreamCandidates Agent5.CompleteExteriorFibers

/-- Test both original carry guesses at the source width bound plus one. -/
def completeCandidates (N : Nat) (low high : List Nat) : List Outer :=
  decodeCandidates (N + 1) low high

/-- Observations of length N+3 from a valid source of width at most N
enumerate its entire valid ten-phase complete-stream fiber. No competing
word-width bound occurs on the right side. -/
theorem mem_completeCandidates (N : Nat) (s q : Outer)
    (hs : s.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hvs : validOuter s = true) (hw : s.B.length ≤ N) :
    q ∈ completeCandidates N
      (originalLow (N + 3) s) (originalHigh (N + 3) s) ↔
    q.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] ∧
      validOuter q = true ∧ sameStreams s q := by
  rw [completeCandidates, mem_decodeCandidates]
  change
    (q.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] ∧
      validOuter q = true ∧ q.B.length ≤ N + 1 ∧
      originalLow (N + 3) q = originalLow (N + 3) s ∧
      originalHigh (N + 3) q = originalHigh (N + 3) s) ↔ _
  constructor
  · rintro ⟨hq, hvq, hqN, hlo, hhi⟩
    have hcut : max s.B.length q.B.length + 2 ≤ N + 3 := by omega
    exact ⟨hq, hvq, (same_streams_iff_prefixes (N + 3) s q hs hq
      (entries_le_of_valid s.c s.B hvs) (entries_le_of_valid q.c q.B hvq)
      hcut).mpr ⟨hlo, hhi⟩⟩
  · rintro ⟨hq, hvq, hstreams⟩
    have hwidth := complete_competitor_length_le s q hs hq hvs hvq hstreams
    exact ⟨hq, hvq, by omega, (hstreams (N + 3)).1, (hstreams (N + 3)).2⟩

/-- The complete-fiber decoder returns at most two words on every input. -/
theorem completeCandidates_length (N : Nat) (low high : List Nat) :
    (completeCandidates N low high).length ≤ 2 := by
  exact decodeCandidates_length (N + 1) low high

/-- The complete-fiber decoder never repeats a state, even on inputs that
are not observations of any valid source. -/
theorem completeCandidates_nodup (N : Nat) (low high : List Nat) :
    (completeCandidates N low high).Nodup := by
  exact decodeCandidates_nodup (N + 1) low high

#print axioms mem_completeCandidates
#print axioms completeCandidates_length
#print axioms completeCandidates_nodup

end Agent5.CompleteStreamDecoder
