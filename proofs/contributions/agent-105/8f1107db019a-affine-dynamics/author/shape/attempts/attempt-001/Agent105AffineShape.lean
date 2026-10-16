import Agent105AffineNormalize
import Agent102RunEndpoints

/-!
Agent #105, session 8f1107db019a: eventual shape of an actual affine-run family.

The existing Agent102.widthAffine_eval supplies the exact actual List length.
This file identifies its nonnegative slope, derives a uniform-in-shift length
increment, and proves eventual constancy of the actual first symbol. Signed
slopes, negative intercepts, empty runs and empty words are all retained.
-/

namespace Agent105.AffineShape

open Agent102
open Agent105.AffineNormalize

/-- The total slope of the runs that survive affine positive-part truncation. -/
def widthSlope (rs : List RunSpec) : Nat :=
  (rs.map (fun r => r.length.positivePart.slope.toNat)).sum

/-- The intercept of Agent #102's exact eventual width affine expression. -/
def widthIntercept (rs : List RunSpec) : Int := (widthAffine rs).intercept

theorem positivePart_slope_nonneg (f : Affine) : 0 ≤ f.positivePart.slope := by
  unfold Affine.positivePart
  split
  · simp [Affine.zero]
  · rename_i h
    dsimp
    omega

theorem widthAffine_slope (rs : List RunSpec) :
    (widthAffine rs).slope = (widthSlope rs : Int) := by
  induction rs with
  | nil => rfl
  | cons r rs ih =>
    change r.length.positivePart.slope + (widthAffine rs).slope =
      ((r.length.positivePart.slope.toNat + widthSlope rs : Nat) : Int)
    rw [Int.natCast_add,
      Int.toNat_of_nonneg (positivePart_slope_nonneg r.length), ih]

theorem widthAffine_slope_nonneg (rs : List RunSpec) :
    0 ≤ (widthAffine rs).slope := by
  rw [widthAffine_slope]
  exact Int.ofNat_zero_le _

theorem widthIntercept_eq_sum (rs : List RunSpec) :
    widthIntercept rs = (rs.map (fun r => r.length.positivePart.intercept)).sum := by
  induction rs with
  | nil => rfl
  | cons r rs ih =>
    change r.length.positivePart.intercept + widthIntercept rs =
      r.length.positivePart.intercept + _
    rw [ih]

/-- Actual word length on Agent #102's explicit length cutoff. -/
theorem wordAt_length_affine (rs : List RunSpec) (k : Nat)
    (hk : lengthCutoff rs ≤ k) :
    ((wordAt rs k).length : Int) =
      (widthSlope rs : Int) * (k : Int) + widthIntercept rs := by
  rw [← widthAffine_eval rs k hk]
  simp only [Affine.eval, widthAffine_slope, widthIntercept]

theorem wordAt_length_eventually (rs : List RunSpec) :
    ∃ K : Nat, ∀ k, K ≤ k →
      ((wordAt rs k).length : Int) =
        (widthSlope rs : Int) * (k : Int) + widthIntercept rs :=
  ⟨lengthCutoff rs, fun k hk => wordAt_length_affine rs k hk⟩

/-- Every nonnegative parameter shift uses the same cutoff. The equality is
between actual natural-number List lengths, without truncating a difference. -/
theorem wordAt_length_shift (rs : List RunSpec) (k s : Nat)
    (hk : lengthCutoff rs ≤ k) :
    (wordAt rs (k + s)).length =
      (wordAt rs k).length + widthSlope rs * s := by
  have hks : lengthCutoff rs ≤ k + s := by omega
  apply Int.ofNat_inj.mp
  simp only [Int.natCast_add, Int.natCast_mul]
  rw [wordAt_length_affine rs (k + s) hks, wordAt_length_affine rs k hk]
  simp only [Int.natCast_add, Int.mul_add]
  omega

