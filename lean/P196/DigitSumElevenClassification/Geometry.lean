import P196.DigitSumTenTermination.DigitGeometry

/-!
Exact folded digit mass and the sparse exterior profiles at digit sum eleven.
The profiles retain the ordinary canonical width and do not identify different
splits of a reflected pair. Only the exceptional width-nine outer profile is
resolved into its two ordinary integer seeds here.
-/

namespace DigitSumElevenClassification

open DecimalDigits DecimalMass LowDigitSumTermination

/-- A central digit and a single exterior mass at the two outer columns. -/
def outerColumns (m centerDigit outerMass i : Nat) : Nat :=
  if i = m then 2 * centerDigit
  else if i = 0 ∨ i = 2 * m then outerMass else 0

/-- Outer mass one and an additional pair adjacent to the center.
The outer condition is tested first, so this also has a fixed meaning at width three. -/
def nearColumns (m centerDigit nearMass i : Nat) : Nat :=
  if i = m then 2 * centerDigit
  else if i = 0 ∨ i = 2 * m then 1
  else if i + 1 = m ∨ i = m + 1 then nearMass else 0

/-- Each exterior pair is counted once in the lower half, with the middle
digit added once to recover the ordinary digit mass. -/
theorem folded_mass (d : Nat → Nat) (m : Nat) :
    wordSum (columnSum d (2 * m + 1)) m + d m =
      wordSum d (2 * m + 1) := by
  have hsplit := DecimalUnboundedMass.wordSum_split d (m + 1) m
  have hwidth : m + 1 + m = 2 * m + 1 := by omega
  rw [hwidth] at hsplit
  change wordSum d (2 * m + 1) =
    (wordSum d m + d m) + wordSum (fun i => d (m + 1 + i)) m at hsplit
  have hreflect : wordSum (reflected d (2 * m + 1)) m =
      wordSum (fun i => d (m + 1 + i)) m := by
    calc
      wordSum (reflected d (2 * m + 1)) m =
          wordSum (reflected (fun i => d (m + 1 + i)) m) m := by
        apply wordSum_congr
        intro i hi
        simp only [reflected]
        congr 1
        omega
      _ = wordSum (fun i => d (m + 1 + i)) m := wordSum_reflected _ _
  change wordSum (fun i => d i + reflected d (2 * m + 1) i) m + d m = _
  rw [wordSum_add, hreflect]
  omega

/-- A positive first coefficient and small total mass leave only an outer
concentration or an outer-plus-last concentration when the last is large. -/
theorem sparse_mass_profiles (q : Nat → Nat) (m s : Nat)
    (hm : 0 < m) (hpos : 0 < q 0) (hmass : wordSum q m = s + 1) :
    ((∀ i, i < m → q i ≤ s) ∧ q (m - 1) < s) ∨
    (∀ i, i < m → q i = if i = 0 then s + 1 else 0) ∨
    (2 ≤ m ∧ ∀ i, i < m →
      q i = if i = 0 then 1 else if i + 1 = m then s else 0) := by
  classical
  have hzeroBound := wordSum_single_le q m 0 (by omega)
  by_cases houter : q 0 = s + 1
  · right
    left
    intro i hi
    by_cases hz : i = 0
    · simpa only [hz, if_pos rfl] using houter
    · have hpair := wordSum_pair_le q m 0 i (by omega) hi (by omega)
      simp only [if_neg hz]
      omega
  have hsmall : ∀ i, i < m → q i ≤ s := by
    intro i hi
    by_cases hz : i = 0
    · subst i
      omega
    · have hpair := wordSum_pair_le q m 0 i (by omega) hi (by omega)
      omega
  by_cases hlast : q (m - 1) < s
  · exact Or.inl ⟨hsmall, hlast⟩
  have hm2 : 2 ≤ m := by
    by_cases hm1 : m = 1
    · subst m
      simp only [wordSum, Nat.zero_add] at hmass
      omega
    · omega
  have hpair := wordSum_pair_le q m 0 (m - 1)
    (by omega) (by omega) (by omega)
  have hzero : q 0 = 1 := by omega
  have hlastEq : q (m - 1) = s := by omega
  right
  right
  refine ⟨hm2, ?_⟩
  intro i hi
  by_cases hz : i = 0
  · simpa only [hz, if_pos rfl] using hzero
  · by_cases hn : i + 1 = m
    · have heq : i = m - 1 := by omega
      simp only [if_neg hz, if_pos hn]
      simpa only [heq] using hlastEq
    · have htriple := wordSum_triple_le q m 0 (m - 1) i
        (by omega) (by omega) hi (by omega) (by omega) (by omega)
      simp only [if_neg hz, if_neg hn]
      omega

