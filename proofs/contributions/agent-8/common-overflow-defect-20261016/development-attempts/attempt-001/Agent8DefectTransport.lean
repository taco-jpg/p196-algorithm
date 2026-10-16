import PairResponse

/-!
Exact transport of an antisymmetric normalized-digit difference through
common terminal carry.  The original integer-polynomial identity appears in
renewal_pass/constructive/STATUS.md, section 2, at source commit
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5.  The decimal normalization and
actual-width pairing used here are the existing DecimalDigits,
FoldedDecimal, and Agent107 APIs; their definitions are unchanged.

All differences are in Int.  Only the old L digit positions are supported,
and paired coefficients are compared only inside the nextWidth-selected
width.  Canonical representations supply its ordinary-integer interpretation
in the companion numeric module.
No coefficient bound, symmetry of the input coefficient words, positivity,
canonical input, future return, or infinite orbit is assumed here.
-/

namespace P196.Agent8.CommonOverflowDefect

open DecimalDigits FoldedDecimal RawSymmetryObstruction
open Agent107.SeamCoefficients Agent107.PairResponse

set_option maxHeartbeats 1000000

/-- The actual normalized-digit difference, zero outside the old width. -/
def oldDigitDefect (q s : Nat → Nat) (L i : Nat) : Int :=
  supported (fun j => (output q j : Int) - (output s j : Int)) L i

/-- Antisymmetry is imposed on normalized digits in the old width. -/
def AntisymmetricDefect (q s : Nat → Nat) (L : Nat) : Prop :=
  ∀ i, i < L →
    oldDigitDefect q s L i = -oldDigitDefect q s L (L - 1 - i)

/-- Multiplication by x^h on coefficient functions, including the left edge. -/
def shift (e : Nat → Int) (h i : Nat) : Int :=
  if h ≤ i then e (i - h) else 0

theorem oldDigitDefect_lt (q s : Nat → Nat) (L i : Nat) (hi : i < L) :
    oldDigitDefect q s L i = (output q i : Int) - (output s i : Int) := by
  simp only [oldDigitDefect, supported, if_pos hi]

theorem oldDigitDefect_zero_of_ge (q s : Nat → Nat) (L i : Nat)
    (hi : L ≤ i) : oldDigitDefect q s L i = 0 := by
  simp only [oldDigitDefect, supported, if_neg (by omega : ¬ i < L)]

theorem oldDigitDefect_zero_width (q s : Nat → Nat) (i : Nat) :
    oldDigitDefect q s 0 i = 0 :=
  oldDigitDefect_zero_of_ge q s 0 i (Nat.zero_le i)

theorem antisymmetricDefect_iff (q s : Nat → Nat) (L : Nat) :
    AntisymmetricDefect q s L ↔
      ∀ i, i < L → (output q i : Int) - (output s i : Int) =
        -((output q (L - 1 - i) : Int) - (output s (L - 1 - i) : Int)) := by
  constructor
  · intro he i hi
    have h := he i hi
    simpa only [oldDigitDefect_lt q s L i hi,
      oldDigitDefect_lt q s L (L - 1 - i) (by omega)] using h
  · intro he i hi
    simpa only [oldDigitDefect_lt q s L i hi,
      oldDigitDefect_lt q s L (L - 1 - i) (by omega)] using he i hi

theorem shift_zero (e : Nat → Int) (i : Nat) : shift e 0 i = e i := by
  simp [shift]

theorem shift_one (e : Nat → Int) (i : Nat) : shift e 1 i = previous e i := by
  cases i <;> simp [shift, previous]

/-- The common terminal carry cancels in the fully supported actual digits. -/
theorem actualCoeff_difference (q s : Nat → Nat) (L : Nat)
    (hc : carry q L = carry s L) (i : Nat) :
    actualCoeff q L i - actualCoeff s L i = oldDigitDefect q s L i := by
  by_cases hi : i < L
  · simp [actualCoeff, oldDigitDefect, supported, hi]
  · by_cases heq : i = L
    · simp [actualCoeff, oldDigitDefect, supported, hi, heq, hc]
    · simp [actualCoeff, oldDigitDefect, supported, hi, heq]

