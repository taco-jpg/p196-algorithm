import SeamMaskRealizability

/-! Construct all seam masses by selecting the last m actual active nines. -/
namespace Agent123.SeamMasks
open DecimalDigits RawSymmetryObstruction

def activeAt (q : Nat → Nat) (i : Nat) : Prop := q i = 9 ∧ carry q i = 1
instance (q : Nat → Nat) (i : Nat) : Decidable (activeAt q i) :=
  inferInstanceAs (Decidable (q i = 9 ∧ carry q i = 1))

def activeCount (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | L + 1 => activeCount q L + if activeAt q L then 1 else 0

def maskMass (k : Nat → Nat) : Nat → Nat
  | 0 => 0
  | L + 1 => maskMass k L + k L

def defectMass (q : Nat → Nat) (cut : Nat → Bool) : Nat → Int
  | 0 => 0
  | L + 1 => defectMass q cut L + seamDefect q cut L

/-- Select the active positions with zero-based active rank at least t. -/
def rankMask (q : Nat → Nat) (t i : Nat) : Nat :=
  if activeAt q i ∧ t ≤ activeCount q i then 1 else 0

theorem activeCount_succ_ge (q : Nat → Nat) (i : Nat) :
    activeCount q i ≤ activeCount q (i + 1) := by
  simp only [activeCount]; split <;> omega

theorem activeAt_next_nine (q : Nat → Nat) (i : Nat)
    (ha : activeAt q i) (hn : q (i + 1) = 9) : activeAt q (i + 1) := by
  refine ⟨hn, ?_⟩
  change (q i + carry q i) / 10 = 1
  rw [ha.1, ha.2]

/-- A global active-rank suffix respects every local nine-run constraint. -/
theorem rankMask_constraints (q : Nat → Nat) (L t : Nat) :
    MaskConstraints q L (rankMask q t) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i hi
    simp only [rankMask]; split <;> omega
  · intro i hi hk
    unfold rankMask at hk
    split at hk
    · rename_i h
      exact h.1
    · omega
  · intro i hi hn
    by_cases h : activeAt q i ∧ t ≤ activeCount q i
    · have ha := activeAt_next_nine q i h.1 hn
      have hc := activeCount_succ_ge q i
      have ht : t ≤ activeCount q (i + 1) := by omega
      simp [rankMask, h, ha, ht]
    · simp [rankMask, h]

/-- Exact finite count, not a sampled or externally evaluated certificate. -/
theorem rankMask_mass (q : Nat → Nat) (t L : Nat) :
    maskMass (rankMask q t) L = activeCount q L - t := by
  induction L with
  | zero => simp [maskMass, activeCount]
  | succ L ih =>
      simp only [maskMass, activeCount, rankMask, ih]
      by_cases ha : activeAt q L <;> by_cases ht : t ≤ activeCount q L <;>
        simp only [ha, ht, and_self, and_false, false_and, true_and, if_true, if_false] <;> omega

theorem defectMass_of_realizes (q : Nat → Nat) (cut : Nat → Bool) (k : Nat → Nat) :
    ∀ L, Realizes q L cut k → defectMass q cut L = (maskMass k L : Int) := by
  intro L
  induction L with
  | zero => intro _; rfl
  | succ L ih =>
      intro hk
      have hp := ih (fun i hi => hk i (by omega))
      have hl := hk L (by omega)
      simp only [defectMass, maskMass]
      omega

/-- Explicit cuts attaining any prescribed integer mass in the full interval. -/
theorem every_mass_realized (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) (m : Nat) (hm : m ≤ activeCount q L) :
    defectMass q (cutsOf (rankMask q (activeCount q L - m))) L = (m : Int) := by
  have hc := rankMask_constraints q L (activeCount q L - m)
  have hr := cutsOf_realizes q L hb _ hc
  have he := defectMass_of_realizes q _ _ L hr
  have hs := rankMask_mass q (activeCount q L - m) L
  have hsub : activeCount q L - (activeCount q L - m) = m := by omega
  rw [hsub] at hs
  rw [hs] at he
  exact he

theorem mass_at_most_activeCount (q : Nat → Nat) (L : Nat) (cut : Nat → Bool)
    (hb : ∀ i, i < L → q i ≤ 18) :
    0 ≤ defectMass q cut L ∧ defectMass q cut L ≤ (activeCount q L : Int) := by
  revert hb
  induction L with
  | zero => intro _; simp [defectMass, activeCount]
  | succ L ih =>
      intro hb
      have hp := ih (fun i hi => hb i (by omega))
      have hd := defect_bounds q (L + 1) cut hb L (by omega)
      by_cases ha : activeAt q L
      · simp only [defectMass, activeCount, if_pos ha]
        constructor <;> omega
      · have hz : seamDefect q cut L = 0 := by
          have hs := IntrinsicSeam.singleton_defect_maximal q cut L
          have hf := IntrinsicSeam.singleton_defect_iff q (L + 1) L hb (by omega)
          have hzero : seamDefect q (fun _ => true) L = 0 := by
            by_cases hn : seamDefect q (fun _ => true) L = 0
            · exact hn
            · exact False.elim (ha (hf.mp hn))
          omega
        simp only [defectMass, activeCount, if_neg ha, hz]
        constructor <;> omega

/-- The image of actual partition mass is exactly a finite integer interval. -/
theorem exists_mass_iff (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) (m : Nat) :
    (∃ cut, defectMass q cut L = (m : Int)) ↔ m ≤ activeCount q L := by
  constructor
  · rintro ⟨cut, hm⟩
    have h := mass_at_most_activeCount q L cut hb
    rw [hm] at h
    omega
  · intro hm
    exact ⟨cutsOf (rankMask q (activeCount q L - m)), every_mass_realized q L hb m hm⟩

end Agent123.SeamMasks
