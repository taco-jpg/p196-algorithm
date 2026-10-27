import P196.Agent114NeutralExteriorCanonical.SuffixNormalization
import P196.Agent114NeutralExteriorPadding.EdgeTransport

/-!
# Agent 114: maximal exterior suffix normalization of one checked edge

The normalized exterior trim is the neutral suffix depth of the actual raw
successor of the normalized source.  An accepted original edge supplies the
natural-number balance needed to recover it by the existing padding transport.
The center words and center trim are unchanged.  This formalizes the exterior
part of the prior paper canonicalization argument; no decimal cycle is claimed.
-/

namespace Agent114.NeutralExteriorCanonical

open Agent120.Neutral Agent114.NeutralExteriorPadding

/-- Remove the neutral suffix from both exteriors and maximally trim the raw
successor of the normalized source.  Its acceptance theorem requires that the
original edge is accepted; no equivalence for arbitrary rejected inputs is used.
-/
def canonicalEdge (b : Nat) (E : Edge) : Edge where
  B := canonB b E.B
  C := E.C
  B2 := canonB b E.B2
  C2 := E.C2
  u := suffixDepth b (nextB b (canonB b E.B) E.C)
  v := E.v

private theorem raw_suffixPad_eq {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    suffixPad b (suffixDepth b E.B) (nextB b (canonB b E.B) E.C) =
      suffixPad b E.u E.B2 := by
  have h := (edgeOK_sound he).1
  have hk : Hyp b (canonB b E.B) E.C := (canonB_hyp_iff b E.B E.C).2 h
  calc
    suffixPad b (suffixDepth b E.B) (nextB b (canonB b E.B) E.C) =
        nextB b (suffixPad b (suffixDepth b E.B) (canonB b E.B)) E.C :=
      (nextB_suffixPad hk (suffixDepth b E.B)).symm
    _ = nextB b E.B E.C := by rw [canonB_decompose]
    _ = suffixPad b E.u E.B2 := (edgeOK_sound he).2.1

/-- The canonical target is determined by the canonical source's raw successor. -/
theorem canonicalEdge_raw_target {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    canonB b (nextB b (canonB b E.B) E.C) = canonB b E.B2 := by
  have h := congrArg (canonB b) (raw_suffixPad_eq he)
  simpa only [canonB_suffixPad] using h

/-- The source and target suffix depths give an exact balance in natural numbers. -/
theorem canonicalEdge_balance {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    suffixDepth b E.B + (canonicalEdge b E).u = E.u + suffixDepth b E.B2 := by
  have h := congrArg (suffixDepth b) (raw_suffixPad_eq he)
  simp only [suffixDepth_suffixPad] at h
  change suffixDepth b E.B + suffixDepth b (nextB b (canonB b E.B) E.C) =
    E.u + suffixDepth b E.B2
  omega

/-- The accepted original edge is the indicated padding of its canonical edge. -/
theorem canonicalEdge_restore {b : Nat} {E : Edge}
    (_he : edgeOK b E = true) :
    padEdge b (suffixDepth b E.B) (suffixDepth b E.B2) E.u
      (canonicalEdge b E) = E := by
  cases E
  simp [padEdge, canonicalEdge, canonB_decompose]

/-- Removing both exterior neutral suffixes preserves acceptance of a checked edge. -/
theorem canonicalEdge_ok {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    edgeOK b (canonicalEdge b E) = true := by
  apply (edgeOK_suffixPad_iff (suffixDepth b E.B) (suffixDepth b E.B2) E.u
    (canonicalEdge_balance he)).1
  rw [canonicalEdge_restore he]
  exact he

/-- The raw successor is precisely the canonical target followed by the forced
maximal neutral suffix. -/
theorem canonicalEdge_raw_eq {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    nextB b (canonB b E.B) E.C =
      suffixPad b (canonicalEdge b E).u (canonB b E.B2) := by
  have h := canonB_decompose b (nextB b (canonB b E.B) E.C)
  rw [canonicalEdge_raw_target he] at h
  exact h.symm

/-- The source suffix cannot exceed the original trim plus the target suffix. -/
theorem canonicalEdge_shift_nonnegative {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    suffixDepth b E.B ≤ E.u + suffixDepth b E.B2 := by
  have h := canonicalEdge_balance he
  omega

/-- The usual trim-shift formula is exact, with no truncated negative case. -/
theorem canonicalEdge_trim_formula {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    (canonicalEdge b E).u = E.u + suffixDepth b E.B2 - suffixDepth b E.B := by
  have h := canonicalEdge_balance he
  omega

/-- Once the target has its maximal neutral suffix removed, its exterior trim
is uniquely forced by the raw successor equation. -/
theorem canonicalEdge_trims_unique {b : Nat} {E : Edge}
    (_he : edgeOK b E = true) (w : Nat)
    (hw : nextB b (canonB b E.B) E.C =
      canonB b E.B2 ++ List.replicate w (b - 1)) :
    w = (canonicalEdge b E).u := by
  have h := congrArg (suffixDepth b) hw
  change suffixDepth b (nextB b (canonB b E.B) E.C) =
    suffixDepth b (suffixPad b w (canonB b E.B2)) at h
  rw [suffixDepth_suffixPad, suffixDepth_canonB] at h
  change w = suffixDepth b (nextB b (canonB b E.B) E.C)
  omega

end Agent114.NeutralExteriorCanonical

#print axioms Agent114.NeutralExteriorCanonical.canonicalEdge_raw_target
#print axioms Agent114.NeutralExteriorCanonical.canonicalEdge_balance
#print axioms Agent114.NeutralExteriorCanonical.canonicalEdge_restore
#print axioms Agent114.NeutralExteriorCanonical.canonicalEdge_ok
#print axioms Agent114.NeutralExteriorCanonical.canonicalEdge_raw_eq
#print axioms Agent114.NeutralExteriorCanonical.canonicalEdge_shift_nonnegative
#print axioms Agent114.NeutralExteriorCanonical.canonicalEdge_trim_formula
#print axioms Agent114.NeutralExteriorCanonical.canonicalEdge_trims_unique
