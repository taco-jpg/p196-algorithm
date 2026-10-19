import P196.CarryPrefixThresholds.CandidateData

/-! Independent literal exclusions for every remaining third coefficient. -/
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace CarryPrefixThresholds.Candidates
open EightCarryMaximalWidth.Candidates (extensions)

private theorem third_point (d : Fin 5) (a : Fin 19) :
    a.val < 19 - d.val →
    (!accepted ([15, 16, a.val + d.val], [14, 18, a.val])) = true := by
  rcases d with ⟨d, hd⟩
  rcases a with ⟨a, ha⟩
  have hdCases : d = 0 ∨ d = 1 ∨ d = 2 ∨ d = 3 ∨ d = 4 := by omega
  have haCases : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨
      a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨
      a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨
      a = 16 ∨ a = 17 ∨ a = 18 := by omega
  rcases hdCases with hdCase | hdCase | hdCase | hdCase | hdCase <;>
    rcases haCases with haCase | haCase | haCase | haCase | haCase |
      haCase | haCase | haCase | haCase | haCase | haCase | haCase |
      haCase | haCase | haCase | haCase | haCase | haCase | haCase <;>
    subst d <;> subst a <;>
    simp only [Fin.val_mk] <;>
    decide +kernel

/-- No third-column extension in the complete bounded domain survives. -/
theorem third_exclusion : thirdStarts.all (fun p => !accepted p) = true := by
  unfold thirdStarts
  rw [List.all_flatMap]
  apply List.all_eq_true.mpr
  intro d hd
  simp only [extensions, secondCover, List.flatMap_cons, List.flatMap_nil,
    List.append_nil]
  rw [List.all_map]
  apply List.all_eq_true.mpr
  intro a ha
  have hd' := List.mem_range.mp hd
  have ha' := List.mem_range.mp ha
  simpa only [Nat.add_zero, List.cons_append, List.nil_append] using
    third_point ⟨d, hd'⟩ ⟨a, by omega⟩ ha'

#print axioms third_exclusion

end CarryPrefixThresholds.Candidates
