import Agent108WindowDefs

/-!
Agent #108, session b31b8818, endpoint window bookkeeping for the existing
fixed-window incoming-weight obstruction.  Complete unpadded windows are
retained, including every short-center and empty-buffer case.
-/

namespace Agent108.WindowWeights

/-- Positive-width complete windows indexed by their actual starting position. -/
theorem windows_eq_map_range {α : Type} (d : Nat) (hd : 0 < d) (w : List α) :
    windows d w = (List.range (w.length + 1 - d)).map
      (fun i => (w.drop i).take d) := by
  induction w with
  | nil =>
      have hz : 0 + 1 - d = 0 := by omega
      simp [windows, hz]
  | cons x xs ih =>
      by_cases h : d ≤ (x :: xs).length
      · have he : (x :: xs).length + 1 - d = (xs.length + 1 - d) + 1 := by
          simp only [List.length_cons] at *
          omega
        rw [windows, if_pos h, he, List.range_succ_eq_map, List.map_cons,
          List.map_map]
        simp only [List.drop_zero]
        congr 1
        simpa only [Function.comp_def, List.drop_succ_cons] using ih
      · have hz : (x :: xs).length + 1 - d = 0 := by omega
        simp [windows, h, hz]

end Agent108.WindowWeights
