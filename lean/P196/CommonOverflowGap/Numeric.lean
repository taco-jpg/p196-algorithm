import P196.CommonOverflowGap.Gap

/-!
Ordinary-integer consequences of exact common-overflow gap transport.
Both initial canonical numerals have the same width, both first additions
overflow, and the normalized old-width digit difference is antisymmetric.
The second outputs may have different widths.  No recurrence, repeated
overflow, or infinite-orbit conclusion is asserted.
-/

namespace P196.CommonOverflowGap

open DecimalDigits FoldedDecimal
open P196.Agent8.CommonOverflowDefect

/-- Exact two-step balance for ordinary decimal reverse-and-add.  Equal
width is assumed only for the initial canonical representations. -/
theorem numeric_overflow_gap_balance
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) :
    Lychrel196.step (Lychrel196.step n) + 9 * Lychrel196.step n =
      Lychrel196.step (Lychrel196.step m) + 9 * Lychrel196.step m := by
  obtain ⟨a, ha, harep⟩ := representation_next n d q L hn hqrep
  obtain ⟨b, hb, hbrep⟩ := representation_next m f s L hm hsrep
  have hwq : nextWidth q L = L + 1 := by simp [nextWidth, hq]
  have hws : nextWidth s L = L + 1 := by simp [nextWidth, hs]
  rw [hwq] at ha harep
  rw [hws] at hb hbrep
  rw [step_eq_word_value (Lychrel196.step n) a (nextColumns q L) (L + 1) ha harep,
    step_eq_word_value (Lychrel196.step m) b (nextColumns s L) (L + 1) hb hbrep,
    step_eq_word_value n d q L hn hqrep,
    step_eq_word_value m f s L hm hsrep]
  exact overflow_value_gap_balance q s L hq hs he

/-- The signed numerical gap after the second addition is minus nine
times the gap after the first addition, including the zero-gap case. -/
theorem numeric_overflow_gap_scale
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) :
    (Lychrel196.step (Lychrel196.step n) : Int) -
        (Lychrel196.step (Lychrel196.step m) : Int) =
      -9 * ((Lychrel196.step n : Int) - (Lychrel196.step m : Int)) := by
  have h := numeric_overflow_gap_balance n m d f q s L hn hm hqrep hsrep hq hs he
  omega

/-- Unequal first outputs are strictly ordered in the opposite direction
after the second addition. -/
theorem numeric_overflow_order_reversal
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) :
    Lychrel196.step (Lychrel196.step n) < Lychrel196.step (Lychrel196.step m) ↔
      Lychrel196.step m < Lychrel196.step n := by
  have h := numeric_overflow_gap_balance n m d f q s L hn hm hqrep hsrep hq hs he
  omega

/-- The oppositely oriented natural difference after the second addition
is exactly nine times the first difference.  This includes either ordering:
both natural subtractions are zero when the first difference is negative. -/
theorem numeric_overflow_natural_gap
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) :
    Lychrel196.step (Lychrel196.step m) - Lychrel196.step (Lychrel196.step n) =
      9 * (Lychrel196.step n - Lychrel196.step m) := by
  have h := numeric_overflow_gap_balance n m d f q s L hn hm hqrep hsrep hq hs he
  omega

end P196.CommonOverflowGap
