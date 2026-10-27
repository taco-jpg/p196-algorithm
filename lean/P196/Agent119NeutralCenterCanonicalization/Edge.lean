import P196.Agent119NeutralCenterCanonicalization.Core

/-!
# Maximal center normalization of an accepted A120 edge

The new center trim is the actual stripping depth of the raw successor.
Its additive balance is proved from accepted input, never assumed through
truncated natural subtraction. Exterior words and their trim are retained.
-/

namespace Agent119.NeutralCenterCanonicalization

open Agent120.Neutral Agent119.NeutralCenterPadding

/-- Keep all exterior data and use the actual maximal center-successor trim. -/
def normalizeEdge (b : Nat) (E : Edge) : Edge where
  B := E.B
  C := coreC b E.C
  B2 := E.B2
  C2 := coreC b E.C2
  u := E.u
  v := depthC b (nextC b E.B (coreC b E.C))

/-- An accepted edge identifies the complete padded raw-center words. -/
theorem normalized_center_equation {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    padC b (depthC b E.C) (nextC b E.B (coreC b E.C)) = padC b E.v E.C2 := by
  obtain ⟨h, _, hC⟩ := edgeOK_sound he
  have hs := Hyp_core h
  rw [← nextC_padC hs (depthC b E.C), ← decompose b E.C]
  exact hC

/-- The normalized target is uniquely the raw center's maximal stripped core. -/
theorem normalize_center_core {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    coreC b (nextC b E.B (coreC b E.C)) = coreC b E.C2 := by
  have hc := congrArg (coreC b) (normalized_center_equation he)
  simpa only [core_padC] using hc

/-- Exact natural balance, with no premise on the target's validity. -/
theorem normalizeEdge_balance {b : Nat} {E : Edge}
    (he : edgeOK b E = true) :
    depthC b E.C + (normalizeEdge b E).v = E.v + depthC b E.C2 := by
  have hd := congrArg (depthC b) (normalized_center_equation he)
  simpa only [depth_padC, normalizeEdge] using hd

/-- Every accepted original edge yields an edge accepted by the unchanged checker. -/
theorem normalizeEdge_ok {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    edgeOK b (normalizeEdge b E) = true := by
  obtain ⟨h, hB, _⟩ := edgeOK_sound he
  have hs := Hyp_core h
  apply edgeOK_of_equations hs
  · change nextB b E.B (coreC b E.C) = E.B2 ++ List.replicate E.u (b - 1)
    have hc := nextB_padC (a := depthC b E.C) hs
    rw [← decompose b E.C] at hc
    exact hc.symm.trans hB
  · change nextC b E.B (coreC b E.C) =
      padC b (depthC b (nextC b E.B (coreC b E.C))) (coreC b E.C2)
    have hd := decompose b (nextC b E.B (coreC b E.C))
    rwa [normalize_center_core he] at hd

theorem normalizeEdge_e1 (b : Nat) (E : Edge) :
    e1 b (normalizeEdge b E).B = e1 b E.B := rfl

theorem normalizeEdge_e2 {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    e2 b (normalizeEdge b E).B (normalizeEdge b E).C = e2 b E.B E.C := by
  have hs := Hyp_core (edgeOK_sound he).1
  have hc := e2_padC (a := depthC b E.C) hs
  rw [← decompose b E.C] at hc
  exact hc.symm

theorem normalizeEdge_gam {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    gam b (normalizeEdge b E).B (normalizeEdge b E).C = gam b E.B E.C := by
  have hs := Hyp_core (edgeOK_sound he).1
  have hc := gam_padC (a := depthC b E.C) hs
  rw [← decompose b E.C] at hc
  exact hc.symm

theorem normalizeEdge_idempotent (b : Nat) (E : Edge) :
    normalizeEdge b (normalizeEdge b E) = normalizeEdge b E := by
  simp only [normalizeEdge, core_idempotent]

/-- On accepted edges whose source and target are already cores, nothing changes. -/
theorem normalizeEdge_retraction {b : Nat} {E : Edge} (he : edgeOK b E = true)
    (hs : depthC b E.C = 0) (ht : depthC b E.C2 = 0) :
    normalizeEdge b E = E := by
  have hC : coreC b E.C = E.C := by
    have hd := decompose b E.C
    simpa only [hs, padC_zero] using hd.symm
  have hC2 : coreC b E.C2 = E.C2 := by
    have hd := decompose b E.C2
    simpa only [ht, padC_zero] using hd.symm
  have hv : (normalizeEdge b E).v = E.v := by
    simpa only [hs, ht, Nat.zero_add, Nat.add_zero] using normalizeEdge_balance he
  cases E with
  | mk B C B2 C2 u v =>
      change depthC b (nextC b B (coreC b C)) = v at hv
      simp only [normalizeEdge, hC, hC2] at *
      rw [hv]

end Agent119.NeutralCenterCanonicalization

#print axioms Agent119.NeutralCenterCanonicalization.normalized_center_equation
#print axioms Agent119.NeutralCenterCanonicalization.normalize_center_core
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdge_balance
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdge_ok
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdge_e2
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdge_gam
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdge_idempotent
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdge_retraction
