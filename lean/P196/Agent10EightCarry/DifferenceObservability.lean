import P196.Agent10EightCarry.ActualCarryObservability

/-!
Agent #10: improving carry reconstruction by controlling neighboring differences.
All coefficient bounds refer to actual zero-extended pair differences.
The polynomial rigidity lemma has no width, degree, or search-cap hypothesis.
-/
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace DifferenceObservability
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open CarryObservabilityActual

abbrev Series := Nat → Int

def smooth (f : Series) (i : Nat) : Int :=
  f i + if i = 0 then 0 else f (i - 1)

def smoothPow : Nat → Series → Series
  | 0, f => f
  | k + 1, f => smooth (smoothPow k f)

def cappedDiff (q r : Nat → Nat) (L : Nat) : Series :=
  fun i => if i < L then (q i : Int) - r i else 0

theorem smoothPow_zero_below (f : Series) (m k : Nat)
    (hz : ∀ j, j < m → f j = 0) :
    ∀ j, j < m → smoothPow k f j = 0 := by
  induction k with
  | zero => exact hz
  | succ k ih =>
    intro j hj
    simp only [smoothPow, smooth, ih j hj]
    by_cases h : j = 0
    · simp [h]
    · have hh := ih (j - 1) (by omega)
      simp [h, hh]

theorem smoothPow_tail (f : Series) (m k : Nat)
    (hz : ∀ j, j < m → f j = 0) :
    ∀ i, smoothPow k (fun j => f (m + j)) i = smoothPow k f (m + i) := by
  induction k with
  | zero => intro i; rfl
  | succ k ih =>
    intro i
    simp only [smoothPow, smooth, ih]
    by_cases hi : i = 0
    · subst i
      simp only [Nat.add_zero, if_pos rfl, Int.add_zero]
      by_cases hm : m = 0
      · simp [hm]
      · have hh := smoothPow_zero_below f m k hz (m - 1) (by omega)
        simp [hm, hh]
    · have hmi : m + i ≠ 0 := by omega
      have he : m + i - 1 = m + (i - 1) := by omega
      simp [hi, hmi, he]

theorem smooth_five_coefficients (f : Series) :
    smoothPow 5 f 0 = f 0 ∧
    smoothPow 5 f 1 = 5*f 0 + f 1 ∧
    smoothPow 5 f 2 = 10*f 0 + 5*f 1 + f 2 ∧
    smoothPow 5 f 3 = 10*f 0 + 10*f 1 + 5*f 2 + f 3 := by
  simp [smoothPow, smooth]
  omega

/-- A bounded integer series cannot survive five smoothings in the unit box.
The four leading coefficients suffice; no degree or finite-state cap occurs. -/
theorem smooth_five_rigidity (f : Series)
    (hf : ∀ i, -9 ≤ f i ∧ f i ≤ 9)
    (hg : ∀ i, -1 ≤ smoothPow 5 f i ∧ smoothPow 5 f i ≤ 1) :
    ∀ i, f i = 0 := by
  intro m
  induction m using Nat.strongRecOn with
  | ind m ih =>
    have ht := smoothPow_tail f m 5 ih
    have hc := smooth_five_coefficients (fun j => f (m + j))
    simp only [Nat.add_zero] at hc
    have h0 := hg m
    have h1 := hg (m + 1)
    have h2 := hg (m + 2)
    have h3 := hg (m + 3)
    have he0 := ht 0
    simp only [Nat.add_zero] at he0
    rw [←he0, hc.1] at h0
    rw [←ht 1, hc.2.1] at h1
    rw [←ht 2, hc.2.2.1] at h2
    rw [←ht 3, hc.2.2.2] at h3
    have hf1 := hf (m + 1)
    have hf2 := hf (m + 2)
    have hf3 := hf (m + 3)
    omega

theorem cappedDiff_bounds (q r : Nat → Nat) (L : Nat)
    (hc : ∀ i, i ≤ L → carry q i = carry r i) :
    ∀ i, -9 ≤ cappedDiff q r L i ∧ cappedDiff q r L i ≤ 9 := by
  intro i
  by_cases hi : i < L
  · have hq := column_equation q i
    have hr := column_equation r i
    have hqb := output_bounded q i
    have hrb := output_bounded r i
    rw [←hc i (by omega), ←hc (i + 1) (by omega)] at hr
    simp only [cappedDiff, if_pos hi]
    omega
  · simp [cappedDiff, hi]

