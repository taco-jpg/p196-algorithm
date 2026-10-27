import P196.Agent114NeutralUniformExterior.UniformChain
import P196.Agent114NeutralExteriorCanonical.CanonicalCycle

/-!
# Exact fixed-width exterior certificate model

The previously used common-width padding reduction is formalized for the
unchanged A120 cycle checker.  A prescribed width cap loses no accepted cycle:
all exterior interfaces may have exactly that width and each exterior trim
may equal its actual overflow.  A further corollary applies after the existing
maximal-suffix canonicalizer, matching canonical-width bounded searches.

This is a model-equivalence theorem, not a search result or a decimal witness.
-/

namespace Agent114.NeutralUniformExterior

open Agent120.Neutral Agent114.NeutralExteriorCanonical

theorem uniformWidth_implies_bound {M : Nat} {es : List Edge} {B : List Nat}
    (hw : UniformWidth M es B) : WidthBound M es B := by
  constructor
  · have h := hw.1
    omega
  · intro e he
    obtain ⟨hB, hB2⟩ := hw.2 e he
    constructor <;> omega

/-- An exterior-width bounded accepted certificate exists exactly when an
accepted width-M certificate with actual-overflow exterior trims exists. -/
theorem bounded_cycle_exists_iff_uniform (b M : Nat) :
    (∃ es B C, cycleOK b es B C = true ∧ WidthBound M es B) ↔
      ∃ es B C, cycleOK b es B C = true ∧ UniformWidth M es B ∧
        (∀ e ∈ es, e.u = gam b e.B e.C) := by
  constructor
  · rintro ⟨es, B, C, hcert, hb⟩
    have hs := hcert
    simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hs
    obtain ⟨⟨⟨⟨_, hc⟩, _⟩, _⟩, _⟩ := hs
    exact ⟨uniformEdges b M es, padWidth b M B, C,
      uniform_cycleOK hcert hb, uniform_widths b M es B hb, uniformEdges_trims hc⟩
  · rintro ⟨es, B, C, hcert, hw, _⟩
    exact ⟨es, B, C, hcert, uniformWidth_implies_bound hw⟩

/-- Maximal exterior suffix removal cannot increase the declared width cap. -/
theorem canonical_width_bound_of_bound (b M : Nat) (es : List Edge) (B : List Nat)
    (hb : WidthBound M es B) :
    WidthBound M (canonicalEdges b es) (canonB b B) := by
  constructor
  · exact Nat.le_trans (canonB_length_le b B) hb.1
  · intro e he
    obtain ⟨E, hE, rfl⟩ := List.mem_map.mp he
    obtain ⟨hB, hB2⟩ := hb.2 E hE
    exact ⟨Nat.le_trans (canonB_length_le b E.B) hB,
      Nat.le_trans (canonB_length_le b E.B2) hB2⟩

/-- The same fixed-width model is complete when only the canonical exterior
widths are bounded.  Original padded representatives may be arbitrarily long. -/
theorem canonical_bounded_cycle_exists_iff_uniform (b M : Nat) :
    (∃ es B C, cycleOK b es B C = true ∧
      WidthBound M (canonicalEdges b es) (canonB b B)) ↔
      ∃ es B C, cycleOK b es B C = true ∧ UniformWidth M es B ∧
        (∀ e ∈ es, e.u = gam b e.B e.C) := by
  constructor
  · rintro ⟨es, B, C, hcert, hb⟩
    apply (bounded_cycle_exists_iff_uniform b M).1
    exact ⟨canonicalEdges b es, canonB b B, C, canonical_cycleOK hcert, hb⟩
  · rintro ⟨es, B, C, hcert, hw, _⟩
    exact ⟨es, B, C, hcert,
      canonical_width_bound_of_bound b M es B (uniformWidth_implies_bound hw)⟩

end Agent114.NeutralUniformExterior

#print axioms Agent114.NeutralUniformExterior.bounded_cycle_exists_iff_uniform
#print axioms Agent114.NeutralUniformExterior.canonical_bounded_cycle_exists_iff_uniform
