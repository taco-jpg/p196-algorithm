import Agent104ExactZeroGap
import SharpProfileBounds

/-!
# Exact mass budgets along finite ordinary reverse-add orbits

The zero-gap input is a concrete property of the initial pair word. The
bounded-prefix theorem propagates it using the actual final carry, then
combines positive endpoints with the existing width growth theorem.
All arithmetic is in Nat; this file makes no real-limit or palindrome claim.
-/

namespace Agent104.FiniteMass

open DecimalDigits DecimalMass FoldedDecimal OverflowCarryNormalization
  CarryHistory Lychrel196 DecimalZeroGap DecimalUnboundedMass
  DecimalQuantitativeMass Agent104.ExactZeroGap

/-- A mass-sensitive uniform zero-gap budget. -/
def gapBound (K0 B : Nat) : Nat := max K0 (max 2 (2 * B / 9 + 1))

/-- Positive endpoints remove the two exterior gap allowances. -/
def widthBound (K0 B : Nat) : Nat :=
  2 * B + (2 * B - 1) * gapBound K0 B

/-- A computable horizon; natural subtraction also covers an immediate escape. -/
def escapeBound (L K0 B : Nat) : Nat := 4 * (widthBound K0 B - L) + 5

/-- Exact finite-prefix width control, with a supplied initial zero-gap bound. -/
theorem bounded_prefix_width (n : Nat) (d : Nat → Nat) (L K0 B N : Nat)
    (hc : Canonical n d L) (hz0 : ZeroBound (columnSum d L) L K0)
    (hs : ∀ t, t ≤ N → digitSum (orbit n t) ≤ B) :
    ∀ t, t ≤ N → (iterPairs (columnSum d L) L t).1 ≤ widthBound K0 B := by
  let q := columnSum d L
  let K := gapBound K0 B
  have ha : Admissible L q := NormalizationBridge.canonical_admissible n d L hc
  have hK0 : K0 ≤ K := Nat.le_max_left _ _
  have hK2 : 2 ≤ K :=
    Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)
  have hKq : 2 * B / 9 + 1 ≤ K :=
    Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)
  have hm : ∀ t, t ≤ N →
      wordSum (iterPairs q L t).2 (iterPairs q L t).1 ≤ 2 * B := by
    intro t ht
    rw [iterPairs_wordSum n d q L t hc (fun _ _ => rfl)]
    exact Nat.mul_le_mul_left 2 (hs t ht)
  have hz : ∀ t, t ≤ N → ZeroBound (iterPairs q L t).2 (iterPairs q L t).1 K := by
    intro t
    induction t with
    | zero =>
      intro _ a k hk hlen hzero
      have hi := hz0 a k hk hlen hzero
      exact Nat.le_trans hi hK0
    | succ t ih =>
      intro ht
      exact zeroBound_next_preserved (iterPairs q L t).2 (iterPairs q L t).1
        (2 * B) K (iterPairs_admissible q L t ha) (hm t (by omega))
        (ih (by omega)) hK2 hKq
  intro t ht
  have had := iterPairs_admissible q L t ha
  have hright : 0 < (iterPairs q L t).2 ((iterPairs q L t).1 - 1) := by
    have he := had.2.2.2.1 0 had.1
    simp only [Nat.sub_zero] at he
    rw [← he]
    exact had.2.1
  have hw := DecimalProfile.length_le_mass_gaps (iterPairs q L t).2
    (iterPairs q L t).1 K had.1 had.2.1 hright (hz t ht)
  have hmass := hm t ht
  have hmul := Nat.mul_le_mul_right K
    (show wordSum (iterPairs q L t).2 (iterPairs q L t).1 - 1 ≤ 2 * B - 1 by omega)
  change (iterPairs q L t).1 ≤ 2 * B + (2 * B - 1) * K
  omega

/-- A bounded finite digit-sum prefix constrains the elapsed time. -/
theorem bounded_prefix_time (n : Nat) (d : Nat → Nat) (L K0 B N : Nat)
    (hc : Canonical n d L) (hz0 : ZeroBound (columnSum d L) L K0)
    (hs : ∀ t, t ≤ N → digitSum (orbit n t) ≤ B) :
    N + 4 * L ≤ 4 * widthBound K0 B + 4 := by
  have ha := NormalizationBridge.canonical_admissible n d L hc
  have hg := DecimalWidthGrowth.width_lower_bound (columnSum d L) L N ha
  have hw := bounded_prefix_width n d L K0 B N hc hz0 hs N (Nat.le_refl N)
  omega

/-- Every supplied ceiling is exceeded within the improved explicit horizon. -/
theorem digitSum_escape_of_canonical (n : Nat) (d : Nat → Nat) (L K0 B : Nat)
    (hc : Canonical n d L) (hz0 : ZeroBound (columnSum d L) L K0) :
    ∃ t, t ≤ escapeBound L K0 B ∧ B < digitSum (orbit n t) := by
  apply Classical.byContradiction
  intro hnone
  have hs : ∀ t, t ≤ escapeBound L K0 B → digitSum (orbit n t) ≤ B := by
    intro t ht
    have hnot : ¬ B < digitSum (orbit n t) := by
      intro hgt
      exact hnone ⟨t, ht, hgt⟩
    omega
  have hh := bounded_prefix_time n d L K0 B (escapeBound L K0 B) hc hz0 hs
  have hinit := bounded_prefix_width n d L K0 B (escapeBound L K0 B) hc hz0 hs
    0 (Nat.zero_le _)
  change L ≤ widthBound K0 B at hinit
  unfold escapeBound at hh
  omega

