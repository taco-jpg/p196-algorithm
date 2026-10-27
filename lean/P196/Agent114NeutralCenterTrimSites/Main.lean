import P196.Agent114NeutralCenterTrimSites.CenterGates
import P196.Agent119NeutralCenterCanonicalization.Main

/-!
# Center-canonical certificates satisfy the exact trim gates

Compose the new symmetry and local boundary theorems with Agent119's existing
accepted-cycle center canonicalizer. The same normalized edges retain their
original verified acceptance and preserved data. This adds no new stripping
algorithm, joint quotient, numerical decoder, search, or decimal witness.
-/

namespace Agent114.NeutralCenterTrimSites

open Agent120.Neutral Agent119.NeutralCenterCanonicalization

/-- Necessary local center restrictions for a symmetric canonical source. -/
def CenterTrimGates (b : Nat) (E : Edge) : Prop :=
  E.C.reverse = E.C ∧ E.C.head? ≠ some (b - 1) ∧
    (gam b E.B E.C = 1 → E.v = 0) ∧
    (0 < E.v → gam b E.B E.C = 0 ∧ CenterTrimSite b E.B E.C)

theorem canonical_center_edge_trim_gates {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hs : E.C.reverse = E.C)
    (hd : depthC b E.C = 0) : CenterTrimGates b E := by
  have hn := symmetric_core_head_ne (edgeOK_sound he).1 hs hd
  exact ⟨hs, hn, fun hg => head_normal_overflow_trim_zero he hg hn,
    fun hv => ⟨head_normal_positive_trim_nonoverflow he hn hv,
      symmetric_positive_trim_site he hs hn hv⟩⟩

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

/-- Every edge of the existing accepted center-normalized cycle obeys the
center trim gates. Source symmetry is derived from actual cycle acceptance. -/
theorem normalized_cycle_center_trim_gates {b : Nat} {es : List Edge} {B C : List Nat}
    (hcert : cycleOK b es B C = true) :
    ∀ E ∈ normalizeEdges b es, CenterTrimGates b E := by
  have hc := cycleOK_normalize hcert
  have hs := (cycle_centers_symmetric hc).2
  have hchain := hc
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hchain
  obtain ⟨⟨⟨⟨_, hchain⟩, _⟩, _⟩, _⟩ := hchain
  intro E hE
  exact canonical_center_edge_trim_gates (accepted_chain_edges hchain E hE)
    (hs E hE).1 (normalizeEdges_core_depth b es E hE).1

/-- Adding symmetry, maximal center stripping and the necessary center trim
gates to the existential certificate problem loses no accepted cycle. -/
theorem cycle_exists_iff_center_trim_gates (b : Nat) :
    (∃ es B C, cycleOK b es B C = true) ↔
      ∃ es B C, cycleOK b es B C = true ∧ C.reverse = C ∧ depthC b C = 0 ∧
        (∀ E ∈ es, depthC b E.C = 0 ∧ depthC b E.C2 = 0 ∧ CenterTrimGates b E) := by
  constructor
  · rintro ⟨es, B, C, hcert⟩
    have hc := cycleOK_normalize hcert
    refine ⟨normalizeEdges b es, B, coreC b C, hc,
      (cycle_centers_symmetric hc).1, depth_core b C, ?_⟩
    intro E hE
    exact ⟨(normalizeEdges_core_depth b es E hE).1,
      (normalizeEdges_core_depth b es E hE).2, normalized_cycle_center_trim_gates hcert E hE⟩
  · rintro ⟨es, B, C, hcert, _, _, _⟩
    exact ⟨es, B, C, hcert⟩

end Agent114.NeutralCenterTrimSites

#print axioms Agent114.NeutralCenterTrimSites.canonical_center_edge_trim_gates
#print axioms Agent114.NeutralCenterTrimSites.normalized_cycle_center_trim_gates
#print axioms Agent114.NeutralCenterTrimSites.cycle_exists_iff_center_trim_gates
