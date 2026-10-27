import P196.Agent119NeutralCenterUnpadding.Inverse

/-!
# Common center-padding cancellation for checked chains and cycles

This is the inverse/common-removal foundation of Agent7's normalization and
Agent117's common-padding reduction. It leaves every trim and exterior intact.
It is separate from phase-dependent prescribed-schedule transport.
-/

namespace Agent119.NeutralCenterUnpadding

open Agent120.Neutral Agent119.NeutralCenterPadding

/-- Add one common depth to every source and target center, retaining both trims. -/
def padEdges (b a : Nat) : List Edge → List Edge
  | [] => []
  | E :: es => transportEdge b a a E.v E :: padEdges b a es

theorem padEdges_length (b a : Nat) (es : List Edge) :
    (padEdges b a es).length = es.length := by
  induction es with
  | nil => rfl
  | cons E es ih => simp only [padEdges, List.length_cons, ih]

theorem padEdges_eq_nil_iff (b a : Nat) (es : List Edge) :
    padEdges b a es = [] ↔ es = [] := by
  cases es <;> simp [padEdges]

theorem endB_padEdges (b a : Nat) (es : List Edge) (B : List Nat) :
    endB (padEdges b a es) B = endB es B := by
  induction es generalizing B with
  | nil => rfl
  | cons E es ih => simpa only [padEdges, endB, transportEdge] using ih E.B2

theorem endC_padEdges (b a : Nat) (es : List Edge) (C : List Nat) :
    endC (padEdges b a es) (padC b a C) = padC b a (endC es C) := by
  induction es generalizing C with
  | nil => rfl
  | cons E es ih => simpa only [padEdges, endC, transportEdge] using ih E.C2

/-- Common padding neither creates nor hides a checked edge or a seam mismatch. -/
theorem chainOK_padEdges_iff (b a : Nat) (es : List Edge) (B C : List Nat) :
    chainOK b (padEdges b a es) B (padC b a C) = true ↔
      chainOK b es B C = true := by
  induction es generalizing B C with
  | nil => simp only [padEdges, chainOK]
  | cons E es ih =>
      simp only [padEdges, chainOK, Bool.and_eq_true, decide_eq_true_eq]
      change
        (((E.B = B ∧ padC b a E.C = padC b a C) ∧
          edgeOK b (transportEdge b a a E.v E) = true) ∧
          chainOK b (padEdges b a es) E.B2 (padC b a E.C2) = true) ↔
        (((E.B = B ∧ E.C = C) ∧ edgeOK b E = true) ∧
          chainOK b es E.B2 E.C2 = true)
      rw [padC_inj b a, edgeOK_transport_iff a a E.v (by omega), ih]

theorem sumGain_padEdges (b a : Nat) (es : List Edge) :
    sumGain (padEdges b a es) = sumGain es := by
  induction es with
  | nil => rfl
  | cons E es ih => simp only [padEdges, sumGain, transportEdge, ih]

theorem sumGam_padEdges (b a : Nat) (es : List Edge) (B C : List Nat)
    (hc : chainOK b es B C = true) :
    sumGam b (padEdges b a es) = sumGam b es := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      have he : edgeOK b E = true := hc.1.2
      simp only [padEdges, sumGam]
      rw [transportEdge_gam he, ih E.B2 E.C2 hc.2]

/-- Full original acceptance, including nonemptiness, both closures, and gain. -/
theorem cycleOK_padEdges_iff (b a : Nat) (es : List Edge) (B C : List Nat) :
    cycleOK b (padEdges b a es) B (padC b a C) = true ↔
      cycleOK b es B C = true := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq]
  constructor
  · rintro ⟨⟨⟨⟨hne, hc⟩, hB⟩, hC⟩, hg⟩
    have hc0 := (chainOK_padEdges_iff b a es B C).mp hc
    rw [sumGam_padEdges b a es B C hc0, sumGain_padEdges] at hg
    refine ⟨⟨⟨⟨?_, hc0⟩, ?_⟩, ?_⟩, hg⟩
    · exact fun h => hne ((padEdges_eq_nil_iff b a es).mpr h)
    · simpa only [endB_padEdges] using hB
    · rw [endC_padEdges] at hC
      exact padC_injective b a hC
  · rintro ⟨⟨⟨⟨hne, hc⟩, hB⟩, hC⟩, hg⟩
    refine ⟨⟨⟨⟨?_, (chainOK_padEdges_iff b a es B C).mpr hc⟩, ?_⟩, ?_⟩, ?_⟩
    · exact fun h => hne ((padEdges_eq_nil_iff b a es).mp h)
    · simpa only [endB_padEdges] using hB
    · rw [endC_padEdges, hC]
    · rwa [sumGam_padEdges b a es B C hc, sumGain_padEdges]

/-- Explicit cancellation direction used by common-padding reductions. -/
theorem cycleOK_of_common_padding {b a : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b (padEdges b a es) B (padC b a C) = true) :
    cycleOK b es B C = true :=
  (cycleOK_padEdges_iff b a es B C).mp hc

/-- An all-neutral center cannot flip the carry, at any length. -/
theorem not_Hyp_neutral_center (b : Nat) (B : List Nat) (m : Nat) :
    ¬ Hyp b B (List.replicate m (b - 1)) := by
  intro h
  have hn := norm_replicate_neutral b h.base m (e1 b B) h.e1_le
  have he := congrArg Prod.snd hn
  change e2 b B (List.replicate m (b - 1)) = e1 b B at he
  exact h.flip he.symm

theorem Hyp_center_ne_nil {b : Nat} {B C : List Nat} (h : Hyp b B C) : C ≠ [] := by
  intro hC
  subst C
  exact not_Hyp_neutral_center b B 0 h

end Agent119.NeutralCenterUnpadding

#print axioms Agent119.NeutralCenterUnpadding.chainOK_padEdges_iff
#print axioms Agent119.NeutralCenterUnpadding.sumGam_padEdges
#print axioms Agent119.NeutralCenterUnpadding.cycleOK_padEdges_iff
#print axioms Agent119.NeutralCenterUnpadding.cycleOK_of_common_padding
#print axioms Agent119.NeutralCenterUnpadding.not_Hyp_neutral_center
