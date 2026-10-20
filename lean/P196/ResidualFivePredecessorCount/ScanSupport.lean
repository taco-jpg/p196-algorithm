import P196.Agent105NumericDecoder.Agent105DecoderScan9df76b

set_option autoImplicit false

/-! Exact finite-payload congruence and literal digit-wrapper transport
for the existing numerical scanner. -/

namespace P196.ResidualFivePredecessorCount

open Agent101
open Agent105DecoderLocal9df76b (decodePair)
open Agent105DecoderScan9df76b (scan)

/-- A scan depends only on the finite digit payload it actually consumes. -/
theorem scan_congr_on_width (L : Nat) (e f : Nat → Nat) (a b : Nat)
    (h : ∀ i, i < L → e i = f i) :
    scan L e a b = scan L f a b := by
  induction L using Nat.strongRecOn generalizing e f a b with
  | ind L ih =>
    match L with
    | 0 => rfl
    | 1 =>
      simp only [scan, h 0 (by omega)]
    | L + 2 =>
      have hzero : e 0 = f 0 := h 0 (by omega)
      have hlast : e (L + 1) = f (L + 1) := h (L + 1) (by omega)
      simp only [scan, hzero, hlast]
      cases hd : decodePair (f 0) (f (L + 1)) a b with
      | none => rfl
      | some E =>
        apply congrArg (Option.map (wrapDigits E.coeff E.coeff))
        exact ih L (by omega) (fun i => e (i + 1))
          (fun i => f (i + 1)) E.low E.high
          (fun i hi => h (i + 1) (by omega))

/-- Scanning a literal digit wrapper uses the original local decoder and
then the unchanged interior scan. The empty interior is included. -/
theorem scan_wrap (u v a b : Nat) (ds : List Nat) :
    scan (ds.length + 2) (digitFn (wrapDigits u v ds)) a b =
      (decodePair u v a b).bind (fun E =>
        (scan ds.length (digitFn ds) E.low E.high).map
          (wrapDigits E.coeff E.coeff)) := by
  rw [scan, Agent105DecoderScan9df76b.digitFn_wrap_zero,
    Agent105DecoderScan9df76b.digitFn_wrap_last]
  cases hd : decodePair u v a b with
  | none => rfl
  | some E =>
    apply congrArg (Option.map (wrapDigits E.coeff E.coeff))
    exact scan_congr_on_width ds.length
      (fun i => digitFn (wrapDigits u v ds) (i + 1))
      (digitFn ds) E.low E.high
      (fun i hi => Agent105DecoderScan9df76b.digitFn_wrap_inner u v ds i hi)

/-- Boolean acceptance is the projection of the exact wrapper equation. -/
theorem scan_wrap_isSome (u v a b : Nat) (ds : List Nat) :
    (scan (wrapDigits u v ds).length
      (digitFn (wrapDigits u v ds)) a b).isSome =
      match decodePair u v a b with
      | none => false
      | some E => (scan ds.length (digitFn ds) E.low E.high).isSome := by
  rw [length_wrapDigits, scan_wrap]
  cases hd : decodePair u v a b with
  | none => rfl
  | some E =>
    exact Option.isSome_map'

end P196.ResidualFivePredecessorCount

#print axioms P196.ResidualFivePredecessorCount.scan_congr_on_width
#print axioms P196.ResidualFivePredecessorCount.scan_wrap
#print axioms P196.ResidualFivePredecessorCount.scan_wrap_isSome
