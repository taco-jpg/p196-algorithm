import Agent108WindowDefs

namespace Agent108.WindowWeights

theorem windows_nil {α : Type} (d : Nat) : windows d ([] : List α) = [] := rfl

theorem windows_short {α : Type} (d : Nat) (w : List α) (h : w.length < d) :
    windows d w = [] := by
  cases w with
  | nil => rfl
  | cons x xs => simp only [windows, if_neg (Nat.not_le.mpr h)]

theorem windows_append_overlap {α : Type} (b : Nat) (a pad c : List α)
    (hp : pad.length = b) :
    windows (b+1) (a ++ pad ++ c) =
      windows (b+1) (a ++ pad) ++ windows (b+1) (pad ++ c) := by
  induction a with
  | nil =>
      have hz : windows (b+1) pad = [] := windows_short _ _ (by omega)
      simp [hz]
  | cons x xs ih =>
      have h1 : b+1 ≤ (x :: (xs ++ pad)).length := by
        simp only [List.length_cons, List.length_append, hp]; omega
      have h2 : b+1 ≤ (x :: (xs ++ pad ++ c)).length := by
        simp only [List.length_cons, List.length_append, hp]; omega
      have ht : (x :: (xs ++ pad ++ c)).take (b+1) =
          (x :: (xs ++ pad)).take (b+1) := by
        change ((x :: (xs ++ pad)) ++ c).take (b+1) = _
        exact List.take_append_of_le_length h1
      simp only [List.cons_append, windows, if_pos h1, if_pos h2,
        List.cons_append, ht]
      exact congrArg (fun t => (x :: (xs ++ pad)).take (b+1) :: t) ih

/-- The exact unpadded sliding-window convention, with no out-of-range starts. -/
theorem windows_eq_range_map {α : Type} (b : Nat) (w : List α) :
    windows (b+1) w =
      (List.range (w.length-b)).map (fun i => (w.drop i).take (b+1)) := by
  induction w with
  | nil => simp [windows]
  | cons x xs ih =>
      by_cases h : b ≤ xs.length
      · have hl : b+1 ≤ (x :: xs).length := by simp only [List.length_cons]; omega
        have hn : (x :: xs).length-b = (xs.length-b)+1 := by
          simp only [List.length_cons]; omega
        simp only [windows, if_pos hl, hn, List.range_succ_eq_map,
          List.map_cons, List.drop_zero, List.map_map, Function.comp_def]
        rw [ih]
        simp
      · have hl : (x :: xs).length < b+1 := by simp only [List.length_cons]; omega
        have hn : (x :: xs).length-b = 0 := by simp only [List.length_cons]; omega
        simp [windows_short _ _ hl, hn]

theorem windows_length {α : Type} (b : Nat) (w : List α) :
    (windows (b+1) w).length = w.length-b := by
  simp [windows_eq_range_map]

#print axioms windows_append_overlap
#print axioms windows_eq_range_map

end Agent108.WindowWeights
