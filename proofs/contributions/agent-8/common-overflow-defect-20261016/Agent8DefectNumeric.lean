import Agent8DefectTransport

/-!
Ordinary decimal consequences of the exact common-overflow defect law.
Canonical representations and actual pair-word agreement are explicit.
The final noncancellation reaches two actual reverse-and-add operations.
-/

namespace P196.Agent8.CommonOverflowDefect

open DecimalDigits FoldedDecimal RawSymmetryObstruction

set_option maxHeartbeats 2000000

/-- The transport equation describes the actual pair words of both next
ordinary integers at their common physical width. -/
theorem numeric_common_carry_transport
    (n m : Nat) (d f q s : Nat → Nat) (L h : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hh : h = 0 ∨ h = 1) (hq : carry q L = h) (hs : carry s L = h)
    (he : AntisymmetricDefect q s L) :
    ∃ a b, Canonical (Lychrel196.step n) a (L + h) ∧
      Canonical (Lychrel196.step m) b (L + h) ∧
      ∀ i, i < L + h →
        (columnSum a (L + h) i : Int) - (columnSum b (L + h) i : Int) =
          oldDigitDefect q s L i - shift (oldDigitDefect q s L) h i := by
  obtain ⟨a, ha, harep⟩ := representation_next n d q L hn hqrep
  obtain ⟨b, hb, hbrep⟩ := representation_next m f s L hm hsrep
  obtain ⟨hwq, hws⟩ := common_carry_width q s L h hh hq hs
  rw [hwq] at ha harep
  rw [hws] at hb hbrep
  refine ⟨a, b, ha, hb, ?_⟩
  intro i hi
  rw [harep i hi, hbrep i hi]
  exact common_carry_transport q s L h hh hq hs he i hi

/-- Without overflow, the antisymmetric digit difference disappears on
the second actual reverse-and-add operation. -/
theorem numeric_no_overflow_cancellation
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hq : carry q L = 0) (hs : carry s L = 0)
    (he : AntisymmetricDefect q s L) :
    Lychrel196.step (Lychrel196.step n) =
      Lychrel196.step (Lychrel196.step m) := by
  obtain ⟨a, ha, harep⟩ := representation_next n d q L hn hqrep
  obtain ⟨b, hb, hbrep⟩ := representation_next m f s L hm hsrep
  have hwq : nextWidth q L = L := by simp [nextWidth, hq]
  have hws : nextWidth s L = L := by simp [nextWidth, hs]
  rw [hwq] at ha harep
  rw [hws] at hb hbrep
  apply (ReverseAddInverse.same_width_step_eq_iff_pair_sums
    (Lychrel196.step n) (Lychrel196.step m) a b L ha hb).mpr
  intro i hi
  rw [harep i hi, hbrep i hi]
  exact no_overflow_cancellation q s L hq hs he i hi

/-- For two actual inputs with the same terminal carry, the first numeric
values agree exactly when all their normalized old digits agree. -/
theorem numeric_first_values_eq_iff_digits_agree
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hc : carry q L = carry s L) :
    Lychrel196.step n = Lychrel196.step m ↔
      ∀ i, i < L → output q i = output s i := by
  constructor
  · intro hval
    have hcols := (ReverseAddInverse.same_width_step_eq_iff_pair_sums
      n m d f L hn hm).mp hval
    apply output_congr_upto q s L
    intro i hi
    rw [← hqrep i hi, ← hsrep i hi]
    exact hcols i hi
  · intro hd
    rw [step_eq_word_value n d q L hn hqrep,
      step_eq_word_value m f s L hm hsrep]
    have hvalues := value_congr (output q) (output s) L hd
    have hqvalue := value_output q L
    have hsvalue := value_output s L
    rw [hc] at hqvalue
    omega

/-- Common overflow is injective on this antisymmetric difference class:
the second actual values agree exactly when the first actual values agree.
This does not assert unrestricted injectivity of reverse-and-add. -/
theorem numeric_overflow_second_values_eq_iff_first_values_eq
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L) :
    Lychrel196.step (Lychrel196.step n) = Lychrel196.step (Lychrel196.step m) ↔
      Lychrel196.step n = Lychrel196.step m := by
  constructor
  · intro htwo
    obtain ⟨a, ha, harep⟩ := representation_next n d q L hn hqrep
    obtain ⟨b, hb, hbrep⟩ := representation_next m f s L hm hsrep
    have hwq : nextWidth q L = L + 1 := by simp [nextWidth, hq]
    have hws : nextWidth s L = L + 1 := by simp [nextWidth, hs]
    rw [hwq] at ha harep
    rw [hws] at hb hbrep
    have hcols := (ReverseAddInverse.same_width_step_eq_iff_pair_sums
      (Lychrel196.step n) (Lychrel196.step m) a b (L + 1) ha hb).mp htwo
    have hnext : ∀ i, i < L + 1 → nextColumns q L i = nextColumns s L i := by
      intro i hi
      rw [← harep i hi, ← hbrep i hi]
      exact hcols i hi
    have hd := (overflow_agreement_iff_digits_agree q s L hq hs he).mp hnext
    exact (numeric_first_values_eq_iff_digits_agree n m d f q s L hn hm hqrep hsrep
      (hq.trans hs.symm)).mpr hd
  · intro hfirst
    exact congrArg Lychrel196.step hfirst

/-- A nonzero actual old-width digit defect forces distinct second
ordinary reverse-and-add values in the common-overflow case. -/
theorem numeric_overflow_noncancellation
    (n m : Nat) (d f q s : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m f L)
    (hqrep : ∀ i, i < L → columnSum d L i = q i)
    (hsrep : ∀ i, i < L → columnSum f L i = s i)
    (hq : carry q L = 1) (hs : carry s L = 1)
    (he : AntisymmetricDefect q s L)
    (hne : ∃ i, i < L ∧ output q i ≠ output s i) :
    Lychrel196.step (Lychrel196.step n) ≠
      Lychrel196.step (Lychrel196.step m) := by
  intro htwo
  have hfirst := (numeric_overflow_second_values_eq_iff_first_values_eq
    n m d f q s L hn hm hqrep hsrep hq hs he).mp htwo
  have hd := (numeric_first_values_eq_iff_digits_agree
    n m d f q s L hn hm hqrep hsrep (hq.trans hs.symm)).mp hfirst
  obtain ⟨i, hi, hneq⟩ := hne
  exact hneq (hd i hi)

end P196.Agent8.CommonOverflowDefect