/-- Equal actual carry values select equal next widths. -/
theorem nextWidth_eq_of_carry_eq (q s : Nat → Nat) (L : Nat)
    (hc : carry q L = carry s L) : nextWidth q L = nextWidth s L := by
  simp only [nextWidth, hc]

/-- A binary terminal carry is exactly the increment of the actual width. -/
theorem common_carry_width (q s : Nat → Nat) (L h : Nat)
    (hh : h = 0 ∨ h = 1) (hq : carry q L = h) (hs : carry s L = h) :
    nextWidth q L = L + h ∧ nextWidth s L = L + h := by
  rcases hh with rfl | rfl <;> simp [nextWidth, hq, hs]

/-- Arithmetic link: pair the supported output digits at the shared actual
width.  No reversal or difference identity is supplied as a premise. -/
theorem nextColumns_difference (q s : Nat → Nat) (L : Nat)
    (hc : carry q L = carry s L) (i : Nat) (hi : i < nextWidth q L) :
    (nextColumns q L i : Int) - (nextColumns s L i : Int) =
      oldDigitDefect q s L i +
        oldDigitDefect q s L (nextWidth q L - 1 - i) := by
  have hw := nextWidth_eq_of_carry_eq q s L hc
  have his : i < nextWidth s L := by rw [← hw]; exact hi
  have hq := nextColumns_actualCoeff q L i hi
  have hs := nextColumns_actualCoeff s L i his
  rw [← hw] at hs
  have hd := actualCoeff_difference q s L hc i
  have hr := actualCoeff_difference q s L hc (nextWidth q L - 1 - i)
  omega

/-- No overflow uses the old reflection, so the antisymmetric defect cancels. -/
theorem no_overflow_transport (q s : Nat → Nat) (L : Nat)
    (hq : carry q L = 0) (hs : carry s L = 0)
    (he : AntisymmetricDefect q s L) (i : Nat) (hi : i < L) :
    (nextColumns q L i : Int) - (nextColumns s L i : Int) = 0 := by
  have hw : nextWidth q L = L := by simp [nextWidth, hq]
  have hp := nextColumns_difference q s L (hq.trans hs.symm) i
    (by rw [hw]; exact hi)
  rw [hw] at hp
  have ha := he i hi
  omega

theorem no_overflow_cancellation (q s : Nat → Nat) (L : Nat)
    (hq : carry q L = 0) (hs : carry s L = 0)
    (he : AntisymmetricDefect q s L) (i : Nat) (hi : i < L) :
    nextColumns q L i = nextColumns s L i := by
  have h := no_overflow_transport q s L hq hs he i hi
  omega

/-- Reflection in width L+1 shifts the old reflection by one.  At i=0
the reflected coefficient is the zero-supported terminal position. -/
theorem overflow_reflected_defect (q s : Nat → Nat) (L : Nat)
    (he : AntisymmetricDefect q s L) (i : Nat) (hi : i < L + 1) :
    oldDigitDefect q s L (L - i) = -previous (oldDigitDefect q s L) i := by
  cases i with
  | zero =>
    simp only [Nat.sub_zero, previous,
      oldDigitDefect_zero_of_ge q s L L (Nat.le_refl L), Int.neg_zero]
  | succ i =>
    have hip : i < L := by omega
    have ha := he i hip
    have hind : L - (i + 1) = L - 1 - i := by omega
    simp only [previous, hind]
    omega

/-- Exact common-overflow identity: the new paired difference is (1-x)e.
Both exterior positions i=0 and i=L are included. -/
theorem overflow_transport (q s : Nat → Nat) (L : Nat)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) (i : Nat) (hi : i < L + 1) :
    (nextColumns q L i : Int) - (nextColumns s L i : Int) =
      oldDigitDefect q s L i - previous (oldDigitDefect q s L) i := by
  have hw : nextWidth q L = L + 1 := by simp [nextWidth, hq]
  have hp := nextColumns_difference q s L (hq.trans hs.symm) i
    (by rw [hw]; exact hi)
  simp only [hw, Nat.add_sub_cancel] at hp
  have hr := overflow_reflected_defect q s L he i hi
  omega

