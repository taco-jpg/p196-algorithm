import P196.Foundations.LychrelDigitSums
import P196.Agent10EightCarry.PrefixCarryBound

/-!
Agent #10: actual decimal inclusion and ten-word carry-history reconstruction.
The existing integrated core is imported once. Historical resume_* modules
must not be imported alongside it, because their declarations are incorporated
in Lychrel196Research already.
-/
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace CarryObservabilityActual
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- The carry immediately inside the second-most-significant column. -/
def observedBit (q : Nat → Nat) (L : Nat) : Bool :=
  decide (carry q (L - 2) = 1)

theorem observedBit_value (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) :
    CarryObservability.innerBit (observedBit q L) = carry q (L - 2) := by
  have hb := carry_bounded q L hq (L - 2) (by omega)
  by_cases h : carry q (L - 2) = 1
  · simp [CarryObservability.innerBit, observedBit, h]
  · have hz : carry q (L - 2) = 0 := by omega
    simp [CarryObservability.innerBit, observedBit, hz]

theorem prefix_valid (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) :
    CarryObservability.Valid (q 0, q 1) := by
  have h0 := ha.2.2.1 0 ha.1
  have h1 := ha.2.2.1 1 (by omega)
  have hp := ha.2.1
  exact ⟨by omega, h0, h1⟩

theorem prefix_overflow (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) :
    CarryObservability.overflow (q 0, q 1) (observedBit q L) = carry q L := by
  have ht := (folded_carry_transition q L 0 ha.1 ha.2.2.2.1).2
  have hn := (folded_carry_transition q L 1 (by omega) ha.2.2.2.1).2
  have hid : L - 1 - 1 = L - 2 := by omega
  simp only [Nat.sub_zero] at ht
  rw [hid] at hn
  change (q 0 + (q 1 + CarryObservability.innerBit (observedBit q L)) / 10) / 10 = carry q L
  rw [observedBit_value q L ha.2.2.1, ←hn, ←ht]

/-- Exact two-column update, including the overlapping width-two/three cases. -/
theorem prefix_step_exact (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) :
    (nextColumns q L 0, nextColumns q L 1) =
      CarryObservability.next (q 0, q 1) (observedBit q L) := by
  have hb := observedBit_value q L ha.2.2.1
  have hf := prefix_overflow q L ha hL
  change (q 0 + (q 1 + CarryObservability.innerBit (observedBit q L)) / 10) / 10 = carry q L at hf
  rw [hb] at hf
  have h0 : carry q 0 = 0 := rfl
  have h1 : carry q 1 = q 0 / 10 := by simp [carry]
  have h2 : carry q 2 = (q 1 + q 0 / 10) / 10 := by simp [carry]
  have hh := (folded_carry_transition q L 1 (by omega) ha.2.2.2.1).2
  have hid : L - 1 - 1 = L - 2 := by omega
  rw [hid] at hh
  dsimp only [CarryObservability.next]
  rw [hb, hf]
  by_cases ho : carry q L = 0
  · rw [if_pos ho]
    have he0 := next_column_no_overflow q L 0 ha.1 ha.2.2.2.1 ho
    have he1 := next_column_no_overflow q L 1 (by omega) ha.2.2.2.1 ho
    simp only [Nat.zero_add, Nat.sub_zero, h0, h1, ho, hh] at he0
    simp only [hid, h1, h2, hh] at he1
    apply Prod.ext <;> dsimp only <;> omega
  · rw [if_neg ho]
    have hlast := carry_bounded q L ha.2.2.1 L (by omega)
    have hc : carry q L = 1 := by omega
    have he0 := next_column_overflow_outer q L ha.1 hc
    have he1 := next_column_overflow_interior q L 1 (by decide) (by omega) ha.2.2.2.1 hc
    rw [h1] at he0
    have hidx : L - 1 + 1 = L := by omega
    simp only [hidx, hc, h1, h2, hh, Nat.sub_self] at he1
    apply Prod.ext <;> dsimp only <;> omega

theorem cost_eq_nooverflow (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) :
    CarryObservability.cost (q 0, q 1) (observedBit q L) =
      (if carry q L = 0 then 1 else 0) := by
  unfold CarryObservability.cost
  rw [prefix_overflow q L ha hL]
  have hb := carry_bounded q L ha.2.2.1 L (by omega)
  by_cases h : carry q L = 0
  · simp [h]
  · have hc : carry q L = 1 := by omega
    simp [hc]

