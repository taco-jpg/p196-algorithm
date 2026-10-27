import P196.ManagerShortTwoRunReturns.CycleRefinement
import P196.Agent2SaturatedProfile.WholeWordBridge

/-!
The head-derived weight is exactly actual decimal width growth. This bridge
supplies every prefix and every temporal carry from one actual full-word orbit.
-/

namespace P196.ManagerShortTwoRun

open SevenColumnProjection DecimalDigits FoldedDecimal OverflowCarryNormalization
open P196.Agent4.WholeWord

theorem headGamma_singleton : ∀ a : Fin 19, ∀ e : Fin 2,
    headGamma a.val ((forwardPrefix [a.val] e.val).headD 0) = (a.val + e.val) / 10 := by
  decide +kernel

/-- Actual width growth is determined by the two consecutive outside columns. -/
theorem actual_headGamma (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    headGamma (q 0) (nextColumns q L 0) = carry q L := by
  have hL := ha.1
  have hb := ha.2.2.1 0 ha.1
  have he := carry_bounded q L ha.2.2.1 (L - 1) (by omega)
  have hp := congrArg (fun xs : List Nat => xs.headD 0)
    (actual_forwardPrefix q L 1 ha (by omega))
  change (forwardPrefix [q 0] (carry q (L - 1))).headD 0 = nextColumns q L 0 at hp
  have hc := congrArg Prod.fst (highDigits_segment q L 0 1 ha.2.2.2.1 (by omega))
  change (q 0 + carry q (L - 1)) / 10 = carry q L at hc
  rw [← hp]
  exact (headGamma_singleton ⟨q 0, by omega⟩ ⟨carry q (L - 1), by omega⟩).trans hc

theorem traceGain_rowsAt_succ (s : Nat → List Nat) (t n : Nat) :
    traceGain (rowsAt s t (n + 1)) =
      headGamma ((s t).headD 0) ((s (t + 1)).headD 0) +
        traceGain (rowsAt s (t + 1) n) := by
  cases n <;> rfl

theorem traceGain_telescopes (s : Nat → List Nat) (w : Nat → Nat)
    (h : ∀ t, w (t + 1) = w t + headGamma ((s t).headD 0) ((s (t + 1)).headD 0))
    (t n : Nat) : w (t + n) = w t + traceGain (rowsAt s t n) := by
  induction n generalizing t with
  | zero => simp [rowsAt, traceGain]
  | succ n ih =>
    rw [traceGain_rowsAt_succ]
    calc
      w (t + (n + 1)) = w ((t + 1) + n) := by congr 1; omega
      _ = w (t + 1) + traceGain (rowsAt s (t + 1) n) := ih (t + 1)
      _ = w t + (headGamma ((s t).headD 0) ((s (t + 1)).headD 0) +
          traceGain (rowsAt s (t + 1) n)) := by rw [h]; omega

theorem actual_traceGain (q : Nat → Nat) (L P : Nat) (ha : Admissible L q) :
    (iterPairs q L P).1 = L +
      traceGain (rowsAt (fun t => [(iterPairs q L t).2 0]) 0 P) := by
  have hs (t : Nat) : (iterPairs q L (t + 1)).1 = (iterPairs q L t).1 +
      headGamma ((iterPairs q L t).2 0) ((iterPairs q L (t + 1)).2 0) := by
    have had := CarryHistory.iterPairs_admissible q L t ha
    have hg := actual_headGamma (iterPairs q L t).2 (iterPairs q L t).1 had
    have hb := carry_bounded (iterPairs q L t).2 (iterPairs q L t).1
      had.2.2.1 (iterPairs q L t).1 (by omega)
    change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 =
      (iterPairs q L t).1 + headGamma ((iterPairs q L t).2 0)
        (nextColumns (iterPairs q L t).2 (iterPairs q L t).1 0)
    rw [hg]
    unfold nextWidth
    split <;> omega
  simpa only [Nat.zero_add, iterPairs, List.headD_cons] using
    traceGain_telescopes (fun t => [(iterPairs q L t).2 0])
      (fun t => (iterPairs q L t).1) hs 0 P

/-- Every actual closed prefix with width gain G occurs in the finite catalog.
All intermediate words are supplied by the existing exact dynamics theorem. -/
theorem actual_prefix_member (q : Nat → Nat) (L P G k : Nat)
    (ha : Admissible L q) (hk : k ≤ L)
    (hclose : ∀ i, i < k → (iterPairs q L P).2 i = q i)
    (hwidth : (iterPairs q L P).1 = L + G) :
    rowsAt (fun t => wordPrefix (iterPairs q L t).2 k) 0 P ∈ candidates P G k := by
  apply candidates_complete (fun t => (iterPairs q L t).2) P G k
  · intro t ht i hi
    have had := CarryHistory.iterPairs_admissible q L t ha
    have hw := iterPairs_width_ge q L t
    have hb := had.2.2.1 i (by omega)
    omega
  · exact ha.2.1
  · intro j hj t ht
    have had := CarryHistory.iterPairs_admissible q L t ha
    have hw := iterPairs_width_ge q L t
    exact actual_forward_admitted (iterPairs q L t).2 (iterPairs q L t).1 j
      had (by omega)
  · exact hclose
  · have hg := actual_traceGain q L P ha
    omega

#print axioms headGamma_singleton
#print axioms actual_headGamma
#print axioms actual_traceGain
#print axioms actual_prefix_member

end P196.ManagerShortTwoRun
