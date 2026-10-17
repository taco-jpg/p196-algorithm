import Agent1PeriodicNinesLedger
import Agent1PeriodicReturnClock

/-!
A temporal restriction on a supplied positive full return in the nine phase.
The actual clock has positive total on such a return. The exact center ledger
therefore forces an additional stripping event, and that event decreases the
center length by at least seven. Centers are nonempty because an empty center
cannot change the incoming carry in the mixed nine phase.

No return is constructed or universally excluded. In particular the result
excludes only the stated class with all source centers of length at most seven.
-/

namespace Agent1.Periodic
open Agent8

private theorem center_nonempty_of_mixed_nines (B H : Word)
    (hB : Bounded B 18)
    (hmix : leftEntry B + rightEntry B H [9,9,9,9] = 1) : H ≠ [] := by
  intro hempty
  rw [rightEntry_nines B H hB, hempty] at hmix
  simp only [terminalCarry] at hmix
  omega

private theorem ninesExtraSum_pos_index (B H : Nat → Word) (N : Nat)
    (hpos : 0 < ninesExtraSum B H N) :
    ∃ i, i < N ∧ 0 < ninesExtraStrips (B i) (H i) := by
  induction N with
  | zero => simp only [ninesExtraSum] at hpos; omega
  | succ N ih =>
      by_cases hprev : 0 < ninesExtraSum B H N
      · obtain ⟨i, hi, hr⟩ := ih hprev
        exact ⟨i, by omega, hr⟩
      · refine ⟨N, by omega, ?_⟩
        simp only [ninesExtraSum] at hpos
        omega

/-- Every positive original-valid full nine return has nonempty centers
through its endpoint and a used transition that drops at least seven entries.
The returned tuple and every carry/clock are the original computed ones. -/
theorem quotient_return_nines_center_excursion (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw0 : w 0 = [9,9,9,9]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    (∀ i, i ≤ N → H i ≠ []) ∧
      ∃ i, i < N ∧ (H (i+1)).length + 7 ≤ (H i).length := by
  have hwN : w N = [9,9,9,9] := hreturn.2.2.trans hw0
  have hphase := quotient_path_nines_phase B H w N hp hw0 hwN
  have hmixed := quotient_path_nines_entry_sum B H w N hp hw0 hwN
  have hused : ∀ i, i < N → H i ≠ [] := by
    intro i hi
    exact center_nonempty_of_mixed_nines (B i) (H i) (hp i hi).1 (hmixed i hi)
  have hnonempty : ∀ i, i ≤ N → H i ≠ [] := by
    intro i hi
    by_cases hend : i = N
    · rw [hend, hreturn.2.1]
      exact hused 0 hN
    · exact hused i (by omega)
  have hbalance := quotient_path_nines_center_balance B H w N hp hw0 hwN
  rw [hreturn.2.1] at hbalance
  obtain ⟨G, hG, hclock, _, _, _⟩ :=
    quotient_return_clock_gain B H w N hp hv hN hreturn
  have hrpos : 0 < ninesExtraSum B H N := by omega
  obtain ⟨i, hi, hri⟩ := ninesExtraSum_pos_index B H N hrpos
  obtain ⟨hB, hH, hw, _, _, hnext, _⟩ := hp i hi
  have hwi := hphase i (by omega)
  have hlocal := quotientCenter_nines_length_balance (B i) (H i) hB hH (hmixed i hi)
  have hgamma := scan_carry_le_one (B i) (H i) (w i) hB hH hw
  change rawGamma (B i) (H i) (w i) ≤ 1 at hgamma
  rw [hwi] at hnext hgamma
  rw [← hnext] at hlocal
  exact ⟨hnonempty, i, hi, by omega⟩

/-- The original quotient has no positive full nine return whose source
centers all have at most seven entries. This is a restricted exclusion. -/
theorem quotient_path_nines_small_centers_no_return (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw0 : w 0 = [9,9,9,9]) (hN : 0 < N)
    (hsmall : ∀ i, i < N → (H i).length ≤ 7) :
    ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0) := by
  intro hreturn
  obtain ⟨hne, i, hi, hdrop⟩ :=
    quotient_return_nines_center_excursion B H w N hp hv hw0 hN hreturn
  have hpositive : 0 < (H (i+1)).length :=
    List.length_pos.mpr (hne (i+1) (by omega))
  have hbound := hsmall i hi
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_return_nines_center_excursion
#print axioms Agent1.Periodic.quotient_path_nines_small_centers_no_return