theorem iterPairs_width_ge_initial (q : Nat → Nat) (L t : Nat) :
    L ≤ (iterPairs q L t).1 := by
  induction t with
  | zero => exact Nat.le_refl L
  | succ t ih =>
    change L ≤ nextWidth (iterPairs q L t).2 (iterPairs q L t).1
    unfold nextWidth
    split <;> omega

abbrev orbitCount (q : Nat → Nat) (L t : Nat) : Nat :=
  noOverflowCount (fun k => (iterPairs q L k).2) (fun k => (iterPairs q L k).1) t

/-- Every actual nine-step interval starting with at least two digits has four
nonoverflow additions. The local graph certificate supplies no extra premise. -/
theorem actual_nine_step_count (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) : 4 ≤ orbitCount q L 9 := by
  let states : Nat → CarryObservability.State := fun t =>
    ((iterPairs q L t).2 0, (iterPairs q L t).2 1)
  let bits : Nat → Bool := fun t => observedBit (iterPairs q L t).2 (iterPairs q L t).1
  have hw : ∀ t, 2 ≤ (iterPairs q L t).1 := by
    intro t
    have h := iterPairs_width_ge_initial q L t
    omega
  apply CarryObservability.nine_step_trajectory_bound states bits (orbitCount q L)
  · rfl
  · intro t _
    exact prefix_valid _ _ (iterPairs_admissible q L t ha) (hw t)
  · intro t _
    exact prefix_step_exact _ _ (iterPairs_admissible q L t ha) (hw t)
  · intro t _
    change orbitCount q L t + (if carry (iterPairs q L t).2 (iterPairs q L t).1 = 0 then 1 else 0) =
      orbitCount q L t + CarryObservability.cost _ _
    rw [cost_eq_nooverflow _ _ (iterPairs_admissible q L t ha) (hw t)]

