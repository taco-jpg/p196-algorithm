import P196.Drafts.Agent106RunBirths.PopulationGrowth

/-!
A finite source set controls the mass of a bounded nonnegative profile when
every positive output coefficient has a positive source within distance t.
The weighted neighborhood sum is estimated by induction on the source width.
The existing clipped interval count handles both the zero boundary and an
arbitrary output summation width.
-/

set_option autoImplicit false

namespace SparseProfileGrowth

open DecimalMass

private theorem indicator_sum (p : Nat → Bool) (K : Nat) :
    wordSum (fun i => if p i then 1 else 0) K =
      (List.range K).countP p := by
  induction K with
  | zero => simp [wordSum]
  | succ K ih =>
    rw [wordSum, ih, List.range_succ, List.countP_append, List.countP_singleton]

private theorem neighborhood_sum_le (a j t K : Nat) :
    wordSum (fun i => if j ≤ i + t ∧ i ≤ j + t then a else 0) K ≤
      (2 * t + 1) * a := by
  let p : Nat → Bool := fun i => decide (j - t ≤ i ∧ i < j + t + 1)
  have he :
      wordSum (fun i => if j ≤ i + t ∧ i ≤ j + t then a else 0) K =
        wordSum (fun i => a * (if p i then 1 else 0)) K := by
    apply wordSum_congr
    intro i _
    by_cases hi : j ≤ i + t ∧ i ≤ j + t
    · have hp : j - t ≤ i ∧ i < j + t + 1 := by omega
      simp [p, hi, hp]
    · have hp : ¬ (j - t ≤ i ∧ i < j + t + 1) := by omega
      simp [p, hi, hp]
  rw [he, wordSum_mul, indicator_sum]
  have hcount : (List.range K).countP p ≤ 2 * t + 1 := by
    change (List.range K).countP
      (fun i => decide (j - t ≤ i ∧ i < j + t + 1)) ≤ 2 * t + 1
    rw [RunBirths.PopulationGrowth.count_interval _ _ _ (by omega)]
    omega
  simpa only [Nat.mul_comm] using Nat.mul_le_mul_left a hcount

private def cone (f : Nat → Nat) (L t i : Nat) : Nat :=
  wordSum (fun j => if j ≤ i + t ∧ i ≤ j + t then f j else 0) L

private theorem cone_sum_le (f : Nat → Nat) (L K t : Nat) :
    wordSum (cone f L t) K ≤ (2 * t + 1) * wordSum f L := by
  induction L with
  | zero =>
    change wordSum (fun _ => 0) K ≤ 0
    simpa only [wordSum_zero] using (Nat.le_refl 0)
  | succ L ih =>
    have hsplit :
        wordSum (cone f (L + 1) t) K =
          wordSum (cone f L t) K +
            wordSum (fun i => if L ≤ i + t ∧ i ≤ L + t then f L else 0) K := by
      change wordSum (fun i => cone f L t i +
        (if L ≤ i + t ∧ i ≤ L + t then f L else 0)) K = _
      exact wordSum_add _ _ K
    calc
      wordSum (cone f (L + 1) t) K =
          wordSum (cone f L t) K +
            wordSum (fun i => if L ≤ i + t ∧ i ≤ L + t then f L else 0) K := hsplit
      _ ≤ (2 * t + 1) * wordSum f L + (2 * t + 1) * f L :=
        Nat.add_le_add ih (neighborhood_sum_le (f L) L t K)
      _ = (2 * t + 1) * wordSum f (L + 1) := by
        rw [wordSum, Nat.mul_add]

/-- Bounded output coefficients with positive sources at distance at most t
have mass at most M times the source mass times the neighborhood size. -/
theorem mass_le_of_positive_origin (f g : Nat → Nat) (L K t M : Nat)
    (hg : ∀ i, i < K → g i ≤ M)
    (ho : ∀ i, i < K → 0 < g i →
      ∃ j, j < L ∧ 0 < f j ∧ j ≤ i + t ∧ i ≤ j + t) :
    wordSum g K ≤ M * (2 * t + 1) * wordSum f L := by
  have hpoint : ∀ i, i < K → g i ≤ M * cone f L t i := by
    intro i hi
    by_cases hz : g i = 0
    · simp [hz]
    · obtain ⟨j, hj, hfj, hleft, hright⟩ := ho i hi (by omega)
      have hcone : 1 ≤ cone f L t i := by
        change 1 ≤ wordSum
          (fun j => if j ≤ i + t ∧ i ≤ j + t then f j else 0) L
        apply DecimalZeroGap.interval_length_le_mass _ L j 1 (by omega)
        intro k hk hk'
        have hkj : k = j := by omega
        subst k
        simpa [hleft, hright] using hfj
      exact Nat.le_trans (hg i hi)
        (by simpa only [Nat.mul_one] using Nat.mul_le_mul_left M hcone)
  have hgap :
      wordSum g K + wordSum (fun i => M * cone f L t i - g i) K =
        wordSum (fun i => M * cone f L t i) K := by
    rw [← wordSum_add]
    apply wordSum_congr
    intro i hi
    exact Nat.add_sub_of_le (hpoint i hi)
  calc
    wordSum g K ≤
        wordSum g K + wordSum (fun i => M * cone f L t i - g i) K :=
      Nat.le_add_right _ _
    _ = wordSum (fun i => M * cone f L t i) K := hgap
    _ = M * wordSum (cone f L t) K := wordSum_mul _ K M
    _ ≤ M * ((2 * t + 1) * wordSum f L) :=
      Nat.mul_le_mul_left M (cone_sum_le f L K t)
    _ = M * (2 * t + 1) * wordSum f L := (Nat.mul_assoc _ _ _).symm

end SparseProfileGrowth

#print axioms SparseProfileGrowth.mass_le_of_positive_origin
