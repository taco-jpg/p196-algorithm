import PopulationObstructions
import UnboundedBirths

/-!
Exact population growth in the actual simultaneous-birth family.
Every k,r gives zero source population of both extreme symbols and
successor populations count(0)=2r, count(18)=2k, hence total width-6.
The counts are over List.range of the complete physical width.
-/

namespace RunBirths.PopulationGrowth

open DecimalDigits FoldedDecimal UnboundedBirths PopulationObstructions

/-- Count all physical positions with the specified coefficient. -/
def indexedCount (v : Nat) (q : Nat → Nat) (L : Nat) : Nat :=
  (List.range L).countP (fun i => q i == v)

/-- This is exactly the full-word count used by the finite obstructions. -/
theorem indexedCount_eq_coefficientCount (v : Nat) (q : Nat → Nat) (L : Nat) :
    indexedCount v q L = coefficientCount v ((List.range L).map q) := by
  simp [indexedCount, coefficientCount, List.count_eq_countP,
    List.countP_map, Function.comp_def]

theorem indexedCount_congr (v L : Nat) (q t : Nat → Nat)
    (h : ∀ i, i < L → q i = t i) : indexedCount v q L = indexedCount v t L := by
  apply List.countP_congr
  intro i hi
  rw [h i (List.mem_range.mp hi)]

/-- A clipped interval count, proved by recursion on the physical width. -/
theorem count_interval (a b L : Nat) (hab : a ≤ b) :
    (List.range L).countP (fun i => decide (a ≤ i ∧ i < b)) =
      min L b - min L a := by
  induction L with
  | zero => simp
  | succ L ih =>
    rw [List.range_succ, List.countP_append, ih]
    by_cases ha : a ≤ L <;> by_cases hb : L < b
    all_goals simp [ha, hb]
    all_goals omega

/-- Disjoint sites contribute additively to the population. -/
theorem count_disjoint_or {α : Type} (p q : α → Bool) (xs : List α)
    (hd : ∀ x, x ∈ xs → ¬ (p x = true ∧ q x = true)) :
    xs.countP (fun x => p x || q x) = xs.countP p + xs.countP q := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    have hx := hd x (by simp)
    have ht : ∀ y, y ∈ xs → ¬ (p y = true ∧ q y = true) := by
      intro y hy
      exact hd y (by simp [hy])
    rw [List.countP_cons, List.countP_cons, List.countP_cons, ih ht]
    cases hp : p x <;> cases hq : q x <;> simp_all <;> omega

theorem source_zero_population (k r : Nat) :
    indexedCount 0 (source k r) (width k r) = 0 ∧
    indexedCount 18 (source k r) (width k r) = 0 := by
  constructor <;> apply List.countP_eq_zero.mpr
  · intro i hi
    have h := (source_no_extremes k r i (List.mem_range.mp hi)).1
    simpa using h
  · intro i hi
    have h := (source_no_extremes k r i (List.mem_range.mp hi)).2
    simpa using h

/-- The central band gives exactly 2r actual newborn zero columns. -/
theorem actual_zero_count (k r : Nat) :
    indexedCount 0 (nextColumns (source k r) (width k r)) (width k r) = 2 * r := by
  have he : indexedCount 0 (nextColumns (source k r) (width k r)) (width k r) =
      (List.range (width k r)).countP
        (fun i => decide (k + 3 ≤ i ∧ i < k + 2 * r + 3)) := by
    apply List.countP_congr
    intro i hi
    simpa using (exact_extreme_positions k r i (List.mem_range.mp hi)).1
  rw [he, count_interval _ _ _ (by omega)]
  unfold width
  omega

/-- The two exterior bands give exactly 2k actual newborn 18 columns. -/
theorem actual_eighteen_count (k r : Nat) :
    indexedCount 18 (nextColumns (source k r) (width k r)) (width k r) = 2 * k := by
  let p : Nat → Bool := fun i => decide (1 ≤ i ∧ i < k + 1)
  let q : Nat → Bool := fun i => decide
    (k + 2 * r + 5 ≤ i ∧ i < 2 * k + 2 * r + 5)
  have he : indexedCount 18 (nextColumns (source k r) (width k r)) (width k r) =
      (List.range (width k r)).countP (fun i => p i || q i) := by
    apply List.countP_congr
    intro i hi
    have h := (exact_extreme_positions k r i (List.mem_range.mp hi)).2
    simp only [Bool.or_eq_true, p, q, decide_eq_true_eq, beq_iff_eq]
    omega
  have hd : ∀ i, i ∈ List.range (width k r) → ¬ (p i = true ∧ q i = true) := by
    intro i _
    simp only [p, q, decide_eq_true_eq]
    omega
  rw [he, count_disjoint_or p q _ hd]
  change (List.range (width k r)).countP (fun i => decide (1 ≤ i ∧ i < k + 1)) +
    (List.range (width k r)).countP
      (fun i => decide (k + 2 * r + 5 ≤ i ∧ i < 2 * k + 2 * r + 5)) = 2 * k
  rw [count_interval _ _ _ (by omega), count_interval _ _ _ (by omega)]
  unfold width
  omega

/-- The target formula and actual next width give the same exact counts. -/
theorem target_population (k r : Nat) :
    indexedCount 0 (target k r) (width k r) = 2 * r ∧
    indexedCount 18 (target k r) (width k r) = 2 * k := by
  have he (v : Nat) : indexedCount v (nextColumns (source k r) (width k r))
      (width k r) = indexedCount v (target k r) (width k r) := by
    apply List.countP_congr
    intro i hi
    rw [actual_update k r i (List.mem_range.mp hi)]
  exact ⟨(he 0).symm.trans (actual_zero_count k r),
    (he 18).symm.trans (actual_eighteen_count k r)⟩

