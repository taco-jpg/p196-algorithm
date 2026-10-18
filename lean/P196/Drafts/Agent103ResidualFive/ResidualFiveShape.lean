import P196.Agent119EightFamilies.EightFamilies

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

open DecimalDigits FoldedDecimal Lychrel196
open OverflowCarryNormalization NormalizationBridge CarryHistory SevenColumnProjection
open Agent119.EightFamilies

theorem fiveSourceDigit_zero (r : Nat) : fiveSourceDigit r 0 = 2 := by
  simp [fiveSourceDigit]

theorem fiveSourceDigit_one (r : Nat) : fiveSourceDigit r 1 = 12 := by
  unfold fiveSourceDigit
  split <;> (try split) <;> omega

theorem fiveSourceDigit_mid (r i : Nat) (h2 : 2 ≤ i) (hi : i ≤ 2 * r + 1) :
    fiveSourceDigit r i = 9 := by
  unfold fiveSourceDigit
  split <;> (try split) <;> omega

theorem fiveSourceDigit_hi1 (r : Nat) : fiveSourceDigit r (2 * r + 2) = 12 := by
  unfold fiveSourceDigit
  split <;> (try split) <;> omega

theorem fiveSourceDigit_hi0 (r : Nat) : fiveSourceDigit r (2 * r + 3) = 2 := by
  simp [fiveSourceDigit]

private theorem segment_append (q : Nat → Nat) (start m n : Nat) :
    segment q start (m + n) = segment q start m ++ segment q (start + m) n := by
  induction m generalizing start with
  | zero => simp [segment]
  | succ m ih =>
      simp only [Nat.succ_add, segment, List.cons_append]
      rw [ih]
      rw [show start + 1 + m = start + (m + 1) by omega]

private theorem segment_replicate (q : Nat → Nat) (start n a : Nat)
    (h : ∀ i, start ≤ i → i < start + n → q i = a) :
    segment q start n = List.replicate n a := by
  induction n generalizing start with
  | zero => rfl
  | succ n ih =>
      simp only [segment, List.replicate_succ]
      rw [h start (by omega) (by omega)]
      congr 1
      apply ih
      intro i h1 h2
      exact h i (by omega) (by omega)

