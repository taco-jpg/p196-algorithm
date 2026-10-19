import P196.CrossWidthCollisionStates.StateSpace
import P196.Agent105InverseBoundaries.Agent105CrossWidthWitness9df76b

/-!
# Ordinary witnesses for the productive collision states

Agent #6: six pairs of positive ordinary integers realize every productive
state and every permitted second-column pair. The canonical digit controls
and collision at the shortest width, together with the retained
nonpalindromic collision, are imported from the existing witness module.
New collisions are checked through their finite positional column sums.
The state witnesses retain the full trace range, including positions
beyond the middle of the shorter word.
-/

set_option autoImplicit false

namespace CrossWidthCollisionStates

open DecimalDigits FoldedDecimal Lychrel196
open Agent105.CrossWidthWitness9df76b

private theorem collision_29_110 :
    Canonical 29 (literalDigit 29) 2 ∧
    Canonical 110 (literalDigit 110) 3 ∧ step 29 = step 110 := by
  obtain ⟨hn, hm, _, hs, ht, _⟩ := palindromic_boundary_witness
  exact ⟨hn, hm, hs.trans ht.symm⟩

private theorem collision_200799_1098900 :
    Canonical 200799 (literalDigit 200799) 6 ∧
    Canonical 1098900 (literalDigit 1098900) 7 ∧
    step 200799 = step 1098900 :=
  ⟨short_canonical, long_canonical, short_step.trans long_step.symm⟩

private theorem collision_209_1100 :
    Canonical 209 (literalDigit 209) 3 ∧
    Canonical 1100 (literalDigit 1100) 4 ∧ step 209 = step 1100 := by
  have hn : Canonical 209 (literalDigit 209) 3 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i _
    exact literalDigit_bounded _ i
  have hm : Canonical 1100 (literalDigit 1100) 4 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i _
    exact literalDigit_bounded _ i
  refine ⟨hn, hm, ?_⟩
  calc
    step 209 = value (columnSum (literalDigit 209) 3) 3 :=
      step_eq_word_value _ _ _ _ hn (fun _ _ => rfl)
    _ = value (columnSum (literalDigit 1100) 4) 4 := by decide +kernel
    _ = step 1100 :=
      (step_eq_word_value _ _ _ _ hm (fun _ _ => rfl)).symm

private theorem collision_998012_1199000 :
    Canonical 998012 (literalDigit 998012) 6 ∧
    Canonical 1199000 (literalDigit 1199000) 7 ∧
    step 998012 = step 1199000 := by
  have hn : Canonical 998012 (literalDigit 998012) 6 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i _
    exact literalDigit_bounded _ i
  have hm : Canonical 1199000 (literalDigit 1199000) 7 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i _
    exact literalDigit_bounded _ i
  refine ⟨hn, hm, ?_⟩
  calc
    step 998012 = value (columnSum (literalDigit 998012) 6) 6 :=
      step_eq_word_value _ _ _ _ hn (fun _ _ => rfl)
    _ = value (columnSum (literalDigit 1199000) 7) 7 := by decide +kernel
    _ = step 1199000 :=
      (step_eq_word_value _ _ _ _ hm (fun _ _ => rfl)).symm

private theorem collision_2009799_10989900 :
    Canonical 2009799 (literalDigit 2009799) 7 ∧
    Canonical 10989900 (literalDigit 10989900) 8 ∧
    step 2009799 = step 10989900 := by
  have hn : Canonical 2009799 (literalDigit 2009799) 7 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i _
    exact literalDigit_bounded _ i
  have hm : Canonical 10989900 (literalDigit 10989900) 8 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i _
    exact literalDigit_bounded _ i
  refine ⟨hn, hm, ?_⟩
  calc
    step 2009799 = value (columnSum (literalDigit 2009799) 7) 7 :=
      step_eq_word_value _ _ _ _ hn (fun _ _ => rfl)
    _ = value (columnSum (literalDigit 10989900) 8) 8 := by decide +kernel
    _ = step 10989900 :=
      (step_eq_word_value _ _ _ _ hm (fun _ _ => rfl)).symm

