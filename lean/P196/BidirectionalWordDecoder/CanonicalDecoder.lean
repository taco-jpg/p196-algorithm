import P196.BidirectionalWordDecoder.StreamDecoder
import P196.PhaseStreamRecovery.CanonicalFibers

/-!
# Constructive canonical recovery without the original phase or width

Agent #5. Decode at the observation width and remove the maximal suffix of
the decoded phase. Correctness needs only an upper bound on the stripped
core length. The original word may contain arbitrarily many extra terminal
phase letters and may therefore be longer than the decoder's width.

The proof imports the exact stripping and phase-padding identities and the
original stripSuffix retraction. No integer-orbit conclusion is asserted.
-/

namespace Agent5.BidirectionalWordDecoder

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.PhaseStreamRecovery

/-- Decode and canonically trim the result, using only a cutoff parameter
and the two observed lists. -/
def decodeCanonicalState (n : Nat) (low high : List Nat) : Outer :=
  let state := decodeState n low high
  { c := state.c, B := stripSuffix state.c state.B }

/-- The original phase and canonical word are recovered as long as the
cutoff bounds the stripped width. The true phase and original width are
absent from the decoder's inputs. Empty cores and zero heads are included. -/
theorem decodeCanonicalState_correct (c N : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18)
    (hN : (stripSuffix c B).length ≤ N) :
    decodeCanonicalState N
      (adicNumeratorDigits (N + 1) (zValue c B - (c : Int)))
      (fractionDigits (N + 1) (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) =
      { c := c, B := stripSuffix c B } := by
  let C := stripSuffix c B
  let P := C ++ List.replicate (N - C.length) c
  have hC : ∀ x ∈ C, x ≤ 18 := Agent116.Exterior.stripSuffix_bounded c B hB
  have hc18 : c ≤ 18 := (phase_facts c 0 hc (by decide)).2.2.2.2
  have hP : ∀ x ∈ P, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hC x hx
    · rw [List.eq_of_mem_replicate hx]
      exact hc18
  have hlen : P.length = N := by
    simp only [P, List.length_append, List.length_replicate]
    change C.length + (N - C.length) = N
    exact Nat.add_sub_of_le hN
  have hdecoded : decodeState N
      (adicNumeratorDigits (N + 1) (zValue c B - (c : Int)))
      (fractionDigits (N + 1) (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) =
      { c := c, B := P } := by
    have h := decodeState_correct c P hc hP
    dsimp only [P, C] at h
    rw [Agent5.TrimmedStreamObservation.phase_padding_low,
      Agent5.TrimmedStreamObservation.phase_padding_high c _ (stripSuffix c B) _ hc,
      stripSuffix_low_stream c _ B, stripSuffix_high_stream c _ B hc] at h
    have hlen' :
        (stripSuffix c B ++ List.replicate (N - (stripSuffix c B).length) c).length = N :=
      hlen
    rw [hlen'] at h
    exact h
  simp only [decodeCanonicalState, hdecoded]
  change { c := c, B := stripSuffix c P } = ({ c := c, B := stripSuffix c B } : Outer)
  simp only [P, C, Agent116.Exterior.stripSuffix_append_replicate,
    Agent116.Exterior.stripSuffix_idempotent]

#print axioms decodeCanonicalState_correct

end Agent5.BidirectionalWordDecoder
