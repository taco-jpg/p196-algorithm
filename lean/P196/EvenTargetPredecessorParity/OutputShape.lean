import P196.Agent105InverseBoundaries.Agent105WidthSupport9df76b

/-!
Agent #6: outer coefficients and canonical output shape for ordinary
predecessors of even targets. The decimal value decomposition gives the
outer coefficient's parity. Existing carry thresholds and canonical-width
uniqueness then identify the target condition needed by the fiber count.
-/

set_option autoImplicit false

namespace EvenTargetPredecessorParity

open Lychrel196 DecimalDigits FoldedDecimal
open Agent105WidthSupport9df76b

/-- Every actual canonical predecessor of an even target has an even
outer pair coefficient. No palindromicity assumption is needed. -/
theorem even_predecessor_outer
    (n Y L : Nat) (d : Nat → Nat)
    (hn : Canonical n d L) (hstep : step n = Y) (heven : Y % 2 = 0) :
    columnSum d L 0 % 2 = 0 := by
  have hv : step n = value (columnSum d L) L :=
    step_eq_word_value n d (columnSum d L) L hn (fun _ _ => rfl)
  have hindex : L - 1 + 1 = L := by have hL := hn.1; omega
  have hshift := value_shift (columnSum d L) (L - 1)
  rw [hindex, ← hv, hstep] at hshift
  omega

/-- For an actual predecessor of an even canonical target, the source is
a singleton or has an outer coefficient at least ten exactly when the
target is a singleton or has leading digit one. -/
theorem even_predecessor_outer_iff
    (n Y L W : Nat) (d e : Nat → Nat)
    (hn : Canonical n d L) (hY : Canonical Y e W)
    (hstep : step n = Y) (heven : Y % 2 = 0) :
    (L = 1 ∨ 10 ≤ columnSum d L 0) ↔
      (W = 1 ∨ e (W - 1) = 1) := by
  let q := columnSum d L
  have hqeven : q 0 % 2 = 0 := even_predecessor_outer n Y L d hn hstep heven
  have ha : Admissible L q := NormalizationBridge.canonical_admissible n d L hn
  have hqpos : 2 ≤ q 0 := by
    have hp := ha.2.1
    omega
  change (L = 1 ∨ 10 ≤ q 0) ↔ (W = 1 ∨ e (W - 1) = 1)
  rcases actual_overflow_cases d L hn.2.1 with hcarry | hcarry
  · change carry q L = 0 at hcarry
    have hnext : Canonical Y (output q) L := by
      simpa only [hstep] using canonical_next_no_overflow n d L hn hcarry
    obtain ⟨hwidth, hdigit⟩ := canonical_width_and_digits_unique hY hnext
    subst W
    have hnotlarge : ¬ 10 ≤ q 0 := by
      intro hlarge
      have ho := OverflowNormalizationNine.outer_large_overflow q L ha hlarge
      omega
    have hindex : L - 1 + 1 = L := by have hL := hn.1; omega
    have hsym : q (L - 1) = q 0 := by
      have hs := columnSum_symmetric d L 0 hn.1
      simpa only [Nat.sub_zero] using hs.symm
    have hcolumn := column_equation q (L - 1)
    rw [hindex, hcarry, hsym] at hcolumn
    have hlast := hdigit (L - 1) (by have hL := hn.1; omega)
    have hnotone : e (L - 1) ≠ 1 := by omega
    simp only [hnotlarge, hnotone, or_false]
  · change carry q L = 1 at hcarry
    have hlarge : 10 ≤ q 0 := by
      by_cases hlarge : 10 ≤ q 0
      · exact hlarge
      · have hsmall : q 0 ≤ 8 := by omega
        have hz := NormalizationBridge.outer_small_no_overflow q L ha hsmall
        omega
    have hnext : Canonical Y (extended q L) (L + 1) := by
      simpa only [hstep] using canonical_next_overflow n d L hn hcarry
    obtain ⟨hwidth, hdigit⟩ := canonical_width_and_digits_unique hnext hY
    have hlast := hdigit L (by omega)
    simp only [extended, Nat.lt_irrefl, if_false, hcarry] at hlast
    have hindex : W - 1 = L := by omega
    have hlead : e (W - 1) = 1 := by
      rw [hindex]
      exact hlast.symm
    constructor
    · intro _
      exact Or.inr hlead
    · intro _
      exact Or.inr hlarge

#print axioms even_predecessor_outer
#print axioms even_predecessor_outer_iff

end EvenTargetPredecessorParity
