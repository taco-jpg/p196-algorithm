import Agent1PeriodicDigits

/-! Literal single-copy template slices used to identify the raw guards. -/
namespace Agent1.Periodic
open Agent8 Agent1.RepeatedBlock

theorem periodicWord_one (B H w : Word) :
    periodicWord B H w 1 = B ++ w ++ H ++ w.reverse ++ B.reverse := by
  simp only [periodicWord, pow, List.append_nil]

theorem take_outer_one (B H w : Word) :
    (periodicWord B H w 1).take B.length = B := by
  rw [periodicWord_one]
  simp only [List.append_assoc, List.take_left]

theorem take_period_one (B H w : Word) :
    ((periodicWord B H w 1).drop B.length).take w.length = w := by
  rw [periodicWord_one]
  simp only [List.append_assoc, List.drop_left, List.take_left]

theorem take_center_one (B H w : Word) :
    ((periodicWord B H w 1).drop (B.length + w.length)).take H.length = H := by
  rw [periodicWord_one]
  have hl : B.length + w.length = (B ++ w).length := List.length_append.symm
  rw [hl]
  rw [show B ++ w ++ H ++ w.reverse ++ B.reverse =
      (B ++ w) ++ (H ++ w.reverse ++ B.reverse) by simp only [List.append_assoc],
    List.drop_left]
  simp only [List.append_assoc, List.take_left]

end Agent1.Periodic

#print axioms Agent1.Periodic.periodicWord_one
#print axioms Agent1.Periodic.take_outer_one
#print axioms Agent1.Periodic.take_period_one
#print axioms Agent1.Periodic.take_center_one
