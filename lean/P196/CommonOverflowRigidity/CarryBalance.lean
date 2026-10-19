import P196.Agent8CommonOverflowDefect.Agent8DefectTransport

/-!
Antisymmetry of the old normalized digits fixes their total digit sum.
After common overflow, applying this observation at two consecutive
normalizations also fixes the second terminal carry. This follows from
the exact digit-sum balance and the binary bound for decimal carries;
the second carry need not be supplied as an additional hypothesis.
-/

set_option autoImplicit false

namespace P196.CommonOverflowRigidity

open DecimalDigits DecimalMass FoldedDecimal
open P196.Agent8.CommonOverflowDefect

/-- Antisymmetric digit differences have zero total unweighted mass. -/
theorem antisymmetric_output_sum (q s : Nat → Nat) (L : Nat)
    (he : AntisymmetricDefect q s L) :
    wordSum (output q) L = wordSum (output s) L := by
  have hp : ∀ i, i < L →
      columnSum (output q) L i = columnSum (output s) L i := by
    intro i hi
    have ha := (antisymmetricDefect_iff q s L).mp he i hi
    simp only [columnSum, reflected]
    omega
  have hsums := wordSum_congr (columnSum (output q) L)
    (columnSum (output s) L) L hp
  rw [wordSum_columns, wordSum_columns] at hsums
  omega

/-- The second terminal carries agree whenever both normalized defects are
antisymmetric and the first transition overflows in both words. No symmetry
or coefficient bound on the original words is needed for this balance. -/
theorem repeated_antisymmetry_carry_eq (q s : Nat → Nat) (L : Nat)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L)
    (henext : AntisymmetricDefect (nextColumns q L) (nextColumns s L)
      (nextWidth q L)) :
    carry (nextColumns q L) (nextWidth q L) =
      carry (nextColumns s L) (nextWidth s L) := by
  have hwq : nextWidth q L = L + 1 := by simp [nextWidth, hq]
  have hws : nextWidth s L = L + 1 := by simp [nextWidth, hs]
  have hsum := antisymmetric_output_sum q s L he
  have hcoeff : wordSum (nextColumns q L) (L + 1) =
      wordSum (nextColumns s L) (L + 1) := by
    have hqcol : nextColumns q L = columnSum (extended q L) (L + 1) := by
      funext i
      simp [nextColumns, hq]
    have hscol : nextColumns s L = columnSum (extended s L) (L + 1) := by
      funext i
      simp [nextColumns, hs]
    rw [hqcol, hscol, wordSum_columns, wordSum_columns,
      wordSum_extended, wordSum_extended, hsum, hq, hs]
  have hout := antisymmetric_output_sum (nextColumns q L)
    (nextColumns s L) (nextWidth q L) henext
  rw [hwq] at hout
  have hdq : ∀ i, i < L + 1 → extended q L i ≤ 9 := by
    intro i _
    by_cases hi : i < L
    · simpa only [extended, if_pos hi] using output_bounded q i
    · simp [extended, hi, hq]
  have hds : ∀ i, i < L + 1 → extended s L i ≤ 9 := by
    intro i _
    by_cases hi : i < L
    · simpa only [extended, if_pos hi] using output_bounded s i
    · simp [extended, hi, hs]
  have hbq : ∀ i, i < L + 1 → nextColumns q L i ≤ 18 := by
    simpa only [nextColumns, hq, if_neg (by decide : ¬ (1 : Nat) = 0)] using
      columnSum_bounded (extended q L) (L + 1) hdq
  have hbs : ∀ i, i < L + 1 → nextColumns s L i ≤ 18 := by
    simpa only [nextColumns, hs, if_neg (by decide : ¬ (1 : Nat) = 0)] using
      columnSum_bounded (extended s L) (L + 1) hds
  have hcq := carry_bounded (nextColumns q L) (L + 1) hbq (L + 1) (by omega)
  have hcs := carry_bounded (nextColumns s L) (L + 1) hbs (L + 1) (by omega)
  have hbalanceq := wordSum_output (nextColumns q L) (L + 1)
  have hbalances := wordSum_output (nextColumns s L) (L + 1)
  rw [hwq, hws]
  omega

end P196.CommonOverflowRigidity
