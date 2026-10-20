import P196.ResidualFivePredecessorMass.Enumeration
import P196.ResidualFivePredecessorMass.WeightedCount

set_option autoImplicit false

/-!
The original complete ordinary predecessor enumerator is evaluated at the
forced residual-five target wrapper. The shorter source-width branch is
empty, and the same-width branch contributes the original coefficient-word
fiber. Its two outer coefficient pairs contribute exactly seven choices.
The resulting weighted sum counts actual ordinary integers.
-/

namespace P196.ResidualFivePredecessorMass

open Agent101
open Agent105DecoderLocal9df76b (decodePair)
open Agent105DecoderScan9df76b (scan decodeAtWidth)
open Agent105NumericDecoder9df76b (decodeNumerical)
open Agent105DecodedFiber9df76b (decodedFiber)
open Agent105WordFiber9df76b (wordFiber)

private theorem decode_one_six_same_width (ds : List Nat) :
    decodeNumerical (digitFn (wrapDigits 1 1 (wrapDigits 6 6 ds)))
      (wrapDigits 1 1 (wrapDigits 6 6 ds)).length
      (wrapDigits 1 1 (wrapDigits 6 6 ds)).length =
      (scan ds.length (digitFn ds) 0 0).map
        (fun qs => wrapDigits 1 1 (wrapDigits 6 6 qs)) := by
  rw [decodeNumerical, if_pos rfl, length_wrapDigits,
    P196.ResidualFivePredecessorCount.decodeAtWidth_wrap
      1 1 0 (wrapDigits 6 6 ds) (by decide)]
  have hone : decodePair 1 1 0 0 = some ⟨1, 0, 0⟩ := by decide
  have hsix : decodePair 6 6 0 0 = some ⟨6, 0, 0⟩ := by decide
  simp only [hone, Nat.zero_lt_succ, if_true]
  rw [length_wrapDigits, P196.ResidualFivePredecessorCount.scan_wrap, hsix]
  simp only [Option.some_bind]
  cases scan ds.length (digitFn ds) 0 0 <;> rfl

private theorem decode_one_six_shorter_width (ds : List Nat) :
    decodeNumerical (digitFn (wrapDigits 1 1 (wrapDigits 6 6 ds)))
      (wrapDigits 1 1 (wrapDigits 6 6 ds)).length
      ((wrapDigits 1 1 (wrapDigits 6 6 ds)).length - 1) = none := by
  have hsub : (wrapDigits 1 1 (wrapDigits 6 6 ds)).length - 1 =
      (wrapDigits 6 6 ds).length + 1 := by
    simp [length_wrapDigits]
  have hne : (wrapDigits 1 1 (wrapDigits 6 6 ds)).length ≠
      (wrapDigits 6 6 ds).length + 1 := by
    simp only [length_wrapDigits] <;> omega
  have hwidth : (wrapDigits 1 1 (wrapDigits 6 6 ds)).length =
      (wrapDigits 6 6 ds).length + 1 + 1 := by
    simp only [length_wrapDigits]
  have hhigh : digitFn (wrapDigits 1 1 (wrapDigits 6 6 ds))
      ((wrapDigits 6 6 ds).length + 1) = 1 :=
    Agent105DecoderScan9df76b.digitFn_wrap_last 1 1 (wrapDigits 6 6 ds)
  rw [hsub, decodeNumerical, if_neg hne, if_pos ⟨hwidth, hhigh⟩]
  exact P196.ResidualFivePredecessorCount.shorter_decode_none 6 6 ds (by decide)

/-- The existing two-width predecessor enumerator at a wrapped list
has seven times the original raw split weight of its successful scan. -/
theorem predecessor_block_length (ds : List Nat) :
    (Agent105Predecessors9df76b.predecessors
      (digitFn (wrapDigits 1 1 (wrapDigits 6 6 ds)))
      (wrapDigits 1 1 (wrapDigits 6 6 ds)).length).length =
      7 * ((scan ds.length (digitFn ds) 0 0).map rawWeight).getD 0 := by
  rw [Agent105Predecessors9df76b.predecessors, List.length_append]
  simp only [decodedFiber, decode_one_six_same_width, decode_one_six_shorter_width]
  cases hs : scan ds.length (digitFn ds) 0 0 with
  | none => simp [hs]
  | some qs => simp [hs, wordFiber_wrap_one_six_length]

private theorem weighted_filter_sum (words : List (List Nat)) :
    ((words.filter (fun ds => (scan ds.length (digitFn ds) 0 0).isSome)).map
      (fun ds => 7 * ((scan ds.length (digitFn ds) 0 0).map rawWeight).getD 0)).sum =
      7 * (words.map
        (fun ds => ((scan ds.length (digitFn ds) 0 0).map rawWeight).getD 0)).sum := by
  induction words with
  | nil => rfl
  | cons ds words ih =>
    cases hs : scan ds.length (digitFn ds) 0 0 <;>
      simp [hs, ih, Nat.mul_add]

/-- The weighted scanner sum is the cardinality of the actual duplicate-free
ordinary integer list, with the original enumeration at both levels. -/
theorem predecessors_length_eq_middle (r : Nat) :
    (predecessors r).length = 7 * middleWeight r 0 0 := by
  rw [predecessors, P196.ResidualFivePredecessorCount.survivorWords_outer_reduction,
    List.flatMap_map, List.length_flatMap]
  simp only [predecessor_block_length]
  exact weighted_filter_sum (rawWords (List.replicate r 9) none)

end P196.ResidualFivePredecessorMass

#print axioms P196.ResidualFivePredecessorMass.predecessor_block_length
#print axioms P196.ResidualFivePredecessorMass.predecessors_length_eq_middle
