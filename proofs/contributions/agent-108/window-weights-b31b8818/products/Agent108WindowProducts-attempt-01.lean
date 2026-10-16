import Agent108WindowDefs

namespace Agent108.WindowWeights

theorem windows_nil {α : Type} (d : Nat) : windows d ([] : List α) = [] := rfl

theorem windows_short {α : Type} (d : Nat) (w : List α) (h : w.length < d) :
    windows d w = [] := by
  cases w with
  | nil => rfl
  | cons x xs => simp [windows, Nat.not_le.mpr h]

theorem windows_append_overlap {α : Type} (b : Nat) (a pad c : List α)
    (hp : pad.length = b) :
    windows (b+1) (a ++ pad ++ c) =
      windows (b+1) (a ++ pad) ++ windows (b+1) (pad ++ c) := by
  induction a with
  | nil =>
      have hz : windows (b+1) pad = [] := windows_short _ _ (by omega)
      simp [hz]
  | cons x xs ih =>
      have h1 : b+1 ≤ (x :: (xs ++ pad)).length := by simp [hp]; omega
      have h2 : b+1 ≤ (x :: (xs ++ pad ++ c)).length := by simp [hp]; omega
      have ht : (x :: (xs ++ pad ++ c)).take (b+1) =
          (x :: (xs ++ pad)).take (b+1) := by
        change ((x :: (xs ++ pad)) ++ c).take (b+1) = _
        exact List.take_append_of_le_length h1
      simp only [List.cons_append, windows, if_pos h1, if_pos h2,
        List.cons_append, ht]
      exact congrArg (fun t => (x :: (xs ++ pad)).take (b+1) :: t) ih

#print axioms windows_append_overlap

end Agent108.WindowWeights
