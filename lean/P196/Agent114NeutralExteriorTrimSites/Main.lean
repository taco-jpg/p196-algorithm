import P196.Agent114NeutralExteriorTrimSites.Overflow
import P196.Agent114NeutralExteriorCanonical.CanonicalCycle

/-!
# Exterior trim gates for the unchanged A120 certificate checker

This formalizes the exterior part of Agent7's prior PAPER Theorem C. A
canonical source can trim only on a nonoverflow step, at one of two exact
terminal coefficient/carry sites. In base ten these sites are (4,0) and
(14,1). The existing accepted-cycle canonicalizer supplies the corresponding
complete-cycle representative. These are necessary restrictions, not a
certificate, a sufficiency theorem, or a decimal nonexistence result.
-/

namespace Agent114.NeutralExteriorTrimSites

open Agent120.Neutral Agent114.NeutralExteriorCanonical

/-- The exact all-base terminal coefficient and its actual incoming carry. -/
def TrimSite (b : Nat) (B : List Nat) : Prop :=
  ∃ P z, B = P ++ [z] ∧
    ((e1 b B = 0 ∧ z = (b - 2) / 2 ∧ (norm b P 0).2 = (b - 2) % 2) ∨
     (e1 b B = 1 ∧ z = (3 * b - 1) / 2 ∧ (norm b P 0).2 = (3 * b - 1) % 2))

private theorem positive_trim_last {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hu : 0 < E.u) :
    (nextB b E.B E.C).getLast? = some (b - 1) := by
  rw [(edgeOK_sound he).2.1]
  have hn : E.u ≠ 0 := by omega
  simp [List.getLast?_append, List.getLast?_replicate, hn]

/-- A positive exterior trim from a canonical source has exactly one of the
two terminal coefficient/carry sites in Agent7's all-base PAPER theorem. -/
theorem canonical_positive_trim_site {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hn : E.B.getLast? ≠ some (b - 1))
    (hu : 0 < E.u) : TrimSite b E.B := by
  have h := (edgeOK_sound he).1
  have hg := canonical_positive_trim_nonoverflow he hn hu
  have hl := positive_trim_last he hu
  rcases List.eq_nil_or_concat E.B with hnil | ⟨P, z, hB⟩
  · exact False.elim (positive_trim_source_ne_nil he hu hnil)
  · simp only [List.concat_eq_append] at hB
    have hz : z ≠ b - 1 := by simpa [hB] using hn
    have hP : ∀ x ∈ P, x ≤ 2 * (b - 1) := by
      intro x hx
      exact h.boundB x (by rw [hB]; exact List.mem_append_left _ hx)
    have ht : (norm b P 0).2 ≤ 1 :=
      norm_carry_le_one b (by have := h.base; omega) P 0 hP (by omega)
    have h' : Hyp b (P ++ [z]) E.C := by simpa [hB] using h
    have hg' : gam b (P ++ [z]) E.C = 0 := by simpa [hB] using hg
    have hl' : (nextB b (P ++ [z]) E.C).getLast? = some (b - 1) := by
      simpa [hB] using hl
    obtain ⟨he0, hz0⟩ | ⟨he1, hz1⟩ :=
      nooverflow_last_thresholds h' hz hg' hl'
    · refine ⟨P, z, hB, Or.inl ?_⟩
      exact ⟨by simpa [hB] using he0, by omega, by omega⟩
    · refine ⟨P, z, hB, Or.inr ?_⟩
      exact ⟨by simpa [hB] using he1, by omega, by omega⟩

