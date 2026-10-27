import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Neutral padding of the center

Adding equally many neutral coefficients to both ends of the center preserves
the carry flip, all exterior data, and the untrimmed exterior transition.
-/

namespace Agent119.NeutralCenterPadding

open Agent120.Neutral

def padC (b a : Nat) (C : List Nat) : List Nat :=
  List.replicate a (b - 1) ++ (C ++ List.replicate a (b - 1))

theorem padC_zero (b : Nat) (C : List Nat) : padC b 0 C = C := by
  simp [padC]

theorem padC_add (b a d : Nat) (C : List Nat) :
    padC b a (padC b d C) = padC b (a + d) C := by
  simp only [padC, List.append_assoc]
  rw [← List.append_assoc (List.replicate a (b - 1)) (List.replicate d (b - 1)),
    List.replicate_append_replicate, List.replicate_append_replicate, Nat.add_comm d a]

theorem padC_length (b a : Nat) (C : List Nat) :
    (padC b a C).length = C.length + 2 * a := by
  simp only [padC, List.length_append, List.length_replicate]
  omega

theorem norm_padC {b a : Nat} {B C : List Nat} (h : Hyp b B C) :
    norm b (padC b a C) (e1 b B) =
      (List.replicate a (xd b B) ++ (DC b B C ++ List.replicate a (yd b B C)),
        e2 b B C) := by
  unfold padC
  rw [norm_append, norm_replicate_neutral b h.base a (e1 b B) h.e1_le]
  simp only
  rw [norm_append]
  change
    (List.replicate a (xd b B) ++
      (DC b B C ++ (norm b (List.replicate a (b - 1)) (e2 b B C)).1),
      (norm b (List.replicate a (b - 1)) (e2 b B C)).2) = _
  rw [norm_replicate_neutral b h.base a (e2 b B C) h.e2_le]
  rfl

theorem e2_padC {b a : Nat} {B C : List Nat} (h : Hyp b B C) :
    e2 b B (padC b a C) = e2 b B C := by
  have hn := congrArg Prod.snd (norm_padC (a := a) h)
  exact hn

theorem DC_padC {b a : Nat} {B C : List Nat} (h : Hyp b B C) :
    DC b B (padC b a C) =
      List.replicate a (xd b B) ++ (DC b B C ++ List.replicate a (yd b B C)) := by
  exact congrArg Prod.fst (norm_padC (a := a) h)

theorem Hyp_padC {b a : Nat} {B C : List Nat} (h : Hyp b B C) :
    Hyp b B (padC b a C) := by
  refine ⟨h.base, h.boundB, ?_, h.ext, ?_⟩
  · intro v hv
    simp only [padC, List.mem_append, List.mem_replicate] at hv
    rcases hv with ⟨_, rfl⟩ | hv | ⟨_, rfl⟩
    · omega
    · exact h.boundC v hv
    · omega
  · rw [e2_padC h]
    exact h.flip

theorem DR_padC {b a : Nat} {B C : List Nat} (h : Hyp b B C) :
    DR b B (padC b a C) = DR b B C := by
  unfold DR
  rw [e2_padC h]

theorem gam_padC {b a : Nat} {B C : List Nat} (h : Hyp b B C) :
    gam b B (padC b a C) = gam b B C := by
  unfold gam
  rw [e2_padC h]

theorem yd_padC {b a : Nat} {B C : List Nat} (h : Hyp b B C) :
    yd b B (padC b a C) = yd b B C := by
  unfold yd
  rw [e2_padC h]

theorem nextB_padC {b a : Nat} {B C : List Nat} (h : Hyp b B C) :
    nextB b B (padC b a C) = nextB b B C := by
  unfold nextB
  rw [gam_padC h, DR_padC h]

end Agent119.NeutralCenterPadding

#print axioms Agent119.NeutralCenterPadding.norm_padC
#print axioms Agent119.NeutralCenterPadding.Hyp_padC
#print axioms Agent119.NeutralCenterPadding.nextB_padC
