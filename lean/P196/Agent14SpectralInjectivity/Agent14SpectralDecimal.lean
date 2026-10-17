import P196.Agent14SpectralInjectivity.Agent14SpectralInjectivity
import P196.Foundations.LychrelDigitSums

/-!
The exact spectral injectivity theorem applied to the original decimal model.
The conclusions recover the finite column-sum word. Distinct positive integers
can have the same word and therefore the same coordinate.
-/

namespace Agent14.Spectral

open DecimalDigits FoldedDecimal

/-- Original admissibility supplies precisely the bounds and reflection used. -/
theorem admissible_coordinate_injective (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (heq : coordinate q L = coordinate r L) :
    ∀ i, i < L → q i = r i := by
  exact coordinate_injective q r L hq.2.2.1 hr.2.2.1
    hq.2.2.2.1 hr.2.2.2.1 heq

/-- The original canonical decimal inputs need only share the stated width. -/
theorem canonical_column_sums_injective (n p : Nat) (d e : Nat → Nat) (L : Nat)
    (hd : Canonical n d L) (he : Canonical p e L)
    (heq : coordinate (columnSum d L) L = coordinate (columnSum e L) L) :
    ∀ i, i < L → columnSum d L i = columnSum e L i := by
  exact coordinate_injective (columnSum d L) (columnSum e L) L
    (columnSum_bounded d L hd.2.1) (columnSum_bounded e L he.2.1)
    (columnSum_symmetric d L) (columnSum_symmetric e L) heq

/-- An exact small source control: the pair word of 196 is (7,18,7). -/
theorem coordinate_196_column_sums :
    coordinate (columnSum (fun i => if i = 0 then 6 else if i = 1 then 9 else 1) 3) 3 =
      158 := by decide

/-- Injectivity of the coordinate does not imply injectivity of input integers. -/
theorem distinct_canonical_inputs_same_coordinate :
    ∃ d e : Nat → Nat,
      Canonical 12 d 2 ∧ Canonical 21 e 2 ∧ (12 : Nat) ≠ 21 ∧
      coordinate (columnSum d 2) 2 = coordinate (columnSum e 2) 2 := by
  let d : Nat → Nat := fun i => if i = 0 then 2 else 1
  let e : Nat → Nat := fun i => if i = 0 then 1 else 2
  have hd : Canonical 12 d 2 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i hi
    simp only [d]
    split <;> decide
  have he : Canonical 21 e 2 := by
    refine ⟨by decide, ?_, by decide, by decide⟩
    intro i hi
    simp only [e]
    split <;> decide
  exact ⟨d, e, hd, he, by decide, by decide⟩

end Agent14.Spectral
