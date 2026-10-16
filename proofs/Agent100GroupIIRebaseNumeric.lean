import Agent100GroupIIRebaseProfiles
import Agent100GroupIIOverflowNumeric

/-! Natural and ordinary-integer realizations of the corrected component.
The component is a new finite pair word, with no assertion that it is the
second iterate of the original component integer. -/

namespace Agent100.GroupIIRebase

set_option maxHeartbeats 2000000
set_option maxRecDepth 10000

open Lychrel196 DecimalDigits FoldedDecimal DelayedOverlapGate
open RawSymmetryObstruction GroupIIOverflow

/-- Nonnegativity makes the signed factorization an actual Nat overlap. -/
theorem actual_whole_rebased (r p u v : Nat) (h : UpperDomain r p u v) :
    ∀ i, i < 2 * r + 8 →
      (wholeOrbit r p u v 2).2 i = shiftOne (rebasedComponent r p u v) i := by
  intro i hi
  have he := actual_whole_rebasedInt r p u v h i hi
  cases i with
  | zero =>
    have hc := rebased_toNat_exact r p u v h 0
    simp [previous, shiftOne] at he ⊢
    omega
  | succ i =>
    have hc := rebased_toNat_exact r p u v h (i + 1)
    have hp := rebased_toNat_exact r p u v h i
    simp [previous, shiftOne] at he ⊢
    omega

/-- The corrected finite component is the pair word of a positive integer. -/
theorem rebased_component_realizable (r p u v : Nat) (h : UpperDomain r p u v) :
    ∃ a da, 0 < a ∧ Canonical a da (2 * r + 7) ∧
      ∀ i, i < 2 * r + 7 →
        columnSum da (2 * r + 7) i = rebasedComponent r p u v i := by
  have ha := rebased_admissible r p u v h
  exact valid_word_realizable (rebasedComponent r p u v) (2 * r + 7)
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2

/-- Every original canonical whole-input realization has the rebased overlap
as the complete pair prefix of its actual second reverse-add output. -/
theorem numeric_rebased_overlap (n : Nat) (d : Nat → Nat)
    (r p u v : Nat) (h : UpperDomain r p u v)
    (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = initial r p u v i) :
    ∃ e, Canonical (orbit n 2) e (2 * r + 8) ∧
      ∀ i, i < 2 * r + 8 →
        columnSum e (2 * r + 8) i = shiftOne (rebasedComponent r p u v) i := by
  obtain ⟨e, he, hrep⟩ := numeric_two_step_representation n d r p u v h hc hr
  refine ⟨e, he, ?_⟩
  intro i hi
  rw [hrep i hi]
  exact actual_whole_rebased r p u v h i hi

/-- The same output can be expressed using the actual canonical digits of
a positive realization of the new component, clipped at its finite width. -/
theorem numeric_rebased_realization (n : Nat) (d : Nat → Nat)
    (r p u v : Nat) (h : UpperDomain r p u v)
    (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = initial r p u v i) :
    ∃ a da e, 0 < a ∧ Canonical a da (2 * r + 7) ∧
      (∀ i, i < 2 * r + 7 →
        columnSum da (2 * r + 7) i = rebasedComponent r p u v i) ∧
      Canonical (orbit n 2) e (2 * r + 8) ∧
      ∀ i, i < 2 * r + 8 →
        columnSum e (2 * r + 8) i =
          shiftOne (finiteWord (2 * r + 7) (columnSum da (2 * r + 7))) i := by
  obtain ⟨a, da, ha, hca, hra⟩ := rebased_component_realizable r p u v h
  obtain ⟨e, he, hq⟩ := numeric_rebased_overlap n d r p u v h hc hr
  refine ⟨a, da, e, ha, hca, hra, he, ?_⟩
  have hf : finiteWord (2 * r + 7) (columnSum da (2 * r + 7)) =
      rebasedComponent r p u v := by
    funext i
    by_cases hi : i < 2 * r + 7
    · simp only [finiteWord, hi, if_true]
      exact hra i hi
    · simp only [finiteWord, hi, if_false]
      exact (rebased_zero_after_width r p u v h i (by omega)).symm
  intro i hi
  rw [hf]
  exact hq i hi

/-- Every upper-domain tuple has both an original positive input and a
positive corrected component realizing this actual two-step relation. -/
theorem realized_rebased_overlap (r p u v : Nat) (h : UpperDomain r p u v) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 7) ∧
      (∀ i, i < 2 * r + 7 →
        columnSum d (2 * r + 7) i = initial r p u v i) ∧
      ∃ a da e, 0 < a ∧ Canonical a da (2 * r + 7) ∧
        (∀ i, i < 2 * r + 7 →
          columnSum da (2 * r + 7) i = rebasedComponent r p u v i) ∧
        Canonical (orbit n 2) e (2 * r + 8) ∧
        ∀ i, i < 2 * r + 8 →
          columnSum e (2 * r + 8) i =
            shiftOne (finiteWord (2 * r + 7) (columnSum da (2 * r + 7))) i := by
  obtain ⟨n, d, hn, hc, hr⟩ := upper_initial_realizable r p u v h
  exact ⟨n, d, hn, hc, hr, numeric_rebased_realization n d r p u v h hc hr⟩

/-- This realization does not identify the new component with the actual
old component orbit: their difference at the first corrected flank is one. -/
theorem rebased_differs_at_flank (r p u v : Nat) (h : UpperDomain r p u v) :
    (rebasedComponent r p u v (r + 1) : Int) -
      ((componentOrbit r p u v 2).2 (r + 1) : Int) = 1 := by
  have he := rebasedInt_actual_component r p u v h (r + 1)
  have hc := rebased_toNat_exact r p u v h (r + 1)
  have hw := (component_two_step_upper r p u v h).1
  have hi : r + 1 < 2 * r + 7 := by omega
  simp only [finiteWord, hw, hi, if_true, rebaseDelta, true_or] at he
  omega

end Agent100.GroupIIRebase

#print axioms Agent100.GroupIIRebase.actual_whole_rebased
#print axioms Agent100.GroupIIRebase.rebased_component_realizable
#print axioms Agent100.GroupIIRebase.numeric_rebased_overlap
#print axioms Agent100.GroupIIRebase.numeric_rebased_realization
#print axioms Agent100.GroupIIRebase.realized_rebased_overlap
#print axioms Agent100.GroupIIRebase.rebased_differs_at_flank
