import P196.CarryPrefixThresholds.CandidateData

/-! Each literal start is checked independently by the Lean kernel. -/
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace CarryPrefixThresholds.Candidates

private theorem outer_point (p r : Fin 18) :
    r.val < p.val →
    (outerCover.contains ([p.val + 1], [r.val + 1]) ||
      !accepted ([p.val + 1], [r.val + 1])) = true := by
  rcases p with ⟨p, hp⟩
  rcases r with ⟨r, hr⟩
  have hpCases : p = 0 ∨ p = 1 ∨ p = 2 ∨ p = 3 ∨ p = 4 ∨
      p = 5 ∨ p = 6 ∨ p = 7 ∨ p = 8 ∨ p = 9 ∨ p = 10 ∨
      p = 11 ∨ p = 12 ∨ p = 13 ∨ p = 14 ∨ p = 15 ∨
      p = 16 ∨ p = 17 := by omega
  have hrCases : r = 0 ∨ r = 1 ∨ r = 2 ∨ r = 3 ∨ r = 4 ∨
      r = 5 ∨ r = 6 ∨ r = 7 ∨ r = 8 ∨ r = 9 ∨ r = 10 ∨
      r = 11 ∨ r = 12 ∨ r = 13 ∨ r = 14 ∨ r = 15 ∨
      r = 16 ∨ r = 17 := by omega
  rcases hpCases with hpCase | hpCase | hpCase | hpCase | hpCase |
    hpCase | hpCase | hpCase | hpCase | hpCase | hpCase | hpCase |
    hpCase | hpCase | hpCase | hpCase | hpCase | hpCase <;>
    rcases hrCases with hrCase | hrCase | hrCase | hrCase | hrCase |
      hrCase | hrCase | hrCase | hrCase | hrCase | hrCase | hrCase |
      hrCase | hrCase | hrCase | hrCase | hrCase | hrCase <;>
    subst p <;> subst r <;>
    simp only [Fin.val_mk] <;>
    decide +kernel

/-- Every surviving positive exterior start belongs to the four-pair cover. -/
theorem outer_cover :
    positiveOuterStarts.all
      (fun p => outerCover.contains p || !accepted p) = true := by
  unfold positiveOuterStarts
  rw [List.all_flatMap]
  apply List.all_eq_true.mpr
  intro p hp
  rw [List.all_map]
  apply List.all_eq_true.mpr
  intro r hr
  have hp' := List.mem_range.mp hp
  have hr' := List.mem_range.mp hr
  exact outer_point ⟨p, hp'⟩ ⟨r, by omega⟩ hr'

#print axioms outer_cover

end CarryPrefixThresholds.Candidates
