import Agent1PeriodicZeroMass

/-!
Coefficient bounds turn interface width into a bound on the actual decimal
digit sum for a zero-period template. No safety, exponent threshold, or
positivity assumption on the numerical cap is used.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

private theorem bounded_sum_le (W : Word) (hW : Bounded W 18) :
    W.sum ≤ 18 * W.length := by
  induction W with
  | nil => simp
  | cons a W ih =>
    have ha : a ≤ 18 := hW a (by simp)
    have ht : Bounded W 18 := by
      intro x hx
      exact hW x (by simp [hx])
    have hs := ih ht
    simp only [List.sum_cons, List.length_cons]
    omega

/-- The original coefficient bounds control the complete exterior-and-center
mass by eighteen times its finite interface width. -/
theorem zero_interface_mass_le (B H : Word)
    (hv : ValidPeriodic B H [0,0,0,0]) :
    2 * B.sum + H.sum ≤ 18 * (2 * B.length + H.length) := by
  have hB := bounded_sum_le B hv.outer_bounded
  have hH := bounded_sum_le H hv.center_bounded
  omega

/-- Every canonical ordinary realization of a zero-period template has digit
sum at most nine times an interface-width bound, at every exponent. -/
theorem zero_period_digitSum_le_width (B H : Word) (k n : Nat)
    (d : Nat → Nat) (M : Nat) (hv : ValidPeriodic B H [0,0,0,0])
    (hc : DecimalDigits.Canonical n d (periodicWord B H [0,0,0,0] k).length)
    (hrep : ∀ i, i < (periodicWord B H [0,0,0,0] k).length →
      DecimalDigits.columnSum d (periodicWord B H [0,0,0,0] k).length i =
        ((periodicWord B H [0,0,0,0] k)[i]?).getD 0)
    (hwidth : 2 * B.length + H.length ≤ M) :
    DecimalMass.digitSum n ≤ 9 * M := by
  have hmass := zero_interface_mass_le B H hv
  have hsum := zero_period_digitSum B H k n d hc hrep
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.zero_interface_mass_le
#print axioms Agent1.Periodic.zero_period_digitSum_le_width
