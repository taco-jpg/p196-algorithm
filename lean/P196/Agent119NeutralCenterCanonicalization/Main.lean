import P196.Agent119NeutralCenterCanonicalization.Edge

/-!
# Canonical center stripping for accepted neutral-band cycles

Every center is replaced by its maximal symmetrically stripped core. The
center trim on each edge is recomputed from the raw successor of that core.
The original checker accepts the resulting chain, and the change in gain
telescopes through the source and target stripping depths. Hence a closed
accepted cycle retains its gain, overflow total, listed length, exteriors,
exterior trims, carry labels, and pointwise core widths.

The forward acceptance theorem is conditional on the original checker.
There is no acceptance equivalence for arbitrary malformed edge lists and
no assertion that the full joint exterior-center transition is deterministic.
-/

namespace Agent119.NeutralCenterCanonicalization

open Agent120.Neutral

/-- Strip the source and target center of each edge and recompute its center trim. -/
def normalizeEdges (b : Nat) : List Edge → List Edge
  | [] => []
  | E :: es => normalizeEdge b E :: normalizeEdges b es

theorem normalizeEdges_length (b : Nat) (es : List Edge) :
    (normalizeEdges b es).length = es.length := by
  induction es with
  | nil => rfl
  | cons E es ih => simp only [normalizeEdges, List.length_cons, ih]

theorem normalizeEdges_eq_nil_iff (b : Nat) (es : List Edge) :
    normalizeEdges b es = [] ↔ es = [] := by
  cases es <;> simp [normalizeEdges]

theorem endB_normalizeEdges (b : Nat) (es : List Edge) (B : List Nat) :
    endB (normalizeEdges b es) B = endB es B := by
  induction es generalizing B with
  | nil => rfl
  | cons E es ih => simpa only [normalizeEdges, endB, normalizeEdge] using ih E.B2

theorem endC_normalizeEdges (b : Nat) (es : List Edge) (C : List Nat) :
    endC (normalizeEdges b es) (coreC b C) = coreC b (endC es C) := by
  induction es generalizing C with
  | nil => rfl
  | cons E es ih => simpa only [normalizeEdges, endC, normalizeEdge] using ih E.C2

