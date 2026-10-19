import P196.CarryPrefixThresholds.CandidateData

/-! Independent literal certificates for the second-column extensions. -/
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace CarryPrefixThresholds.Candidates
open EightCarryMaximalWidth.Candidates (extensions)

private theorem second_point (p : Pair) (hp : p ∈ outerCover)
    (d : Fin 5) (a : Fin 17) :
    a.val < 17 - d.val →
    (secondCover.contains (p.1 ++ [a.val], p.2 ++ [a.val + (d.val + 2)]) ||
      !accepted (p.1 ++ [a.val], p.2 ++ [a.val + (d.val + 2)])) = true := by
  simp only [outerCover, List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl | rfl | rfl
  all_goals
    rcases d with ⟨d, hd⟩
    rcases a with ⟨a, ha⟩
    have hdCases : d = 0 ∨ d = 1 ∨ d = 2 ∨ d = 3 ∨ d = 4 := by omega
    have haCases : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨
        a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨
        a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 := by omega
    rcases hdCases with hdCase | hdCase | hdCase | hdCase | hdCase <;>
      rcases haCases with haCase | haCase | haCase | haCase | haCase |
        haCase | haCase | haCase | haCase | haCase | haCase | haCase |
        haCase | haCase | haCase | haCase | haCase <;>
      subst d <;> subst a <;>
      simp only [Fin.val_mk] <;>
      decide +kernel

/-- The bounded second-column extensions are covered by one literal pair. -/
theorem second_cover :
    secondStarts.all
      (fun p => secondCover.contains p || !accepted p) = true := by
  unfold secondStarts
  rw [List.all_flatMap]
  apply List.all_eq_true.mpr
  intro d hd
  unfold extensions
  rw [List.all_flatMap]
  apply List.all_eq_true.mpr
  intro p hp
  rw [List.all_map]
  apply List.all_eq_true.mpr
  intro a ha
  have hd' := List.mem_range.mp hd
  have ha' := List.mem_range.mp ha
  simpa only [Nat.add_zero] using
    second_point p hp ⟨d, hd'⟩ ⟨a, by omega⟩ ha'

#print axioms second_cover

end CarryPrefixThresholds.Candidates
