import P196.Foundations.Agent1PeriodicGuardFacts

/-!
The all-nine branch of the actual period-four quotient. Both incoming bits
are computed by the original finite scans. The zipper retains the actual
terminal carry; no independent clock or boundary-carry choice is introduced.
-/

namespace Agent1.Periodic

open Agent8

private theorem four_nines_carry (e : Nat) (he : e ≤ 1) :
    terminalCarry [9,9,9,9] e = e := by
  have hb : e = 0 ∨ e = 1 := by omega
  rcases hb with rfl | rfl <;> rfl

private theorem four_nines_bounded : Bounded [9,9,9,9] 18 := by
  intro x hx
  simp only [List.mem_cons, List.not_mem_nil, or_false, or_self] at hx
  subst x
  decide

/-- The original all-nine scan transmits the actual exterior carry unchanged
to the center; the center scan alone then supplies the right entry. -/
theorem rightEntry_nines (B H : Word) (hB : Bounded B 18) :
    rightEntry B H [9,9,9,9] = terminalCarry H (leftEntry B) := by
  have ha : leftEntry B ≤ 1 := terminalCarry_le_one B 0 hB (by decide)
  unfold rightEntry leftCarry
  rw [four_nines_carry _ ha]

/-- Both all-nine boundary carries are genuine computed bit carries, even
when the exterior or center is empty. -/
theorem nines_entry_bits (B H : Word) (hB : Bounded B 18) (hH : Bounded H 18) :
    leftEntry B ≤ 1 ∧ rightEntry B H [9,9,9,9] ≤ 1 := by
  have ha : leftEntry B ≤ 1 := terminalCarry_le_one B 0 hB (by decide)
  refine ⟨ha, ?_⟩
  rw [rightEntry_nines B H hB]
  exact terminalCarry_le_one H _ hH ha

/-- The literal raw all-nine period is the constant block determined by its
two actual incoming carries. The computed terminal clock may be either bit;
rotating a constant digit block leaves this exact formula unchanged. -/
theorem rawPeriod_nines (B H : Word) (hB : Bounded B 18) (hH : Bounded H 18) :
    rawPeriod B H [9,9,9,9] =
      List.replicate 4 (18 - 9*(leftEntry B + rightEntry B H [9,9,9,9])) := by
  obtain ⟨ha, hb⟩ := nines_entry_bits B H hB hH
  have hl : leftCarry B [9,9,9,9] = leftEntry B := four_nines_carry _ ha
  have hr : rightCarry B H [9,9,9,9] = rightEntry B H [9,9,9,9] := by
    change terminalCarry [9,9,9,9] (rightEntry B H [9,9,9,9]) = _
    exact four_nines_carry _ hb
  have hg : rawGamma B H [9,9,9,9] ≤ 1 :=
    scan_carry_le_one B H [9,9,9,9] hB hH four_nines_bounded
  rw [(raw_blocks_eq_zipper B H [9,9,9,9] hB hH four_nines_bounded rfl).2.1]
  unfold leftPeriodDigits rightPeriodDigits
  rw [hl, hr]
  change zipperPeriod (fixedDigits [9,9,9,9] (leftEntry B))
    (fixedDigits [9,9,9,9] (rightEntry B H [9,9,9,9])) (rawGamma B H [9,9,9,9]) = _
  have ha' : leftEntry B = 0 ∨ leftEntry B = 1 := by omega
  have hb' : rightEntry B H [9,9,9,9] = 0 ∨ rightEntry B H [9,9,9,9] = 1 := by omega
  have hg' : rawGamma B H [9,9,9,9] = 0 ∨ rawGamma B H [9,9,9,9] = 1 := by omega
  rcases ha' with ha' | ha' <;> rcases hb' with hb' | hb' <;>
    rcases hg' with hg' | hg' <;> rw [ha', hb', hg'] <;> rfl

end Agent1.Periodic

#print axioms Agent1.Periodic.rightEntry_nines
#print axioms Agent1.Periodic.nines_entry_bits
#print axioms Agent1.Periodic.rawPeriod_nines