/-- Decimal specialization: the terminal sites are coefficient 4/carry 0
with e1=0, or coefficient 14/carry 1 with e1=1. -/
theorem decimal_positive_trim_site {E : Edge}
    (he : edgeOK 10 E = true) (hn : E.B.getLast? ≠ some 9) (hu : 0 < E.u) :
    (∃ P, E.B = P ++ [4] ∧ e1 10 E.B = 0 ∧ (norm 10 P 0).2 = 0) ∨
    (∃ P, E.B = P ++ [14] ∧ e1 10 E.B = 1 ∧ (norm 10 P 0).2 = 1) := by
  obtain ⟨P, z, hB, hs⟩ := canonical_positive_trim_site he hn hu
  rcases hs with ⟨he0, hz, ht⟩ | ⟨he1, hz, ht⟩
  · left
    change z = 4 at hz
    change (norm 10 P 0).2 = 0 at ht
    exact ⟨P, by simpa [hz] using hB, he0, ht⟩
  · right
    change z = 14 at hz
    change (norm 10 P 0).2 = 1 at ht
    exact ⟨P, by simpa [hz] using hB, he1, ht⟩

/-- Necessary exterior restrictions; this predicate does not assert edge
acceptance or sufficiency of a terminal site. -/
def ExteriorTrimGates (b : Nat) (E : Edge) : Prop :=
  (gam b E.B E.C = 1 → E.u = 0) ∧
    (0 < E.u → gam b E.B E.C = 0 ∧ TrimSite b E.B)

theorem canonical_edge_trim_gates {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hn : E.B.getLast? ≠ some (b - 1)) :
    ExteriorTrimGates b E := by
  exact ⟨fun hg => canonical_overflow_trim_zero he hg hn,
    fun hu => ⟨canonical_positive_trim_nonoverflow he hn hu,
      canonical_positive_trim_site he hn hu⟩⟩

private theorem accepted_chain_edges {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) : ∀ E ∈ es, edgeOK b E = true := by
  induction es generalizing B C with
  | nil => simp
  | cons e es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, ht⟩ := hc
      intro E hE
      rcases List.mem_cons.mp hE with rfl | hE
      · exact he
      · exact ih ht E hE

/-- Every edge of the accepted canonical cycle obeys the exterior trim gates. -/
theorem canonical_cycle_trim_gates {b : Nat} {es : List Edge} {B C : List Nat}
    (hcert : cycleOK b es B C = true) :
    ∀ E ∈ canonicalEdges b es, ExteriorTrimGates b E := by
  have hc := canonical_cycleOK hcert
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hc
  obtain ⟨⟨⟨⟨_, hchain⟩, _⟩, _⟩, _⟩ := hc
  intro E hE
  exact canonical_edge_trim_gates (accepted_chain_edges hchain E hE)
    ((canonicalEdges_normal b es E hE).1)

/-- Restricting accepted cycle existence to the proved canonical exterior
trim gates loses no certificate. This is an existential statement. -/
theorem cycle_exists_iff_exterior_trim_gates (b : Nat) :
    (∃ es B C, cycleOK b es B C = true) ↔
      ∃ es B C, cycleOK b es B C = true ∧ B.getLast? ≠ some (b - 1) ∧
        (∀ E ∈ es, E.B.getLast? ≠ some (b - 1) ∧
          E.B2.getLast? ≠ some (b - 1) ∧ ExteriorTrimGates b E) := by
  constructor
  · rintro ⟨es, B, C, hcert⟩
    refine ⟨canonicalEdges b es, canonB b B, C, canonical_cycleOK hcert,
      canonB_last_ne b B, ?_⟩
    intro E hE
    exact ⟨(canonicalEdges_normal b es E hE).1,
      (canonicalEdges_normal b es E hE).2, canonical_cycle_trim_gates hcert E hE⟩
  · rintro ⟨es, B, C, hcert, _, _⟩
    exact ⟨es, B, C, hcert⟩

end Agent114.NeutralExteriorTrimSites

#print axioms Agent114.NeutralExteriorTrimSites.canonical_positive_trim_site
#print axioms Agent114.NeutralExteriorTrimSites.decimal_positive_trim_site
#print axioms Agent114.NeutralExteriorTrimSites.canonical_edge_trim_gates
#print axioms Agent114.NeutralExteriorTrimSites.canonical_cycle_trim_gates
#print axioms Agent114.NeutralExteriorTrimSites.cycle_exists_iff_exterior_trim_gates
