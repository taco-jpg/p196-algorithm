import LychrelDigitSums

/-!
# Arbitrarily many separate births in one actual decimal step

Repeat the source block (1,9,1,10,9,9,10,1,9,1) m times. Its real
no-overflow successor repeats (2,18,3,1,0,0,1,3,18,2) m times.
Every source position avoids both extremes. Each target block contains
one new maximal zero run and two separate new maximal 18 runs.
This is a family of finite single steps, not repeated regeneration in time.
-/

namespace RunBirths.RepeatedBirths

open DecimalDigits FoldedDecimal

def width (m : Nat) : Nat := 10 * m

def blockSource (r : Nat) : Nat :=
  if r = 3 ∨ r = 6 then 10
  else if r = 1 ∨ r = 4 ∨ r = 5 ∨ r = 8 then 9 else 1

def source (m i : Nat) : Nat :=
  if i < width m then blockSource (i % 10) else 0

def incoming (m i : Nat) : Nat :=
  if i < width m ∧ 4 ≤ i % 10 ∧ i % 10 ≤ 7 then 1 else 0

def blockDigits (r : Nat) : Nat :=
  if r = 0 ∨ r = 2 ∨ r = 6 ∨ r = 9 then 1
  else if r = 1 ∨ r = 8 then 9
  else if r = 7 then 2 else 0

def normalized (m i : Nat) : Nat :=
  if i < width m then blockDigits (i % 10) else 0

def blockTarget (r : Nat) : Nat :=
  if r = 0 ∨ r = 9 then 2
  else if r = 1 ∨ r = 8 then 18
  else if r = 2 ∨ r = 7 then 3
  else if r = 3 ∨ r = 6 then 1 else 0

def target (m i : Nat) : Nat :=
  if i < width m then blockTarget (i % 10) else 0

theorem source_bounded (m i : Nat) : source m i ≤ 18 := by
  unfold source blockSource
  repeat first | omega | split

theorem normalized_bounded (m i : Nat) : normalized m i ≤ 9 := by
  unfold normalized blockDigits
  repeat first | omega | split

theorem exact_column_equation (m i : Nat) :
    normalized m i + 10 * incoming m (i + 1) = source m i + incoming m i := by
  unfold normalized source incoming blockDigits blockSource width
  have hr : i % 10 < 10 := Nat.mod_lt _ (by decide)
  have hs : (i + 1) % 10 < 10 := Nat.mod_lt _ (by decide)
  repeat first | omega | split

theorem actual_carry (m i : Nat) : carry (source m) i = incoming m i := by
  induction i with
  | zero => simp [carry, incoming]
  | succ i ih =>
    have he := exact_column_equation m i
    have hd := normalized_bounded m i
    simp only [carry, ih]
    omega

theorem actual_output (m i : Nat) : output (source m) i = normalized m i := by
  have he := exact_column_equation m i
  have hd := normalized_bounded m i
  simp only [output, actual_carry]
  omega

theorem no_overflow (m : Nat) : carry (source m) (width m) = 0 := by
  rw [actual_carry]
  simp [incoming]

theorem actual_width (m : Nat) : nextWidth (source m) (width m) = width m := by
  simp only [nextWidth, no_overflow, if_true]

theorem mirror_residue (m i : Nat) (hi : i < width m) :
    (width m - 1 - i) % 10 = 9 - i % 10 := by
  unfold width at *
  omega

theorem source_symmetric (m i : Nat) (hi : i < width m) :
    source m i = source m (width m - 1 - i) := by
  have hj : width m - 1 - i < width m := by omega
  have hmod := mirror_residue m i hi
  have hr : i % 10 < 10 := Nat.mod_lt _ (by decide)
  simp only [source, hi, hj, if_true, hmod]
  unfold blockSource
  repeat first | omega | split

theorem source_admissible (m : Nat) (hm : 0 < m) :
    Admissible (width m) (source m) := by
  refine ⟨by unfold width; omega, ?_,
    (fun i _ => source_bounded m i), source_symmetric m, ?_⟩
  · simp [source, width, blockSource, show 0 < 10 * m by omega]
  · intro i hi heq
    unfold width at hi heq
    omega

theorem exact_pair_equation (m i : Nat) (hi : i < width m) :
    columnSum (normalized m) (width m) i = target m i := by
  have hj : width m - 1 - i < width m := by omega
  have hmod := mirror_residue m i hi
  have hr : i % 10 < 10 := Nat.mod_lt _ (by decide)
  simp only [columnSum, reflected, normalized, target, hi, hj, if_true, hmod]
  unfold blockDigits blockTarget
  repeat first | omega | split

theorem actual_update (m i : Nat) (hi : i < width m) :
    nextColumns (source m) (width m) i = target m i := by
  simp only [nextColumns, no_overflow, if_true, columnSum, reflected, actual_output]
  exact exact_pair_equation m i hi

theorem source_no_extremes (m i : Nat) (hi : i < width m) :
    source m i ≠ 0 ∧ source m i ≠ 18 := by
  simp only [source, hi, if_true]
  unfold blockSource
  repeat first | omega | split

#print axioms source_bounded
#print axioms normalized_bounded
#print axioms exact_column_equation
#print axioms actual_carry
#print axioms actual_output
#print axioms no_overflow
#print axioms actual_width
#print axioms mirror_residue
#print axioms source_symmetric
#print axioms source_admissible
#print axioms exact_pair_equation
#print axioms actual_update
#print axioms source_no_extremes

end RunBirths.RepeatedBirths
