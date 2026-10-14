import LychrelDigitSums

/-!
# Effective digit-sum escape and running-maximum bounds

This continuation uses only Lean 4.19 and Std. It supplies a computable
decimal length, an explicit finite-time escape bound for the ordinary
decimal reverse-and-add orbit, and an exact inequality for its running
maximum digit sum. All carry propagation and numeric representation
hypotheses are discharged using the imported theorems.
-/

namespace DecimalQuantitativeMass

open DecimalDigits DecimalMass FoldedDecimal OverflowCarryNormalization
  CarryHistory Lychrel196 DecimalZeroGap DecimalUnboundedMass

/-- Canonical decimal length; zero has length zero. -/
def decimalLength (n : Nat) : Nat :=
  if h : n = 0 then 0 else decimalLength (n / 10) + 1
termination_by n
decreasing_by
  exact Nat.div_lt_self (Nat.pos_of_ne_zero h) (by decide)

theorem decimalLength_zero : decimalLength 0 = 0 := by
  rw [decimalLength]
  simp

/-- The ordinary division algorithm counts the length of every decimal
representation whose leading digit is nonzero. -/
theorem decimalLength_value (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    decimalLength (value d L) = L := by
  induction L generalizing d with
  | zero => exact decimalLength_zero
  | succ L ih =>
    have hlead' : 0 < d L := by simpa using hlead
    have hp : 0 < value d (L + 1) :=
      value_positive d (L + 1) (by omega) (by simpa using hlead')
    have hd0 := hd 0 (by omega)
    have hdiv : value d (L + 1) / 10 = value (fun i => d (i + 1)) L := by
      rw [value_shift]
      omega
    have htail : L = 0 ∨ 0 < (fun i => d (i + 1)) (L - 1) := by
      by_cases hL : L = 0
      · exact Or.inl hL
      · right
        have heq : L - 1 + 1 = L := by omega
        simpa only [heq] using hlead'
    rw [decimalLength]
    simp only [Nat.ne_of_gt hp, ↓reduceDIte]
    rw [hdiv, ih (fun i => d (i + 1)) (fun i hi => hd (i + 1) (by omega)) htail]

theorem decimalLength_of_canonical (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) : decimalLength n = L := by
  rw [← hc.2.2.2]
  exact decimalLength_value d L hc.2.1 (Or.inr hc.2.2.1)

/-- Uniform zero-run budget for a digit-sum ceiling `B`. -/
def gapBound (L B : Nat) : Nat := max L (2 * B + 2)

/-- A coarse width bound whenever all digit sums remain at most `B`. -/
def widthBound (L B : Nat) : Nat := (2 * B + 1) * (gapBound L B + 1)

/-- The guaranteed digit-sum escape horizon, retaining the initial width. -/
def escapeBound (L B : Nat) : Nat := 4 * (widthBound L B - L) + 5

theorem initial_le_widthBound (L B : Nat) : L ≤ widthBound L B := by
  have hgap : L ≤ gapBound L B := Nat.le_max_left _ _
  have hm := Nat.mul_le_mul_right (gapBound L B + 1)
    (show 1 ≤ 2 * B + 1 by omega)
  simp only [Nat.one_mul] at hm
  unfold widthBound
  omega

/-- A digit-sum bound through a finite horizon gives the same uniform
width bound at every time up to that horizon. -/
theorem bounded_prefix_width (n : Nat) (d : Nat → Nat) (L B N : Nat)
    (hc : Canonical n d L)
    (hs : ∀ t, t ≤ N → digitSum (orbit n t) ≤ B) :
    ∀ t, t ≤ N → (iterPairs (columnSum d L) L t).1 ≤ widthBound L B := by
  let q := columnSum d L
  let K := gapBound L B
  have ha : Admissible L q := NormalizationBridge.canonical_admissible n d L hc
  have hK : 2 * B + 2 ≤ K := Nat.le_max_right _ _
  have hLK : L ≤ K := Nat.le_max_left _ _
  have hm : ∀ t, t ≤ N →
      wordSum (iterPairs q L t).2 (iterPairs q L t).1 ≤ 2 * B := by
    intro t ht
    rw [iterPairs_wordSum n d q L t hc (fun _ _ => rfl)]
    exact Nat.mul_le_mul_left 2 (hs t ht)
  have hz : ∀ t, t ≤ N → ZeroBound (iterPairs q L t).2 (iterPairs q L t).1 K := by
    intro t
    induction t with
    | zero =>
      intro _ a k _ hlen _
      change a + k ≤ L at hlen
      omega
    | succ t ih =>
      intro ht
      exact zeroBound_next (iterPairs q L t).2 (iterPairs q L t).1 (2 * B) K
        (iterPairs_admissible q L t ha) (hm t (by omega)) (ih (by omega)) hK
  intro t ht
  exact length_le_of_mass_zero_runs (iterPairs q L t).2
    (iterPairs q L t).1 (2 * B) K (hm t ht) (hz t ht)

/-- A finite digit-sum ceiling constrains the elapsed time. -/
theorem bounded_prefix_time (n : Nat) (d : Nat → Nat) (L B N : Nat)
    (hc : Canonical n d L)
    (hs : ∀ t, t ≤ N → digitSum (orbit n t) ≤ B) :
    N + 4 * L ≤ 4 * widthBound L B + 4 := by
  have ha := NormalizationBridge.canonical_admissible n d L hc
  have hg := DecimalWidthGrowth.width_lower_bound (columnSum d L) L N ha
  have hw := bounded_prefix_width n d L B N hc hs N (Nat.le_refl N)
  omega

/-- Explicit escape for every canonical positive input. No initial
digit-sum bound is needed: if it already exceeds `B`, time zero works. -/
theorem digitSum_escape_of_canonical (n : Nat) (d : Nat → Nat) (L B : Nat)
    (hc : Canonical n d L) :
    ∃ t, t ≤ escapeBound L B ∧ B < digitSum (orbit n t) := by
  apply Classical.byContradiction
  intro hnone
  have hs : ∀ t, t ≤ escapeBound L B → digitSum (orbit n t) ≤ B := by
    intro t ht
    have hnot : ¬ B < digitSum (orbit n t) := by
      intro hgt
      exact hnone ⟨t, ht, hgt⟩
    omega
  have hh := bounded_prefix_time n d L B (escapeBound L B) hc hs
  have hinit := initial_le_widthBound L B
  unfold escapeBound at hh
  omega

/-- Fully numeric finite-time escape: a positive ordinary integer orbit
exceeds every digit-sum ceiling by an explicit computable horizon. -/
theorem digitSum_escape (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t ≤ escapeBound (decimalLength n) B ∧ B < digitSum (orbit n t) := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hlength := decimalLength_of_canonical n d L hc
  rw [hlength]
  exact digitSum_escape_of_canonical n d L B hc

/-- The slightly simpler coarse horizon requested without a subtraction. -/
theorem digitSum_escape_coarse (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t ≤ 4 * widthBound (decimalLength n) B + 5 ∧
      B < digitSum (orbit n t) := by
  obtain ⟨t, ht, hgt⟩ := digitSum_escape n hn B
  refine ⟨t, ?_, hgt⟩
  unfold escapeBound at ht
  omega

/-- The maximum ordinary digit sum among the first `N + 1` orbit states. -/
def runningMax (n : Nat) : Nat → Nat
  | 0 => digitSum n
  | N + 1 => max (runningMax n N) (digitSum (orbit n (N + 1)))

theorem digitSum_le_runningMax (n N t : Nat) (ht : t ≤ N) :
    digitSum (orbit n t) ≤ runningMax n N := by
  induction N with
  | zero =>
    have heq : t = 0 := by omega
    subst t
    exact Nat.le_refl _
  | succ N ih =>
    by_cases htN : t ≤ N
    · exact Nat.le_trans (ih htN) (Nat.le_max_left _ _)
    · have heq : t = N + 1 := by omega
      subst t
      exact Nat.le_max_right _ _

/-- The recursively computed running maximum is attained by an actual
state within the claimed finite horizon. -/
theorem runningMax_attained (n N : Nat) :
    ∃ t, t ≤ N ∧ digitSum (orbit n t) = runningMax n N := by
  induction N with
  | zero => exact ⟨0, Nat.le_refl _, rfl⟩
  | succ N ih =>
    by_cases hnew : runningMax n N ≤ digitSum (orbit n (N + 1))
    · refine ⟨N + 1, Nat.le_refl _, ?_⟩
      simp only [runningMax, Nat.max_eq_right hnew]
    · obtain ⟨t, ht, heq⟩ := ih
      refine ⟨t, by omega, ?_⟩
      have hold : digitSum (orbit n (N + 1)) ≤ runningMax n N := by omega
      simpa only [runningMax, Nat.max_eq_left hold] using heq

/-- Exact lower-growth constraint on the running maximum. For fixed
initial length its right side is quadratic in the maximum digit sum. -/
theorem runningMax_lower_bound (n : Nat) (hn : 0 < n) (N : Nat) :
    N + 4 * decimalLength n ≤
      4 * ((2 * runningMax n N + 1) *
        (max (decimalLength n) (2 * runningMax n N + 2) + 1)) + 4 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hlength := decimalLength_of_canonical n d L hc
  rw [hlength]
  exact bounded_prefix_time n d L (runningMax n N) N hc
    (fun t ht => digitSum_le_runningMax n N t ht)

#print axioms decimalLength_of_canonical
#print axioms bounded_prefix_time
#print axioms digitSum_escape
#print axioms digitSum_escape_coarse
#print axioms runningMax_attained
#print axioms runningMax_lower_bound

end DecimalQuantitativeMass
