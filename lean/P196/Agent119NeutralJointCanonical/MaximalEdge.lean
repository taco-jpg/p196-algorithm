import P196.Agent119NeutralCenterCanonicalization.Edge
import P196.Agent114NeutralExteriorCanonical.CanonicalEdge

/-!
# The unique maximal target of a checked neutral-band edge

This is the local uniqueness step in Agent7's paper joint normal form
(#315/#326). It reuses Agent114's exterior canonicalizer and Agent119's
center canonicalizer. Applying the established core and depth laws to the
unchanged checker's two successor equations forces both target words and
both trim counts. The source need not be normalized, and no validity
hypothesis is imposed on the target.
-/

namespace Agent119.NeutralJointCanonical

open Agent120.Neutral
open Agent114.NeutralExteriorCanonical
open Agent114.NeutralExteriorPadding (suffixPad)
open Agent119.NeutralCenterCanonicalization
open Agent119.NeutralCenterPadding (padC)

/-- Both interface words are fixed by their maximal neutral stripping maps. -/
def Normal (b : Nat) (B C : List Nat) : Prop :=
  canonB b B = B ∧ coreC b C = C

theorem normal_cores (b : Nat) (B C : List Nat) :
    Normal b (canonB b B) (coreC b C) :=
  ⟨canonB_idempotent b B, core_idempotent b C⟩

/-- Keep the actual source and maximally strip each of its raw successor words. -/
def rawEdge (b : Nat) (B C : List Nat) : Edge where
  B := B
  C := C
  B2 := canonB b (nextB b B C)
  C2 := coreC b (nextC b B C)
  u := suffixDepth b (nextB b B C)
  v := depthC b (nextC b B C)

theorem rawEdge_target_normal (b : Nat) (B C : List Nat) :
    Normal b (rawEdge b B C).B2 (rawEdge b B C).C2 :=
  normal_cores b (nextB b B C) (nextC b B C)

/-- Every valid source has an accepted edge with maximally stripped targets. -/
theorem rawEdge_ok {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    edgeOK b (rawEdge b B C) = true := by
  apply Agent119.NeutralCenterPadding.edgeOK_of_equations h
  · exact (canonB_decompose b (nextB b B C)).symm
  · exact decompose b (nextC b B C)

/-- This local constructor checks precisely the original source hypotheses. -/
theorem rawEdge_ok_iff (b : Nat) (B C : List Nat) :
    edgeOK b (rawEdge b B C) = true ↔ Hyp b B C :=
  ⟨fun h => (edgeOK_sound h).1, rawEdge_ok⟩

/-- Normal targets force the complete checked edge, with no source normality premise. -/
theorem maximal_edge_eq_raw {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (ht : Normal b E.B2 E.C2) :
    E = rawEdge b E.B E.C := by
  obtain ⟨_, hB, hC⟩ := edgeOK_sound he
  change nextB b E.B E.C = suffixPad b E.u E.B2 at hB
  change nextC b E.B E.C = padC b E.v E.C2 at hC

  have hzB : suffixDepth b E.B2 = 0 := by
    have h := congrArg (suffixDepth b) ht.1
    rw [suffixDepth_canonB] at h
    exact h.symm
  have hzC : depthC b E.C2 = 0 := by
    have h := congrArg (depthC b) ht.2
    rw [depth_core] at h
    exact h.symm

  have hBt : canonB b (nextB b E.B E.C) = E.B2 := by
    rw [hB, canonB_suffixPad, ht.1]
  have hCt : coreC b (nextC b E.B E.C) = E.C2 := by
    rw [hC, core_padC, ht.2]
  have hu : suffixDepth b (nextB b E.B E.C) = E.u := by
    rw [hB, suffixDepth_suffixPad, hzB, Nat.zero_add]
  have hv : depthC b (nextC b E.B E.C) = E.v := by
    rw [hC, depth_padC, hzC, Nat.add_zero]

  cases E
  simp only [rawEdge, hBt, hCt, hu, hv]

/-- At a fixed source, at most one accepted edge has jointly normalized targets. -/
theorem maximal_edge_unique {b : Nat} {E F : Edge}
    (he : edgeOK b E = true) (hf : edgeOK b F = true)
    (htE : Normal b E.B2 E.C2) (htF : Normal b F.B2 F.C2)
    (hB : E.B = F.B) (hC : E.C = F.C) : E = F := by
  calc
    E = rawEdge b E.B E.C := maximal_edge_eq_raw he htE
    _ = rawEdge b F.B F.C := by rw [hB, hC]
    _ = F := (maximal_edge_eq_raw hf htF).symm

end Agent119.NeutralJointCanonical

#print axioms Agent119.NeutralJointCanonical.normal_cores
#print axioms Agent119.NeutralJointCanonical.rawEdge_target_normal
#print axioms Agent119.NeutralJointCanonical.rawEdge_ok
#print axioms Agent119.NeutralJointCanonical.rawEdge_ok_iff
#print axioms Agent119.NeutralJointCanonical.maximal_edge_eq_raw
#print axioms Agent119.NeutralJointCanonical.maximal_edge_unique
