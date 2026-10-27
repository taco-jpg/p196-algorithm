import P196.Agent119NeutralCenterPadding.Padding
import P196.Agent119NeutralCenterPadding.WordAlgebra

/-!
# Checked neutral-center padding transport

Formalizes the local covariance behind Agent7's paper normalization theorem
and Agent107's prescribed-schedule transport. The Agent120 checker is unchanged.
This module supplies local checked-edge transport, not a decimal certificate.
-/

namespace Agent119.NeutralCenterPadding

open Agent120.Neutral

theorem nextC_eq_pairs (b : Nat) (B C : List Nat) :
    nextC b B C =
      if gam b B C = 0 then pairs (DC b B C)
      else pairs (DC b B C ++ [yd b B C]) := by
  simp [nextC, pairs, List.reverse_append]

/-- The raw center successor commutes with arbitrary symmetric neutral padding. -/
theorem nextC_padC {b : Nat} {B C : List Nat} (h : Hyp b B C) (a : Nat) :
    nextC b B (padC b a C) = padC b a (nextC b B C) := by
  simp only [nextC_eq_pairs, gam_padC (a := a) h, DC_padC (a := a) h, yd_padC (a := a) h]
  split
  · rw [pairs_sandwich, h.xy]
    rfl
  · rw [sandwich_append_same, pairs_sandwich, h.xy]
    rfl

/-- Converse to the existing edgeOK_sound, without changing its acceptance test. -/
theorem edgeOK_of_equations {b : Nat} {E : Edge} (h : Hyp b E.B E.C)
    (hB : nextB b E.B E.C = E.B2 ++ List.replicate E.u (b - 1))
    (hC : nextC b E.B E.C = padC b E.v E.C2) : edgeOK b E = true := by
  simp only [edgeOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true]
  exact ⟨⟨⟨⟨⟨⟨h.base, h.boundB⟩, h.boundC⟩, h.ext⟩, h.flip⟩, hB⟩, hC⟩

/-- Pad source and target centers and prescribe the new center trim. -/
def transportEdge (b a a' w : Nat) (E : Edge) : Edge where
  B := E.B
  C := padC b a E.C
  B2 := E.B2
  C2 := padC b a' E.C2
  u := E.u
  v := w

/-- The exact additive balance transports a valid edge through the same checker. -/
theorem edgeOK_transport {b : Nat} {E : Edge} (he : edgeOK b E = true)
    (a a' w : Nat) (balance : a + E.v = w + a') :
    edgeOK b (transportEdge b a a' w E) = true := by
  obtain ⟨h, hB, hC⟩ := edgeOK_sound he
  apply edgeOK_of_equations
  · exact Hyp_padC (a := a) h
  · change nextB b E.B (padC b a E.C) = E.B2 ++ List.replicate E.u (b - 1)
    rw [nextB_padC (a := a) h]
    exact hB
  · change nextC b E.B (padC b a E.C) = padC b w (padC b a' E.C2)
    rw [nextC_padC h a]
    change nextC b E.B E.C = padC b E.v E.C2 at hC
    rw [hC, padC_add, padC_add, balance]

/-- Padding does not alter the overflow label of the transported checked edge. -/
theorem transportEdge_gam {b : Nat} {E : Edge} (he : edgeOK b E = true)
    (a a' w : Nat) :
    gam b (transportEdge b a a' w E).B (transportEdge b a a' w E).C =
      gam b E.B E.C := by
  exact gam_padC (a := a) (edgeOK_sound he).1

end Agent119.NeutralCenterPadding

#print axioms Agent119.NeutralCenterPadding.nextC_eq_pairs
#print axioms Agent119.NeutralCenterPadding.nextC_padC
#print axioms Agent119.NeutralCenterPadding.edgeOK_of_equations
#print axioms Agent119.NeutralCenterPadding.edgeOK_transport
#print axioms Agent119.NeutralCenterPadding.transportEdge_gam