/-- Exactly six output columns are nonextreme, for every k and r. -/
theorem actual_total_count (k r : Nat) :
    indexedCount 0 (nextColumns (source k r) (width k r))
        (nextWidth (source k r) (width k r)) +
      indexedCount 18 (nextColumns (source k r) (width k r))
        (nextWidth (source k r) (width k r)) = width k r - 6 := by
  rw [actual_width, actual_zero_count, actual_eighteen_count]
  unfold width
  omega

/-- One step from an extreme-free admissible word has arbitrarily large
populations of both extreme symbols simultaneously. -/
theorem no_uniform_birth_bound (B : Nat) :
    ∃ L q, Admissible L q ∧
      indexedCount 0 q L = 0 ∧ indexedCount 18 q L = 0 ∧
      B < indexedCount 0 (nextColumns q L) (nextWidth q L) ∧
      B < indexedCount 18 (nextColumns q L) (nextWidth q L) := by
  refine ⟨width (B + 1) (B + 1), source (B + 1) (B + 1),
    source_admissible _ _, (source_zero_population _ _).1,
    (source_zero_population _ _).2, ?_, ?_⟩
  · rw [actual_width, actual_zero_count]
    omega
  · rw [actual_width, actual_eighteen_count]
    omega

/-- All exact populations occur in canonical decimal expansions of an
actual positive integer and its ordinary reverse-and-add successor. -/
theorem realized_population_formula (k r : Nat) :
    ∃ n d e, 0 < n ∧ Canonical n d (width k r) ∧
      Canonical (Lychrel196.step n) e (width k r) ∧
      indexedCount 0 (columnSum d (width k r)) (width k r) = 0 ∧
      indexedCount 18 (columnSum d (width k r)) (width k r) = 0 ∧
      indexedCount 0 (columnSum e (width k r)) (width k r) = 2 * r ∧
      indexedCount 18 (columnSum e (width k r)) (width k r) = 2 * k ∧
      indexedCount 0 (columnSum e (width k r)) (width k r) +
        indexedCount 18 (columnSum e (width k r)) (width k r) = width k r - 6 := by
  obtain ⟨n, d, e, hn, hc, hsource, he, htarget⟩ := numeric_family_realized k r
  have hs0 := (indexedCount_congr 0 _ _ _ hsource).trans (source_zero_population k r).1
  have hs18 := (indexedCount_congr 18 _ _ _ hsource).trans (source_zero_population k r).2
  have ht0 := (indexedCount_congr 0 _ _ _ htarget).trans (target_population k r).1
  have ht18 := (indexedCount_congr 18 _ _ _ htarget).trans (target_population k r).2
  refine ⟨n, d, e, hn, hc, he, hs0, hs18, ht0, ht18, ?_⟩
  rw [ht0, ht18]
  unfold width
  omega

/-- The two populations can independently exceed any prescribed bounds
in one genuine integer reverse-and-add step from an extreme-free input. -/
theorem simultaneous_integer_births_unbounded (B0 B18 : Nat) :
    ∃ n d e L, 0 < n ∧ Canonical n d L ∧ Canonical (Lychrel196.step n) e L ∧
      indexedCount 0 (columnSum d L) L = 0 ∧
      indexedCount 18 (columnSum d L) L = 0 ∧
      B0 < indexedCount 0 (columnSum e L) L ∧
      B18 < indexedCount 18 (columnSum e L) L ∧
      indexedCount 0 (columnSum e L) L + indexedCount 18 (columnSum e L) L = L - 6 := by
  obtain ⟨n, d, e, hn, hc, he, hs0, hs18, ht0, ht18, ht⟩ :=
    realized_population_formula (B18 + 1) (B0 + 1)
  refine ⟨n, d, e, width (B18 + 1) (B0 + 1), hn, hc, he, hs0, hs18, ?_, ?_, ht⟩
  · omega
  · omega

/-- Thus no uniform constant bounds the total number of newly appearing
extreme columns, even if the proposed bound is restricted to actual steps
whose input has neither extreme. Different physical widths are allowed. -/
theorem no_uniform_integer_total_bound :
    ¬ ∃ B : Nat, ∀ (n : Nat) (d e : Nat → Nat) (L M : Nat),
      0 < n → Canonical n d L → Canonical (Lychrel196.step n) e M →
      indexedCount 0 (columnSum d L) L = 0 →
      indexedCount 18 (columnSum d L) L = 0 →
      indexedCount 0 (columnSum e M) M + indexedCount 18 (columnSum e M) M ≤ B := by
  rintro ⟨B, hB⟩
  obtain ⟨n, d, e, L, hn, hc, he, hs0, hs18, ht0, ht18, _⟩ :=
    simultaneous_integer_births_unbounded B B
  have hb := hB n d e L L hn hc he hs0 hs18
  omega

#print axioms indexedCount_eq_coefficientCount
#print axioms indexedCount_congr
#print axioms count_interval
#print axioms count_disjoint_or
#print axioms source_zero_population
#print axioms actual_zero_count
#print axioms actual_eighteen_count
#print axioms target_population
#print axioms actual_total_count
#print axioms no_uniform_birth_bound
#print axioms realized_population_formula
#print axioms simultaneous_integer_births_unbounded
#print axioms no_uniform_integer_total_bound

end RunBirths.PopulationGrowth
