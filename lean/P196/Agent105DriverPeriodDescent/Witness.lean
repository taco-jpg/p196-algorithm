import P196.Drafts.Agent120NeutralBandCalibration.A120Template

/-!
# A four-step exterior with a two-step joint driver

Every assertion here uses the existing `Agent120.Neutral` definitions.  The
centers are separate one-edge carry fixtures.  No center cycle is asserted.
-/

namespace Agent105.DriverPeriod

open Agent120.Neutral

/-- One actual exterior edge, retaining its per-edge center fixture and labels. -/
structure ExteriorEdge (b : Nat) (B C B' : List Nat) (e g u : Nat) : Prop where
  hyp : Hyp b B C
  carry : e1 b B = e
  overflow : gam b B C = g
  next_eq : nextB b B C = B' ++ List.replicate u (b - 1)

def block0 : List Nat := [4, 7, 7, 8, 3]
def block1 : List Nat := [9, 3, 4, 5, 8]
def block2 : List Nat := [4, 7, 7, 10, 2, 2]
def block3 : List Nat := [9, 3, 4, 9]

def padded0 : List Nat := [4, 7, 7, 8, 3, 5]
def padded1 : List Nat := [9, 3, 4, 5, 8, 5]
def padded2 : List Nat := [4, 7, 7, 10, 2, 2]
def padded3 : List Nat := [9, 3, 4, 9, 5, 5]

private theorem block0_hyp : Hyp 6 block0 [10] := by
  refine ⟨by decide, ?_, ?_, by decide, by decide⟩
  · intro v hv
    simp [block0] at hv
    omega
  · intro v hv
    simp at hv
    omega

private theorem block1_hyp : Hyp 6 block1 [0] := by
  refine ⟨by decide, ?_, ?_, by decide, by decide⟩
  · intro v hv
    simp [block1] at hv
    omega
  · intro v hv
    simp at hv
    omega

private theorem block2_hyp : Hyp 6 block2 [10] := by
  refine ⟨by decide, ?_, ?_, by decide, by decide⟩
  · intro v hv
    simp [block2] at hv
    omega
  · intro v hv
    simp at hv
    omega

private theorem block3_hyp : Hyp 6 block3 [0] := by
  refine ⟨by decide, ?_, ?_, by decide, by decide⟩
  · intro v hv
    simp [block3] at hv
    omega
  · intro v hv
    simp at hv
    omega

/-- Four canonical exterior edges close, with joint labels `01` repeated twice. -/
theorem canonical_four_edges :
    ExteriorEdge 6 block0 [10] block1 0 0 0 ∧
    ExteriorEdge 6 block1 [0] block2 1 1 0 ∧
    ExteriorEdge 6 block2 [10] block3 0 0 2 ∧
    ExteriorEdge 6 block3 [0] block0 1 1 0 := by
  exact ⟨⟨block0_hyp, by decide, by decide, by decide⟩,
    ⟨block1_hyp, by decide, by decide, by decide⟩,
    ⟨block2_hyp, by decide, by decide, by decide⟩,
    ⟨block3_hyp, by decide, by decide, by decide⟩⟩

/-- The canonical words are genuinely four distinct exterior states. -/
theorem canonical_four_distinct :
    List.Pairwise (fun B B' : List Nat => B ≠ B') [block0, block1, block2, block3] := by
  decide

/-- The displayed length-six words are neutral suffix pads of the canonical words. -/
theorem padded_identifications :
    padded0 = block0 ++ List.replicate (6 - block0.length) 5 ∧
    padded1 = block1 ++ List.replicate (6 - block1.length) 5 ∧
    padded2 = block2 ++ List.replicate (6 - block2.length) 5 ∧
    padded3 = block3 ++ List.replicate (6 - block3.length) 5 := by
  decide

private theorem padded0_hyp : Hyp 6 padded0 [10] := by
  refine ⟨by decide, ?_, ?_, by decide, by decide⟩
  · intro v hv
    simp [padded0] at hv
    omega
  · intro v hv
    simp at hv
    omega

private theorem padded1_hyp : Hyp 6 padded1 [0] := by
  refine ⟨by decide, ?_, ?_, by decide, by decide⟩
  · intro v hv
    simp [padded1] at hv
    omega
  · intro v hv
    simp at hv
    omega

private theorem padded2_hyp : Hyp 6 padded2 [10] := by
  refine ⟨by decide, ?_, ?_, by decide, by decide⟩
  · intro v hv
    simp [padded2] at hv
    omega
  · intro v hv
    simp at hv
    omega

private theorem padded3_hyp : Hyp 6 padded3 [0] := by
  refine ⟨by decide, ?_, ?_, by decide, by decide⟩
  · intro v hv
    simp [padded3] at hv
    omega
  · intro v hv
    simp at hv
    omega

/-- At common width six, even the trim stream is `01` repeated twice. -/
theorem padded_four_edges :
    ExteriorEdge 6 padded0 [10] padded1 0 0 0 ∧
    ExteriorEdge 6 padded1 [0] padded2 1 1 1 ∧
    ExteriorEdge 6 padded2 [10] padded3 0 0 0 ∧
    ExteriorEdge 6 padded3 [0] padded0 1 1 1 := by
  exact ⟨⟨padded0_hyp, by decide, by decide, by decide⟩,
    ⟨padded1_hyp, by decide, by decide, by decide⟩,
    ⟨padded2_hyp, by decide, by decide, by decide⟩,
    ⟨padded3_hyp, by decide, by decide, by decide⟩⟩

theorem padded_four_lengths :
    padded0.length = 6 ∧ padded1.length = 6 ∧
    padded2.length = 6 ∧ padded3.length = 6 := by
  decide

theorem padded_four_distinct :
    List.Pairwise (fun B B' : List Nat => B ≠ B') [padded0, padded1, padded2, padded3] := by
  decide

end Agent105.DriverPeriod