private theorem collision_21008999_101098910 :
    Canonical 21008999 (literalDigit 21008999) 8 ∧
    Canonical 101098910 (literalDigit 101098910) 9 ∧
    step 21008999 = step 101098910 := by
  have hn : Canonical 21008999 (literalDigit 21008999) 8 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i _
    exact literalDigit_bounded _ i
  have hm : Canonical 101098910 (literalDigit 101098910) 9 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i _
    exact literalDigit_bounded _ i
  refine ⟨hn, hm, ?_⟩
  calc
    step 21008999 = value (columnSum (literalDigit 21008999) 8) 8 :=
      step_eq_word_value _ _ _ _ hn (fun _ _ => rfl)
    _ = value (columnSum (literalDigit 101098910) 9) 9 := by decide +kernel
    _ = step 101098910 :=
      (step_eq_word_value _ _ _ _ hm (fun _ _ => rfl)).symm

/-- Every productive state occurs in a genuine ordinary collision
whose longer source has at most nine decimal digits. The index ranges
over the entire shorter source, not only its first half. -/
theorem productive_realized_small (s : State) (hs : s ∈ productive) :
    ∃ (n m L K i : Nat) (d e : Nat → Nat),
      Canonical n d L ∧ Canonical m e K ∧ L < K ∧ step n = step m ∧
      1 ≤ i ∧ i ≤ L ∧ K ≤ 9 ∧
      stateAt (columnSum d L) (columnSum e K) L i = s := by
  simp only [productive, List.mem_cons, List.not_mem_nil, or_false] at hs
  rcases hs with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · obtain ⟨hn, hm, hstep⟩ := collision_29_110
    exact ⟨29, 110, 2, 3, 1, literalDigit 29, literalDigit 110,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_200799_1098900
    exact ⟨200799, 1098900, 6, 7, 3, literalDigit 200799, literalDigit 1098900,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_209_1100
    exact ⟨209, 1100, 3, 4, 2, literalDigit 209, literalDigit 1100,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_998012_1199000
    exact ⟨998012, 1199000, 6, 7, 3, literalDigit 998012, literalDigit 1199000,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_998012_1199000
    exact ⟨998012, 1199000, 6, 7, 5, literalDigit 998012, literalDigit 1199000,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_2009799_10989900
    exact ⟨2009799, 10989900, 7, 8, 4, literalDigit 2009799, literalDigit 10989900,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_998012_1199000
    exact ⟨998012, 1199000, 6, 7, 4, literalDigit 998012, literalDigit 1199000,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_21008999_101098910
    exact ⟨21008999, 101098910, 8, 9, 3, literalDigit 21008999, literalDigit 101098910,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_998012_1199000
    exact ⟨998012, 1199000, 6, 7, 2, literalDigit 998012, literalDigit 1199000,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_200799_1098900
    exact ⟨200799, 1098900, 6, 7, 5, literalDigit 200799, literalDigit 1098900,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_200799_1098900
    exact ⟨200799, 1098900, 6, 7, 2, literalDigit 200799, literalDigit 1098900,
      hn, hm, by decide, hstep, by decide, by decide, by decide, by decide +kernel⟩

/-- Every listed second-column pair occurs in two positive ordinary
sources of different widths with exactly the same successor. -/
theorem second_pair_realized (a b : Nat) (h : (a, b) ∈ secondPairs) :
    ∃ (n m L K : Nat) (d e : Nat → Nat),
      Canonical n d L ∧ Canonical m e K ∧ L < K ∧ step n = step m ∧
      columnSum d L 1 = a ∧ columnSum e K 1 = b := by
  simp only [secondPairs, List.mem_cons, List.not_mem_nil, or_false,
    Prod.mk.injEq] at h
  rcases h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_209_1100
    exact ⟨209, 1100, 3, 4, literalDigit 209, literalDigit 1100,
      hn, hm, by decide, hstep, by decide +kernel, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_200799_1098900
    exact ⟨200799, 1098900, 6, 7, literalDigit 200799, literalDigit 1098900,
      hn, hm, by decide, hstep, by decide +kernel, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_998012_1199000
    exact ⟨998012, 1199000, 6, 7, literalDigit 998012, literalDigit 1199000,
      hn, hm, by decide, hstep, by decide +kernel, by decide +kernel⟩
  · obtain ⟨hn, hm, hstep⟩ := collision_29_110
    exact ⟨29, 110, 2, 3, literalDigit 29, literalDigit 110,
      hn, hm, by decide, hstep, by decide +kernel, by decide +kernel⟩

end CrossWidthCollisionStates

#print axioms CrossWidthCollisionStates.productive_realized_small
#print axioms CrossWidthCollisionStates.second_pair_realized
