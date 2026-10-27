import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Word algebra for neutral center padding

These identities concern arbitrary natural-number lists and require no
digit bounds, symmetry, carry assumptions, or restriction on padding length.
-/

namespace Agent119.NeutralCenterPadding

open Agent120.Neutral

/-- Mirrored addition pairs the two constant outer runs with each other. -/
theorem pairs_sandwich (a x y : Nat) (D : List Nat) :
    pairs (List.replicate a x ++ (D ++ List.replicate a y)) =
      List.replicate a (x + y) ++ (pairs D ++ List.replicate a (x + y)) := by
  have h1 : (List.replicate a x).length = (List.replicate a y).length := by simp
  have h2 : D.length = D.reverse.length := by simp
  unfold pairs
  simp only [List.reverse_append, List.reverse_replicate, List.append_assoc]
  rw [List.zipWith_append h1, List.zipWith_append h2]
  simp [Nat.add_comm]

/-- An extra right-boundary symbol can be moved across its constant run. -/
theorem sandwich_append_same (a x y : Nat) (D : List Nat) :
    (List.replicate a x ++ (D ++ List.replicate a y)) ++ [y] =
      List.replicate a x ++ ((D ++ [y]) ++ List.replicate a y) := by
  have hy : List.replicate a y ++ [y] = [y] ++ List.replicate a y := by
    change List.replicate a y ++ List.replicate 1 y =
      List.replicate 1 y ++ List.replicate a y
    simp only [List.replicate_append_replicate]
    rw [Nat.add_comm]
  simp only [List.append_assoc]
  rw [hy]

end Agent119.NeutralCenterPadding

#print axioms Agent119.NeutralCenterPadding.pairs_sandwich
#print axioms Agent119.NeutralCenterPadding.sandwich_append_same
