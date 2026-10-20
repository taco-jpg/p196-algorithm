import P196.Agent105AllPredecessors.Agent105Predecessors9df76b
import P196.ResidualFivePredecessorCount.OuterReduction

set_option autoImplicit false

/-!
Transport of the original complete ordinary predecessor enumeration through
an outer digit pair of ones and an arbitrary next pair decoded with zero
inner carries. The local hypotheses are retained explicitly, so the result
applies beyond the residual-five specialization and to an empty interior.
-/

namespace P196.ResidualFivePredecessorDigitMass

open Agent101
open Agent105DecoderLocal9df76b (decodePair)
open Agent105DecoderScan9df76b (scan)
open Agent105NumericDecoder9df76b (decodeNumerical)
open Agent105DecodedFiber9df76b (decodedFiber)
open Agent105WordFiber9df76b (wordFiber)

/-- An arbitrary second pair with a zero-carry local decode transports the
same-width numerical decoder to the unchanged interior scanner. -/
theorem decodeNumerical_wrap_one_pair (u v q : Nat) (ds : List Nat)
    (hlocal : decodePair u v 0 0 = some ⟨q, 0, 0⟩) :
    decodeNumerical (digitFn (wrapDigits 1 1 (wrapDigits u v ds)))
      (wrapDigits 1 1 (wrapDigits u v ds)).length
      (wrapDigits 1 1 (wrapDigits u v ds)).length =
      (scan ds.length (digitFn ds) 0 0).map
        (fun qs => wrapDigits 1 1 (wrapDigits q q qs)) := by
  rw [decodeNumerical, if_pos rfl, length_wrapDigits,
    P196.ResidualFivePredecessorCount.decodeAtWidth_wrap
      1 1 0 (wrapDigits u v ds) (by decide)]
  have hone : decodePair 1 1 0 0 = some ⟨1, 0, 0⟩ := by decide
  simp only [hone, Nat.zero_lt_succ, if_true]
  rw [length_wrapDigits, P196.ResidualFivePredecessorCount.scan_wrap, hlocal]
  simp only [Option.some_bind]
  cases scan ds.length (digitFn ds) 0 0 <;> rfl

/-- The complete original two-width enumeration reduces to one decoded
coefficient fiber when its shorter-width first local pair is impossible.
The identity preserves the list order and needs no canonicality assumption. -/
theorem predecessors_wrap_one_pair (u v q : Nat) (ds : List Nat)
    (hlocal : decodePair u v 0 0 = some ⟨q, 0, 0⟩)
    (hshort : decodePair 1 v 0 1 = none) :
    Agent105Predecessors9df76b.predecessors
      (digitFn (wrapDigits 1 1 (wrapDigits u v ds)))
      (wrapDigits 1 1 (wrapDigits u v ds)).length =
      match scan ds.length (digitFn ds) 0 0 with
      | none => []
      | some qs => wordFiber (wrapDigits 1 1 (wrapDigits q q qs)) := by
  have hsub : (wrapDigits 1 1 (wrapDigits u v ds)).length - 1 =
      (wrapDigits u v ds).length + 1 := by simp [length_wrapDigits]
  have hne : (wrapDigits 1 1 (wrapDigits u v ds)).length ≠
      (wrapDigits 1 1 (wrapDigits u v ds)).length - 1 := by
    simp only [length_wrapDigits]
    omega
  have hshorter :
      decodeNumerical (digitFn (wrapDigits 1 1 (wrapDigits u v ds)))
        (wrapDigits 1 1 (wrapDigits u v ds)).length
        ((wrapDigits 1 1 (wrapDigits u v ds)).length - 1) = none := by
    rw [decodeNumerical, if_neg hne]
    split
    · rw [hsub]
      exact P196.ResidualFivePredecessorCount.shorter_decode_none u v ds hshort
    · rfl
  rw [Agent105Predecessors9df76b.predecessors]
  simp only [decodedFiber, decodeNumerical_wrap_one_pair u v q ds hlocal, hshorter]
  cases scan ds.length (digitFn ds) 0 0 <;> simp

/-- The residual-five wrapper is an instance of the generic complete-list
transport, retaining every ordinary predecessor admitted by the decoder. -/
theorem predecessors_wrap_one_six (ds : List Nat) :
    Agent105Predecessors9df76b.predecessors
      (digitFn (wrapDigits 1 1 (wrapDigits 6 6 ds)))
      (wrapDigits 1 1 (wrapDigits 6 6 ds)).length =
      match scan ds.length (digitFn ds) 0 0 with
      | none => []
      | some qs => wordFiber (wrapDigits 1 1 (wrapDigits 6 6 qs)) := by
  exact predecessors_wrap_one_pair 6 6 6 ds (by decide) (by decide)

end P196.ResidualFivePredecessorDigitMass

#print axioms P196.ResidualFivePredecessorDigitMass.decodeNumerical_wrap_one_pair
#print axioms P196.ResidualFivePredecessorDigitMass.predecessors_wrap_one_pair
#print axioms P196.ResidualFivePredecessorDigitMass.predecessors_wrap_one_six