/-- Ten complete carry words identify all initial pair sums at every width >=2.
This is not an all-time prediction of those carry words or of palindrome avoidance. -/
theorem ten_carry_words_determine_pair_sums_wide (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hL : 2 ≤ L)
    (hc : ∀ t, t < 10 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i = r i := by
  apply iterPairs_endpoint_carry_history_injective q r L 9 hq hr
  · intro t ht i hi
    exact hc t (by omega) i hi
  · exact actual_nine_step_count q L hq hL

/-- Finite input agreement propagates even when irrelevant function tails differ. -/
theorem next_state_congr_upto (q r : Nat → Nat) (L : Nat)
    (he : ∀ i, i < L → q i = r i) :
    nextWidth q L = nextWidth r L ∧
      ∀ i, i < nextWidth q L → nextColumns q L i = nextColumns r L i := by
  have hc := carry_congr_upto q r L he L (Nat.le_refl L)
  constructor
  · simp only [nextWidth, hc]
  · intro i hi
    by_cases h : carry q L = 0
    · have hr : carry r L = 0 := by rw [←hc]; exact h
      have hiL : i < L := by simpa only [nextWidth, h, if_true] using hi
      have hjL : L - 1 - i < L := by omega
      simp only [nextColumns, h, hr, if_true, columnSum, reflected]
      rw [output_congr_upto q r L he i hiL,
        output_congr_upto q r L he (L - 1 - i) hjL]
    · have hr : ¬carry r L = 0 := by rw [←hc]; exact h
      simp only [nextColumns, h, hr, if_false, columnSum, reflected,
        extended_congr_upto q r L he]

theorem iterPairs_congr_upto (q r : Nat → Nat) (L t : Nat)
    (he : ∀ i, i < L → q i = r i) :
    (iterPairs q L t).1 = (iterPairs r L t).1 ∧
      ∀ i, i < (iterPairs q L t).1 →
        (iterPairs q L t).2 i = (iterPairs r L t).2 i := by
  induction t with
  | zero => exact ⟨rfl, he⟩
  | succ t ih =>
    rcases ih with ⟨hw, hp⟩
    have hn := next_state_congr_upto (iterPairs q L t).2 (iterPairs r L t).2
      (iterPairs q L t).1 hp
    constructor
    · change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 =
        nextWidth (iterPairs r L t).2 (iterPairs r L t).1
      rw [←hw]
      exact hn.1
    · intro i hi
      change nextColumns (iterPairs q L t).2 (iterPairs q L t).1 i =
        nextColumns (iterPairs r L t).2 (iterPairs r L t).1 i
      rw [←hw]
      exact hn.2 i hi

theorem orbitCount_congr (q r : Nat → Nat) (L t : Nat)
    (he : ∀ i, i < L → q i = r i) : orbitCount q L t = orbitCount r L t := by
  have hc : ∀ k, carry (iterPairs q L k).2 (iterPairs q L k).1 =
      carry (iterPairs r L k).2 (iterPairs r L k).1 := by
    intro k
    rcases iterPairs_congr_upto q r L k he with ⟨hw, hp⟩
    have h := carry_congr_upto (iterPairs q L k).2 (iterPairs r L k).2
      (iterPairs q L k).1 hp (iterPairs q L k).1 (Nat.le_refl _)
    exact h.trans (congrArg (carry (iterPairs r L k).2) hw)
  induction t with
  | zero => rfl
  | succ t ih =>
    change orbitCount q L t + (if carry (iterPairs q L t).2 (iterPairs q L t).1 = 0 then 1 else 0) =
      orbitCount r L t + (if carry (iterPairs r L t).2 (iterPairs r L t).1 = 0 then 1 else 0)
    rw [ih, hc t]

/-- Only 18 one-column inputs are checked; no all-width inference is hidden. -/
theorem singleton_nine_count :
    ∀ a : Fin 18, 4 ≤ orbitCount (fun _ => a.val + 1) 1 9 := by
  decide +kernel

/-- The nine-step count bound now includes every positive admissible width. -/
theorem actual_nine_step_count_all_widths (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) : 4 ≤ orbitCount q L 9 := by
  by_cases hL : 2 ≤ L
  · exact actual_nine_step_count q L ha hL
  · have hp := ha.1
    have heL : L = 1 := by omega
    subst L
    have hq0 := ha.2.1
    have hq0' := ha.2.2.1 0 (by decide)
    have hidx : q 0 - 1 < 18 := by omega
    have h := singleton_nine_count ⟨q 0 - 1, hidx⟩
    change 4 ≤ orbitCount (fun _ => q 0 - 1 + 1) 1 9 at h
    have heq : q 0 - 1 + 1 = q 0 := by omega
    rw [heq] at h
    have he : ∀ i, i < 1 → q i = (fun _ => q 0) i := by
      intro i hi
      have hz : i = 0 := by omega
      subst i
      rfl
    rw [orbitCount_congr q (fun _ => q 0) 1 9 he]
    exact h

/-- Ten complete consecutive carry words determine the initial pair-sum word
for every admissible decimal width. The bound is not asserted optimal. -/
theorem ten_carry_words_determine_pair_sums (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r)
    (hc : ∀ t, t < 10 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    ∀ i, i < L → q i = r i := by
  apply iterPairs_endpoint_carry_history_injective q r L 9 hq hr
  · intro t ht i hi
    exact hc t (by omega) i hi
  · exact actual_nine_step_count_all_widths q L hq

/-- Equal observed histories force equality of the NEXT ordinary integer,
not necessarily of the initial digit splitting. -/
theorem ten_carry_words_determine_next_integer
    (n m : Nat) (d e : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m e L)
    (hc : ∀ t, t < 10 → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) :
    Lychrel196.step n = Lychrel196.step m := by
  have hq := NormalizationBridge.canonical_admissible n d L hn
  have hr := NormalizationBridge.canonical_admissible m e L hm
  have he := ten_carry_words_determine_pair_sums (columnSum d L) (columnSum e L) L hq hr hc
  calc
    Lychrel196.step n = value (columnSum d L) L :=
      step_eq_word_value n d (columnSum d L) L hn (by intro i hi; rfl)
    _ = value (columnSum e L) L := value_congr _ _ L he
    _ = Lychrel196.step m :=
      (step_eq_word_value m e (columnSum e L) L hm (by intro i hi; rfl)).symm

#print axioms observedBit_value
#print axioms prefix_valid
#print axioms prefix_overflow
#print axioms prefix_step_exact
#print axioms cost_eq_nooverflow
#print axioms iterPairs_width_ge_initial
#print axioms actual_nine_step_count
#print axioms ten_carry_words_determine_pair_sums_wide
#print axioms next_state_congr_upto
#print axioms iterPairs_congr_upto
#print axioms orbitCount_congr
#print axioms singleton_nine_count
#print axioms actual_nine_step_count_all_widths
#print axioms ten_carry_words_determine_pair_sums
#print axioms ten_carry_words_determine_next_integer
end CarryObservabilityActual
