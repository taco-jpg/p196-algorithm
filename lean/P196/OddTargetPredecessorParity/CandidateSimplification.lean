import P196.OddTargetPredecessorParity.CandidateBounds
import P196.Drafts.Agent108ModularAutonomy.DigitPerturbation

/-!
# The selected candidate needs only a palindrome test

Agent #6: at the width chosen by the target's leading and units digits,
the numerical interval in the candidate test follows from palindromicity.
For the shorter width, the candidate has units zero or five. The existing
reversal residue theorem then excludes a longer numeral with leading one.
-/

set_option autoImplicit false

namespace OddTargetPredecessorParity

open DecimalDigits Lychrel196 Agent101

/-- For an odd canonical target, the selected-width candidate's range
conditions are automatic once its width is at least two and it is a
palindrome. -/
theorem candidateAccepts_selectedWidth_iff
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (hodd : Y % 2 = 1) :
    candidateAccepts Y (selectedWidth e W) ↔
      2 ≤ selectedWidth e W ∧
        Palindrome (shiftedHalf Y (selectedWidth e W)) := by
  constructor
  · intro h
    exact ⟨h.1, h.2.2.2⟩
  · rintro ⟨hL, hpal⟩
    obtain ⟨K, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hY.1)
    by_cases hs : e K = 1 ∧ e 0 = 9
    · have hselected : selectedWidth e (K + 1) = K := by
        simp only [selectedWidth, Nat.add_sub_cancel, if_pos hs]
      rw [hselected] at hL hpal ⊢
      let B := 10 ^ (K - 1)
      let p := shiftedHalf Y K
      change Palindrome p at hpal
      have hpdef : p = (Y + B + 1) / 2 := rfl
      have hBpos : 0 < B := Nat.pow_pos (by decide)
      have hindex : K - 1 + 1 = K := by omega
      have hpow : 10 ^ K = B * 10 := by
        calc
          10 ^ K = 10 ^ (K - 1 + 1) := by rw [hindex]
          _ = B * 10 := by rw [Nat.pow_succ]
      have hBmod : B % 10 = 0 := by
        obtain ⟨j, hj⟩ := Nat.exists_eq_succ_of_ne_zero
          (show K - 1 ≠ 0 by omega)
        change 10 ^ (K - 1) % 10 = 0
        rw [hj, Nat.pow_succ, Nat.mul_mod]
        simp
      have hYmod : Y % 10 = 9 :=
        (ModularAutonomy.canonical_units Y (K + 1) e hY).trans hs.2
      have hdouble : p + p = Y + B + 1 := by omega
      have hpmod : p % 10 = 0 ∨ p % 10 = 5 := by omega
      have hYbounds : 10 * B ≤ Y ∧ Y < 20 * B := by
        have htail := bounded_value_lt_pow e K
          (fun i hi => hY.2.1 i (by omega))
        have hv := hY.2.2.2
        simp only [value] at hv
        rw [hs.1, Nat.one_mul, hpow] at hv
        rw [hpow] at htail
        omega
      have hlower : B ≤ p := by omega
      have hrough : p < 11 * B := by omega
      have hfit : p < 10 ^ K := by
        by_cases hfit : p < 10 ^ K
        · exact hfit
        · have hwidth : decimalWidth p (K + 1) := by
            refine ⟨by omega, ?_, ?_⟩
            · simpa only [Nat.add_sub_cancel] using (Nat.le_of_not_gt hfit)
            · rw [Nat.pow_succ, hpow]
              omega
          obtain ⟨d, hc⟩ := (decimalWidth_iff_canonical p (K + 1)).mp hwidth
          have hr := AstraModular.reverse10_mod10 p d (K + 1) hc
          have hfixed : reverse10 p = p := hpal
          rw [hfixed] at hr
          simp only [Nat.add_sub_cancel] at hr
          have hleadpos : 0 < d K := by simpa only [Nat.add_sub_cancel] using hc.2.2.1
          have hlead : d K = 5 := by omega
          have hv := hc.2.2.2
          simp only [value] at hv
          rw [hlead, hpow] at hv
          omega
      obtain ⟨d, hc⟩ := (decimalWidth_iff_canonical p K).mp
        ⟨by omega, hlower, hfit⟩
      have hr := AstraModular.reverse10_mod10 p d K hc
      have hfixed : reverse10 p = p := hpal
      rw [hfixed] at hr
      have hlead : d (K - 1) ≤ 5 := by omega
      have hupper := (canonical_leading_le_five_iff p K d hc).mp hlead
      change 2 ≤ K ∧ B ≤ p ∧ p < 6 * B ∧ Palindrome p
      exact ⟨hL, hlower, hupper, hpal⟩
    · have hselected : selectedWidth e (K + 1) = K + 1 := by
        simp only [selectedWidth, Nat.add_sub_cancel, if_neg hs]
      rw [hselected] at hL hpal ⊢
      let B := 10 ^ K
      let p := shiftedHalf Y (K + 1)
      have hpdef : p = (Y + B + 1) / 2 := rfl
      have hBpos : 0 < B := Nat.pow_pos (by decide)
      have hwidth := canonical_decimalWidth Y e (K + 1) hY
      have hYlower : B ≤ Y := hwidth.2.1
      have hYupper : Y < B * 10 := by
        simpa only [Nat.pow_succ] using hwidth.2.2
      change 2 ≤ K + 1 ∧ B ≤ p ∧ p < 6 * B ∧ Palindrome p
      exact ⟨hL, by omega, by omega, hpal⟩

#print axioms candidateAccepts_selectedWidth_iff

end OddTargetPredecessorParity
