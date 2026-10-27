import P196.Agent119NeutralLengthAccounting.StepLengths
import P196.Agent114NeutralExteriorPadding.EdgeTransport

/-!
# Agent 114: uniform exterior width for a checked edge

Pad both exterior endpoints to a common width bound.  The existing checked-edge
length identity makes the replacement trim exactly the overflow bit, and the
existing suffix transport proves acceptance.  Center words and center trims
remain unchanged.  This is a reduction for certificates, not a new certificate.
-/

namespace Agent114.NeutralUniformExterior

open Agent120.Neutral Agent114.NeutralExteriorPadding

/-- Add the neutral suffix needed to reach width `M` when the input fits. -/
def padWidth (b M : Nat) (B : List Nat) : List Nat :=
  suffixPad b (M - B.length) B

/-- Pad both exterior endpoints to width `M` and use overflow as the new trim. -/
def uniformEdge (b M : Nat) (E : Edge) : Edge :=
  padEdge b (M - E.B.length) (M - E.B2.length) (gam b E.B E.C) E

theorem padWidth_length (b M : Nat) (B : List Nat) (hB : B.length ≤ M) :
    (padWidth b M B).length = M := by
  simp only [padWidth, suffixPad, List.length_append, List.length_replicate]
  omega

/-- Exact natural-number balance for the prescribed common width. -/
theorem uniformEdge_balance {b M : Nat} {E : Edge}
    (he : edgeOK b E = true) (hB : E.B.length ≤ M) (hB2 : E.B2.length ≤ M) :
    (M - E.B.length) + E.u = gam b E.B E.C + (M - E.B2.length) := by
  have h := (Agent119.NeutralLengthAccounting.edge_lengths he).1
  omega

/-- Common-width exterior padding preserves acceptance of a checked edge. -/
theorem uniformEdge_ok {b M : Nat} {E : Edge}
    (he : edgeOK b E = true) (hB : E.B.length ≤ M) (hB2 : E.B2.length ≤ M) :
    edgeOK b (uniformEdge b M E) = true := by
  exact edgeOK_suffixPad (M - E.B.length) (M - E.B2.length) (gam b E.B E.C)
    (uniformEdge_balance he hB hB2) he

theorem uniformEdge_widths (b M : Nat) (E : Edge)
    (hB : E.B.length ≤ M) (hB2 : E.B2.length ≤ M) :
    (uniformEdge b M E).B.length = M ∧ (uniformEdge b M E).B2.length = M := by
  change (padWidth b M E.B).length = M ∧ (padWidth b M E.B2).length = M
  exact ⟨padWidth_length b M E.B hB, padWidth_length b M E.B2 hB2⟩

/-- The replacement trim is the actual overflow of the padded source. -/
theorem uniformEdge_trim_eq_gam {b M : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    (uniformEdge b M E).u =
      gam b (uniformEdge b M E).B (uniformEdge b M E).C := by
  change gam b E.B E.C = gam b (suffixPad b (M - E.B.length) E.B) E.C
  exact (gam_suffixPad (edgeOK_sound he).1 (M - E.B.length)).symm

/-- In every checked equal-width exterior edge, the trim already equals overflow. -/
theorem equal_width_trim {b : Nat} {E : Edge} (he : edgeOK b E = true)
    (hwidth : E.B.length = E.B2.length) :
    E.u = gam b E.B E.C := by
  have h := (Agent119.NeutralLengthAccounting.edge_lengths he).1
  omega

end Agent114.NeutralUniformExterior

#print axioms Agent114.NeutralUniformExterior.padWidth_length
#print axioms Agent114.NeutralUniformExterior.uniformEdge_balance
#print axioms Agent114.NeutralUniformExterior.uniformEdge_ok
#print axioms Agent114.NeutralUniformExterior.uniformEdge_widths
#print axioms Agent114.NeutralUniformExterior.uniformEdge_trim_eq_gam
#print axioms Agent114.NeutralUniformExterior.equal_width_trim
