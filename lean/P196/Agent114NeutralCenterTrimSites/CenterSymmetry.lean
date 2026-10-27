import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Agent 114: center symmetry for the unchanged A120 checker

Every raw center successor is invariant under reversal, for arbitrary inputs.
An accepted edge therefore has a symmetric target center, even if its source
center was not symmetric.  Closure of a nonempty accepted cycle forces all
of its source and target centers, including the specified start, to be
symmetric.  No digit or carry hypothesis is added to the original checker.
-/

namespace Agent114.NeutralCenterTrimSites

open Agent120.Neutral

/-- The raw center successor is symmetric for all inputs in either branch. -/
theorem nextC_reverse (b : Nat) (B C : List Nat) :
    (nextC b B C).reverse = nextC b B C := by
  unfold nextC
  split
  · simpa only [List.reverse_reverse] using
      (zipWith_add_reverse_swap (DC b B C) (DC b B C).reverse (by simp)).symm
  · simpa only [List.reverse_cons, List.reverse_append, List.reverse_nil,
      List.nil_append, List.reverse_reverse, List.singleton_append] using
      (zipWith_add_reverse_swap (DC b B C ++ [yd b B C])
        (yd b B C :: (DC b B C).reverse) (by simp)).symm

/-- Equal trimming at the two ends of a symmetric raw center leaves a
symmetric target.  The source need not be symmetric. -/
theorem edge_target_center_symmetric {b : Nat} {E : Edge}
    (he : edgeOK b E = true) : E.C2.reverse = E.C2 := by
  have hs := nextC_reverse b E.B E.C
  rw [(edgeOK_sound he).2.2] at hs
  simpa only [List.reverse_append, List.reverse_replicate, List.append_assoc,
    List.append_cancel_left_eq, List.append_cancel_right_eq] using hs

/-- A symmetric start and an accepted chain give symmetric centers at every
listed source and target, and at the final state. -/
theorem chain_centers_symmetric {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hC : C.reverse = C) :
    (endC es C).reverse = endC es C ∧
      ∀ E ∈ es, E.C.reverse = E.C ∧ E.C2.reverse = E.C2 := by
  induction es generalizing B C with
  | nil => exact ⟨hC, by simp⟩
  | cons e es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, heC⟩, he⟩, ht⟩ := hc
      have h2 := edge_target_center_symmetric he
      obtain ⟨hEnd, hMembers⟩ := ih ht h2
      refine ⟨hEnd, ?_⟩
      intro E hE
      rcases List.mem_cons.mp hE with rfl | hE
      · exact ⟨by rw [heC]; exact hC, h2⟩
      · exact hMembers E hE

/-- After at least one accepted edge, the final center is symmetric without
any assumption on the initial center. -/
theorem nonempty_chain_endC_symmetric {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hne : es ≠ []) :
    (endC es C).reverse = endC es C := by
  cases es with
  | nil => exact False.elim (hne rfl)
  | cons e es =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, ht⟩ := hc
      exact (chain_centers_symmetric ht (edge_target_center_symmetric he)).1

/-- Nonempty cycle closure supplies the initial symmetry, so every accepted
cycle already has symmetric centers throughout. -/
theorem cycle_centers_symmetric {b : Nat} {es : List Edge} {B C : List Nat}
    (hcert : cycleOK b es B C = true) :
    C.reverse = C ∧ ∀ E ∈ es, E.C.reverse = E.C ∧ E.C2.reverse = E.C2 := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hcert
  obtain ⟨⟨⟨⟨hne, hc⟩, _⟩, hend⟩, _⟩ := hcert
  have hC : C.reverse = C := by
    simpa only [hend] using nonempty_chain_endC_symmetric hc hne
  exact ⟨hC, (chain_centers_symmetric hc hC).2⟩

end Agent114.NeutralCenterTrimSites

#print axioms Agent114.NeutralCenterTrimSites.nextC_reverse
#print axioms Agent114.NeutralCenterTrimSites.edge_target_center_symmetric
#print axioms Agent114.NeutralCenterTrimSites.chain_centers_symmetric
#print axioms Agent114.NeutralCenterTrimSites.nonempty_chain_endC_symmetric
#print axioms Agent114.NeutralCenterTrimSites.cycle_centers_symmetric
