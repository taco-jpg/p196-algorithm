import P196.Agent113FiveLayer.FiveLayerRows0
import P196.Agent113FiveLayer.FiveLayerRows1
import P196.Agent113FiveLayer.FiveLayerRows2
import P196.Agent113FiveLayer.FiveLayerRows3
import P196.Agent113FiveLayer.FiveLayerRows4

/-!
# Agent #113: the uniform five-layer obstruction, kernel-checked

Written source: `proofs/chat-6acee928/originals/p196_uniform_five_layer_obstruction.md`,
section 1, statements (1)–(2) (written proof only until now).

* `five_layer_strong`: if `X` has width at least five and its outer four pair
  sums are `(q0, 0, q2, 0)` with `q0 ∈ {10,12,14,16}`, `q2 ∈ {0,10,12,14,16}`,
  then no positive orbit reaches `X` at any time `t ≥ 5`. Inner positions are
  unconstrained, so this is stronger than the written statement.
* `five_layer`: the written statement. If every odd pair sum of `X` is 0 and
  every even pair sum lies in `{0,10,12,14,16}` (width at least five), then
  `orbit A 5 ≠ X` (indeed `orbit A t ≠ X` for every `t ≥ 5`) for every `A > 0`.
* `no_196_full_pattern`: no state of the orbit of 196, at any time, has the
  written pattern.
* `sharp_four`: `orbit 10000 4 = 80008`, which has the written pattern, so
  five cannot be lowered to four.

These are restricted-pattern exclusions; they do not prove that 196 is a
Lychrel number.
-/

namespace Agent113.FiveLayer

open Lychrel196 Agent113.FourColumn
open Agent113.TwoDigit (width pairAt digitAt)

theorem cert5_checked : cert5.Checked where
  rest := by
    intro r hr
    have hr' : r < 5 := hr
    have : r = 0 ∨ r = 1 ∨ r = 2 ∨ r = 3 ∨ r = 4 := by omega
    rcases this with rfl | rfl | rfl | rfl | rfl
    · exact rows0
    · exact rows1
    · exact rows2
    · exact rows3
    · exact rows4
  short := cert5_short

/-- The outer-four-column pattern (strengthened hypothesis). -/
def OuterPattern (X : Nat) : Prop :=
  5 ≤ width X ∧ pairAt X 0 ∈ [10, 12, 14, 16] ∧ pairAt X 1 = 0 ∧
    pairAt X 2 ∈ [0, 10, 12, 14, 16] ∧ pairAt X 3 = 0

/-- The written pattern (1): every odd pair sum is 0, every even pair sum is
in {0,10,12,14,16}; width at least five. -/
def FullPattern (X : Nat) : Prop :=
  5 ≤ width X ∧ ∀ j, j < width X →
    (j % 2 = 1 → pairAt X j = 0) ∧ (j % 2 = 0 → pairAt X j ∈ [0, 10, 12, 14, 16])

theorem outer_in_layer0 (X : Nat) (h : OuterPattern X) :
    cert5.inLayer 0 (quad X) = true := by
  obtain ⟨_, h0, h1, h2, h3⟩ := h
  simp only [quad, h1, h3]
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at h0 h2
  rcases h0 with h0 | h0 | h0 | h0 <;> rcases h2 with h2 | h2 | h2 | h2 | h2 <;>
    (rw [h0, h2]; decide)

/-- Strengthened five-layer obstruction. -/
theorem five_layer_strong :
    ∀ A t X, 0 < A → orbit A t = X → OuterPattern X → t < 5 := by
  intro A t X hA hrun hX
  have hw4 : 4 ≤ width X := by have := hX.1; omega
  exact cert5.depth_bound cert5_checked A t X hA hrun hw4 (outer_in_layer0 X hX)

