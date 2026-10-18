import P196.Drafts.D20261015ScalarHierarchyReviewSourceSnapshots.ActualPrefixLift

/-! Exact ten-edge scalar root and its actual two-column lift. The root
table agrees with job zero of the frozen component certificate. -/

namespace ScalarRoot

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory ActualPrefixLift

def rootEdges : List (Nat × Nat × Nat) :=
  [(0, 1, 0), (1, 2, 0), (2, 3, 0), (2, 3, 1), (3, 4, 1),
   (4, 5, 0), (4, 5, 1), (5, 6, 1), (6, 0, 0), (6, 0, 1)]

def root : Graph (Fin 7) where
  valid _ := True
  phase p := p.val
  last p := ScalarClock.phaseValue p.val
  low p := ScalarClock.phaseValue p.val / 10
  edge p r c := (p.val, r.val, c) ∈ rootEdges

/-- A kernel evaluation of all 98 possible root triples. -/
theorem root_edge_exact : ∀ (p r : Fin 7) (c : Fin 2),
    root.edge p r c.val ↔ r.val = (p.val + 1) % 7 ∧
      (ScalarClock.step (ScalarClock.phaseValue p.val) (decide (c.val = 1))).1 =
        ScalarClock.phaseValue r.val := by
  unfold root
  decide

def phasePath (s i : Nat) : Fin 7 := ⟨(s + i) % 7, Nat.mod_lt _ (by decide)⟩

/-- Every finite actual scalar-clock interval lies in the exact root graph. -/
theorem actual_root_path (q : Nat → Nat) (L a s n : Nat)
    (ha : Admissible L q)
    (hc : ∀ i, i < n → (state q L a i).2 0 = ScalarClock.phase (s + i)) :
    ActualPath root q L 1 a s (phasePath s) n := by
  refine ⟨hc, ?_, ?_⟩
  · intro i hi
    refine ⟨True.intro, rfl, ?_, ?_⟩
    · simpa only [root, phasePath, ScalarClock.phase, Nat.sub_self] using (hc i hi).symm
    · change ScalarClock.phaseValue ((s + i) % 7) / 10 =
        carry (state q L a i).2 1
      simp only [carry, Nat.add_zero]
      rw [hc i hi]
      rfl
  · intro i hi
    have had := state_admissible q L a i ha
    have hb : label q L 1 a i < 2 := by
      have hh := carry_bounded (state q L a i).2 (state q L a i).1
        had.2.2.1 ((state q L a i).1 - 1) (by omega)
      change carry (state q L a i).2 ((state q L a i).1 - 1) < 2
      omega
    apply (root_edge_exact (phasePath s i) (phasePath s (i + 1))
      ⟨label q L 1 a i, hb⟩).mpr
    refine ⟨?_, ?_⟩
    · simp only [phasePath]
      omega
    · have hs := congrArg Prod.fst (ActualScalar.actual_scalar_step
        (state q L a i).2 (state q L a i).1 had)
      simp only [Prod.fst] at hs
      have hn : nextColumns (state q L a i).2 (state q L a i).1 0 =
          (state q L a (i + 1)).2 0 := by
        simp only [state, Nat.add_assoc, iterPairs]
        rfl
      rw [hn, hc (i + 1) hi, hc i (by omega)] at hs
      exact hs.symm

def twoColumnId (v : Fin 7 × Fin 19) : Nat := 19 * v.1.val + v.2.val

theorem twoColumnId_lt (v : Fin 7 × Fin 19) : twoColumnId v < 133 := by
  have hp := v.1.isLt
  have ha := v.2.isLt
  unfold twoColumnId
  omega

theorem twoColumnId_parent (v : Fin 7 × Fin 19) : twoColumnId v / 19 = v.1.val := by
  have ha := v.2.isLt
  unfold twoColumnId
  omega

theorem twoColumnId_coefficient (v : Fin 7 × Fin 19) : twoColumnId v % 19 = v.2.val := by
  have ha := v.2.isLt
  unfold twoColumnId
  omega

/-- The first concrete spatial refinement is an actual path on 133 vertices.
Its edge labels are the actual carries entering the high two-column block. -/
theorem actual_two_column_path (q : Nat → Nat) (L a s n : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L)
    (hc : ∀ i, i < n → (state q L a i).2 0 = ScalarClock.phase (s + i)) :
    ∃ path, ActualPath (lift root) q L 2 a s path n ∧
      ∀ i, (path i).1 = phasePath s i ∧
        (path i).2.val = (state q L a i).2 1 ∧ twoColumnId (path i) < 133 := by
  let path := childPath q L 1 a (phasePath s) ha (by omega)
  refine ⟨path, actual_path_lifts root q L 1 a s n (phasePath s) ha (by decide)
    (by omega) (actual_root_path q L a s n ha hc), ?_⟩
  intro i
  exact ⟨rfl, rfl, twoColumnId_lt (path i)⟩

end ScalarRoot
