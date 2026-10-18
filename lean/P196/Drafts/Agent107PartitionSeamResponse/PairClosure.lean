import P196.Agent8CommonOverflowDefect.PairResponse
import P196.Drafts.Agent107PartitionSeamResponse.SeamMass

/-!
Common-clock independent pairing is exact if and only if every actual seam
carry defect vanishes. The mass identity is derived, including both possible
actual widths and the isolated terminal carry; it is not a premise.
-/

namespace Agent107.PairClosure

open DecimalDigits DecimalMass FoldedDecimal RawSymmetryObstruction
open Agent107.SeamCoefficients Agent107.SeamMass Agent107.PairResponse

/-- The isolated raw digit sum paired at the actual whole-word width. -/
def rawPair (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat) : Int :=
  resetRaw q cut L i + resetRaw q cut L (nextWidth q L - 1 - i)

theorem intSum_congr (f g : Nat → Int) (L : Nat)
    (h : ∀ i, i < L → f i = g i) : intSum f L = intSum g L := by
  induction L with
  | zero => rfl
  | succ L ih =>
      simp only [intSum, ih (fun i hi => h i (by omega)), h L (by omega)]

theorem intSum_add (f g : Nat → Int) (L : Nat) :
    intSum (fun i => f i + g i) L = intSum f L + intSum g L := by
  induction L with
  | zero => rfl
  | succ L ih => simp only [intSum, ih]; omega

theorem intSum_natCast (f : Nat → Nat) (L : Nat) :
    intSum (fun i => (f i : Int)) L = (wordSum f L : Int) := by
  induction L with
  | zero => rfl
  | succ L ih => simp only [intSum, wordSum, ih, Int.natCast_add]

theorem intSum_shift (f : Nat → Int) (L : Nat) :
    intSum f (L + 1) = f 0 + intSum (fun i => f (i + 1)) L := by
  induction L with
  | zero => simp [intSum]
  | succ L ih => simp only [intSum] at ih ⊢; omega

theorem intSum_reflected (f : Nat → Int) (L : Nat) :
    intSum (fun i => f (L - 1 - i)) L = intSum f L := by
  induction L generalizing f with
  | zero => rfl
  | succ L ih =>
      have hr : intSum (fun i => f (L + 1 - 1 - i)) L =
          intSum (fun i => f ((L - 1 - i) + 1)) L := by
        apply intSum_congr
        intro i hi
        congr 1
        omega
      rw [intSum, hr, ih (fun i => f (i + 1)), intSum_shift]
      simp [Int.add_comm]

theorem actualCoeff_prefix_mass (q : Nat → Nat) (L : Nat) :
    intSum (actualCoeff q L) L = (wordSum (output q) L : Int) := by
  rw [intSum_congr _ (fun i => (output q i : Int)) L
    (fun i hi => actualCoeff_lt q L i hi), intSum_natCast]