/-- Checked seams remain checked after stripping their two identical centers. -/
theorem chainOK_normalize {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    chainOK b (normalizeEdges b es) B (coreC b C) = true := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, he⟩, hes⟩ := hc
      simp only [normalizeEdges, chainOK, Bool.and_eq_true, decide_eq_true_eq]
      change (((E.B = B ∧ coreC b E.C = coreC b C) ∧
        edgeOK b (normalizeEdge b E) = true) ∧
        chainOK b (normalizeEdges b es) E.B2 (coreC b E.C2) = true)
      exact ⟨⟨⟨hB, congrArg (coreC b) hC⟩, normalizeEdge_ok he⟩, ih hes⟩

/-- On an open checked chain, gain changes by the difference of endpoint depths. -/
theorem chain_gain_balance {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    sumGain (normalizeEdges b es) + depthC b C =
      sumGain es + depthC b (endC es C) := by
  induction es generalizing B C with
  | nil => simp only [normalizeEdges, sumGain, endC]
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, hC⟩, he⟩, hes⟩ := hc
      have heq := normalizeEdge_balance he
      have htail := ih hes
      subst C
      change E.u + (normalizeEdge b E).v + sumGain (normalizeEdges b es) +
          depthC b E.C = E.u + E.v + sumGain es + depthC b (endC es E.C2)
      omega

/-- Center closure cancels the endpoint depth contribution exactly. -/
theorem sumGain_normalize_closed {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hC : endC es C = C) :
    sumGain (normalizeEdges b es) = sumGain es := by
  have h := chain_gain_balance hc
  rw [hC] at h
  omega

theorem sumGam_normalize {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    sumGam b (normalizeEdges b es) = sumGam b es := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      simp only [normalizeEdges, sumGam]
      rw [normalizeEdge_gam hc.1.2, ih hc.2]

/-- Exterior interfaces, exterior trims, both carry labels, and overflows agree
at every listed position of a checked chain. -/
theorem normalizeEdges_streams {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    (normalizeEdges b es).map
        (fun E => (E.B, E.B2, E.u, e1 b E.B, e2 b E.B E.C, gam b E.B E.C)) =
      es.map (fun E => (E.B, E.B2, E.u, e1 b E.B, e2 b E.B E.C, gam b E.B E.C)) := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      simp only [normalizeEdges, List.map_cons]
      rw [normalizeEdge_e1, normalizeEdge_e2 hc.1.2, normalizeEdge_gam hc.1.2, ih hc.2]
      rfl

/-- Every normalized source and target has zero remaining symmetric neutral depth. -/
theorem normalizeEdges_core_depth (b : Nat) (es : List Edge) :
    ∀ E ∈ normalizeEdges b es, depthC b E.C = 0 ∧ depthC b E.C2 = 0 := by
  induction es with
  | nil => intro E hE; cases hE
  | cons E es ih =>
      intro D hD
      simp only [normalizeEdges, List.mem_cons] at hD
      rcases hD with rfl | hD
      · exact ⟨depth_core b E.C, depth_core b E.C2⟩
      · exact ih D hD

/-- The listed center widths become precisely the corresponding core widths. -/
theorem normalizeEdges_core_widths (b : Nat) (es : List Edge) :
    (normalizeEdges b es).map (fun E => (E.C.length, E.C2.length)) =
      es.map (fun E => ((coreC b E.C).length, (coreC b E.C2).length)) := by
  induction es with
  | nil => rfl
  | cons E es ih => simp only [normalizeEdges, List.map_cons, normalizeEdge, ih]

/-- Full original acceptance is retained after maximal center stripping. -/
theorem cycleOK_normalize {b : Nat} {es : List Edge} {B C : List Nat}
    (h : cycleOK b es B C = true) :
    cycleOK b (normalizeEdges b es) B (coreC b C) = true := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at h ⊢
  obtain ⟨⟨⟨⟨hne, hc⟩, hB⟩, hC⟩, hg⟩ := h
  refine ⟨⟨⟨⟨?_, chainOK_normalize hc⟩, ?_⟩, ?_⟩, ?_⟩
  · exact fun hnil => hne ((normalizeEdges_eq_nil_iff b es).mp hnil)
  · rwa [endB_normalizeEdges]
  · rw [endC_normalizeEdges, hC]
  · rwa [sumGam_normalize hc, sumGain_normalize_closed hc hC]

theorem normalizeEdges_idempotent (b : Nat) (es : List Edge) :
    normalizeEdges b (normalizeEdges b es) = normalizeEdges b es := by
  induction es with
  | nil => rfl
  | cons E es ih =>
      simp only [normalizeEdges, normalizeEdge_idempotent, ih]

/-- A checked list whose centers are already fully stripped is fixed. -/
theorem normalizeEdges_retraction {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true)
    (hs : ∀ E ∈ es, depthC b E.C = 0 ∧ depthC b E.C2 = 0) :
    normalizeEdges b es = es := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      have hE := hs E (List.mem_cons_self)
      have htail : ∀ D ∈ es, depthC b D.C = 0 ∧ depthC b D.C2 = 0 := by
        intro D hD
        exact hs D (List.mem_cons_of_mem E hD)
      simp only [normalizeEdges, normalizeEdge_retraction hc.1.2 hE.1 hE.2,
        ih hc.2 htail]

end Agent119.NeutralCenterCanonicalization

#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdges_length
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdges_eq_nil_iff
#print axioms Agent119.NeutralCenterCanonicalization.endB_normalizeEdges
#print axioms Agent119.NeutralCenterCanonicalization.endC_normalizeEdges
#print axioms Agent119.NeutralCenterCanonicalization.chainOK_normalize
#print axioms Agent119.NeutralCenterCanonicalization.chain_gain_balance
#print axioms Agent119.NeutralCenterCanonicalization.sumGain_normalize_closed
#print axioms Agent119.NeutralCenterCanonicalization.sumGam_normalize
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdges_streams
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdges_core_depth
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdges_core_widths
#print axioms Agent119.NeutralCenterCanonicalization.cycleOK_normalize
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdges_idempotent
#print axioms Agent119.NeutralCenterCanonicalization.normalizeEdges_retraction
