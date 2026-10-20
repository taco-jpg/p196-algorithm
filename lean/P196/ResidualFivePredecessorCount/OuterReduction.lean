import P196.ResidualFivePredecessorCount.DecoderBridge
import P196.ResidualFivePredecessorCount.ScanSupport

set_option autoImplicit false

/-!
The complete original residual-five enumeration has two outer pair choices
and seven next-pair choices. The existing numerical decoder accepts only
the literal outer digits 1, 6, ..., 6, 1, with zero carries entering the
remaining complementary-pair word. The shorter-source branch is excluded
by its first local decoding equation, including the empty middle word.
-/

namespace P196.ResidualFivePredecessorCount

open Agent101
open Agent105DecoderLocal9df76b (decodePair)
open Agent105DecoderScan9df76b (scan decodeAtWidth)
open Agent105NumericDecoder9df76b (decodeNumerical)

private theorem pairChoices_two :
    pairChoices true 2 = [(0, 2), (1, 1)] := by decide

private theorem pairChoices_twelve :
    pairChoices false 12 =
      [(3, 9), (4, 8), (5, 7), (6, 6), (7, 5), (8, 4), (9, 3)] := by
  decide

private theorem hasPositivePredecessorB_wrap (u v : Nat) (ds : List Nat) :
    hasPositivePredecessorB (wrapDigits u v ds) =
      ((decodeAtWidth (digitFn (wrapDigits u v ds)) (ds.length + 2) 0).isSome ||
      (if v = 1 then
        decodeAtWidth (digitFn (wrapDigits u v ds)) (ds.length + 1) 1
       else none).isSome) := by
  have hsub : ds.length + 2 - 1 = ds.length + 1 := by omega
  have hne : ds.length + 2 ≠ ds.length + 1 := by omega
  simp [hasPositivePredecessorB, length_wrapDigits, decodeNumerical,
    hsub, hne, Agent105DecoderScan9df76b.digitFn_wrap_last]

/-- The positive first coefficient check in the existing width decoder
is retained explicitly when transporting a literal outer digit pair. -/
theorem decodeAtWidth_wrap (u v b : Nat) (ds : List Nat)
    (hb : b ≤ 1) :
    decodeAtWidth (digitFn (wrapDigits u v ds)) (ds.length + 2) b =
      match decodePair u v 0 b with
      | none => none
      | some E =>
        if 0 < E.coeff then
          (scan ds.length (digitFn ds) E.low E.high).map
            (wrapDigits E.coeff E.coeff)
        else none := by
  rw [decodeAtWidth, if_pos (show 0 < ds.length + 2 ∧ b ≤ 1 from ⟨by omega, hb⟩),
    scan_wrap]
  cases hd : decodePair u v 0 b with
  | none => rfl
  | some E =>
    cases hi : scan ds.length (digitFn ds) E.low E.high <;>
      simp [hi, Agent105DecoderScan9df76b.digitFn_wrap_zero]

private theorem rejects_outer_zero_two (ds : List Nat) :
    hasPositivePredecessorB (wrapDigits 0 2 ds) = false := by
  rw [hasPositivePredecessorB_wrap, decodeAtWidth_wrap 0 2 0 ds (by decide)]
  have hlocal : decodePair 0 2 0 0 = none := by decide
  simp [hlocal]

private theorem shorter_scan_none (u v : Nat) (ds : List Nat)
    (hlocal : decodePair 1 v 0 1 = none) :
    scan ((wrapDigits u v ds).length + 1)
      (digitFn (wrapDigits 1 1 (wrapDigits u v ds))) 0 1 = none := by
  have hlen : (wrapDigits u v ds).length + 1 = (ds.length + 1) + 2 := by
    rw [length_wrapDigits]
  rw [hlen, scan, Agent105DecoderScan9df76b.digitFn_wrap_zero]
  have hhigh :
      digitFn (wrapDigits 1 1 (wrapDigits u v ds)) ((ds.length + 1) + 1) = v := by
    rw [Agent105DecoderScan9df76b.digitFn_wrap_inner 1 1
      (wrapDigits u v ds) (ds.length + 1) (by rw [length_wrapDigits]; omega),
      Agent105DecoderScan9df76b.digitFn_wrap_last]
  rw [hhigh, hlocal]

