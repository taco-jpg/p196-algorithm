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

/-- One exact source/target block at any of the m physical block positions. -/
theorem actual_block_update (m j r : Nat) (hj : j < m) (hr : r < 10) :
    source m (10 * j + r) = blockSource r ∧
      nextColumns (source m) (width m) (10 * j + r) = blockTarget r := by
  have hi : 10 * j + r < width m := by unfold width; omega
  have hmod : (10 * j + r) % 10 = r := by omega
  rw [actual_update m _ hi]
  simp [source, target, hi, hmod]

/-- All and only the stated residue classes contain the newly born extremes. -/
theorem exact_extreme_positions (m i : Nat) (hi : i < width m) :
    (nextColumns (source m) (width m) i = 0 ↔ i % 10 = 4 ∨ i % 10 = 5) ∧
    (nextColumns (source m) (width m) i = 18 ↔ i % 10 = 1 ∨ i % 10 = 8) := by
  have hr : i % 10 < 10 := Nat.mod_lt _ (by decide)
  rw [actual_update m i hi]
  simp only [target, hi, if_true]
  unfold blockTarget
  repeat first | omega | split

/-- A length-two maximal zero run with both physical neighbors present. -/
def IsolatedZeroPair (q : Nat → Nat) (L a : Nat) : Prop :=
  0 < a ∧ a + 2 < L ∧ q (a - 1) ≠ 0 ∧
    q a = 0 ∧ q (a + 1) = 0 ∧ q (a + 2) ≠ 0

/-- A singleton maximal 18 run with both physical neighbors present. -/
def IsolatedEighteen (q : Nat → Nat) (L a : Nat) : Prop :=
  0 < a ∧ a + 1 < L ∧ q (a - 1) ≠ 18 ∧
    q a = 18 ∧ q (a + 1) ≠ 18

theorem new_zero_run (m j : Nat) (hj : j < m) :
    IsolatedZeroPair (nextColumns (source m) (width m)) (width m) (10 * j + 4) := by
  have h3 := (actual_block_update m j 3 hj (by decide)).2
  have h4 := (actual_block_update m j 4 hj (by decide)).2
  have h5 := (actual_block_update m j 5 hj (by decide)).2
  have h6 := (actual_block_update m j 6 hj (by decide)).2
  simp [blockTarget] at h3 h4 h5 h6
  have hb : 10 * j + 6 < width m := by unfold width; omega
  unfold IsolatedZeroPair
  have hp : 10 * j + 4 - 1 = 10 * j + 3 := by omega
  rw [hp]
  refine ⟨by omega, by omega, by omega, h4, ?_, ?_⟩
  · simpa only [Nat.add_assoc] using h5
  · have hn : nextColumns (source m) (width m) (10 * j + 6) ≠ 0 := by omega
    simpa only [Nat.add_assoc] using hn

theorem new_eighteen_left (m j : Nat) (hj : j < m) :
    IsolatedEighteen (nextColumns (source m) (width m)) (width m) (10 * j + 1) := by
  have h0 := (actual_block_update m j 0 hj (by decide)).2
  have h1 := (actual_block_update m j 1 hj (by decide)).2
  have h2 := (actual_block_update m j 2 hj (by decide)).2
  simp [blockTarget] at h0 h1 h2
  have hb : 10 * j + 2 < width m := by unfold width; omega
  unfold IsolatedEighteen
  have hp : 10 * j + 1 - 1 = 10 * j + 0 := by omega
  rw [hp]
  simp only [Nat.add_zero]
  refine ⟨by omega, by omega, by omega, h1, ?_⟩
  have hn : nextColumns (source m) (width m) (10 * j + 2) ≠ 18 := by omega
  simpa only [Nat.add_assoc] using hn

theorem new_eighteen_right (m j : Nat) (hj : j < m) :
    IsolatedEighteen (nextColumns (source m) (width m)) (width m) (10 * j + 8) := by
  have h7 := (actual_block_update m j 7 hj (by decide)).2
  have h8 := (actual_block_update m j 8 hj (by decide)).2
  have h9 := (actual_block_update m j 9 hj (by decide)).2
  simp [blockTarget] at h7 h8 h9
  have hb : 10 * j + 9 < width m := by unfold width; omega
  unfold IsolatedEighteen
  have hp : 10 * j + 8 - 1 = 10 * j + 7 := by omega
  rw [hp]
  refine ⟨by omega, by omega, by omega, h8, ?_⟩
  have hn : nextColumns (source m) (width m) (10 * j + 9) ≠ 18 := by omega
  simpa only [Nat.add_assoc] using hn

