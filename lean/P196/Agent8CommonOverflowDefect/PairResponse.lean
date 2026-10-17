import P196.Agent8CommonOverflowDefect.SeamCoefficients

/-!
The complete partition response reflected at the actual overflow-dependent
width, and its ordinary-integer representation.  No recurrence is assumed.
-/

namespace Agent107.PairResponse

open DecimalDigits FoldedDecimal RawSymmetryObstruction
open Agent107.SeamCoefficients

/-- Pairing the fully supported output digits uses the actual next width. -/
theorem nextColumns_actualCoeff (q : Nat → Nat) (L i : Nat)
    (hi : i < nextWidth q L) :
    (nextColumns q L i : Int) =
      actualCoeff q L i + actualCoeff q L (nextWidth q L - 1 - i) := by
  by_cases hc : carry q L = 0
  · have hiL : i < L := by simpa only [nextWidth, hc, if_true] using hi
    have hm : L - 1 - i < L := by omega
    simp only [nextColumns, nextWidth, hc, if_true, columnSum, reflected,
      actualCoeff_lt q L i hiL, actualCoeff_lt q L (L - 1 - i) hm]
    omega
  · have hiL : i ≤ L := by
      simp only [nextWidth, hc, if_false] at hi
      omega
    have hm : L + 1 - 1 - i ≤ L := by omega
    simp only [nextColumns, nextWidth, hc, if_false, columnSum, reflected,
      actualCoeff_eq_extended q L i hiL,
      actualCoeff_eq_extended q L (L + 1 - 1 - i) hm]
    omega

/-- The complete coefficient response and its reflection, including the
terminal carry and every seam, with no disjoint-prefix requirement. -/
theorem pair_response (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hi : i < nextWidth q L) :
    (nextColumns q L i : Int) =
      resetRaw q cut L i + resetRaw q cut L (nextWidth q L - 1 - i) +
      correction q cut L i + correction q cut L (nextWidth q L - 1 - i) := by
  rw [nextColumns_actualCoeff q L i hi,
    coefficient_response q cut L i,
    coefficient_response q cut L (nextWidth q L - 1 - i)]
  omega

/-- For an ordinary canonical input these formulas describe the actual
next reverse-and-add integer, not merely a symbolic word. -/
theorem numeric_pair_response (n : Nat) (d q : Nat → Nat) (L : Nat)
    (cut : Nat → Bool) (hc : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i) :
    ∃ e, Canonical (Lychrel196.step n) e (nextWidth q L) ∧
      ∀ i, i < nextWidth q L →
        (columnSum e (nextWidth q L) i : Int) =
          resetRaw q cut L i + resetRaw q cut L (nextWidth q L - 1 - i) +
          correction q cut L i + correction q cut L (nextWidth q L - 1 - i) := by
  obtain ⟨e, he, hcols⟩ := representation_next n d q L hc hrep
  refine ⟨e, he, ?_⟩
  intro i hi
  rw [hcols i hi]
  exact pair_response q cut L i hi

end Agent107.PairResponse
