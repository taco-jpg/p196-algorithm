import P196.Agent1PeriodicNineExcursion.Agent1PeriodicNinesExcursion
import P196.Agent1PeriodicNineClockStrip.Agent1PeriodicCenterNormalPath
import P196.Agent1PeriodicNineClockStrip.Agent1PeriodicNinesClockStrip

/-!
A stronger necessary center excursion on a supplied positive full nine return.
Every state of a returned quotient path is literally center-normalized. At
clock one the checked boundary ancestry theorem therefore forbids additional
stripping. A stripping event forced by the positive return clock must instead
have clock zero and remove at least eight center entries.

This excludes only the stated bounded-center class. No qualifying full return
or general no-return theorem is supplied, and no conclusion about 196 follows.
-/

namespace Agent1.Periodic
open Agent8

/-- A positive original-valid full nine return contains a center drop of at
least eight. Normalization is derived from the actual closed path. -/
theorem quotient_return_nines_center_drop_eight (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw0 : w 0 = [9,9,9,9]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    (∀ i, i ≤ N → H i ≠ []) ∧
      ∃ i, i < N ∧ (H (i+1)).length + 8 ≤ (H i).length := by
  obtain ⟨hne, i, hi, hdrop⟩ :=
    quotient_return_nines_center_excursion B H w N hp hv hw0 hN hreturn
  have hwN : w N = [9,9,9,9] := hreturn.2.2.trans hw0
  have hwi := quotient_path_nines_phase B H w N hp hw0 hwN i (by omega)
  have hmix := quotient_path_nines_entry_sum B H w N hp hw0 hwN i hi
  obtain ⟨hB, hH, hw, _, _, hnext, _⟩ := hp i hi
  have hlocal := quotientCenter_nines_length_balance (B i) (H i) hB hH hmix
  rw [hwi] at hnext
  rw [← hnext] at hlocal
  have hgamma := scan_carry_le_one (B i) (H i) (w i) hB hH hw
  change rawGamma (B i) (H i) (w i) ≤ 1 at hgamma
  rw [hwi] at hgamma
  have hgzero : rawGamma (B i) (H i) [9,9,9,9] = 0 := by
    by_cases hz : rawGamma (B i) (H i) [9,9,9,9] = 0
    · exact hz
    · have hg : rawGamma (B i) (H i) [9,9,9,9] = 1 := by omega
      have hvi : ValidPeriodic (B i) (H i) [9,9,9,9] := by
        simpa only [hwi] using quotient_path_valid B H w N hp hv i (by omega)
      have hn : stripPeriodCenter [9,9,9,9] (H i) = (H i, 0) := by
        simpa only [hwi] using
          quotient_path_return_centers_normal B H w N hp hN
            hreturn.2.1 hreturn.2.2 i (by omega)
      have hcount := centerPeriods_nines_clock_one (B i) (H i) hvi hn hmix hg
      have hformula := centerPeriods_nines_mixed (B i) (H i) hB hH hmix
      change centerPeriods (B i) (H i) [9,9,9,9] =
        ninesExtraStrips (B i) (H i) + 1 at hformula
      omega
  rw [hgzero] at hlocal
  exact ⟨hne, i, hi, by omega⟩

/-- No positive original-valid full nine return can keep all source centers
of length at most eight. No normalization premise is imposed on the input. -/
theorem quotient_path_nines_centers_le_eight_no_return (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw0 : w 0 = [9,9,9,9]) (hN : 0 < N)
    (hsmall : ∀ i, i < N → (H i).length ≤ 8) :
    ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0) := by
  intro hreturn
  obtain ⟨hne, i, hi, hdrop⟩ :=
    quotient_return_nines_center_drop_eight B H w N hp hv hw0 hN hreturn
  have hpositive : 0 < (H (i+1)).length :=
    List.length_pos.mpr (hne (i+1) (by omega))
  have hbound := hsmall i hi
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_return_nines_center_drop_eight
#print axioms Agent1.Periodic.quotient_path_nines_centers_le_eight_no_return
