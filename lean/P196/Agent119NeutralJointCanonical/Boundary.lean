import P196.Agent119NeutralJointCanonical.Main

/-!
# Exact boundaries of the joint canonicalization statements

A decimal source can satisfy all original hypotheses yet have no valid next
source after its maximal edge. Also, malformed inputs need not be fixed after
one application of the joint canonicalizer. Both small examples are reduced
by the ordinary kernel-backed decision procedure; neither is a cycle.
-/

namespace Agent119.NeutralJointCanonical

open Agent120.Neutral

/-- The decimal source ([1],[10]) steps to ([3],[0]), which fails Hyp. -/
theorem decimal_source_not_invariant :
    edgeOK 10 (rawEdge 10 [1] [10]) = true ∧
      ¬ Hyp 10 (rawEdge 10 [1] [10]).B2 (rawEdge 10 [1] [10]).C2 := by
  constructor
  · decide
  · intro h
    have ht := rawEdge_ok h
    have hf : edgeOK 10
        (rawEdge 10 (rawEdge 10 [1] [10]).B2 (rawEdge 10 [1] [10]).C2) = false := by
      decide
    rw [hf] at ht
    contradiction

/-- Acceptance is necessary for the stated joint idempotence theorem. -/
theorem joint_not_idempotent_without_acceptance :
    let E : Edge := { B := [4], C := [1, 0, 1], B2 := [], C2 := [0], u := 0, v := 0 }
    jointEdge 2 (jointEdge 2 E) ≠ jointEdge 2 E := by
  decide

end Agent119.NeutralJointCanonical

#print axioms Agent119.NeutralJointCanonical.decimal_source_not_invariant
#print axioms Agent119.NeutralJointCanonical.joint_not_idempotent_without_acceptance
