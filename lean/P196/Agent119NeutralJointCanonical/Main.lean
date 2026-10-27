import P196.Agent119NeutralJointCanonical.JointEdge
import P196.Agent119NeutralCenterCanonicalization.Main

/-!
# Accepted A120 cycles in the joint deterministic quotient

Every accepted cycle maps to a fully stripped accepted cycle. Its carry and
overflow labels, listed edge count, and total gain are preserved; every
interface width is pointwise no larger. Every resulting edge is the unique
maximal raw successor of its source. The source hypotheses are checked at
every phase of a cycle, rather than assumed invariant under one raw step.

These are kernel bridges for Agent7's prior paper normal form and deterministic
quotient, using the existing exterior and center canonicalizers. They supply
neither a decimal certificate nor a general exclusion of certificates.
-/

namespace Agent119.NeutralJointCanonical

open Agent120.Neutral
open Agent114.NeutralExteriorCanonical
open Agent119.NeutralCenterCanonicalization

/-- Normalize both interfaces at each listed position. -/
def jointEdges (b : Nat) (es : List Edge) : List Edge := es.map (jointEdge b)

theorem jointEdges_eq_composition (b : Nat) (es : List Edge) :
    jointEdges b es = normalizeEdges b (canonicalEdges b es) := by
  induction es with
  | nil => rfl
  | cons E es ih => exact congrArg (List.cons (jointEdge b E)) ih

theorem jointEdges_length (b : Nat) (es : List Edge) :
    (jointEdges b es).length = es.length := by simp [jointEdges]

theorem jointEdges_normal (b : Nat) (es : List Edge) :
    ∀ E ∈ jointEdges b es, Normal b E.B E.C ∧ Normal b E.B2 E.C2 := by
  intro E hE
  obtain ⟨D, _, rfl⟩ := List.mem_map.mp hE
  exact ⟨jointEdge_source_normal b D, jointEdge_target_normal b D⟩

/-- Corresponding source and target widths are bounded in their original order. -/
theorem jointEdges_widths (b : Nat) (es : List Edge) :
    ∀ p ∈ (jointEdges b es).zip es,
      p.1.B.length ≤ p.2.B.length ∧ p.1.C.length ≤ p.2.C.length ∧
      p.1.B2.length ≤ p.2.B2.length ∧ p.1.C2.length ≤ p.2.C2.length := by
  induction es with
  | nil => intro p hp; cases hp
  | cons E es ih =>
      intro p hp
      change p ∈ (jointEdge b E, E) :: (jointEdges b es).zip es at hp
      rcases List.mem_cons.mp hp with rfl | hp
      · exact jointEdge_widths b E
      · exact ih p hp