theorem shorter_decode_none (u v : Nat) (ds : List Nat)
    (hlocal : decodePair 1 v 0 1 = none) :
    decodeAtWidth (digitFn (wrapDigits 1 1 (wrapDigits u v ds)))
      ((wrapDigits u v ds).length + 1) 1 = none := by
  simp [decodeAtWidth, shorter_scan_none u v ds hlocal]

private theorem accepts_outer_one_one (u v : Nat) (ds : List Nat)
    (hshort : decodePair 1 v 0 1 = none) :
    hasPositivePredecessorB (wrapDigits 1 1 (wrapDigits u v ds)) =
      (scan (wrapDigits u v ds).length (digitFn (wrapDigits u v ds)) 0 0).isSome := by
  rw [hasPositivePredecessorB_wrap,
    decodeAtWidth_wrap 1 1 0 (wrapDigits u v ds) (by decide)]
  have hlocal : decodePair 1 1 0 0 = some ⟨1, 0, 0⟩ := by decide
  simp [hlocal, shorter_decode_none u v ds hshort]

private theorem rejects_second_pair (u v : Nat) (ds : List Nat)
    (hshort : decodePair 1 v 0 1 = none)
    (hsame : decodePair u v 0 0 = none) :
    hasPositivePredecessorB (wrapDigits 1 1 (wrapDigits u v ds)) = false := by
  rw [accepts_outer_one_one u v ds hshort, scan_wrap_isSome, hsame]

/-- The one surviving outside choice preserves exactly the original middle
scanner's acceptance predicate. This also checks the shorter source width. -/
theorem accepts_one_six_wrapper (ds : List Nat) :
    hasPositivePredecessorB (wrapDigits 1 1 (wrapDigits 6 6 ds)) =
      (scan ds.length (digitFn ds) 0 0).isSome := by
  rw [accepts_outer_one_one 6 6 ds (by decide), scan_wrap_isSome]
  have hlocal : decodePair 6 6 0 0 = some ⟨6, 0, 0⟩ := by decide
  simp [hlocal]

/-- Exact list identity for the original complete fiber filter. No target
digit words are omitted, and the enumeration order is preserved. -/
theorem survivorWords_outer_reduction (r : Nat) :
    survivorWords r =
      ((rawWords (List.replicate r 9) none).filter
        (fun ds => (scan ds.length (digitFn ds) 0 0).isSome)).map
          (fun ds => wrapDigits 1 1 (wrapDigits 6 6 ds)) := by
  have h39 (ds : List Nat) := rejects_second_pair 3 9 ds (by decide) (by decide)
  have h48 (ds : List Nat) := rejects_second_pair 4 8 ds (by decide) (by decide)
  have h57 (ds : List Nat) := rejects_second_pair 5 7 ds (by decide) (by decide)
  have h75 (ds : List Nat) := rejects_second_pair 7 5 ds (by decide) (by decide)
  have h84 (ds : List Nat) := rejects_second_pair 8 4 ds (by decide) (by decide)
  have h93 (ds : List Nat) := rejects_second_pair 9 3 ds (by decide) (by decide)
  have hfalse : (rawWords (List.replicate r 9) none).filter (fun _ => false) = [] := by
    apply List.filter_eq_nil_iff.mpr
    simp
  unfold survivorWords Agent103.ResidualFiveFibers.half
  rw [canonicalWords, pairChoices_two, rawWords, pairChoices_twelve]
  simp only [List.flatMap_cons, List.flatMap_nil, List.map_append,
    List.map_nil, List.append_nil, List.map_map, List.filter_append,
    List.filter_map]
  simp [Function.comp_def, rejects_outer_zero_two, h39, h48, h57,
    h75, h84, h93, accepts_one_six_wrapper, hfalse]

end P196.ResidualFivePredecessorCount

#print axioms P196.ResidualFivePredecessorCount.accepts_one_six_wrapper
#print axioms P196.ResidualFivePredecessorCount.survivorWords_outer_reduction