/-- Full zero-extended difference recurrence, including the new overflow column. -/
theorem capped_next_difference (q r : Nat → Nat) (L i : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ j, j ≤ L → carry q j = carry r j) :
    cappedDiff (nextColumns q L) (nextColumns r L) (nextWidth q L) i =
      if carry q L = 0 then 2 * cappedDiff q r L i else smooth (cappedDiff q r L) i := by
  have hcr := hc L (Nat.le_refl L)
  by_cases ho : carry q L = 0
  · have hor : carry r L = 0 := by omega
    have hnw : nextWidth q L = L := by simp [nextWidth, ho]
    rw [if_pos ho, hnw]
    by_cases hi : i < L
    · have heq := next_column_no_overflow q L i hi hq.2.2.2.1 ho
      have her := next_column_no_overflow r L i hi hr.2.2.2.1 hor
      rw [←hc (i+1) (by omega), ←hc (L-i) (by omega),
        ←hc i (by omega), ←hc (L-1-i) (by omega)] at her
      simp only [cappedDiff, if_pos hi]
      omega
    · simp [cappedDiff, hi]
  · have hcb := carry_bounded q L hq.2.2.1 L (Nat.le_refl L)
    have hoq : carry q L = 1 := by omega
    have hor : carry r L = 1 := by omega
    have hnw : nextWidth q L = L + 1 := by simp [nextWidth, ho]
    rw [if_neg ho, hnw]
    by_cases hi : i < L + 1
    · by_cases hz : i = 0
      · subst i
        have heq := next_column_overflow_outer q L hq.1 hoq
        have her := next_column_overflow_outer r L hr.1 hor
        rw [←hc 1 (by have := hq.1; omega)] at her
        simp only [smooth, if_pos rfl, Int.add_zero, cappedDiff, if_pos hi, if_pos hq.1, if_true]
        omega
      · by_cases hil : i < L
        · have heq := next_column_overflow_interior q L i (by omega) hil hq.2.2.2.1 hoq
          have her := next_column_overflow_interior r L i (by omega) hil hr.2.2.2.1 hor
          rw [←hc (i+1) (by omega), ←hc (L-i+1) (by omega),
            ←hc i (by omega), ←hc (L-i) (by omega)] at her
          have him : i - 1 < L := by omega
          simp only [cappedDiff, if_pos hi, if_pos hil, smooth, if_neg hz, if_pos him]
          omega
        · have he : i = L := by omega
          subst i
          have hL := hq.1
          have ha := NormalizationBridge.admissible_next q L hq
          have hb := NormalizationBridge.admissible_next r L hr
          have hnr : nextWidth r L = L + 1 := by simp [nextWidth, hor]
          rw [hnw] at ha
          rw [hnr] at hb
          have hesq := ha.2.2.2.1 L (by omega)
          have hesr := hb.2.2.2.1 L (by omega)
          have hid : L + 1 - 1 - L = 0 := by omega
          rw [hid] at hesq hesr
          have heq := next_column_overflow_outer q L hL hoq
          have her := next_column_overflow_outer r L hr.1 hor
          rw [←hc 1 (by omega)] at her
          have hsq := hq.2.2.2.1 0 hL
          have hsr := hr.2.2.2.1 0 hr.1
          simp only [Nat.sub_zero] at hsq hsr
          have hlast : L - 1 < L := by omega
          simp only [cappedDiff, if_pos hi, if_neg (Nat.lt_irrefl L), smooth,
            if_neg hz, if_pos hlast, Int.zero_add, hesq, hesr]
          omega
    · have hil : ¬i < L := by omega
      have him : ¬i - 1 < L := by omega
      have hz : i ≠ 0 := by omega
      simp [cappedDiff, hi, hil, smooth, hz, him]

theorem smooth_scale (a : Int) (f : Series) (i : Nat) :
    smooth (fun j => a * f j) i = a * smooth f i := by
  by_cases h : i = 0
  · simp [smooth, h]
  · simp [smooth, h, Int.mul_add]

