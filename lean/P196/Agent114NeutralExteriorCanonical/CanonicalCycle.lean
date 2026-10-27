import P196.Agent114NeutralExteriorCanonical.CanonicalEdge
import P196.Agent114NeutralExteriorCycle.CycleTransport

/-!
# Exterior canonicalization of complete A120 certificates

Strip each exterior's maximal neutral suffix and use the uniquely forced
maximal exterior trim at each edge.  The accepted original chain is a padded
version of the normalized chain, so the verified transport theorem applies
in its reverse direction.  Centers and their trims are unchanged.

This formalizes the exterior part of Agent 7's prior paper normalization
argument.  It does not assert a decimal certificate or a joint center
canonicalizer, and it does not assert checker equality on rejected inputs.
-/

namespace Agent114.NeutralExteriorCanonical

open Agent120.Neutral Agent114.NeutralExteriorPadding Agent114.NeutralExteriorCycle

/-- Normalize every exterior source and target, preserving the edge order. -/
def canonicalEdges (b : Nat) (es : List Edge) : List Edge :=
  es.map (canonicalEdge b)

theorem canonicalEdges_length (b : Nat) (es : List Edge) :
    (canonicalEdges b es).length = es.length := by
  simp [canonicalEdges]

/-- All normalized exterior interfaces have no terminal neutral coefficient. -/
theorem canonicalEdges_normal (b : Nat) (es : List Edge) :
    ∀ e ∈ canonicalEdges b es,
      e.B.getLast? ≠ some (b - 1) ∧ e.B2.getLast? ≠ some (b - 1) := by
  intro e he
  obtain ⟨E, _, rfl⟩ := List.mem_map.mp he
  exact ⟨canonB_last_ne b E.B, canonB_last_ne b E.B2⟩

/-- Center sources, center targets, and their trim counts remain identical. -/
theorem canonicalEdges_centers (b : Nat) (es : List Edge) :
    (canonicalEdges b es).map (fun e => (e.C, e.C2, e.v)) =
      es.map (fun e => (e.C, e.C2, e.v)) := by
  induction es with
  | nil => rfl
  | cons e es ih =>
      simpa only [canonicalEdges, List.map_cons, canonicalEdge] using
        congrArg (List.cons (e.C, e.C2, e.v)) ih

/-- An accepted original chain is a consistently padded normalized chain. -/
theorem canonical_chain_plan (b : Nat) (es : List Edge) (B C : List Nat)
    (hc : chainOK b es B C = true) :
    PadChain b (suffixDepth b B) (suffixDepth b (endB es B))
      (canonicalEdges b es) es := by
  induction es generalizing B C with
  | nil => exact PadChain.nil (suffixDepth b B)
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, he⟩, hr⟩ := hc
      subst B
      subst C
      have hp := PadChain.cons E.u (canonicalEdge_balance he) (ih E.B2 E.C2 hr)
      rw [canonicalEdge_restore he] at hp
      exact hp

/-- Canonicalization preserves acceptance of every checked chain. -/
theorem canonical_chainOK {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    chainOK b (canonicalEdges b es) (canonB b B) C = true := by
  have hp := canonical_chain_plan b es B C hc
  apply (hp.chainOK_iff (canonB b B) C).1
  simpa only [canonB_decompose] using hc

/-- The accepted normalized chain has the same two carries and overflow bits. -/
theorem canonical_chain_streams {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    (canonicalEdges b es).map (fun e => (e1 b e.B, e2 b e.B e.C, gam b e.B e.C)) =
      es.map (fun e => (e1 b e.B, e2 b e.B e.C, gam b e.B e.C)) := by
  have hp := canonical_chain_plan b es B C hc
  exact (hp.streams_eq (canonB b B) C (canonical_chainOK hc)).symm

/-- Every accepted cycle has an accepted exterior-normalized representative. -/
theorem canonical_cycleOK {b : Nat} {es : List Edge} {B C : List Nat}
    (hcert : cycleOK b es B C = true) :
    cycleOK b (canonicalEdges b es) (canonB b B) C = true := by
  have hs := hcert
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hs
  obtain ⟨⟨⟨⟨_, hc⟩, hB⟩, _⟩, _⟩ := hs
  have hp := canonical_chain_plan b es B C hc
  rw [hB] at hp
  apply (hp.cycleOK_iff (canonB b B) C).1
  simpa only [canonB_decompose] using hcert

/-- Exterior canonicalization preserves total gain on an accepted cycle. -/
theorem canonical_cycle_gain {b : Nat} {es : List Edge} {B C : List Nat}
    (hcert : cycleOK b es B C = true) :
    sumGain (canonicalEdges b es) = sumGain es := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hcert
  obtain ⟨⟨⟨⟨_, hc⟩, hB⟩, _⟩, _⟩ := hcert
  have hp := canonical_chain_plan b es B C hc
  rw [hB] at hp
  exact hp.sumGain_eq.symm

/-- Overflow totals are unchanged already for any accepted open chain. -/
theorem canonical_chain_sumGam {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    sumGam b (canonicalEdges b es) = sumGam b es := by
  have hp := canonical_chain_plan b es B C hc
  exact (hp.sumGam_eq (canonB b B) C (canonical_chainOK hc)).symm

/-- Restricting certificate existence to exterior-normalized cycles loses none.
The claim is existential, not pointwise checker equality for rejected data. -/
theorem cycle_exists_iff_exterior_normal (b : Nat) :
    (∃ es B C, cycleOK b es B C = true) ↔
      ∃ es B C, cycleOK b es B C = true ∧ B.getLast? ≠ some (b - 1) ∧
        (∀ e ∈ es, e.B.getLast? ≠ some (b - 1) ∧ e.B2.getLast? ≠ some (b - 1)) := by
  constructor
  · rintro ⟨es, B, C, hc⟩
    exact ⟨canonicalEdges b es, canonB b B, C, canonical_cycleOK hc,
      canonB_last_ne b B, canonicalEdges_normal b es⟩
  · rintro ⟨es, B, C, hc, _, _⟩
    exact ⟨es, B, C, hc⟩

end Agent114.NeutralExteriorCanonical

#print axioms Agent114.NeutralExteriorCanonical.canonical_chain_plan
#print axioms Agent114.NeutralExteriorCanonical.canonical_cycleOK
#print axioms Agent114.NeutralExteriorCanonical.canonical_cycle_gain
#print axioms Agent114.NeutralExteriorCanonical.cycle_exists_iff_exterior_normal