theorem joint_chainOK {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    chainOK b (jointEdges b es) (canonB b B) (coreC b C) = true := by
  rw [jointEdges_eq_composition]
  exact chainOK_normalize (canonical_chainOK hc)

/-- Full original Boolean acceptance is retained by the joint canonicalizer. -/
theorem joint_cycleOK {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) :
    cycleOK b (jointEdges b es) (canonB b B) (coreC b C) = true := by
  rw [jointEdges_eq_composition]
  exact cycleOK_normalize (canonical_cycleOK hc)

theorem joint_chain_streams {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    (jointEdges b es).map (fun E => (e1 b E.B, e2 b E.B E.C, gam b E.B E.C)) =
      es.map (fun E => (e1 b E.B, e2 b E.B E.C, gam b E.B E.C)) := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      change (e1 b (jointEdge b E).B, e2 b (jointEdge b E).B (jointEdge b E).C,
          gam b (jointEdge b E).B (jointEdge b E).C) ::
          (jointEdges b es).map (fun D => (e1 b D.B, e2 b D.B D.C, gam b D.B D.C)) =
        (e1 b E.B, e2 b E.B E.C, gam b E.B E.C) ::
          es.map (fun D => (e1 b D.B, e2 b D.B D.C, gam b D.B D.C))
      rw [jointEdge_streams hc.1.2, ih hc.2]

theorem joint_chain_sumGam {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    sumGam b (jointEdges b es) = sumGam b es := by
  rw [jointEdges_eq_composition, sumGam_normalize (canonical_chainOK hc),
    canonical_chain_sumGam hc]

/-- Both depth changes telescope around a closed accepted cycle. -/
theorem joint_cycle_gain {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) :
    sumGain (jointEdges b es) = sumGain es := by
  have hx := canonical_cycleOK hc
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hx
  rw [jointEdges_eq_composition,
    sumGain_normalize_closed hx.1.1.1.2 hx.1.2, canonical_cycle_gain hc]

private theorem chain_edges {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) : ∀ E ∈ es, edgeOK b E = true := by
  induction es generalizing B C with
  | nil => intro E hE; cases hE
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      intro D hD
      rcases List.mem_cons.mp hD with rfl | hD
      · exact hc.1.2
      · exact ih hc.2 D hD

/-- Every edge in the normalized chain is the deterministic maximal raw edge
at its own source, including its uniquely forced two natural trim counts. -/
theorem joint_chain_deterministic {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    ∀ E ∈ jointEdges b es, E = rawEdge b E.B E.C := by
  intro E hE
  obtain ⟨D, hD, rfl⟩ := List.mem_map.mp hE
  exact maximal_edge_eq_raw (jointEdge_ok (chain_edges hc D hD))
    (jointEdge_target_normal b D)

theorem jointEdges_idempotent {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    jointEdges b (jointEdges b es) = jointEdges b es := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      change jointEdge b (jointEdge b E) :: jointEdges b (jointEdges b es) =
        jointEdge b E :: jointEdges b es
      rw [jointEdge_idempotent hc.1.2, ih hc.2]

theorem jointEdges_retraction {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true)
    (hn : ∀ E ∈ es, Normal b E.B E.C ∧ Normal b E.B2 E.C2) :
    jointEdges b es = es := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      have hE := hn E List.mem_cons_self
      have ht : ∀ D ∈ es, Normal b D.B D.C ∧ Normal b D.B2 D.C2 := by
        intro D hD
        exact hn D (List.mem_cons_of_mem E hD)
      change jointEdge b E :: jointEdges b es = E :: es
      rw [jointEdge_retraction hc.1.2 hE.1 hE.2, ih hc.2 ht]

/-- Restricting to fully normal, deterministic cycles loses no accepted cycle.
The fixed listed length is preserved; no least-period assertion is made. -/
theorem cycle_exists_length_iff_joint_normal (b p : Nat) :
    (∃ es B C, es.length = p ∧ cycleOK b es B C = true) ↔
      ∃ es B C, es.length = p ∧ cycleOK b es B C = true ∧ Normal b B C ∧
        (∀ E ∈ es, Normal b E.B E.C ∧ Normal b E.B2 E.C2 ∧
          E = rawEdge b E.B E.C) := by
  constructor
  · rintro ⟨es, B, C, hp, hc⟩
    have hchain := hc
    simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hchain
    refine ⟨jointEdges b es, canonB b B, coreC b C,
      (jointEdges_length b es).trans hp, joint_cycleOK hc, normal_cores b B C, ?_⟩
    intro E hE
    have hn := jointEdges_normal b es E hE
    exact ⟨hn.1, hn.2, joint_chain_deterministic hchain.1.1.1.2 E hE⟩
  · rintro ⟨es, B, C, hp, hc, _, _⟩
    exact ⟨es, B, C, hp, hc⟩

end Agent119.NeutralJointCanonical

#print axioms Agent119.NeutralJointCanonical.jointEdges_eq_composition
#print axioms Agent119.NeutralJointCanonical.jointEdges_length
#print axioms Agent119.NeutralJointCanonical.jointEdges_normal
#print axioms Agent119.NeutralJointCanonical.jointEdges_widths
#print axioms Agent119.NeutralJointCanonical.joint_chainOK
#print axioms Agent119.NeutralJointCanonical.joint_cycleOK
#print axioms Agent119.NeutralJointCanonical.joint_chain_streams
#print axioms Agent119.NeutralJointCanonical.joint_chain_sumGam
#print axioms Agent119.NeutralJointCanonical.joint_cycle_gain
#print axioms Agent119.NeutralJointCanonical.joint_chain_deterministic
#print axioms Agent119.NeutralJointCanonical.jointEdges_idempotent
#print axioms Agent119.NeutralJointCanonical.jointEdges_retraction
#print axioms Agent119.NeutralJointCanonical.cycle_exists_length_iff_joint_normal
