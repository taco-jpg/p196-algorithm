import RawSymmetryObstruction

/-!
Exact coefficient response for any finite decimal word and any cut pattern.
The actual normalized output is explicitly zero extended: the final carry
occupies exactly column L, not every column at or beyond L.
-/

namespace Agent107.SeamCoefficients

open DecimalDigits RawSymmetryObstruction

/-- Actual emitted digits, the single terminal carry slot, then zeros. -/
def actualCoeff (q : Nat → Nat) (L i : Nat) : Int :=
  if i < L then (output q i : Int)
  else if i = L then (carry q L : Int) else 0

/-- Finite actual-minus-isolated outgoing-carry word. -/
def defect (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat) : Int :=
  supported (seamDefect q cut) L i

/-- Coefficients of (x-10) times the finite carry-defect word. -/
def correction (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat) : Int :=
  previous (defect q cut L) i - 10 * defect q cut L i

theorem actualCoeff_lt (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    actualCoeff q L i = (output q i : Int) := by
  simp [actualCoeff, hi]

theorem actualCoeff_terminal (q : Nat → Nat) (L : Nat) :
    actualCoeff q L L = (carry q L : Int) := by
  simp [actualCoeff]

theorem actualCoeff_zero_of_gt (q : Nat → Nat) (L i : Nat) (hi : L < i) :
    actualCoeff q L i = 0 := by
  simp [actualCoeff, show ¬ i < L by omega, show i ≠ L by omega]

theorem actualCoeff_eq_extended (q : Nat → Nat) (L i : Nat) (hi : i ≤ L) :
    actualCoeff q L i = (extended q L i : Int) := by
  by_cases hlt : i < L
  · simp [actualCoeff, extended, hlt]
  · have heq : i = L := by omega
    subst i
    simp [actualCoeff, extended]

theorem defect_lt (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hi : i < L) : defect q cut L i = seamDefect q cut i := by
  exact supported_lt _ L i hi

theorem defect_zero_of_ge (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hi : L ≤ i) : defect q cut L i = 0 := by
  simp [defect, supported, show ¬ i < L by omega]

/-- The ordinary column equations determine every coefficient, including
the terminal carry and the zero tail. No coefficient bound is assumed. -/
theorem actualCoeff_eq_raw (q : Nat → Nat) (L i : Nat) :
    actualCoeff q L i =
      raw (fun j => (q j : Int)) (fun j => (carry q (j + 1) : Int)) L i := by
  by_cases hi : i < L
  · have hc := column_equation q i
    cases i with
    | zero =>
        simp only [actualCoeff, if_pos hi, raw, supported_lt _ L 0 hi, previous]
        simp only [carry] at hc
        omega
    | succ i =>
        have hip : i < L := by omega
        simp only [actualCoeff, if_pos hi, raw, supported_lt _ L (i + 1) hi,
          previous, supported_lt _ L i hip]
        omega
  · by_cases heq : i = L
    · subst i
      cases L with
      | zero => simp [actualCoeff, raw, supported, previous, carry]
      | succ L =>
          simp [actualCoeff, raw, supported, previous]
    · have hgt : L < i := by omega
      cases i with
      | zero => omega
      | succ i =>
          have hip : ¬ i < L := by omega
          simp [actualCoeff, raw, supported, previous, hi, heq, hip]

/-- The full arbitrary-cut identity D = E + (x-10)K, coefficientwise.
Here E is the actual placed sum of isolated-block normalizations. -/
theorem coefficient_response (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat) :
    actualCoeff q L i = resetRaw q cut L i + correction q cut L i := by
  rw [actualCoeff_eq_raw]
  cases i with
  | zero =>
      simp only [resetRaw, raw, correction, defect, previous]
      by_cases hi : 0 < L
      · simp only [supported, if_pos hi, seamDefect]
        omega
      · simp only [supported, if_neg hi]
        omega
  | succ i =>
      simp only [resetRaw, raw, correction, defect, previous]
      by_cases hi : i + 1 < L <;> by_cases hp : i < L <;>
        simp only [supported, hi, hp, if_true, if_false, seamDefect] <;> omega

theorem defect_nonnegative (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat) :
    0 ≤ defect q cut L i := by
  by_cases hi : i < L
  · rw [defect_lt q cut L i hi]
    have h := resetOut_le_actual q cut i
    unfold seamDefect
    omega
  · rw [defect_zero_of_ge q cut L i (by omega)]
    omega

theorem defect_le_one (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) : defect q cut L i ≤ 1 := by
  by_cases hi : i < L
  · rw [defect_lt q cut L i hi]
    have h := carry_bounded q L hq (i + 1) (by omega)
    unfold seamDefect
    omega
  · rw [defect_zero_of_ge q cut L i (by omega)]
    omega

theorem defect_binary (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) :
    defect q cut L i = 0 ∨ defect q cut L i = 1 := by
  have hlo := defect_nonnegative q cut L i
  have hhi := defect_le_one q cut L i hq
  omega

/-- Vanishing on the finite original word implies vanishing everywhere. -/
theorem defect_zero_of_no_activity (q : Nat → Nat) (cut : Nat → Bool) (L : Nat)
    (hz : ∀ i, i < L → seamDefect q cut i = 0) :
    ∀ i, defect q cut L i = 0 := by
  intro i
  by_cases hi : i < L
  · rw [defect_lt q cut L i hi, hz i hi]
  · exact defect_zero_of_ge q cut L i (by omega)

theorem coefficients_agree_of_no_activity (q : Nat → Nat) (cut : Nat → Bool)
    (L : Nat) (hz : ∀ i, i < L → seamDefect q cut i = 0) :
    ∀ i, actualCoeff q L i = resetRaw q cut L i := by
  have hzero := defect_zero_of_no_activity q cut L hz
  intro i
  rw [coefficient_response]
  cases i <;> simp [correction, previous, hzero]

/-- Equality of the actual and raw coefficients forces each carry defect
to vanish, by induction from the left boundary. -/
theorem no_activity_of_coefficients_agree (q : Nat → Nat) (cut : Nat → Bool)
    (L : Nat) (heq : ∀ i, i < L → actualCoeff q L i = resetRaw q cut L i) :
    ∀ i, i < L → seamDefect q cut i = 0 := by
  intro i
  induction i with
  | zero =>
      intro hi
      have hr := coefficient_response q cut L 0
      have he := heq 0 hi
      simp only [correction, previous, defect_lt q cut L 0 hi] at hr
      omega
  | succ i ih =>
      intro hi
      have hp := ih (by omega)
      have hr := coefficient_response q cut L (i + 1)
      have he := heq (i + 1) hi
      simp only [correction, previous, defect_lt q cut L (i + 1) hi,
        defect_lt q cut L i (by omega), hp] at hr
      omega

theorem no_activity_iff_coefficients_agree (q : Nat → Nat) (cut : Nat → Bool)
    (L : Nat) :
    (∀ i, i < L → seamDefect q cut i = 0) ↔
      (∀ i, actualCoeff q L i = resetRaw q cut L i) := by
  constructor
  · exact coefficients_agree_of_no_activity q cut L
  · intro heq
    exact no_activity_of_coefficients_agree q cut L (fun i _ => heq i)

end Agent107.SeamCoefficients