theorem raw_prefix_mass (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    intSum (resetRaw q cut L) L = (wordSum (rawCoeff q cut) L : Int) := by
  rw [intSum_congr _ (fun i => (rawCoeff q cut i : Int)) L
    (fun i hi => resetRaw_lt q cut L i hi), intSum_natCast]

/-- The no-overflow case has no hidden isolated carry beyond its width. -/
theorem isolated_terminal_zero_of_nooverflow (q : Nat → Nat)
    (cut : Nat → Bool) (L : Nat) (hc : carry q L = 0) :
    prevNat (resetOut q cut) L = 0 := by
  have h := previous_le_actual q cut L
  omega

/-- The actual width includes precisely the final carry when nonzero. -/
theorem actual_mass_at_actual_width (q : Nat → Nat) (L : Nat) :
    intSum (actualCoeff q L) (nextWidth q L) =
      ((wordSum (output q) L + carry q L : Nat) : Int) := by
  by_cases hc : carry q L = 0
  · simp only [nextWidth, hc, if_true, Nat.add_zero]
    exact actualCoeff_prefix_mass q L
  · simp only [nextWidth, hc, if_false, intSum, actualCoeff_terminal,
      actualCoeff_prefix_mass, Int.natCast_add]

/-- At the actual width the raw mass still includes each isolated terminal
carry, even if its isolated overflow clock differs from the whole clock. -/
theorem raw_mass_at_actual_width (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    intSum (resetRaw q cut L) (nextWidth q L) =
      ((wordSum (rawCoeff q cut) L + prevNat (resetOut q cut) L : Nat) : Int) := by
  by_cases hc : carry q L = 0
  · have hz := isolated_terminal_zero_of_nooverflow q cut L hc
    simp only [nextWidth, hc, if_true, hz, Nat.add_zero]
    exact raw_prefix_mass q cut L
  · simp only [nextWidth, hc, if_false, intSum, resetRaw_terminal,
      raw_prefix_mass, Int.natCast_add]

theorem raw_pair_mass (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    intSum (rawPair q cut L) (nextWidth q L) =
      2 * intSum (resetRaw q cut L) (nextWidth q L) := by
  unfold rawPair
  rw [intSum_add, intSum_reflected]
  omega

theorem actual_pair_mass (q : Nat → Nat) (L : Nat) :
    intSum (fun i => (nextColumns q L i : Int)) (nextWidth q L) =
      2 * intSum (actualCoeff q L) (nextWidth q L) := by
  rw [intSum_congr _
    (fun i => actualCoeff q L i + actualCoeff q L (nextWidth q L - 1 - i))
    (nextWidth q L) (fun i hi => nextColumns_actualCoeff q L i hi)]
  rw [intSum_add, intSum_reflected]
  omega

/-- Full common-clock pair mass correction. All quantities are computed
from the actual word and cut pattern; no mass identity is assumed. -/
theorem pair_mass_response (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    intSum (fun i => (nextColumns q L i : Int)) (nextWidth q L) +
      18 * intSum (seamDefect q cut) L =
        intSum (rawPair q cut L) (nextWidth q L) := by
  have h := normalized_seam_mass q cut L
  rw [actual_pair_mass, raw_pair_mass,
    actual_mass_at_actual_width, raw_mass_at_actual_width]
  omega

theorem pair_agrees_of_no_activity (q : Nat → Nat) (cut : Nat → Bool) (L : Nat)
    (hz : ∀ i, i < L → seamDefect q cut i = 0) :
    ∀ i, i < nextWidth q L → (nextColumns q L i : Int) = rawPair q cut L i := by
  have he := coefficients_agree_of_no_activity q cut L hz
  intro i hi
  rw [nextColumns_actualCoeff q L i hi, he i, he (nextWidth q L - 1 - i)]
  rfl

/-- Reflection cannot cancel a nonzero seam correction: its total mass
loss is strictly positive because every seam defect is nonnegative. -/
theorem no_activity_of_pair_agrees (q : Nat → Nat) (cut : Nat → Bool) (L : Nat)
    (he : ∀ i, i < nextWidth q L →
      (nextColumns q L i : Int) = rawPair q cut L i) :
    ∀ i, i < L → seamDefect q cut i = 0 := by
  have hs := intSum_congr _ _ (nextWidth q L) he
  have hm := pair_mass_response q cut L
  have hz : intSum (seamDefect q cut) L = 0 := by omega
  exact (defect_sum_zero_iff q cut L).mp hz

/-- Exact common-clock component pairing is equivalent to no active seam,
for every finite word and arbitrary finite cut pattern. -/
theorem pair_agrees_iff_no_activity (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    (∀ i, i < nextWidth q L → (nextColumns q L i : Int) = rawPair q cut L i) ↔
      (∀ i, i < L → seamDefect q cut i = 0) := by
  exact ⟨no_activity_of_pair_agrees q cut L, pair_agrees_of_no_activity q cut L⟩

/-- For an ordinary canonical input, the unique actual next pair word
equals the common-clock isolated raw pairing exactly when all seams vanish. -/
theorem numeric_pair_agrees_iff_no_activity (n : Nat) (d q : Nat → Nat) (L : Nat)
    (cut : Nat → Bool) (hc : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i) :
    ∃ e, Canonical (Lychrel196.step n) e (nextWidth q L) ∧
      ((∀ i, i < nextWidth q L →
        (columnSum e (nextWidth q L) i : Int) = rawPair q cut L i) ↔
        (∀ i, i < L → seamDefect q cut i = 0)) := by
  obtain ⟨e, he, hcols⟩ := representation_next n d q L hc hrep
  refine ⟨e, he, ?_⟩
  have hiff := pair_agrees_iff_no_activity q cut L
  constructor
  · intro h
    apply hiff.mp
    intro i hi
    rw [← hcols i hi]
    exact h i hi
  · intro hz
    have h := hiff.mpr hz
    intro i hi
    rw [hcols i hi]
    exact h i hi

end Agent107.PairClosure
