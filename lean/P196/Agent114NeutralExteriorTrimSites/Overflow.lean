import P196.Agent114NeutralExteriorTrimSites.LastCoefficient
import P196.Agent114NeutralExteriorCanonical.CanonicalEdge

/-!
# Agent 114: exterior suffix depth on overflow steps

An overflow step preserves the exact maximal neutral suffix depth.  For an
accepted edge, its exterior trim is therefore exactly the loss of suffix
depth.  In particular, a source with no neutral suffix cannot trim on an
overflow step; no normalization of the target is required.  These statements
use the original A120 hypotheses and checker in every base at least two.
-/

namespace Agent114.NeutralExteriorTrimSites

open Agent120.Neutral Agent114.NeutralExteriorPadding
  Agent114.NeutralExteriorCanonical

private theorem suffixDepth_zero_of_last_ne {b : Nat} {B : List Nat}
    (hn : B.getLast? ≠ some (b - 1)) : suffixDepth b B = 0 := by
  have hk : canonB b B = B := (canonB_eq_self_iff b B).2 hn
  simpa only [hk] using suffixDepth_canonB b B

/-- Overflow preserves the whole maximal neutral suffix, including for empty
exterior words.  This is a raw successor identity, before choosing a trim. -/
theorem overflow_suffixDepth {b : Nat} {B C : List Nat}
    (h : Hyp b B C) (hg : gam b B C = 1) :
    suffixDepth b (nextB b B C) = suffixDepth b B := by
  have hk : Hyp b (canonB b B) C := (canonB_hyp_iff b B C).2 h
  have hgam := gam_suffixPad hk (suffixDepth b B)
  rw [canonB_decompose] at hgam
  have hgk : gam b (canonB b B) C = 1 := hgam.symm.trans hg
  have hlast : (nextB b (canonB b B) C).getLast? ≠ some (b - 1) := by
    intro hr
    exact canonB_last_ne b B ((overflow_last_neutral_iff hk hgk).1 hr)
  have hzero := suffixDepth_zero_of_last_ne hlast
  have hcov := nextB_suffixPad hk (suffixDepth b B)
  rw [canonB_decompose] at hcov
  calc
    suffixDepth b (nextB b B C) =
        suffixDepth b (suffixPad b (suffixDepth b B)
          (nextB b (canonB b B) C)) := congrArg (suffixDepth b) hcov
    _ = suffixDepth b (nextB b (canonB b B) C) + suffixDepth b B :=
      suffixDepth_suffixPad b (suffixDepth b B) _
    _ = suffixDepth b B := by rw [hzero, Nat.zero_add]

/-- An accepted overflow edge can trim only neutral suffix already present
in its source; the remaining suffix is exactly the target suffix. -/
theorem overflow_edge_depth_balance {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hg : gam b E.B E.C = 1) :
    suffixDepth b E.B = suffixDepth b E.B2 + E.u := by
  have hd := congrArg (suffixDepth b) (edgeOK_sound he).2.1
  change suffixDepth b (nextB b E.B E.C) =
    suffixDepth b (suffixPad b E.u E.B2) at hd
  rw [overflow_suffixDepth (edgeOK_sound he).1 hg,
    suffixDepth_suffixPad] at hd
  exact hd

/-- Source normalization alone forces zero exterior trim on overflow. -/
theorem canonical_overflow_trim_zero {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hg : gam b E.B E.C = 1)
    (hn : E.B.getLast? ≠ some (b - 1)) : E.u = 0 := by
  have hd := overflow_edge_depth_balance he hg
  have hz := suffixDepth_zero_of_last_ne hn
  omega

/-- Positive trim from a normalized source is possible only without overflow. -/
theorem canonical_positive_trim_nonoverflow {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hn : E.B.getLast? ≠ some (b - 1))
    (hu : 0 < E.u) : gam b E.B E.C = 0 := by
  have hgle := (edgeOK_sound he).1.gam_le
  have hgne : gam b E.B E.C ≠ 1 := by
    intro hg
    have hz := canonical_overflow_trim_zero he hg hn
    omega
  omega

/-- An empty exterior can never be the source of an accepted positive trim.
No source or target normalization assumption is needed. -/
theorem positive_trim_source_ne_nil {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hu : 0 < E.u) : E.B ≠ [] := by
  intro hB
  have hn : E.B.getLast? ≠ some (b - 1) := by simp [hB]
  have hg0 := canonical_positive_trim_nonoverflow he hn hu
  have hf : 0 ≠ e2 b [] E.C := by
    simpa [hB, e1] using (edgeOK_sound he).1.flip
  have he20 : e2 b [] E.C = 0 := by
    simpa [hB, gam] using hg0
  exact hf he20.symm

end Agent114.NeutralExteriorTrimSites

#print axioms Agent114.NeutralExteriorTrimSites.overflow_suffixDepth
#print axioms Agent114.NeutralExteriorTrimSites.overflow_edge_depth_balance
#print axioms Agent114.NeutralExteriorTrimSites.canonical_overflow_trim_zero
#print axioms Agent114.NeutralExteriorTrimSites.canonical_positive_trim_nonoverflow
#print axioms Agent114.NeutralExteriorTrimSites.positive_trim_source_ne_nil
