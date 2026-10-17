import P196.Foundations.Agent1PeriodicWidthPath
import P196.Foundations.Agent1PeriodicNines
import P196.Foundations.Agent1PeriodicPhase
import P196.Foundations.Agent1PeriodicZeroPeriod

/-!
Finite phase persistence conditional on a return to the all-nine phase.
The existing actual nine update has only zero, nine and eighteen outputs;
zero and eighteen absorb subsequent bounded phase updates. This module
asserts neither unconditional nine persistence nor a full tuple return.
-/

namespace Agent1.Periodic
open Agent8

private theorem rawPeriod_eighteen_absorbing (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) :
    rawPeriod B H [18,18,18,18] = [18,18,18,18] := by
  have hw : Bounded [18,18,18,18] 18 := by
    intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false, or_self] at hx
    subst x
    exact Nat.le_refl _
  rw [rawPeriod_eq_phaseImage B H [18,18,18,18] hB hH hw rfl (by decide)]
  have hg : rawGamma B H [18,18,18,18] ≤ 1 :=
    scan_carry_le_one B H [18,18,18,18] hB hH hw
  have hc : rawGamma B H [18,18,18,18] = 0 ∨
      rawGamma B H [18,18,18,18] = 1 := by omega
  rcases hc with hc | hc <;> rw [hc] <;> rfl

private theorem rawPeriod_nines_trichotomy (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) :
    rawPeriod B H [9,9,9,9] = [9,9,9,9] ∨
      rawPeriod B H [9,9,9,9] = [0,0,0,0] ∨
      rawPeriod B H [9,9,9,9] = [18,18,18,18] := by
  obtain ⟨ha, hb⟩ := nines_entry_bits B H hB hH
  have hs : leftEntry B + rightEntry B H [9,9,9,9] = 0 ∨
      leftEntry B + rightEntry B H [9,9,9,9] = 1 ∨
      leftEntry B + rightEntry B H [9,9,9,9] = 2 := by omega
  rw [rawPeriod_nines B H hB hH]
  rcases hs with hs | hs | hs <;> rw [hs] <;> decide

private theorem quotient_path_nines_trichotomy (B H w : Nat → Word)
    (N : Nat) (hp : QuotientPath B H w N) (hw0 : w 0 = [9,9,9,9]) :
    w N = [9,9,9,9] ∨ w N = [0,0,0,0] ∨ w N = [18,18,18,18] := by
  revert hp
  induction N with
  | zero => intro _; exact Or.inl hw0
  | succ N ih =>
      intro hp
      have hprefix : QuotientPath B H w N := fun i hi => hp i (by omega)
      obtain ⟨hB, hH, _, _, _, _, hnext⟩ := hp N (by omega)
      rw [hnext]
      rcases ih hprefix with hn | hz | he
      · rw [hn]
        exact rawPeriod_nines_trichotomy (B N) (H N) hB hH
      · rw [hz, rawPeriod_zero (B N) (H N) hB hH]
        exact Or.inr (Or.inl rfl)
      · rw [he, rawPeriod_eighteen_absorbing (B N) (H N) hB hH]
        exact Or.inr (Or.inr rfl)

/-- A finite quotient path beginning and ending at four nines has that
phase at every state, including both endpoints. No original validity,
positive length, exterior return, center return or catalog premise is used. -/
theorem quotient_path_nines_phase (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hw0 : w 0 = [9,9,9,9])
    (hwN : w N = [9,9,9,9]) :
    ∀ i, i ≤ N → w i = [9,9,9,9] := by
  revert hp hwN
  induction N with
  | zero =>
      intro _ _ i hi
      have hi0 : i = 0 := by omega
      simpa only [hi0] using hw0
  | succ N ih =>
      intro hp hwN
      have hprefix : QuotientPath B H w N := fun i hi => hp i (by omega)
      have hmid : w N = [9,9,9,9] := by
        obtain ⟨hB, hH, _, _, _, _, hnext⟩ := hp N (by omega)
        rcases quotient_path_nines_trichotomy B H w N hprefix hw0 with hn | hz | he
        · exact hn
        · rw [hwN, hz, rawPeriod_zero (B N) (H N) hB hH] at hnext
          contradiction
        · rw [hwN, he, rawPeriod_eighteen_absorbing (B N) (H N) hB hH] at hnext
          contradiction
      intro i hi
      by_cases hend : i = N+1
      · simpa only [hend] using hwN
      · exact ih hprefix hmid i (by omega)

/-- Every used nine-return transition has mixed actual boundary entries.
These are computed scans of B and H, rather than freely assigned bits. -/
theorem quotient_path_nines_entry_sum (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) (hw0 : w 0 = [9,9,9,9])
    (hwN : w N = [9,9,9,9]) (i : Nat) (hi : i < N) :
    leftEntry (B i) + rightEntry (B i) (H i) [9,9,9,9] = 1 := by
  have hall := quotient_path_nines_phase B H w N hp hw0 hwN
  obtain ⟨hB, hH, _, _, _, _, hnext⟩ := hp i hi
  rw [hall i (by omega), hall (i+1) (by omega)] at hnext
  have hhead := congrArg (fun W : Word => W.headD 0) hnext
  rw [rawPeriod_nines (B i) (H i) hB hH] at hhead
  change 9 = 18 - 9*(leftEntry (B i) + rightEntry (B i) (H i) [9,9,9,9]) at hhead
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_path_nines_phase
#print axioms Agent1.Periodic.quotient_path_nines_entry_sum