/-- Enumerate both 18 singletons of each block in physical order. -/
def eighteenStart (k : Nat) : Nat :=
  10 * (k / 2) + if k % 2 = 0 then 1 else 8

theorem eighteenStart_injective : ∀ i j, eighteenStart i = eighteenStart j → i = j := by
  intro i j hij
  unfold eighteenStart at hij
  split at hij <;> split at hij <;> omega

theorem new_eighteen_run (m k : Nat) (hk : k < 2 * m) :
    IsolatedEighteen (nextColumns (source m) (width m)) (width m) (eighteenStart k) := by
  have hj : k / 2 < m := by omega
  by_cases h : k % 2 = 0
  · simpa only [eighteenStart, h, if_true] using new_eighteen_left m (k / 2) hj
  · simpa only [eighteenStart, h, if_false] using new_eighteen_right m (k / 2) hj

/-- This family has positive finite decimal realizations. -/
theorem family_realized (m : Nat) (hm : 0 < m) :
    ∃ n d, 0 < n ∧ Canonical n d (width m) ∧
      (∀ i, i < width m → columnSum d (width m) i = source m i) := by
  obtain ⟨hL, ho, hb, hs, hp⟩ := source_admissible m hm
  exact valid_word_realizable (source m) (width m) hL ho hb hs hp

/-- The target is the column word of the actual numeric reverse-and-add step. -/
theorem numeric_family_realized (m : Nat) (hm : 0 < m) :
    ∃ n d e, 0 < n ∧ Canonical n d (width m) ∧
      (∀ i, i < width m → columnSum d (width m) i = source m i) ∧
      Canonical (Lychrel196.step n) e (width m) ∧
      (∀ i, i < width m → columnSum e (width m) i = target m i) := by
  obtain ⟨n, d, hp, hc, hr⟩ := family_realized m hm
  obtain ⟨e, he, hn⟩ := representation_next n d (source m) (width m) hc hr
  rw [actual_width] at he hn
  refine ⟨n, d, e, hp, hc, hr, he, ?_⟩
  intro i hi
  exact (hn i hi).trans (actual_update m i hi)

/-- No uniform finite bound on the number of separate newly created runs
of either extreme exists, even in a single no-overflow step from a word
with neither extreme. The two injections enumerate B+1 zero pairs and
2*(B+1) distinct 18 singleton runs, each with explicit nonextreme neighbors. -/
theorem arbitrarily_many_separate_birth_runs (B : Nat) :
    ∃ (L : Nat) (q : Nat → Nat)
      (z : Fin (B + 1) → Nat) (e : Fin (2 * (B + 1)) → Nat),
      Admissible L q ∧ carry q L = 0 ∧
      (∀ i, i < L → q i ≠ 0 ∧ q i ≠ 18) ∧
      (∀ i j, z i = z j → i = j) ∧ (∀ i j, e i = e j → i = j) ∧
      (∀ j, IsolatedZeroPair (nextColumns q L) L (z j)) ∧
      (∀ j, IsolatedEighteen (nextColumns q L) L (e j)) := by
  refine ⟨width (B + 1), source (B + 1), (fun j => 10 * j.val + 4),
    (fun j => eighteenStart j.val), source_admissible _ (by omega),
    no_overflow _, source_no_extremes _, ?_, ?_, ?_, ?_⟩
  · intro i j hij
    change 10 * i.val + 4 = 10 * j.val + 4 at hij
    apply Fin.ext
    omega
  · intro i j hij
    apply Fin.ext
    exact eighteenStart_injective _ _ hij
  · intro j
    exact new_zero_run (B + 1) j.val j.isLt
  · intro j
    exact new_eighteen_run (B + 1) j.val j.isLt

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
#print axioms actual_block_update
#print axioms exact_extreme_positions
#print axioms new_zero_run
#print axioms new_eighteen_left
#print axioms new_eighteen_right
#print axioms eighteenStart_injective
#print axioms new_eighteen_run
#print axioms family_realized
#print axioms numeric_family_realized
#print axioms arbitrarily_many_separate_birth_runs

end RunBirths.RepeatedBirths
