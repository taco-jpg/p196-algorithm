import P196.Agent114NeutralExteriorPadding.ExteriorPadding
import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Neutral exterior padding: exact transport of checked edges

This formalizes the exterior part of the previously established neutral-padding
argument.  The original checker is unchanged.  No cycle instance or decimal
Lychrel existence theorem is asserted.
-/

namespace Agent114.NeutralExteriorPadding

open Agent120.Neutral

/-- Exact propositional characterization of the unchanged Boolean edge check. -/
theorem edgeOK_iff (b : Nat) (E : Edge) :
    edgeOK b E = true ↔
      Hyp b E.B E.C ∧
      nextB b E.B E.C = E.B2 ++ List.replicate E.u (b - 1) ∧
      nextC b E.B E.C =
        List.replicate E.v (b - 1) ++ (E.C2 ++ List.replicate E.v (b - 1)) := by
  constructor
  · exact edgeOK_sound
  · rintro ⟨h, hB, hC⟩
    simp only [edgeOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true]
    exact ⟨⟨⟨⟨⟨⟨h.base, h.boundB⟩, h.boundC⟩, h.ext⟩, h.flip⟩, hB⟩, hC⟩

/-- Pad the source/target exterior and replace its trim count. -/
def padEdge (b a a' w : Nat) (E : Edge) : Edge where
  B := suffixPad b a E.B
  C := E.C
  B2 := suffixPad b a' E.B2
  C2 := E.C2
  u := w
  v := E.v

/-- Reallocate neutral exterior coefficients without changing edge acceptance.
The count equation includes both padding offsets; all parameters are natural.
-/
theorem edgeOK_suffixPad_iff {b : Nat} {E : Edge} (a a' w : Nat)
    (hcount : a + E.u = w + a') :
    edgeOK b (padEdge b a a' w E) = true ↔ edgeOK b E = true := by
  have htail :
      suffixPad b a' E.B2 ++ List.replicate w (b - 1) =
        (E.B2 ++ List.replicate E.u (b - 1)) ++ List.replicate a (b - 1) := by
    simp only [suffixPad, List.append_assoc, List.replicate_append_replicate]
    have hc : a' + w = E.u + a := by omega
    rw [hc]
  rw [edgeOK_iff, edgeOK_iff]
  constructor
  · rintro ⟨hp, hB, hC⟩
    change Hyp b (suffixPad b a E.B) E.C at hp
    have h : Hyp b E.B E.C := (hyp_suffixPad_iff a).1 hp
    change nextB b (suffixPad b a E.B) E.C =
      suffixPad b a' E.B2 ++ List.replicate w (b - 1) at hB
    rw [nextB_suffixPad h a, htail] at hB
    have hB0 : nextB b E.B E.C = E.B2 ++ List.replicate E.u (b - 1) :=
      List.append_cancel_right hB
    change nextC b (suffixPad b a E.B) E.C =
      List.replicate E.v (b - 1) ++ (E.C2 ++ List.replicate E.v (b - 1)) at hC
    rw [nextC_suffixPad h a] at hC
    exact ⟨h, hB0, hC⟩
  · rintro ⟨h, hB, hC⟩
    refine ⟨(hyp_suffixPad_iff a).2 h, ?_, ?_⟩
    · change nextB b (suffixPad b a E.B) E.C =
        suffixPad b a' E.B2 ++ List.replicate w (b - 1)
      rw [nextB_suffixPad h a, htail, hB]
      rfl
    · change nextC b (suffixPad b a E.B) E.C =
        List.replicate E.v (b - 1) ++ (E.C2 ++ List.replicate E.v (b - 1))
      rw [nextC_suffixPad h a]
      exact hC

/-- A checked edge remains checked after the stated exterior redistribution. -/
theorem edgeOK_suffixPad {b : Nat} {E : Edge} (a a' w : Nat)
    (hcount : a + E.u = w + a') (h : edgeOK b E = true) :
    edgeOK b (padEdge b a a' w E) = true :=
  (edgeOK_suffixPad_iff a a' w hcount).2 h

end Agent114.NeutralExteriorPadding
