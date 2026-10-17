import P196.Foundations.Agent1PeriodicValidity

/-!
The exact raw period and maximal quotient preserve the constant-zero period.
All carry and zipper operations are the unchanged original operations. This
module does not assert the existence or impossibility of a quotient cycle.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

private theorem four_zero_carry (e : Nat) (he : e ≤ 1) :
    terminalCarry [0,0,0,0] e = 0 := by
  have h : e / 10 = 0 := Nat.div_eq_of_lt (by omega)
  simp [terminalCarry, h]

private theorem four_zero_bounded : Bounded [0,0,0,0] 18 := by
  intro x hx
  simp only [List.mem_cons, List.not_mem_nil, or_false, or_self] at hx
  subst x
  decide

/-- The stabilized left digit period is zero even if its first copy received
an incoming carry. The original first-copy guard retains that transient. -/
theorem leftPeriodDigits_zero (B : Word) (hB : Bounded B 18) :
    leftPeriodDigits B [0,0,0,0] = [0,0,0,0] := by
  have he : leftEntry B ≤ 1 := terminalCarry_le_one B 0 hB (by decide)
  unfold leftPeriodDigits leftCarry
  rw [four_zero_carry (leftEntry B) he]
  rfl

/-- The reflected stable digit period is zero for every bounded center and
exterior; no independent carry choice is introduced. -/
theorem rightPeriodDigits_zero (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) :
    rightPeriodDigits B H [0,0,0,0] = [0,0,0,0] := by
  have he : leftEntry B ≤ 1 := terminalCarry_le_one B 0 hB (by decide)
  have hl : leftCarry B [0,0,0,0] = 0 := four_zero_carry _ he
  have hr : rightEntry B H [0,0,0,0] ≤ 1 :=
    terminalCarry_le_one H _ hH (by rw [hl]; decide)
  unfold rightPeriodDigits rightCarry
  change fixedDigits [0,0,0,0]
    (terminalCarry [0,0,0,0] (rightEntry B H [0,0,0,0])) = _
  rw [four_zero_carry _ hr]
  rfl

/-- The literal exponent-three raw slice remains four zeros, for both actual
terminal-carry cases. Only the original coefficient bounds are needed. -/
theorem rawPeriod_zero (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) :
    rawPeriod B H [0,0,0,0] = [0,0,0,0] := by
  rw [(raw_blocks_eq_zipper B H [0,0,0,0] hB hH four_zero_bounded rfl).2.1,
    leftPeriodDigits_zero B hB, rightPeriodDigits_zero B H hB hH]
  have hg : rawGamma B H [0,0,0,0] ≤ 1 :=
    scan_carry_le_one B H [0,0,0,0] hB hH four_zero_bounded
  have hc : rawGamma B H [0,0,0,0] = 0 ∨ rawGamma B H [0,0,0,0] = 1 := by omega
  rcases hc with hc | hc <;> rw [hc] <;> rfl

/-- Original full validity is preserved by the exact maximal quotient while
the period is kept literally equal to four zeros. -/
theorem zero_quotient_valid (B H : Word) (hv : ValidPeriodic B H [0,0,0,0]) :
    ValidPeriodic (quotientOuter B H [0,0,0,0])
      (quotientCenter B H [0,0,0,0]) [0,0,0,0] := by
  have h := quotient_valid B H [0,0,0,0] hv
  rw [rawPeriod_zero B H hv.outer_bounded hv.center_bounded] at h
  exact h

end Agent1.Periodic

#print axioms Agent1.Periodic.leftPeriodDigits_zero
#print axioms Agent1.Periodic.rightPeriodDigits_zero
#print axioms Agent1.Periodic.rawPeriod_zero
#print axioms Agent1.Periodic.zero_quotient_valid