/-- An upper bound on the lower half of the pair word also holds on its
reflected half, excluding only the center. -/
theorem exterior_le_of_half (d : Nat → Nat) (m bound : Nat)
    (hhalf : ∀ i, i < m → columnSum d (2 * m + 1) i ≤ bound) :
    ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ bound := by
  intro i hi hic
  by_cases hlo : i < m
  · exact hhalf i hlo
  · rw [columnSum_symmetric d (2 * m + 1) i hi]
    exact hhalf _ (by omega)

/-- The two center-adjacent columns have the same pair coefficient. -/
theorem near_le_of_half_last (d : Nat → Nat) (m bound : Nat) (hm : 0 < m)
    (hlast : columnSum d (2 * m + 1) (m - 1) ≤ bound) :
    ∀ i, i < 2 * m + 1 → (i + 1 = m ∨ i = m + 1) →
      columnSum d (2 * m + 1) i ≤ bound := by
  intro i hi hnear
  rcases hnear with hlow | hhigh
  · have heq : i = m - 1 := by omega
    simpa only [heq] using hlast
  · rw [columnSum_symmetric d (2 * m + 1) i hi]
    have heq : 2 * m + 1 - 1 - i = m - 1 := by omega
    simpa only [heq] using hlast

/-- Lower-half equality, symmetry, and the center determine the full pair word. -/
theorem columns_eq_of_half (d q : Nat → Nat) (m : Nat)
    (hcenter : q m = 2 * d m)
    (hsym : ∀ i, i < 2 * m + 1 → q i = q (2 * m + 1 - 1 - i))
    (hhalf : ∀ i, i < m → columnSum d (2 * m + 1) i = q i) :
    ∀ i, i < 2 * m + 1 → columnSum d (2 * m + 1) i = q i := by
  intro i hi
  by_cases hic : i = m
  · subst i
    have heq : 2 * m + 1 - 1 - m = m := by omega
    simp only [columnSum, reflected, heq]
    omega
  · by_cases hlo : i < m
    · exact hhalf i hlo
    · rw [columnSum_symmetric d (2 * m + 1) i hi, hsym i hi]
      exact hhalf _ (by omega)

theorem outerColumns_symmetric (m c a i : Nat) (hi : i < 2 * m + 1) :
    outerColumns m c a i = outerColumns m c a (2 * m + 1 - 1 - i) := by
  have hc : (2 * m + 1 - 1 - i = m) ↔ i = m := by omega
  have he : (2 * m + 1 - 1 - i = 0 ∨
      2 * m + 1 - 1 - i = 2 * m) ↔ (i = 0 ∨ i = 2 * m) := by omega
  simp only [outerColumns, hc, he]

theorem nearColumns_symmetric (m c b i : Nat) (hi : i < 2 * m + 1) :
    nearColumns m c b i = nearColumns m c b (2 * m + 1 - 1 - i) := by
  have hc : (2 * m + 1 - 1 - i = m) ↔ i = m := by omega
  have he : (2 * m + 1 - 1 - i = 0 ∨
      2 * m + 1 - 1 - i = 2 * m) ↔ (i = 0 ∨ i = 2 * m) := by omega
  have hn : (2 * m + 1 - 1 - i + 1 = m ∨
      2 * m + 1 - 1 - i = m + 1) ↔ (i + 1 = m ∨ i = m + 1) := by omega
  simp only [nearColumns, hc, he, hn]

theorem outer_columns_of_half (d : Nat → Nat) (m c a : Nat) (hmid : d m = c)
    (hhalf : ∀ i, i < m →
      columnSum d (2 * m + 1) i = if i = 0 then a else 0) :
    ∀ i, i < 2 * m + 1 → columnSum d (2 * m + 1) i = outerColumns m c a i := by
  apply columns_eq_of_half d (outerColumns m c a) m
  · simp [outerColumns, hmid]
  · exact outerColumns_symmetric m c a
  · intro i hi
    have hic : i ≠ m := by omega
    have hie : i ≠ 2 * m := by omega
    simpa only [outerColumns, if_neg hic, hie, or_false] using hhalf i hi

theorem near_columns_of_half (d : Nat → Nat) (m c b : Nat) (hmid : d m = c)
    (hhalf : ∀ i, i < m → columnSum d (2 * m + 1) i =
      if i = 0 then 1 else if i + 1 = m then b else 0) :
    ∀ i, i < 2 * m + 1 → columnSum d (2 * m + 1) i = nearColumns m c b i := by
  apply columns_eq_of_half d (nearColumns m c b) m
  · simp [nearColumns, hmid]
  · exact nearColumns_symmetric m c b
  · intro i hi
    have hic : i ≠ m := by omega
    have hie : i ≠ 2 * m := by omega
    have hin : i ≠ m + 1 := by omega
    simpa only [nearColumns, if_neg hic, hie, hin, or_false] using hhalf i hi

