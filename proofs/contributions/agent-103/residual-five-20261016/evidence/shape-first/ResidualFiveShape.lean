import PrefixInverse

/-!
The forced no-overflow source shape of the residual `55 0^(2r) 55` pair word.
Only the terminal carry vanishes: its unique source has an internal carry run.
-/

namespace Agent103.ResidualFive

open SevenColumn

/-- The unique source pair coefficients, listed from the units end. -/
def fiveSourceDigit (r i : Nat) : Nat :=
  if i = 0 ∨ i = 2 * r + 3 then 2
  else if i = 1 ∨ i = 2 * r + 2 then 12 else 9

private theorem edge_five_00 {a z : Nat} (_ha : a < 19) (hz : z < 2)
    (hy : carry a z = 0) (hv : 5 = lowDigit a 0 + lowDigit a z) :
    a = 2 ∧ z = 1 := by
  simp only [carry, lowDigit, Nat.add_zero] at hy hv
  omega

private theorem edge_five_01 {a z : Nat} (_ha : a < 19) (hz : z < 2)
    (hy : carry a z = 1) (hv : 5 = lowDigit a 0 + lowDigit a z) :
    a = 12 ∧ z = 1 := by
  simp only [carry, lowDigit, Nat.add_zero] at hy hv
  omega

private theorem edge_zero_11 {a z : Nat} (_ha : a < 19) (hz : z < 2)
    (hy : carry a z = 1) (hv : 0 = lowDigit a 1 + lowDigit a z) :
    a = 9 ∧ z = 1 := by
  simp only [carry, lowDigit] at hy hv
  omega

private theorem edge_five_11 {a z : Nat} (_ha : a < 19) (hz : z < 2)
    (hy : carry a z = 1) (hv : 5 = lowDigit a 1 + lowDigit a z) :
    a = 12 ∧ z = 0 := by
  simp only [carry, lowDigit] at hy hv
  omega

private theorem edge_five_10 {a z : Nat} (_ha : a < 19) (hz : z < 2)
    (hy : carry a z = 0) (hv : 5 = lowDigit a 1 + lowDigit a z) :
    a = 2 ∧ z = 0 := by
  simp only [carry, lowDigit] at hy hv
  omega

private theorem noOverflow_zero_run (k : Nat) {s : List Nat}
    (h : NoOverflow (List.replicate k 0 ++ [5, 5]) s 1 1) :
    s = List.replicate k 9 ++ [12, 2] := by
  induction k generalizing s with
  | zero =>
      simp only [List.replicate_zero, List.nil_append] at h ⊢
      cases h with
      | @cons p s v a x y z ha hz hy hv tail =>
          obtain ⟨rfl, rfl⟩ := edge_five_11 ha hz hy hv
          change NoOverflow [5] s 1 0 at tail
          cases tail with
          | @cons p s v a x y z ha hz hy hv tail =>
              obtain ⟨rfl, rfl⟩ := edge_five_10 ha hz hy hv
              cases tail
              rfl
  | succ k ih =>
      simp only [List.replicate_succ, List.cons_append] at h ⊢
      cases h with
      | @cons p s v a x y z ha hz hy hv tail =>
          obtain ⟨rfl, rfl⟩ := edge_zero_11 ha hz hy hv
          change NoOverflow (List.replicate k 0 ++ [5, 5]) s 1 1 at tail
          rw [ih tail]

/-- The inverse is unique for every zero-run length, including zero. -/
theorem noOverflow_five_shape (k : Nat) {s : List Nat}
    (h : NoOverflow (5 :: 5 :: (List.replicate k 0 ++ [5, 5])) s 0 0) :
    s = 2 :: 12 :: (List.replicate k 9 ++ [12, 2]) := by
  cases h with
  | @cons p s v a x y z ha hz hy hv tail =>
      obtain ⟨rfl, rfl⟩ := edge_five_00 ha hz hy hv
      change NoOverflow (5 :: (List.replicate k 0 ++ [5, 5])) s 0 1 at tail
      cases tail with
      | @cons p s v a x y z ha hz hy hv tail =>
          obtain ⟨rfl, rfl⟩ := edge_five_01 ha hz hy hv
          change NoOverflow (List.replicate k 0 ++ [5, 5]) s 1 1 at tail
          rw [noOverflow_zero_run k tail]

end Agent103.ResidualFive

#print axioms Agent103.ResidualFive.noOverflow_five_shape