private theorem segment_congr (q q' : Nat → Nat) (start n : Nat)
    (h : ∀ i, start ≤ i → i < start + n → q i = q' i) :
    segment q start n = segment q' start n := by
  induction n generalizing start with
  | zero => rfl
  | succ n ih =>
      simp only [segment]
      rw [h start (by omega) (by omega)]
      congr 1
      apply ih
      intro i h1 h2
      exact h i (by omega) (by omega)

private theorem eq_of_segment_eq {q q' : Nat → Nat} {n : Nat}
    (h : segment q 0 n = segment q' 0 n) (i : Nat) (hi : i < n) : q i = q' i := by
  have h1 := congrArg (fun l => l[i]?) h
  simp only [segment_eq_range_map] at h1
  rw [List.getElem?_map, List.getElem?_map, List.getElem?_range' hi] at h1
  simp only [Nat.zero_add, Option.map_some', Nat.one_mul] at h1
  exact Option.some.inj h1

theorem segment_famDigit_five (r : Nat) :
    segment (famDigit 5 r) 0 (2 * r + 4) =
      5 :: 5 :: (List.replicate (2 * r) 0 ++ [5, 5]) := by
  change famDigit 5 r 0 :: famDigit 5 r 1 :: segment (famDigit 5 r) 2 (2 * r + 2) = _
  rw [famDigit_zero, famDigit_one, segment_append]
  rw [segment_replicate (famDigit 5 r) 2 (2 * r) 0 (by
    intro i h1 h2
    exact famDigit_mid 5 r i h1 (by omega))]
  change 5 :: 5 :: (List.replicate (2 * r) 0 ++
    [famDigit 5 r (2 + 2 * r), famDigit 5 r (2 + 2 * r + 1)]) = _
  rw [show 2 + 2 * r = 2 * r + 2 by omega,
    show 2 * r + 2 + 1 = 2 * r + 3 by omega, famDigit_hi1, famDigit_hi0]

theorem segment_fiveSourceDigit (r : Nat) :
    segment (fiveSourceDigit r) 0 (2 * r + 4) =
      2 :: 12 :: (List.replicate (2 * r) 9 ++ [12, 2]) := by
  change fiveSourceDigit r 0 :: fiveSourceDigit r 1 ::
    segment (fiveSourceDigit r) 2 (2 * r + 2) = _
  rw [fiveSourceDigit_zero, fiveSourceDigit_one, segment_append]
  rw [segment_replicate (fiveSourceDigit r) 2 (2 * r) 9 (by
    intro i h1 h2
    exact fiveSourceDigit_mid r i h1 (by omega))]
  change 2 :: 12 :: (List.replicate (2 * r) 9 ++
    [fiveSourceDigit r (2 + 2 * r), fiveSourceDigit r (2 + 2 * r + 1)]) = _
  rw [show 2 + 2 * r = 2 * r + 2 by omega,
    show 2 * r + 2 + 1 = 2 * r + 3 by omega, fiveSourceDigit_hi1, fiveSourceDigit_hi0]

/-- Carries are one precisely from column 2 to the last input column. -/
theorem five_source_carry (q : Nat → Nat) (r : Nat)
    (hq : ∀ i, i < 2 * r + 4 → q i = fiveSourceDigit r i)
    (i : Nat) (hi : i ≤ 2 * r + 4) :
    DecimalDigits.carry q i = if 2 ≤ i ∧ i ≤ 2 * r + 3 then 1 else 0 := by
  induction i with
  | zero => rfl
  | succ i ih =>
      show (q i + DecimalDigits.carry q i) / 10 = _
      rw [hq i (by omega), ih (by omega)]
      unfold fiveSourceDigit
      split <;> (try split) <;> (try split) <;> (try split) <;> omega

/-- The canonical output digits: `33 0^(2r) 22`, from the most significant end. -/
def fiveOutputDigit (r i : Nat) : Nat :=
  if i = 0 ∨ i = 1 then 2 else if i = 2 * r + 2 ∨ i = 2 * r + 3 then 3 else 0

theorem five_source_output (q : Nat → Nat) (r : Nat)
    (hq : ∀ i, i < 2 * r + 4 → q i = fiveSourceDigit r i)
    (i : Nat) (hi : i < 2 * r + 4) :
    output q i = fiveOutputDigit r i := by
  show (q i + DecimalDigits.carry q i) % 10 = _
  rw [hq i hi, five_source_carry q r hq i (by omega)]
  unfold fiveSourceDigit fiveOutputDigit
  split <;> (try split) <;> (try split) <;> (try split) <;> (try split) <;> omega

theorem fiveOutputDigit_zero (r : Nat) : fiveOutputDigit r 0 = 2 := by
  simp [fiveOutputDigit]

theorem fiveOutputDigit_one (r : Nat) : fiveOutputDigit r 1 = 2 := by
  simp [fiveOutputDigit]

theorem fiveOutputDigit_mid (r i : Nat) (h2 : 2 ≤ i) (hi : i ≤ 2 * r + 1) :
    fiveOutputDigit r i = 0 := by
  unfold fiveOutputDigit
  split <;> (try split) <;> omega

theorem fiveOutputDigit_hi1 (r : Nat) : fiveOutputDigit r (2 * r + 2) = 3 := by
  unfold fiveOutputDigit
  split <;> (try split) <;> omega

theorem fiveOutputDigit_hi0 (r : Nat) : fiveOutputDigit r (2 * r + 3) = 3 := by
  unfold fiveOutputDigit
  split <;> (try split) <;> omega

theorem five_source_output_value (q : Nat → Nat) (r : Nat)
    (hq : ∀ i, i < 2 * r + 4 → q i = fiveSourceDigit r i) :
    value (output q) (2 * r + 4) = 33 * 10 ^ (2 * r + 2) + 22 := by
  rw [value_congr (output q) (fiveOutputDigit r) (2 * r + 4)
    (five_source_output q r hq)]
  rw [value_sparse (fiveOutputDigit r) r (fun i h1 h2 => fiveOutputDigit_mid r i h1 h2)]
  rw [fiveOutputDigit_zero, fiveOutputDigit_one, fiveOutputDigit_hi1, fiveOutputDigit_hi0]
  omega

/-- The residual family forces both the previous pair coefficients and the
intermediate natural number, provided its production has terminal carry zero. -/
theorem middle_no_overflow_five (s r : Nat)
    (hW : (V (s + 1)).1 = 2 * r + 4)
    (hq : ∀ i, i < 2 * r + 4 → (V (s + 1)).2 i = famDigit 5 r i)
    (hc : DecimalDigits.carry (V s).2 (V s).1 = 0) :
    (∀ i, i < 2 * r + 4 → (V s).2 i = fiveSourceDigit r i) ∧
      orbit 196 (s + 1) = 33 * 10 ^ (2 * r + 2) + 22 := by
  have hW1 : (V (s + 1)).1 = (V s).1 := by
    rw [V_succ_fst]
    simp [nextWidth, hc]
  have hLx : (V s).1 = 2 * r + 4 := by omega
  have hno := actual_noOverflow (V s).2 (V s).1 0 (V s).1
    (V_adm s) (by omega) hc
  rw [Nat.sub_zero, hc, ← V_succ_snd, hLx] at hno
  have ht := segment_congr (V (s + 1)).2 (famDigit 5 r) 0 (2 * r + 4)
    (fun i _ hi => hq i (by omega))
  rw [ht, segment_famDigit_five] at hno
  have hshape := noOverflow_five_shape (2 * r) hno
  rw [← segment_fiveSourceDigit] at hshape
  have hqi : ∀ i, i < 2 * r + 4 → (V s).2 i = fiveSourceDigit r i :=
    eq_of_segment_eq hshape
  refine ⟨hqi, ?_⟩
  have hcan := next_digits_no_overflow s hc
  rw [← hcan.2.2.2, hLx]
  exact five_source_output_value (V s).2 r hqi

end Agent103.ResidualFive

#print axioms Agent103.ResidualFive.noOverflow_five_shape
#print axioms Agent103.ResidualFive.five_source_carry
#print axioms Agent103.ResidualFive.five_source_output_value
#print axioms Agent103.ResidualFive.middle_no_overflow_five