/-- At middle digit eight and total mass eleven, failure of the refined
three-step bounds leaves exactly outer mass three or outer one with near two. -/
theorem center_eight_profiles (d : Nat → Nat) (m : Nat) (hm : 0 < m)
    (hlead : 0 < d (2 * m)) (hmass : wordSum d (2 * m + 1) = 11)
    (hmid : d m = 8) :
    ((∀ i, i < 2 * m + 1 → i ≠ m → columnSum d (2 * m + 1) i ≤ 2) ∧
      (∀ i, i < 2 * m + 1 → (i + 1 = m ∨ i = m + 1) →
        columnSum d (2 * m + 1) i ≤ 1)) ∨
    (∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = outerColumns m 8 3 i) ∨
    (2 ≤ m ∧ ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = nearColumns m 8 2 i) := by
  have hfold := folded_mass d m
  have hmassq : wordSum (columnSum d (2 * m + 1)) m = 2 + 1 := by omega
  have hpos : 0 < columnSum d (2 * m + 1) 0 := by
    simp only [columnSum, reflected, Nat.sub_zero]
    have heq : 2 * m + 1 - 1 = 2 * m := by omega
    rw [heq]
    omega
  obtain heasy | houter | hnear :=
    sparse_mass_profiles (columnSum d (2 * m + 1)) m 2 hm hpos hmassq
  · left
    refine ⟨exterior_le_of_half d m 2 heasy.1, ?_⟩
    apply near_le_of_half_last d m 1 hm
    omega
  · right
    left
    exact outer_columns_of_half d m 8 3 hmid houter
  · right
    right
    exact ⟨hnear.1, near_columns_of_half d m 8 2 hmid hnear.2⟩

/-- At middle digit nine and total mass eleven, failure of the refined
four-step bounds leaves exactly outer mass two or outer one with near one. -/
theorem center_nine_profiles (d : Nat → Nat) (m : Nat) (hm : 0 < m)
    (hlead : 0 < d (2 * m)) (hmass : wordSum d (2 * m + 1) = 11)
    (hmid : d m = 9) :
    ((∀ i, i < 2 * m + 1 → i ≠ m → columnSum d (2 * m + 1) i ≤ 1) ∧
      (∀ i, i < 2 * m + 1 → (i + 1 = m ∨ i = m + 1) →
        columnSum d (2 * m + 1) i = 0)) ∨
    (∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = outerColumns m 9 2 i) ∨
    (2 ≤ m ∧ ∀ i, i < 2 * m + 1 →
      columnSum d (2 * m + 1) i = nearColumns m 9 1 i) := by
  have hfold := folded_mass d m
  have hmassq : wordSum (columnSum d (2 * m + 1)) m = 1 + 1 := by omega
  have hpos : 0 < columnSum d (2 * m + 1) 0 := by
    simp only [columnSum, reflected, Nat.sub_zero]
    have heq : 2 * m + 1 - 1 = 2 * m := by omega
    rw [heq]
    omega
  obtain heasy | houter | hnear :=
    sparse_mass_profiles (columnSum d (2 * m + 1)) m 1 hm hpos hmassq
  · left
    refine ⟨exterior_le_of_half d m 1 heasy.1, ?_⟩
    have hlast : columnSum d (2 * m + 1) (m - 1) ≤ 0 := by omega
    have hnear := near_le_of_half_last d m 0 hm hlast
    intro i hi hn
    have h := hnear i hi hn
    omega
  · right
    left
    exact outer_columns_of_half d m 9 2 hmid houter
  · right
    right
    exact ⟨hnear.1, near_columns_of_half d m 9 1 hmid hnear.2⟩

/-- The width-nine outer-two profile represents only the palindromic seed
100090001 and the zero-units seed 200090000. -/
theorem width_nine_outer_two (n : Nat) (d : Nat → Nat)
    (hcan : Canonical n d 9)
    (hcols : ∀ i, i < 9 → columnSum d 9 i = outerColumns 4 9 2 i) :
    n = 100090001 ∨ n = 200090000 := by
  have h0 := hcols 0 (by decide)
  have h1 := hcols 1 (by decide)
  have h2 := hcols 2 (by decide)
  have h3 := hcols 3 (by decide)
  have h4 := hcols 4 (by decide)
  simp [columnSum, reflected, outerColumns] at h0 h1 h2 h3 h4
  have hlead : 0 < d 8 := by simpa using hcan.2.2.1
  have hv := hcan.2.2.2
  simp [value] at hv
  have hcases : d 8 = 1 ∨ d 8 = 2 := by omega
  rcases hcases with hone | htwo
  · left
    omega
  · right
    omega

end DigitSumElevenClassification
