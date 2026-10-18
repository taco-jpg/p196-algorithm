import P196.Drafts.D20261015ScalarHierarchyReviewSourceSnapshots.ScalarRoot

/-! The frozen abstract lift permits unbounded Nat edge labels.
This does not invalidate actual orbit lifting, whose carry labels are bits,
but unrestricted Realization cannot encode it into a bit-only graph. -/

namespace LabelNineCounterexample

open ActualPrefixLift ScalarRoot

def source : Fin 7 × Fin 19 := (⟨0, by decide⟩, ⟨0, by decide⟩)
def target : Fin 7 × Fin 19 := (⟨1, by decide⟩, ⟨9, by decide⟩)

theorem valid_endpoints : (lift root).valid source ∧ (lift root).valid target := by
  exact ⟨True.intro, True.intro⟩

theorem label_nine_edge : (lift root).edge source target 9 := by
  refine ⟨0, ?_, ?_⟩
  · change (0, 1, 0) ∈ rootEdges
    decide
  · change PrefixExtension.ExtensionChoice 4 0 0 0 0 9 0 9
    unfold PrefixExtension.ExtensionChoice
    decide

theorem no_unrestricted_realization_into_bit_labels {W : Type} (H : Graph W)
    (encode : (Fin 7 × Fin 19) → W)
    (hbits : ∀ u v c, H.edge u v c → c ≤ 1) :
    ¬ Realization (lift root) H encode := by
  intro hr
  have he := hr.edges source target 9 valid_endpoints.1 valid_endpoints.2 label_nine_edge
  have hb := hbits _ _ _ he
  omega

end LabelNineCounterexample

#print axioms LabelNineCounterexample.valid_endpoints
#print axioms LabelNineCounterexample.label_nine_edge
#print axioms LabelNineCounterexample.no_unrestricted_realization_into_bit_labels