/-- Coefficientwise form of the integer-polynomial identity (1-x^h)e. -/
theorem common_carry_transport (q s : Nat → Nat) (L h : Nat)
    (hh : h = 0 ∨ h = 1) (hq : carry q L = h) (hs : carry s L = h)
    (he : AntisymmetricDefect q s L) (i : Nat) (hi : i < L + h) :
    (nextColumns q L i : Int) - (nextColumns s L i : Int) =
      oldDigitDefect q s L i - shift (oldDigitDefect q s L) h i := by
  rcases hh with rfl | rfl
  · have hiL : i < L := by simpa only [Nat.add_zero] using hi
    simpa only [shift_zero, Int.sub_self] using
      no_overflow_transport q s L hq hs he i hiL
  · simpa only [shift_one] using overflow_transport q s L hq hs he i hi

/-- Finite differences determine the entire finite prefix, starting at
the zero left boundary.  This is proved, not assumed by noncancellation. -/
theorem finite_difference_injective (a b : Nat → Int) (L : Nat)
    (h : ∀ i, i < L → a i - previous a i = b i - previous b i) :
    ∀ i, i < L → a i = b i := by
  intro i
  induction i with
  | zero =>
    intro hi
    have hz := h 0 hi
    simp only [previous] at hz
    omega
  | succ i ih =>
    intro hi
    have hp := ih (by omega)
    have hn := h (i + 1) hi
    simp only [previous] at hn
    omega

theorem finite_difference_zero_iff (e : Nat → Int) (L : Nat) :
    (∀ i, i < L → e i - previous e i = 0) ↔
      (∀ i, i < L → e i = 0) := by
  constructor
  · intro h
    apply finite_difference_injective e (fun _ => 0) L
    intro i hi
    have hz := h i hi
    cases i <;> simpa only [previous, Int.sub_zero] using hz
  · intro h i hi
    cases i with
    | zero => simp only [previous, h 0 hi, Int.sub_zero]
    | succ i => simp only [previous, h (i + 1) hi, h i (by omega), Int.sub_self]

/-- Within the antisymmetric class, common-overflow pairing agrees exactly
when all old normalized digits agree. -/
theorem overflow_agreement_iff_digits_agree (q s : Nat → Nat) (L : Nat)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) :
    (∀ i, i < L + 1 → nextColumns q L i = nextColumns s L i) ↔
      (∀ i, i < L → output q i = output s i) := by
  constructor
  · intro hp
    have hd : ∀ i, i < L →
        oldDigitDefect q s L i - previous (oldDigitDefect q s L) i = 0 := by
      intro i hi
      have ht := overflow_transport q s L hq hs he i (by omega)
      have ha := hp i (by omega)
      rw [ha] at ht
      omega
    have hz := (finite_difference_zero_iff (oldDigitDefect q s L) L).mp hd
    intro i hi
    have hzi := hz i hi
    rw [oldDigitDefect_lt q s L i hi] at hzi
    omega
  · intro hd
    have hz : ∀ i, oldDigitDefect q s L i = 0 := by
      intro i
      by_cases hi : i < L
      · rw [oldDigitDefect_lt q s L i hi, hd i hi]
        omega
      · exact oldDigitDefect_zero_of_ge q s L i (by omega)
    intro i hi
    have ht := overflow_transport q s L hq hs he i hi
    have hp : previous (oldDigitDefect q s L) i = 0 := by
      cases i <;> simp only [previous, hz]
    rw [hz i, hp] at ht
    omega

/-- Every actual nonzero old digit difference produces a nonzero paired
successor difference.  The witness is derived using finite differences. -/
theorem overflow_noncancellation (q s : Nat → Nat) (L : Nat)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L)
    (hne : ∃ i, i < L ∧ output q i ≠ output s i) :
    ∃ i, i < L + 1 ∧ nextColumns q L i ≠ nextColumns s L i := by
  classical
  by_contra hresult
  have hp : ∀ i, i < L + 1 → nextColumns q L i = nextColumns s L i := by
    intro i hi
    by_contra hneq
    exact hresult ⟨i, hi, hneq⟩
  have hd := (overflow_agreement_iff_digits_agree q s L hq hs he).mp hp
  obtain ⟨i, hi, hneq⟩ := hne
  exact hneq (hd i hi)

end P196.Agent8.CommonOverflowDefect
