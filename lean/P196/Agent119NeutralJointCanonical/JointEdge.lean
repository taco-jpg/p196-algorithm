import P196.Agent119NeutralJointCanonical.MaximalEdge
import P196.Agent114NeutralExteriorCanonical.CanonicalCycle

/-!
# Joint maximal normalization of one accepted A120 edge

Compose the existing exterior and center canonicalizers. Maximal-target
uniqueness identifies the result with the raw maximal successor of its fully
stripped source. This formalizes Agent7's prior paper quotient argument using
Agent114's exterior and Agent119's center proofs without changing the checker.
All acceptance, uniqueness, and retraction claims retain their acceptance
premises; the next target is not asserted to satisfy the source hypotheses.
-/

namespace Agent119.NeutralJointCanonical

open Agent120.Neutral
open Agent114.NeutralExteriorCanonical
open Agent119.NeutralCenterCanonicalization

/-- Normalize exterior interfaces, then center interfaces, and recompute trims. -/
def jointEdge (b : Nat) (E : Edge) : Edge :=
  normalizeEdge b (canonicalEdge b E)

theorem jointEdge_source_normal (b : Nat) (E : Edge) :
    Normal b (jointEdge b E).B (jointEdge b E).C :=
  normal_cores b E.B E.C

theorem jointEdge_target_normal (b : Nat) (E : Edge) :
    Normal b (jointEdge b E).B2 (jointEdge b E).C2 :=
  normal_cores b E.B2 E.C2

theorem jointEdge_ok {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    edgeOK b (jointEdge b E) = true :=
  normalizeEdge_ok (canonicalEdge_ok he)

/-- The joint-normalized edge is determined by its normalized source alone. -/
theorem jointEdge_eq_raw {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    jointEdge b E = rawEdge b (canonB b E.B) (coreC b E.C) :=
  maximal_edge_eq_raw (jointEdge_ok he) (jointEdge_target_normal b E)

/-- Equal normalized sources give identical normalized accepted edges. -/
theorem jointEdge_eq_of_source_cores {b : Nat} {E F : Edge}
    (he : edgeOK b E = true) (hf : edgeOK b F = true)
    (hB : canonB b E.B = canonB b F.B) (hC : coreC b E.C = coreC b F.C) :
    jointEdge b E = jointEdge b F := by
  rw [jointEdge_eq_raw he, jointEdge_eq_raw hf, hB, hC]

theorem jointEdge_retraction {b : Nat} {E : Edge} (he : edgeOK b E = true)
    (hs : Normal b E.B E.C) (ht : Normal b E.B2 E.C2) :
    jointEdge b E = E := by
  calc
    jointEdge b E = rawEdge b (canonB b E.B) (coreC b E.C) := jointEdge_eq_raw he
    _ = rawEdge b E.B E.C := by rw [hs.1, hs.2]
    _ = E := (maximal_edge_eq_raw he ht).symm

theorem jointEdge_idempotent {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    jointEdge b (jointEdge b E) = jointEdge b E :=
  jointEdge_retraction (jointEdge_ok he)
    (jointEdge_source_normal b E) (jointEdge_target_normal b E)

/-- The two existing canonicalizers commute on accepted edges. -/
theorem jointEdge_commutes {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    normalizeEdge b (canonicalEdge b E) = canonicalEdge b (normalizeEdge b E) := by
  apply maximal_edge_unique (jointEdge_ok he) (canonicalEdge_ok (normalizeEdge_ok he))
    (jointEdge_target_normal b E) (normal_cores b E.B2 E.C2) rfl rfl

/-- Both exterior and center widths decrease or remain equal, at both ends. -/
theorem jointEdge_widths (b : Nat) (E : Edge) :
    (jointEdge b E).B.length ≤ E.B.length ∧
    (jointEdge b E).C.length ≤ E.C.length ∧
    (jointEdge b E).B2.length ≤ E.B2.length ∧
    (jointEdge b E).C2.length ≤ E.C2.length :=
  ⟨canonB_length_le b E.B, core_length_le b E.C,
    canonB_length_le b E.B2, core_length_le b E.C2⟩

private theorem exterior_streams {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    (e1 b (canonicalEdge b E).B,
      e2 b (canonicalEdge b E).B (canonicalEdge b E).C,
      gam b (canonicalEdge b E).B (canonicalEdge b E).C) =
    (e1 b E.B, e2 b E.B E.C, gam b E.B E.C) := by
  have hc : chainOK b [E] E.B E.C = true := by simp [chainOK, he]
  have hs := canonical_chain_streams hc
  simpa [canonicalEdges] using hs

/-- The complete carry/overflow label is unchanged on an accepted edge. -/
theorem jointEdge_streams {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    (e1 b (jointEdge b E).B,
      e2 b (jointEdge b E).B (jointEdge b E).C,
      gam b (jointEdge b E).B (jointEdge b E).C) =
    (e1 b E.B, e2 b E.B E.C, gam b E.B E.C) := by
  unfold jointEdge
  rw [normalizeEdge_e1, normalizeEdge_e2 (canonicalEdge_ok he),
    normalizeEdge_gam (canonicalEdge_ok he)]
  exact exterior_streams he

end Agent119.NeutralJointCanonical

#print axioms Agent119.NeutralJointCanonical.jointEdge_source_normal
#print axioms Agent119.NeutralJointCanonical.jointEdge_target_normal
#print axioms Agent119.NeutralJointCanonical.jointEdge_ok
#print axioms Agent119.NeutralJointCanonical.jointEdge_eq_raw
#print axioms Agent119.NeutralJointCanonical.jointEdge_eq_of_source_cores
#print axioms Agent119.NeutralJointCanonical.jointEdge_retraction
#print axioms Agent119.NeutralJointCanonical.jointEdge_idempotent
#print axioms Agent119.NeutralJointCanonical.jointEdge_commutes
#print axioms Agent119.NeutralJointCanonical.jointEdge_widths
#print axioms Agent119.NeutralJointCanonical.jointEdge_streams
