import P196.Agent8CommonOverflowDefect.Agent8DefectTransport

/-!
Exact numerical evaluation of the existing common-overflow defect law.
The actual carry and normalization functions are unchanged.  The structural
theorem needs no coefficient bound, symmetry, positivity, or canonicality
assumption: its terminal carries are both exactly one, and its normalized
old-width digit difference is antisymmetric.

This is a finite one-transition statement about paired output words.  It
does not establish preservation of its hypotheses under later transitions.
-/

namespace P196.CommonOverflowGap

open DecimalDigits FoldedDecimal RawSymmetryObstruction
open P196.Agent8.CommonOverflowDefect

private theorem defect_eq_extended_difference (q s : Nat → Nat) (L : Nat)
    (hc : carry q L = carry s L) (i : Nat) :
    oldDigitDefect q s L i =
      (extended q L i : Int) - (extended s L i : Int) := by
  by_cases hi : i < L
  · rw [oldDigitDefect_lt q s L i hi]
    simp only [extended, if_pos hi]
  · have hz := oldDigitDefect_zero_of_ge q s L i (by omega)
    simpa only [extended, if_neg hi, hc, Int.sub_self] using hz

private theorem previous_defect_eq_extended_difference
    (q s : Nat → Nat) (L : Nat)
    (hc : carry q L = carry s L) (i : Nat) :
    previous (oldDigitDefect q s L) i =
      (prevNat (extended q L) i : Int) -
        (prevNat (extended s L) i : Int) := by
  cases i with
  | zero => simp only [previous, prevNat, Int.natCast_zero, Int.sub_self]
  | succ i =>
    exact defect_eq_extended_difference q s L hc i

private theorem value_previous (d : Nat → Nat) (L : Nat) :
    value (prevNat d) (L + 1) = 10 * value d L := by
  rw [value_shift]
  simp only [prevNat, Nat.zero_add]

private theorem value_extended_prefix (q : Nat → Nat) (L : Nat) :
    value (extended q L) L = value (output q) L := by
  apply value_congr
  intro i hi
  simp only [extended, if_pos hi]

private theorem overflow_column_balance (q s : Nat → Nat) (L : Nat)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) (i : Nat) (hi : i < L + 1) :
    nextColumns q L i + extended s L i + prevNat (extended q L) i =
      nextColumns s L i + extended q L i + prevNat (extended s L) i := by
  have hc := hq.trans hs.symm
  have ht := overflow_transport q s L hq hs he i hi
  rw [defect_eq_extended_difference q s L hc i,
    previous_defect_eq_extended_difference q s L hc i] at ht
  omega

/-- Evaluating the exact common-overflow response at ten reverses and
multiplies its numerical difference by nine.  No digit or coefficient
bounds are needed beyond the explicit actual-carry hypotheses. -/
theorem overflow_value_gap_balance (q s : Nat → Nat) (L : Nat)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) :
    value (nextColumns q L) (L + 1) + 9 * value q L =
      value (nextColumns s L) (L + 1) + 9 * value s L := by
  have hv := value_congr
    (fun i => nextColumns q L i + extended s L i + prevNat (extended q L) i)
    (fun i => nextColumns s L i + extended q L i + prevNat (extended s L) i)
    (L + 1) (overflow_column_balance q s L hq hs he)
  simp only [value_add, value_previous, value_extended_prefix,
    value_extended, hq, hs, Nat.one_mul] at hv
  have hqv := value_output q L
  have hsv := value_output s L
  rw [hq, Nat.one_mul] at hqv
  rw [hs, Nat.one_mul] at hsv
  omega

end P196.CommonOverflowGap