theorem matched_widths (q r : Nat → Nat) (L K : Nat)
    (hc : ∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    (iterPairs q L K).1 = (iterPairs r L K).1 := by
  induction K with
  | zero => rfl
  | succ K ih =>
    have hw := ih (fun t ht => hc t (by omega))
    have hh := hc K (by omega) (iterPairs q L K).1 (Nat.le_refl _)
    change nextWidth (iterPairs q L K).2 (iterPairs q L K).1 =
      nextWidth (iterPairs r L K).2 (iterPairs r L K).1
    rw [←hw]
    simp only [nextWidth, hh]

theorem orbitCount_le (q : Nat → Nat) (L K : Nat) : orbitCount q L K ≤ K := by
  have h := DecimalWidthGrowth.width_count_identity q L K
  have hw := iterPairs_width_ge_initial q L K
  change (iterPairs q L K).1 + orbitCount q L K = L + K at h
  omega

/-- Equality of complete carries cancels every affine carry term at every index.
The overflow contribution is the smoothing operator, including the extra column. -/
theorem matched_difference_formula (q r : Nat → Nat) (L K : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, cappedDiff (iterPairs q L K).2 (iterPairs r L K).2 (iterPairs q L K).1 i =
      (2:Int)^(orbitCount q L K) * smoothPow (K - orbitCount q L K) (cappedDiff q r L) i := by
  induction K with
  | zero => intro i; simp [iterPairs, orbitCount, noOverflowCount, smoothPow]
  | succ K ih =>
    have ih' := ih (fun t ht => hc t (by omega))
    have hw := matched_widths q r L K (fun t ht => hc t (by omega))
    have ha := iterPairs_admissible q L K hq
    have hb := iterPairs_admissible r L K hr
    rw [←hw] at hb
    have he := capped_next_difference (iterPairs q L K).2 (iterPairs r L K).2
      (iterPairs q L K).1
    have hN := orbitCount_le q L K
    have hf : cappedDiff (iterPairs q L K).2 (iterPairs r L K).2 (iterPairs q L K).1 =
        fun i => (2:Int)^(orbitCount q L K) *
          smoothPow (K - orbitCount q L K) (cappedDiff q r L) i := funext ih'
    intro i
    change cappedDiff
      (nextColumns (iterPairs q L K).2 (iterPairs q L K).1)
      (nextColumns (iterPairs r L K).2 (iterPairs r L K).1)
      (nextWidth (iterPairs q L K).2 (iterPairs q L K).1) i = _
    rw [←hw, he i ha hb (hc K (by omega))]
    by_cases ho : carry (iterPairs q L K).2 (iterPairs q L K).1 = 0
    · have hn : orbitCount q L (K + 1) = orbitCount q L K + 1 := by
        simp only [orbitCount, noOverflowCount, ho, if_true]
      have hh : K + 1 - (orbitCount q L K + 1) = K - orbitCount q L K := by omega
      rw [if_pos ho, ih' i, hn, hh, Int.pow_succ]
      simp only [Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
    · have hn : orbitCount q L (K + 1) = orbitCount q L K := by
        simp only [orbitCount, noOverflowCount, ho, if_false, Nat.add_zero]
      have hh : K + 1 - orbitCount q L K = (K - orbitCount q L K) + 1 := by omega
      rw [if_neg ho, hf, hn, hh, smoothPow, smooth_scale]

/-- Eight actual transitions contain at least three nonoverflow steps.
This follows from the checked nine-step bound, since one extra step adds at most one. -/
theorem actual_eight_step_count (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) : 3 ≤ orbitCount q L 8 := by
  have h := actual_nine_step_count_all_widths q L hq
  change 4 ≤ orbitCount q L 8 +
    (if carry (iterPairs q L 8).2 (iterPairs q L 8).1 = 0 then 1 else 0) at h
  split at h <;> omega

/-- Nine complete carry words determine every initial pair sum at every
positive admissible decimal width. No all-time safety assertion is made. -/
theorem nine_carry_words_determine_pair_sums (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 9 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i = r i := by
  by_cases hN : 4 ≤ orbitCount q L 8
  · apply iterPairs_endpoint_carry_history_injective q r L 8 hq hr
    · intro t ht i hi
      exact hc t (by omega) i hi
    · exact hN
  · have hlo := actual_eight_step_count q L hq
    have hn : orbitCount q L 8 = 3 := by omega
    have hf := matched_difference_formula q r L 8 hq hr (fun t ht => hc t (by omega))
    have hb := cappedDiff_bounds (iterPairs q L 8).2 (iterPairs r L 8).2
      (iterPairs q L 8).1 (hc 8 (by decide))
    have hsmall : ∀ i, -1 ≤ smoothPow 5 (cappedDiff q r L) i ∧
        smoothPow 5 (cappedDiff q r L) i ≤ 1 := by
      intro i
      have he := hf i
      rw [hn] at he
      change cappedDiff (iterPairs q L 8).2 (iterPairs r L 8).2 (iterPairs q L 8).1 i =
        8 * smoothPow 5 (cappedDiff q r L) i at he
      have h := hb i
      rw [he] at h
      omega
    have hzero := smooth_five_rigidity (cappedDiff q r L)
      (cappedDiff_bounds q r L (hc 0 (by decide))) hsmall
    intro i hi
    have h := hzero i
    simp only [cappedDiff, if_pos hi] at h
    omega

/-- Numeric consequence of the nine-word theorem: the next integer is fixed,
while the initial digit splitting can still differ. -/
theorem nine_carry_words_determine_next_integer
    (n m : Nat) (d e : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m e L)
    (hc : ∀ t, t < 9 → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) :
    Lychrel196.step n = Lychrel196.step m := by
  have hq := NormalizationBridge.canonical_admissible n d L hn
  have hr := NormalizationBridge.canonical_admissible m e L hm
  have he := nine_carry_words_determine_pair_sums (columnSum d L) (columnSum e L) L hq hr hc
  calc
    Lychrel196.step n = value (columnSum d L) L :=
      step_eq_word_value n d (columnSum d L) L hn (by intro i hi; rfl)
    _ = value (columnSum e L) L := value_congr _ _ L he
    _ = Lychrel196.step m :=
      (step_eq_word_value m e (columnSum e L) L hm (by intro i hi; rfl)).symm

#print axioms smoothPow_zero_below
#print axioms smoothPow_tail
#print axioms smooth_five_coefficients
#print axioms smooth_five_rigidity
#print axioms cappedDiff_bounds
#print axioms capped_next_difference
#print axioms smooth_scale
#print axioms matched_widths
#print axioms orbitCount_le
#print axioms matched_difference_formula
#print axioms actual_eight_step_count
#print axioms nine_carry_words_determine_pair_sums
#print axioms nine_carry_words_determine_next_integer
end DifferenceObservability
