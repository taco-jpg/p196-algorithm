import Agent108WindowDefs
import Mathlib.Data.Real.Archimedean
import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Algebra.Order.Field.Power
import Mathlib.Data.List.Nodup
import Mathlib.Tactic.Linarith

/-!
Agent #108, session b31b8818: finite binary sums and real growth algebra.

This module proves a generic weighted-family lower-bound interface.  The
`incoming` function is arbitrary.  Applying the final obstruction to an
actual reverse-and-add incoming operator requires a separate proof of the
displayed family-total identity and its inclusion lower bound.  Neither
an arithmetic transition nor an infinite nonpalindromicity claim is made
by this interface.
-/

namespace Agent108.WindowWeights

noncomputable section

/-- The product of beta for each true choice and 1 for each false choice. -/
def binaryWeight (beta : ℝ) : List Bool → ℝ
  | [] => 1
  | false :: es => binaryWeight beta es
  | true :: es => beta * binaryWeight beta es

theorem binaryWeight_eq_prod (beta : ℝ) (es : List Bool) :
    binaryWeight beta es = (es.map (fun e => if e then beta else 1)).prod := by
  induction es with
  | nil => simp [binaryWeight]
  | cons e es ih => cases e <;> simp [binaryWeight, ih]

theorem binaryWeight_pos {beta : ℝ} (hbeta : 0 < beta) (es : List Bool) :
    0 < binaryWeight beta es := by
  induction es with
  | nil => simp [binaryWeight]
  | cons e es ih =>
      cases e with
      | false => simpa [binaryWeight] using ih
      | true => simpa [binaryWeight] using mul_pos hbeta ih

theorem choices_mem_length (r : ℕ) {es : List Bool} (hes : es ∈ choices r) :
    es.length = r := by
  induction r generalizing es with
  | zero =>
      simp only [choices, List.mem_singleton] at hes
      simp [hes]
  | succ r ih =>
      simp only [choices, List.mem_append, List.mem_map] at hes
      rcases hes with ⟨es, hmem, rfl⟩ | ⟨es, hmem, rfl⟩ <;> simp [ih hmem]

theorem choices_nodup (r : ℕ) : (choices r).Nodup := by
  induction r with
  | zero => simp [choices]
  | succ r ih =>
      rw [choices]
      apply List.Nodup.append
      · exact List.Nodup.map (fun _ _ h => (List.cons.inj h).2) ih
      · exact List.Nodup.map (fun _ _ h => (List.cons.inj h).2) ih
      · intro es hfalse htrue
        obtain ⟨a, _, ha⟩ := List.mem_map.mp hfalse
        obtain ⟨b, _, hb⟩ := List.mem_map.mp htrue
        have h : false :: a = true :: b := ha.trans hb.symm
        exact Bool.false_ne_true (List.cons.inj h).1

theorem sum_map_real_mul {α : Type} (c : ℝ) (f : α → ℝ) (xs : List α) :
    (xs.map (fun x => c * f x)).sum = c * (xs.map f).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih, mul_add]

/-- Exact sum over every binary choice, with each choice occurring once. -/
theorem weighted_choices_sum (beta : ℝ) (r : ℕ) :
    ((choices r).map (binaryWeight beta)).sum = (1 + beta) ^ r := by
  induction r with
  | zero => simp [choices, binaryWeight]
  | succ r ih =>
      simp only [choices, List.map_append, List.sum_append, List.map_map,
        Function.comp_def]
      change ((choices r).map (binaryWeight beta)).sum +
        ((choices r).map (fun es => beta * binaryWeight beta es)).sum = _
      rw [sum_map_real_mul, ih, pow_succ]
      ring

/-- Transport a pointwise family formula into its exact finite total. -/
theorem weighted_family_total (r : ℕ) (C targetWeight beta : ℝ)
    (weight : List Bool → ℝ)
    (hweight : ∀ es ∈ choices r, weight es = C * targetWeight * binaryWeight beta es) :
    ((choices r).map weight).sum = C * targetWeight * (1 + beta) ^ r := by
  rw [List.map_congr_left hweight, sum_map_real_mul, weighted_choices_sum]

/-- Positive prefactors preserve unbounded growth of a real base above one. -/
theorem scaled_pow_unbounded (C beta : ℝ) (hC : 0 < C) (hbeta : 0 < beta)
    (K : ℝ) : ∃ r : ℕ, K < C * (1 + beta) ^ r := by
  obtain ⟨r, hr⟩ := pow_unbounded_of_one_lt (K / C)
    (show (1 : ℝ) < 1 + beta by linarith)
  refine ⟨r, ?_⟩
  have h := (div_lt_iff₀ hC).mp hr
  simpa only [mul_comm] using h

/-- A uniform positive geometric subfamily lower bound beats every constant. -/
theorem incoming_exceeds_every_constant
    (C beta : ℝ) (hC : 0 < C) (hbeta : 0 < beta)
    (targetWeight incoming : ℕ → ℝ)
    (htarget : ∀ r, 0 < targetWeight r)
    (hlower : ∀ r, C * targetWeight r * (1 + beta) ^ r ≤ incoming r)
    (K : ℝ) : ∃ r, K * targetWeight r < incoming r := by
  obtain ⟨r, hr⟩ := scaled_pow_unbounded C beta hC hbeta K
  refine ⟨r, lt_of_lt_of_le ?_ (hlower r)⟩
  have h := mul_lt_mul_of_pos_right hr (htarget r)
  calc
    K * targetWeight r < (C * (1 + beta) ^ r) * targetWeight r := h
    _ = C * targetWeight r * (1 + beta) ^ r := by ring

/-- Conditional family-total interface; no concrete incoming map is assumed. -/
theorem no_uniform_bound_of_family_total
    (C beta : ℝ) (hC : 0 < C) (hbeta : 0 < beta)
    (targetWeight familyTotal incoming : ℕ → ℝ)
    (htarget : ∀ r, 0 < targetWeight r)
    (hfamily : ∀ r, familyTotal r = C * targetWeight r * (1 + beta) ^ r)
    (hinclusion : ∀ r, familyTotal r ≤ incoming r) :
    ¬ ∃ K : ℝ, ∀ r, incoming r ≤ K * targetWeight r := by
  rintro ⟨K, hK⟩
  have hlower (r : ℕ) : C * targetWeight r * (1 + beta) ^ r ≤ incoming r := by
    rw [← hfamily r]
    exact hinclusion r
  obtain ⟨r, hr⟩ :=
    incoming_exceeds_every_constant C beta hC hbeta targetWeight incoming htarget hlower K
  exact (not_lt_of_ge (hK r)) hr

end Agent108.WindowWeights
