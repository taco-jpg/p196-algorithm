import P196.Drafts.D20261015ExternalIntrinsicReviewSources.IntrinsicSeam

/-! Exact constructive characterization of partition seam masks.
Words and all arithmetic are the existing decimal coefficient semantics.
No temporal closure or palindrome-avoiding orbit is assumed or concluded. -/
namespace Agent123.SeamMasks
open DecimalDigits RawSymmetryObstruction

/-- Binary activity, with upward closure inside each consecutive nine-run. -/
def MaskConstraints (q : Nat → Nat) (L : Nat) (k : Nat → Nat) : Prop :=
  (∀ i, i < L → k i ≤ 1) ∧
  (∀ i, i < L → k i ≠ 0 → q i = 9 ∧ carry q i = 1) ∧
  (∀ i, i + 1 < L → q (i + 1) = 9 → k i ≤ k (i + 1))

def Realizes (q : Nat → Nat) (L : Nat) (cut : Nat → Bool) (k : Nat → Nat) : Prop :=
  ∀ i, i < L → seamDefect q cut i = (k i : Int)

/-- All selected positions may be cuts; redundant later cuts are harmless. -/
def cutsOf (k : Nat → Nat) (i : Nat) : Bool := decide (k i = 1)

theorem defect_zero (q : Nat → Nat) (cut : Nat → Bool) :
    seamDefect q cut 0 = 0 := by
  simp [seamDefect, carry, resetOut]

theorem defect_bounds (q : Nat → Nat) (L : Nat) (cut : Nat → Bool)
    (hb : ∀ i, i < L → q i ≤ 18) (i : Nat) (hi : i < L) :
    0 ≤ seamDefect q cut i ∧ seamDefect q cut i ≤ 1 := by
  have ha := resetOut_le_actual q cut i
  have hc := carry_bounded q L hb (i + 1) (by omega)
  simp only [seamDefect]
  constructor <;> omega

/-- Exact one-column automaton for the actual-minus-isolated carry. -/
theorem defect_succ (q : Nat → Nat) (L : Nat) (cut : Nat → Bool)
    (hb : ∀ j, j < L → q j ≤ 18) (i : Nat) (hi : i + 1 < L) :
    seamDefect q cut (i + 1) =
      if q (i + 1) = 9 then
        if cut (i + 1) then (carry q (i + 1) : Int) else seamDefect q cut i
      else 0 := by
  have hq := hb (i + 1) hi
  have hc := carry_bounded q L hb (i + 1) (by omega)
  have hr := resetOut_bounded q cut L hb i (by omega)
  have ha := resetOut_le_actual q cut i
  have hs : carry q (i + 1 + 1) = (q (i + 1) + carry q (i + 1)) / 10 := rfl
  simp only [seamDefect, hs, resetOut]
  by_cases hn : q (i + 1) = 9 <;> cases he : cut (i + 1) <;>
    simp only [hn, he, if_true, if_false, Bool.false_eq_true] <;> omega

theorem defect_persists (q : Nat → Nat) (L : Nat) (cut : Nat → Bool)
    (hb : ∀ j, j < L → q j ≤ 18) (i : Nat) (hi : i + 1 < L)
    (hn : q (i + 1) = 9) :
    seamDefect q cut i ≤ seamDefect q cut (i + 1) := by
  rw [defect_succ q L cut hb i hi, if_pos hn]
  split
  · simp only [seamDefect]; omega
  · exact Int.le_refl _

theorem realizes_constraints (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) (cut : Nat → Bool) (k : Nat → Nat)
    (hk : Realizes q L cut k) : MaskConstraints q L k := by
  refine ⟨?_, ?_, ?_⟩
  · intro i hi
    have h := defect_bounds q L cut hb i hi
    rw [hk i hi] at h
    omega
  · intro i hi hn
    have h := IntrinsicSeam.singleton_defect_maximal q cut i
    rw [hk i hi] at h
    have hs : seamDefect q (fun _ => true) i ≠ 0 := by omega
    exact (IntrinsicSeam.singleton_defect_iff q L i hb hi).mp hs
  · intro i hi hn
    have h := defect_persists q L cut hb i hi hn
    rw [hk i (by omega), hk (i + 1) hi] at h
    omega

/-- Explicit sufficiency: cut exactly at every selected coefficient. -/
theorem cutsOf_realizes (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) (k : Nat → Nat)
    (hk : MaskConstraints q L k) : Realizes q L (cutsOf k) k := by
  intro i
  induction i with
  | zero =>
      intro hi
      have hz : k 0 = 0 := by
        by_cases hn : k 0 = 0
        · exact hn
        · have hc := (hk.2.1 0 hi hn).2
          change 0 = 1 at hc
          omega
      simp [defect_zero, hz]
  | succ i ih =>
      intro hi
      have hp := ih (by omega)
      rw [defect_succ q L (cutsOf k) hb i hi]
      by_cases h1 : k (i + 1) = 1
      · have ha := hk.2.1 (i + 1) hi (by omega)
        simp [ha.1, ha.2, cutsOf, h1]
      · have hz : k (i + 1) = 0 := by have h := hk.1 (i + 1) hi; omega
        by_cases hn : q (i + 1) = 9
        · have hprev : k i = 0 := by have h := hk.2.2 i hi hn; omega
          simp [hn, cutsOf, h1, hp, hprev, hz]
        · simp [hn, hz]

/-- No quantified certificate premise remains: these local constraints are exact. -/
theorem realizable_iff (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) (k : Nat → Nat) :
    (∃ cut, Realizes q L cut k) ↔ MaskConstraints q L k := by
  constructor
  · rintro ⟨cut, hk⟩
    exact realizes_constraints q L hb cut k hk
  · intro hk
    exact ⟨cutsOf k, cutsOf_realizes q L hb k hk⟩

/-- On any all-nine interval, selection cannot disappear before the interval ends. -/
theorem selected_suffix (q : Nat → Nat) (L : Nat) (k : Nat → Nat)
    (hk : MaskConstraints q L k) (a d : Nat)
    (hL : a + d < L) (hn : ∀ i, a < i → i ≤ a + d → q i = 9)
    (ha : k a = 1) : k (a + d) = 1 := by
  revert hL hn
  induction d with
  | zero => intro _ _; simpa using ha
  | succ d ih =>
      intro hL hn
      have hp := ih (by omega) (by intro i h1 h2; exact hn i h1 (by omega))
      have hs := hk.2.2 (a + d) (by omega) (hn (a + d + 1) (by omega) (by omega))
      rw [hp] at hs
      have hb := hk.1 (a + d + 1) (by omega)
      simpa only [Nat.add_assoc] using Nat.le_antisymm hb hs

end Agent123.SeamMasks