theorem wordAt_length_shift_eventually (rs : List RunSpec) :
    ∃ K : Nat, ∀ k, K ≤ k → ∀ s : Nat,
      (wordAt rs (k + s)).length =
        (wordAt rs k).length + widthSlope rs * s :=
  ⟨lengthCutoff rs, fun k hk s => wordAt_length_shift rs k s hk⟩

/-- The optional first symbol is eventually fixed; `none` records actual
empty words and is not identified with a word whose first digit is zero. -/
theorem wordAt_headOption_eventually (rs : List RunSpec) :
    ∃ d : Option Nat, ∃ K : Nat, ∀ k, K ≤ k → (wordAt rs k).head? = d := by
  induction rs with
  | nil => exact ⟨none, 0, fun _ _ => rfl⟩
  | cons r rs ih =>
    rcases lengthDichotomy r.length with hz | hp
    · obtain ⟨K₀, hzero⟩ := hz
      obtain ⟨d, K₁, hd⟩ := ih
      refine ⟨d, max K₀ K₁, ?_⟩
      intro k hk
      have hz := hzero k (Nat.le_trans (Nat.le_max_left _ _) hk)
      have ht := hd k (Nat.le_trans (Nat.le_max_right _ _) hk)
      simpa [Agent102.wordAt_cons, hz] using ht
    · obtain ⟨K, hpos⟩ := hp
      refine ⟨some r.digit, K, ?_⟩
      intro k hk
      have hp : (r.length.eval k).toNat ≠ 0 := Nat.ne_of_gt (hpos k hk)
      simp [Agent102.wordAt_cons, List.head?_replicate, hp]

theorem wordAt_headD_eventually (rs : List RunSpec) (default : Nat) :
    ∃ d K : Nat, ∀ k, K ≤ k → (wordAt rs k).headD default = d := by
  obtain ⟨d, K, hd⟩ := wordAt_headOption_eventually rs
  refine ⟨d.getD default, K, ?_⟩
  intro k hk
  simp only [List.headD_eq_head?_getD, hd k hk]

theorem wordAt_head_eventually (rs : List RunSpec) :
    ∃ d K : Nat, ∀ k, K ≤ k → (wordAt rs k).headD 0 = d :=
  wordAt_headD_eventually rs 0

/-- Head and exact width-increment data can be used on one common tail.
Strictly positive width growth remains an explicit hypothesis of applications. -/
theorem wordAt_head_width_eventually (rs : List RunSpec) :
    ∃ d K : Nat, ∀ k, K ≤ k →
      (wordAt rs k).headD 0 = d ∧
        ∀ s : Nat, (wordAt rs (k + s)).length =
          (wordAt rs k).length + widthSlope rs * s := by
  obtain ⟨d, K, hd⟩ := wordAt_head_eventually rs
  refine ⟨d, max K (lengthCutoff rs), ?_⟩
  intro k hk
  exact ⟨hd k (Nat.le_trans (Nat.le_max_left _ _) hk),
    fun s => wordAt_length_shift rs k s (Nat.le_trans (Nat.le_max_right _ _) hk)⟩

end Agent105.AffineShape

#print axioms Agent105.AffineShape.positivePart_slope_nonneg
#print axioms Agent105.AffineShape.widthAffine_slope
#print axioms Agent105.AffineShape.widthAffine_slope_nonneg
#print axioms Agent105.AffineShape.widthIntercept_eq_sum
#print axioms Agent105.AffineShape.wordAt_length_affine
#print axioms Agent105.AffineShape.wordAt_length_eventually
#print axioms Agent105.AffineShape.wordAt_length_shift
#print axioms Agent105.AffineShape.wordAt_length_shift_eventually
#print axioms Agent105.AffineShape.wordAt_headOption_eventually
#print axioms Agent105.AffineShape.wordAt_headD_eventually
#print axioms Agent105.AffineShape.wordAt_head_eventually
#print axioms Agent105.AffineShape.wordAt_head_width_eventually
