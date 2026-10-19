import P196.BidirectionalWordDecoder.Numeric
import P196.PhaseStreamRecovery.Decoder

/-!
# Executable recovery of the original exterior state

Agent #5. Recover the phase and actual high carry from the two observed
prefixes, extract the old positional values, and run the constructive word
decoder. The numerical decoder's wider coefficient domain does not enlarge
the hypotheses of the original stream identities: this module keeps their
bound of eighteen and the original nonneutral phases.

All functions are total on arbitrary observed lists. Correctness is proved
for the original streams, including empty, zero-head, and untrimmed words.
-/

namespace Agent5.BidirectionalWordDecoder

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.StreamObservationInjectivity
open Agent5.PhaseStreamRecovery

/-- Extract both positional coefficient values using only the width and
the two observed lists. The phase and high carry are decoded internally. -/
def observedValues (n : Nat) (low high : List Nat) : Nat × Nat :=
  let c := decodePhase n low high
  let g := decodeHighCarry n low high
  let k := if 10 ≤ c then 1 else 0
  (lowValue low - (c - 10 * k) * 10 ^ n,
    (if g = 0 then highValue high / 10 else highValue high) - k)

/-- The internally decoded phase and carry recover the original pair of
positional values, without receiving either as a separate argument. -/
theorem observedValues_correct (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    observedValues B.length
      (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
      (fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) =
      (lowValue B, highValue B) := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let g := (normalize B.reverse k).2
  let low := adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int))
  let high := fractionDigits (B.length + 1) (rhoNum c B)
    (9 * 10 ^ B.length * 10 ^ g)
  have hphase : decodePhase B.length low high = c :=
    decodePhase_correct c B hc hB
  have hcarry : decodeHighCarry B.length low high = g :=
    decodeHighCarry_correct c B hc hB
  have hl : lowValue low = lowValue B + (c - 10 * k) * 10 ^ B.length :=
    low_stream_prefix_value c B hc hB
  have hr : highValue high =
      if g = 0 then 10 * (highValue B + k) + (c - 9 * k)
      else highValue B + k := high_stream_prefix_value c B hc hB
  have ht : c - 9 * k < 9 := (phase_tail_digit c hc).2
  change observedValues B.length low high = (lowValue B, highValue B)
  unfold observedValues
  rw [hphase, hcarry]
  change (lowValue low - (c - 10 * k) * 10 ^ B.length,
    (if g = 0 then highValue high / 10 else highValue high) - k) =
      (lowValue B, highValue B)
  apply Prod.ext
  · change lowValue low - (c - 10 * k) * 10 ^ B.length = lowValue B
    rw [hl, Nat.add_sub_cancel_right]
  · change (if g = 0 then highValue high / 10 else highValue high) - k = highValue B
    rw [hr]
    by_cases hg : g = 0
    · simp only [if_pos hg]
      omega
    · simp [hg]

/-- A total executable decoder returning the existing exterior state type. -/
def decodeState (n : Nat) (low high : List Nat) : Outer :=
  let values := observedValues n low high
  { c := decodePhase n low high,
    B := decodeValues n values.1 values.2 }

/-- Complete original prefixes recover every coefficient and the phase
algorithmically. No trimming, positive head, or known carry is required. -/
theorem decodeState_correct (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    decodeState B.length
      (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
      (fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) =
      { c := c, B := B } := by
  have hb90 : ∀ x ∈ B, x ≤ 90 := by
    intro x hx
    have := hB x hx
    omega
  simp only [decodeState, observedValues_correct c B hc hB,
    decodePhase_correct c B hc hB, decodeValues_correct B hb90]

#print axioms observedValues_correct
#print axioms decodeState_correct

end Agent5.BidirectionalWordDecoder
