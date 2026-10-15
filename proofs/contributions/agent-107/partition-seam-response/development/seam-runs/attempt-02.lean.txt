import RawSymmetryObstruction

/-!
Exact local seam response on a genuine block of a cut partition.
The block may be all nines, and its initial carry is the actual whole-word
carry. No symmetry or freely chosen interior carry is assumed.
-/

namespace Agent107.SeamRuns

open DecimalDigits IncomingCarrySensitivity RawSymmetryObstruction

/-- On a genuine partition block, the outgoing seam defect is the incoming
actual carry precisely on the maximal initial run of nines. -/
theorem seamDefect_on_block (q : Nat → Nat) (cut : Nat → Bool)
    (a L ell i : Nat)
    (ha : a = 0 ∨ cut a = true)
    (hinside : ∀ j, 0 < j → j < L → cut (a + j) = false)
    (hq : ∀ j, j < a + L → q j ≤ 18)
    (hrun : InitialNineRun (fun j => q (a + j)) L ell)
    (hi : i < L) :
    seamDefect q cut (a + i) =
      if i < ell then (carry q a : Int) else 0 := by
  unfold seamDefect
  rw [resetOut_on_block q cut a i ha
    (fun j hj hji => hinside j hj (by omega)), carryWith_zero]
  have h := actual_block_outgoing_run q a L ell i hq hrun hi
  simpa only [Nat.add_assoc] using h

/-- The actual terminal carry equals the isolated terminal carry plus the
incoming carry exactly when the entire block is nine. This also covers L=0. -/
theorem actual_block_terminal_transfer (q : Nat → Nat) (a L ell : Nat)
    (hq : ∀ j, j < a + L → q j ≤ 18)
    (hrun : InitialNineRun (fun j => q (a + j)) L ell) :
    carry q (a + L) = carry (fun j => q (a + j)) L +
      if ell = L then carry q a else 0 := by
  have h := actual_block_carry_defect q a L L hq (Nat.le_refl L)
  rw [nineIndicator_of_run (fun j => q (a + j)) L ell L hrun
    (Nat.le_refl L)] at h
  have hle := hrun.1
  by_cases heq : ell = L
  · subst ell
    simp only [Nat.le_refl, if_true, Int.mul_one] at h
    simp only [if_true]
    omega
  · have hlt : ¬ L ≤ ell := by omega
    simp only [if_neg hlt, Int.mul_zero] at h
    simp only [if_neg heq, Nat.add_zero]
    omega

/-- The actual next-block incoming carry in terms of the genuine partition
block's isolated outgoing carry. Nonempty blocks have a final column. -/
theorem actual_partition_block_terminal_transfer
    (q : Nat → Nat) (cut : Nat → Bool) (a L ell : Nat)
    (hL : 0 < L)
    (ha : a = 0 ∨ cut a = true)
    (hinside : ∀ j, 0 < j → j < L → cut (a + j) = false)
    (hq : ∀ j, j < a + L → q j ≤ 18)
    (hrun : InitialNineRun (fun j => q (a + j)) L ell) :
    carry q (a + L) = resetOut q cut (a + (L - 1)) +
      if ell = L then carry q a else 0 := by
  rw [resetOut_on_block q cut a (L - 1) ha
    (fun j hj hjL => hinside j hj (by omega)), carryWith_zero]
  have heq : L - 1 + 1 = L := by omega
  rw [heq]
  exact actual_block_terminal_transfer q a L ell hq hrun

theorem int_sum_append (xs ys : List Int) :
    (xs ++ ys).sum = xs.sum + ys.sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih, Int.add_assoc]

/-- A constant initial-run indicator has exactly min(n,ell) contributions. -/
theorem sum_initial_run (n ell : Nat) (c : Int) :
    ((List.range n).map (fun i => if i < ell then c else 0)).sum =
      c * (min n ell : Nat) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [List.range_succ, List.map_append, int_sum_append]
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
      Int.add_zero]
    rw [ih]
    by_cases hn : n < ell
    · have hns : n + 1 ≤ ell := by omega
      rw [if_pos hn, Nat.min_eq_left (by omega), Nat.min_eq_left hns]
      simp [Int.natCast_add, Int.mul_add]
    · have hle : ell ≤ n := by omega
      rw [if_neg hn, Nat.min_eq_right hle,
        Nat.min_eq_right (by omega)]
      simp

/-- Sum of outgoing seam defects over a finite block, in local coordinates. -/
def blockDefectSum (q : Nat → Nat) (cut : Nat → Bool) (a L : Nat) : Int :=
  ((List.range L).map (fun i => seamDefect q cut (a + i))).sum

/-- The entire block defect mass is the actual incoming carry times the
length of its initial nine-run, including the all-nine case. -/
theorem block_defect_sum (q : Nat → Nat) (cut : Nat → Bool)
    (a L ell : Nat)
    (ha : a = 0 ∨ cut a = true)
    (hinside : ∀ j, 0 < j → j < L → cut (a + j) = false)
    (hq : ∀ j, j < a + L → q j ≤ 18)
    (hrun : InitialNineRun (fun j => q (a + j)) L ell) :
    blockDefectSum q cut a L = (carry q a : Int) * (ell : Int) := by
  unfold blockDefectSum
  have hmaps :
      (List.range L).map (fun i => seamDefect q cut (a + i)) =
      (List.range L).map (fun i => if i < ell then (carry q a : Int) else 0) := by
    apply List.map_congr_left
    intro i hi
    exact seamDefect_on_block q cut a L ell i ha hinside hq hrun
      (List.mem_range.mp hi)
  rw [hmaps, sum_initial_run, Nat.min_eq_right hrun.1]

#print axioms seamDefect_on_block
#print axioms actual_block_terminal_transfer
#print axioms actual_partition_block_terminal_transfer
#print axioms int_sum_append
#print axioms sum_initial_run
#print axioms block_defect_sum

end Agent107.SeamRuns
