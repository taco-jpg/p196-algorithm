import P196.Agent8CommonOverflowDefect.RawSymmetryObstruction

/-!
Exact mass loss for the actual reset-carry construction attached to an arbitrary
cut function.  The terminal isolated carry is included in the raw mass.  No
symmetry, regular spacing of cuts, or bound on the generic input word is used.
-/

namespace Agent107.SeamMass

open DecimalDigits DecimalMass RawSymmetryObstruction Lychrel196

/-- Integer sum over the columns `0, ..., L - 1`. -/
def intSum (f : Nat → Int) : Nat → Int
  | 0 => 0
  | L + 1 => intSum f L + f L

/-- Summing the actual raw column equations retains the terminal isolated
carry and counts every isolated outgoing carry exactly once. -/
theorem raw_mass_balance (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    wordSum (rawCoeff q cut) L + prevNat (resetOut q cut) L +
      9 * wordSum (resetOut q cut) L = wordSum q L := by
  induction L with
  | zero => simp [wordSum, prevNat]
  | succ L ih =>
      have hcol := raw_column_equation q cut L
      simp only [wordSum, prevNat]
      omega

/-- The total seam defect is the difference of the actual and isolated
outgoing-carry counts. -/
theorem defect_sum_balance (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    intSum (seamDefect q cut) L =
      (carryCount q L : Int) - (wordSum (resetOut q cut) L : Int) := by
  induction L with
  | zero => simp [intSum, carryCount, wordSum]
  | succ L ih =>
      simp only [intSum, carryCount, wordSum, seamDefect, Int.natCast_add] at ih ⊢
      omega

/-- Exact generic normalized mass response for every cut function. -/
theorem normalized_seam_mass (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    ((wordSum (output q) L + carry q L : Nat) : Int) +
      9 * intSum (seamDefect q cut) L =
        ((wordSum (rawCoeff q cut) L + prevNat (resetOut q cut) L : Nat) : Int) := by
  have hraw := raw_mass_balance q cut L
  have hactual := wordSum_output q L
  have hdefect := defect_sum_balance q cut L
  omega

/-- The actual numeric reverse-and-add step, including its final carry, has
exactly the ordinary digit sum used in the mass formula. -/
theorem actual_step_mass (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    wordSum (output (columnSum d L)) L + carry (columnSum d L) L =
      digitSum (step n) := by
  have hstep := digitSum_step_balance d L hc.2.1 (Or.inr hc.2.2.1)
  have hactual := wordSum_output (columnSum d L) L
  have hcolumns := wordSum_columns d L
  have hvalue := digitSum_value d L hc.2.1
  rw [hc.2.2.2] at hstep hvalue
  omega

/-- Arbitrary-partition mass identity for an ordinary canonical decimal
input.  The correction is nine times the total actual seam carry defect. -/
theorem actual_step_seam_mass (n : Nat) (d : Nat → Nat) (L : Nat)
    (cut : Nat → Bool) (hc : Canonical n d L) :
    (digitSum (step n) : Int) +
      9 * intSum (seamDefect (columnSum d L) cut) L =
        ((wordSum (rawCoeff (columnSum d L) cut) L +
          prevNat (resetOut (columnSum d L) cut) L : Nat) : Int) := by
  have h := normalized_seam_mass (columnSum d L) cut L
  rw [actual_step_mass n d L hc] at h
  exact h

/-- Resetting at a cut can only remove carries. -/
theorem seamDefect_nonnegative (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    0 ≤ seamDefect q cut i := by
  have h := resetOut_le_actual q cut i
  unfold seamDefect
  omega

theorem intSum_nonnegative (f : Nat → Int) (L : Nat)
    (hf : ∀ i, i < L → 0 ≤ f i) : 0 ≤ intSum f L := by
  induction L with
  | zero => simp [intSum]
  | succ L ih =>
      have hp := ih (fun i hi => hf i (by omega))
      have hl := hf L (by omega)
      simp only [intSum]
      omega

theorem intSum_zero_iff (f : Nat → Int) (L : Nat)
    (hf : ∀ i, i < L → 0 ≤ f i) :
    intSum f L = 0 ↔ ∀ i, i < L → f i = 0 := by
  induction L with
  | zero => simp [intSum]
  | succ L ih =>
      have hp := intSum_nonnegative f L (fun i hi => hf i (by omega))
      have hl := hf L (by omega)
      have hz : intSum f (L + 1) = 0 ↔ intSum f L = 0 ∧ f L = 0 := by
        simp only [intSum]
        omega
      rw [hz, ih (fun i hi => hf i (by omega))]
      constructor
      · rintro ⟨hprefix, hlast⟩ i hi
        by_cases hi' : i < L
        · exact hprefix i hi'
        · have he : i = L := by omega
          simpa only [he] using hlast
      · intro h
        exact ⟨fun i hi => h i (by omega), h L (by omega)⟩

theorem defect_sum_nonnegative (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    0 ≤ intSum (seamDefect q cut) L :=
  intSum_nonnegative _ L (fun i _ => seamDefect_nonnegative q cut i)

/-- No cancellation is possible among actual seam defects. -/
theorem defect_sum_zero_iff (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    intSum (seamDefect q cut) L = 0 ↔
      ∀ i, i < L → seamDefect q cut i = 0 :=
  intSum_zero_iff _ L (fun i _ => seamDefect_nonnegative q cut i)

/-- Separate raw mass is an upper bound for the actual step's digit sum. -/
theorem actual_step_mass_le_raw (n : Nat) (d : Nat → Nat) (L : Nat)
    (cut : Nat → Bool) (hc : Canonical n d L) :
    digitSum (step n) ≤ wordSum (rawCoeff (columnSum d L) cut) L +
      prevNat (resetOut (columnSum d L) cut) L := by
  have h := actual_step_seam_mass n d L cut hc
  have hn := defect_sum_nonnegative (columnSum d L) cut L
  omega

/-- The mass correction vanishes exactly when every column's actual and
reset outgoing carries agree. -/
theorem actual_step_mass_eq_raw_iff (n : Nat) (d : Nat → Nat) (L : Nat)
    (cut : Nat → Bool) (hc : Canonical n d L) :
    digitSum (step n) = wordSum (rawCoeff (columnSum d L) cut) L +
      prevNat (resetOut (columnSum d L) cut) L ↔
        ∀ i, i < L → seamDefect (columnSum d L) cut i = 0 := by
  have h := actual_step_seam_mass n d L cut hc
  rw [← defect_sum_zero_iff (columnSum d L) cut L]
  omega

/-- A nonzero actual defect produces at least nine units of digit-mass loss. -/
theorem nonzero_defect_mass_gap (n : Nat) (d : Nat → Nat) (L : Nat)
    (cut : Nat → Bool) (hc : Canonical n d L)
    (hdef : ∃ i, i < L ∧ seamDefect (columnSum d L) cut i ≠ 0) :
    digitSum (step n) + 9 ≤ wordSum (rawCoeff (columnSum d L) cut) L +
      prevNat (resetOut (columnSum d L) cut) L := by
  have h := actual_step_seam_mass n d L cut hc
  have hn := defect_sum_nonnegative (columnSum d L) cut L
  have hz : intSum (seamDefect (columnSum d L) cut) L ≠ 0 := by
    intro hz
    have hall := (defect_sum_zero_iff (columnSum d L) cut L).mp hz
    obtain ⟨i, hi, hne⟩ := hdef
    exact hne (hall i hi)
  omega

#print axioms raw_mass_balance
#print axioms defect_sum_balance
#print axioms normalized_seam_mass
#print axioms actual_step_mass
#print axioms actual_step_seam_mass
#print axioms seamDefect_nonnegative
#print axioms defect_sum_zero_iff
#print axioms actual_step_mass_le_raw
#print axioms actual_step_mass_eq_raw_iff
#print axioms nonzero_defect_mass_gap

end Agent107.SeamMass