theorem pairAt_zero_pos (X : Nat) (hX : 0 < X) : 1 ≤ pairAt X 0 := by
  obtain ⟨d, L, hcan⟩ := DecimalDigits.canonical_exists X hX
  rw [Agent113.TwoDigit.canonical_pairAt hcan 0 hcan.1]
  have := hcan.2.2.1
  simp only [DecimalDigits.columnSum, DecimalDigits.reflected, Nat.sub_zero]
  omega

theorem full_to_outer (X : Nat) (h : FullPattern X) : OuterPattern X := by
  obtain ⟨hw, hall⟩ := h
  have hX : 0 < X := by
    rcases Nat.eq_zero_or_pos X with h0 | h0
    · subst h0
      have : width 0 = 0 := DecimalQuantitativeMass.decimalLength_zero
      omega
    · exact h0
  have p0 := (hall 0 (by omega)).2 rfl
  have p1 := (hall 1 (by omega)).1 rfl
  have p2 := (hall 2 (by omega)).2 rfl
  have p3 := (hall 3 (by omega)).1 rfl
  have hpos := pairAt_zero_pos X hX
  refine ⟨hw, ?_, p1, p2, p3⟩
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at p0 ⊢
  omega

/-- The written five-layer obstruction: `T^5(A) = X` is impossible, and so is
`T^t(A) = X` for every `t ≥ 5`. -/
theorem five_layer (A X : Nat) (hA : 0 < A) (hX : FullPattern X) :
    ∀ t, 5 ≤ t → orbit A t ≠ X := by
  intro t ht hrun
  have := five_layer_strong A t X hA hrun (full_to_outer X hX)
  omega

theorem width_lt_five (m : Nat) (hm : 0 < m) (h : m < 10000) : width m < 5 := by
  have := width_le_of_lt m 4 hm (by simpa using h)
  omega

/-- No state of the orbit of 196 has the written pattern, at any time. -/
theorem no_196_full_pattern : ∀ t, ¬ FullPattern (orbit 196 t) := by
  intro t ht
  rcases Nat.lt_or_ge t 5 with h | h
  · have o : orbit 196 0 = 196 ∧ orbit 196 1 = 887 ∧ orbit 196 2 = 1675 ∧
        orbit 196 3 = 7436 ∧ orbit 196 4 = 13783 := by decide
    have hw := ht.1
    have : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 := by omega
    rcases this with rfl | rfl | rfl | rfl | rfl
    · rw [o.1] at hw; have := width_lt_five 196 (by decide) (by decide); omega
    · rw [o.2.1] at hw; have := width_lt_five 887 (by decide) (by decide); omega
    · rw [o.2.2.1] at hw; have := width_lt_five 1675 (by decide) (by decide); omega
    · rw [o.2.2.2.1] at hw; have := width_lt_five 7436 (by decide) (by decide); omega
    · rw [o.2.2.2.2] at ht
      have hw5 : width 13783 = 5 := width_eq_of_bounds 13783 4 (by decide) (by decide)
      have p1 := (ht.2 1 (by rw [hw5]; decide)).1 rfl
      simp only [pairAt, hw5, digitAt] at p1
      exact absurd p1 (by decide)
  · exact five_layer 196 (orbit 196 t) (by decide) ht t h rfl

/-- Sharpness: four steps are possible. -/
theorem sharp_four : orbit 10000 4 = 80008 ∧ FullPattern 80008 := by
  refine ⟨by decide, ?_⟩
  have hw5 : width 80008 = 5 := width_eq_of_bounds 80008 4 (by decide) (by decide)
  refine ⟨by rw [hw5]; decide, ?_⟩
  intro j hj
  rw [hw5] at hj
  have : j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 := by omega
  rcases this with rfl | rfl | rfl | rfl | rfl <;>
    (simp only [pairAt, hw5, digitAt]; decide)

#print axioms cert5_checked
#print axioms five_layer_strong
#print axioms five_layer
#print axioms no_196_full_pattern
#print axioms sharp_four

end Agent113.FiveLayer
