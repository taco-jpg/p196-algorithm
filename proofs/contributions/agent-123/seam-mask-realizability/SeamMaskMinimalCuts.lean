import SeamMaskMass

/-! Least-cut realization and explicit finite-run suffix thresholds. -/
namespace Agent123.SeamMasks
open DecimalDigits RawSymmetryObstruction

/-- Only the zero-to-one frontier of the desired mask needs a cut. -/
def minimalCuts (k : Nat → Nat) : Nat → Bool
  | 0 => false
  | i + 1 => decide (k (i + 1) = 1 ∧ k i = 0)

theorem minimalCuts_realizes (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) (k : Nat → Nat)
    (hk : MaskConstraints q L k) : Realizes q L (minimalCuts k) k := by
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
      rw [defect_succ q L (minimalCuts k) hb i hi]
      by_cases h1 : k (i + 1) = 1
      · have ha := hk.2.1 (i + 1) hi (by omega)
        by_cases h0 : k i = 0
        · simp [ha.1, ha.2, minimalCuts, h1, h0]
        · have hp1 : k i = 1 := by have h := hk.1 i (by omega); omega
          simp [ha.1, minimalCuts, h1, h0, hp, hp1]
      · have hz : k (i + 1) = 0 := by have h := hk.1 (i + 1) hi; omega
        by_cases hn : q (i + 1) = 9
        · have hprev : k i = 0 := by have h := hk.2.2 i hi hn; omega
          simp [hn, minimalCuts, h1, hp, hprev, hz]
        · simp [hn, hz]

/-- Every actual realization must cut at a selected suffix's initial position. -/
theorem frontier_cut_mandatory (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) (cut : Nat → Bool) (k : Nat → Nat)
    (hr : Realizes q L cut k) (i : Nat) (hi : i + 1 < L)
    (h1 : k (i + 1) = 1) (h0 : k i = 0) : cut (i + 1) = true := by
  have hk := realizes_constraints q L hb cut k hr
  have hn := (hk.2.1 (i + 1) hi (by omega)).1
  have hs := defect_succ q L cut hb i hi
  rw [if_pos hn] at hs
  cases he : cut (i + 1) with
  | false =>
      rw [he, if_false] at hs
      rw [hr (i + 1) hi, hr i (by omega), h1, h0] at hs
      omega
  | true => rfl

/-- Least cut set, not merely some realization or a cut-count upper bound. -/
theorem minimum_partition (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) (cut : Nat → Bool) (k : Nat → Nat)
    (hr : Realizes q L cut k) :
    Realizes q L (minimalCuts k) k ∧
      ∀ i, i < L → minimalCuts k i = true → cut i = true := by
  refine ⟨minimalCuts_realizes q L hb k (realizes_constraints q L hb cut k hr), ?_⟩
  intro i hi hm
  cases i with
  | zero => simp [minimalCuts] at hm
  | succ i =>
      have h : k (i + 1) = 1 ∧ k i = 0 := by simpa [minimalCuts] using hm
      exact frontier_cut_mandatory q L hb cut k hr i hi h.1 h.2

/-- Every nine-run restriction is exactly one terminal suffix, possibly empty.
Maximality and initial activity are not needed for this stronger local form. -/
theorem suffix_threshold (q : Nat → Nat) (L : Nat) (k : Nat → Nat)
    (hk : MaskConstraints q L k) (a len : Nat)
    (hL : a + len ≤ L) (hn : ∀ i, a ≤ i → i < a + len → q i = 9) :
    ∃ r, a ≤ r ∧ r ≤ a + len ∧
      ∀ i, a ≤ i → i < a + len → (k i = 1 ↔ r ≤ i) := by
  revert hL hn
  induction len with
  | zero =>
      intro hL hn
      refine ⟨a, by omega, by omega, ?_⟩
      intro i hi hj
      omega
  | succ len ih =>
      intro hL hn
      obtain ⟨r, hra, hrb, hr⟩ := ih (by omega)
        (by intro i hi hj; exact hn i hi (by omega))
      by_cases hlast : k (a + len) = 1
      · refine ⟨r, hra, by omega, ?_⟩
        intro i hi hj
        by_cases he : i = a + len
        · subst i
          exact ⟨fun _ => hrb, fun _ => hlast⟩
        · exact hr i hi (by omega)
      · refine ⟨a + len + 1, by omega, by omega, ?_⟩
        intro i hi hj
        constructor
        · intro hki
          have hs := selected_suffix q L k hk i (a + len - i) (by omega)
            (by intro j hij hjb; exact hn j (by omega) (by omega)) hki
          have he : i + (a + len - i) = a + len := by omega
          rw [he] at hs
          exact False.elim (hlast hs)
        · intro he
          omega

end Agent123.SeamMasks
