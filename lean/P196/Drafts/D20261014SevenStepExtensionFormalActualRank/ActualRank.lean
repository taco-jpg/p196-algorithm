import P196.Drafts.D20261014SevenStepExtensionFormalNoFourReturns.RankData
import P196.Drafts.D20261014SevenStepFormalSevenStepOrbit.SevenStepOrbit

/-! Actual whole-word orbit edges satisfy the finite rank-table interface.
The Boolean input is always the whole word's carry at width minus six. -/

namespace ActualRank

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary SevenStepOrbit SixPrefix RankCertificate

def rankAt (q : Nat → Nat) (L t : Nat) : Nat :=
  RankCertificate.rank (t % 7)
    ((iterPairs q L t).2 3) ((iterPairs q L t).2 4) ((iterPairs q L t).2 5)

theorem tail_bounds (q : Nat → Nat) (L t : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    (iterPairs q L t).2 3 < 19 ∧ (iterPairs q L t).2 4 < 19 ∧
      (iterPairs q L t).2 5 < 19 := by
  have hw := widthAt_lower q L t
  change L ≤ (iterPairs q L t).1 at hw
  have had := iterPairs_admissible q L t ha
  have h3 := had.2.2.1 3 (by omega)
  have h4 := had.2.2.1 4 (by omega)
  have h5 := had.2.2.1 5 (by omega)
  omega

theorem assemble_eq_boundary6 (q : Nat → Nat) (phase : Nat)
    (hb : ActualBoundary.boundary q = phasePrefix phase) :
    assemble phase (q 3) (q 4) (q 5) = boundary6 q := by
  have h0 := congrArg Prefix.a hb
  have h1 := congrArg Prefix.b hb
  have h2 := congrArg Prefix.c hb
  change q 0 = (phasePrefix phase).a at h0
  change q 1 = (phasePrefix phase).b at h1
  change q 2 = (phasePrefix phase).c at h2
  simp only [assemble, boundary6, ← h0, ← h1, ← h2]

theorem actual_six_step_at (q : Nat → Nat) (L t : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    (boundary6 (iterPairs q L (t + 1)).2, overflowAt q L t) =
      SixPrefix.step (boundary6 (iterPairs q L t).2)
        (SixPrefix.actualControl (iterPairs q L t).2 (iterPairs q L t).1) := by
  have hw := widthAt_lower q L t
  change L ≤ (iterPairs q L t).1 at hw
  exact actual_boundary6_step (iterPairs q L t).2 (iterPairs q L t).1
    (by omega) (iterPairs_admissible q L t ha)

/-- Every actual clock-preserving edge has bounded tail coordinates and
the exact accepted-edge fields used by the finite rank certificate. -/
theorem actual_clock_edge (q : Nat → Nat) (L t : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hbefore : boundaryAt q L t = phasePrefix (t % 7))
    (hafter : boundaryAt q L (t + 1) = phasePrefix ((t + 1) % 7))
    (hover : overflowAt q L t = phaseOverflow (t % 7)) :
    let s := iterPairs q L t
    let p := t % 7
    let result := SixPrefix.step (assemble p (s.2 3) (s.2 4) (s.2 5))
      (SixPrefix.actualControl s.2 s.1)
    s.2 3 < 19 ∧ s.2 4 < 19 ∧ s.2 5 < 19 ∧
      first3 result.1 = phasePrefix ((p + 1) % 7) ∧
      result.2 = phaseOverflow p ∧
      rankAt q L (t + 1) = RankCertificate.rank ((p + 1) % 7)
        result.1.x3 result.1.x4 result.1.x5 := by
  dsimp only
  have hb := assemble_eq_boundary6 (iterPairs q L t).2 (t % 7) hbefore
  have hs := actual_six_step_at q L t hL ha
  rw [← hb] at hs
  have hphase : (t % 7 + 1) % 7 = (t + 1) % 7 := by omega
  obtain ⟨h3, h4, h5⟩ := tail_bounds q L t hL ha
  refine ⟨h3, h4, h5, ?_, ?_, ?_⟩
  · have hp := congrArg (fun z : Prefix6 × Nat => first3 z.1) hs
    change boundaryAt q L (t + 1) = _ at hp
    rw [hphase]
    exact hp.symm.trans hafter
  · have hp := congrArg Prod.snd hs
    exact hp.symm.trans hover
  · have hp := congrArg (fun z : Prefix6 × Nat =>
      RankCertificate.rank ((t + 1) % 7) z.1.x3 z.1.x4 z.1.x5) hs
    rw [hphase]
    exact hp

end ActualRank