/-- Every finite initial word has its width as a valid initial gap budget. -/
theorem digitSum_escape (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t ≤ escapeBound (decimalLength n) (decimalLength n) B ∧
      B < digitSum (orbit n t) := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hlength := decimalLength_of_canonical n d L hc
  rw [hlength]
  exact digitSum_escape_of_canonical n d L L B hc (by
    intro a k _ hbound _
    omega)

/-- The seed-dependent constant used in the quadratic running-maximum bound. -/
def seedConstant (K0 : Nat) : Nat := max K0 2 + 1

/-- Keep the exact quadratic leading coefficient using the quotient by nine. -/
theorem widthBound_scaled (K0 B : Nat) :
    9 * widthBound K0 B ≤ 4 * B * B + 18 * seedConstant K0 * B := by
  have hgap : gapBound K0 B + 1 ≤ seedConstant K0 + 2 * B / 9 := by
    unfold gapBound seedConstant
    omega
  have hfirst : widthBound K0 B ≤ 2 * B * (gapBound K0 B + 1) := by
    have hh := Nat.mul_le_mul_right (gapBound K0 B)
      (show 2 * B - 1 ≤ 2 * B by omega)
    unfold widthBound
    rw [Nat.mul_add, Nat.mul_one]
    omega
  have hsecond := Nat.mul_le_mul_left (2 * B) hgap
  have hthird := Nat.mul_le_mul_left 9 (Nat.le_trans hfirst hsecond)
  have hquot : 9 * (2 * B / 9) ≤ 2 * B := by omega
  have hfourth := Nat.mul_le_mul_left (2 * B) hquot
  have heq1 : 9 * (2 * B * (seedConstant K0 + 2 * B / 9)) =
      18 * seedConstant K0 * B + 2 * B * (9 * (2 * B / 9)) := by
    calc
      9 * (2 * B * (seedConstant K0 + 2 * B / 9)) =
          18 * B * seedConstant K0 + 18 * B * (2 * B / 9) := by
        simp only [Nat.mul_add, ← Nat.mul_assoc]
      _ = 18 * seedConstant K0 * B + 2 * B * (9 * (2 * B / 9)) := by
        rw [Nat.mul_right_comm 18 B (seedConstant K0)]
        congr 1
        calc
          18 * B * (2 * B / 9) = (2 * 9) * B * (2 * B / 9) := rfl
          _ = 2 * B * (9 * (2 * B / 9)) := by ac_rfl
  have heq2 : 2 * B * (2 * B) = 4 * B * B := by
    simp only [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]
  rw [heq1] at hthird
  rw [heq2] at hfourth
  omega

/-- Quadratic Nat bound for the actual running maximum, with initial gaps. -/
theorem runningMax_square_bound_of_canonical (n : Nat) (d : Nat → Nat)
    (L K0 N : Nat) (hc : Canonical n d L) (hz0 : ZeroBound (columnSum d L) L K0) :
    9 * (N + 4 * L) ≤ 16 * runningMax n N * runningMax n N +
      72 * seedConstant K0 * runningMax n N + 36 := by
  have ht := bounded_prefix_time n d L K0 (runningMax n N) N hc hz0
    (fun t htn => digitSum_le_runningMax n N t htn)
  have hw := widthBound_scaled K0 (runningMax n N)
  have ht9 : 9 * (N + 4 * L) ≤ 36 * widthBound K0 (runningMax n N) + 36 := by
    simpa only [Nat.mul_add, ← Nat.mul_assoc] using Nat.mul_le_mul_left 9 ht
  have hw4 : 36 * widthBound K0 (runningMax n N) ≤
      16 * runningMax n N * runningMax n N +
        72 * seedConstant K0 * runningMax n N := by
    simpa only [Nat.mul_add, ← Nat.mul_assoc] using Nat.mul_le_mul_left 4 hw
  exact Nat.le_trans ht9 (Nat.add_le_add_right hw4 36)

/-- A fully numeric square bound for every positive ordinary initial seed. -/
theorem runningMax_square_bound (n : Nat) (hn : 0 < n) (N : Nat) :
    9 * (N + 4 * decimalLength n) ≤ 16 * runningMax n N * runningMax n N +
      72 * seedConstant (decimalLength n) * runningMax n N + 36 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hlength := decimalLength_of_canonical n d L hc
  rw [hlength]
  exact runningMax_square_bound_of_canonical n d L L N hc (by
    intro a k _ hbound _
    omega)

#print axioms bounded_prefix_width
#print axioms bounded_prefix_time
#print axioms digitSum_escape_of_canonical
#print axioms digitSum_escape
#print axioms widthBound_scaled
#print axioms runningMax_square_bound_of_canonical
#print axioms runningMax_square_bound

end Agent104.FiniteMass
