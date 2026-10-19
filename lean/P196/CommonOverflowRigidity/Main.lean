import P196.CommonOverflowRigidity.Scan
import P196.CommonOverflowRigidity.CarryBalance

/-!
An antisymmetric normalized-digit defect cannot remain nonzero at two
consecutive normalizations of bounded symmetric decimal column words when the
first normalization overflows in both words. The second terminal carries
are derived to agree; no second-overflow premise is needed.

The ordinary-integer endpoint uses canonical initial numerals of the same
width and concludes equality after one reverse-and-add step. It does not
determine the original digit split, assert future preservation of a
hypothesis, or concern an infinite orbit or the orbit of 196.
-/

set_option autoImplicit false

namespace P196.CommonOverflowRigidity

open DecimalDigits FoldedDecimal
open P196.Agent8.CommonOverflowDefect

/-- Repeated antisymmetry after common first overflow is rigid on symmetric
column words bounded by eighteen. Positivity and center parity are not
needed for this algebraic statement. The second common carry is derived. -/
theorem bounded_symmetric_repeated_antisymmetry_rigid (q s : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hs : ∀ i, i < L → s i ≤ 18)
    (hqs : ∀ i, i < L → q i = q (L - 1 - i))
    (hss : ∀ i, i < L → s i = s (L - 1 - i))
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (he1 : AntisymmetricDefect q s L)
    (he2 : AntisymmetricDefect (nextColumns q L) (nextColumns s L) (nextWidth q L)) :
    ∀ i, i < L → q i = s i := by
  have hwq : nextWidth q L = L + 1 := by simp [nextWidth, hq1]
  have hws : nextWidth s L = L + 1 := by simp [nextWidth, hs1]
  have hc2 := repeated_antisymmetry_carry_eq q s L hq1 hs1 he1 he2
  rw [hwq, hws] at hc2
  rw [hwq] at he2
  have hout := repeated_antisymmetry_outputs_of_carry_eq q s L hq hs hqs hss
    hq1 hs1 he1 hc2 he2
  have hc := ReverseAddInverse.carries_equal_of_symmetric_output_equal q s L
    hq hs hqs hss hout (hq1.trans hs1.symm)
  intro i hi
  have hqi := column_equation q i
  have hsi := column_equation s i
  have hoi := hout i hi
  have hci := hc i (by omega)
  have hcn := hc (i + 1) (by omega)
  omega

/-- The exact admissible-word form: repeated antisymmetry after common
first overflow forces equality of the initial coefficient words. -/
theorem repeated_antisymmetry_rigid (q s : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hs : Admissible L s)
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (he1 : AntisymmetricDefect q s L)
    (he2 : AntisymmetricDefect (nextColumns q L) (nextColumns s L) (nextWidth q L)) :
    ∀ i, i < L → q i = s i :=
  bounded_symmetric_repeated_antisymmetry_rigid q s L hq.2.2.1 hs.2.2.1
    hq.2.2.2.1 hs.2.2.2.1 hq1 hs1 he1 he2

/-- For canonical numerals of one initial width, repeated antisymmetry
after common first overflow forces equality of the ordinary first outputs.
The original integers themselves need not agree. -/
theorem numeric_repeated_antisymmetry_step_eq
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (he1 : AntisymmetricDefect q s L)
    (he2 : AntisymmetricDefect (nextColumns q L) (nextColumns s L) (nextWidth q L)) :
    Lychrel196.step n = Lychrel196.step m := by
  have hq := NormalizationBridge.admissible_congr L (columnSum d L) q
    (NormalizationBridge.canonical_admissible n d L hn) hqrep
  have hs := NormalizationBridge.admissible_congr L (columnSum f L) s
    (NormalizationBridge.canonical_admissible m f L hm) hsrep
  have heq := repeated_antisymmetry_rigid q s L hq hs hq1 hs1 he1 he2
  rw [step_eq_word_value n d q L hn hqrep, step_eq_word_value m f s L hm hsrep]
  exact value_congr q s L heq

end P196.CommonOverflowRigidity
