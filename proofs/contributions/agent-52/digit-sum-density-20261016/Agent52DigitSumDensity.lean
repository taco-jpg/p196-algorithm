import Agent52Density
import Agent9DigitSumIntervalCounts

/-!
# Real lower densities of decimal digit-sum excursions

This is the decimal analytic consequence of section 6 of the retained
strengthening notes. It uses the original natural-number reverse-add orbit,
which continues after palindromes, and Agent 9's unchanged interval count.
The threshold may be zero. The seed must be positive. The denominator is
one more than the sharp escape bound because the escape window includes
both endpoints.
-/

namespace P196.Agent52.Density

open P196.Agent9.IntervalCounts

/-- A finite real error bound, uniform over every natural starting time. -/
theorem digitSum_intervalDensity_lower_bound
    (n : Nat) (hn : 0 < n) (B s N : Nat) (hN : 0 < N) :
    1 / ((DecimalUniformEscape.sharpDigitSumEscapeBound B + 1 : Nat) : ℝ) -
        1 / (N : ℝ) ≤
      intervalDensity (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t)) s N :=
  count_intervalDensity_lower_bound
    (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t))
    (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) (by omega)
    (digitSum_interval_count n hn B) s N hN

/-- One interval-length threshold controls all translates of the actual orbit. -/
theorem digitSum_intervalDensity_eventually_lower_bound
    (n : Nat) (hn : 0 < n) (B : Nat) (ε : ℝ) (hε : 0 < ε) :
    ∃ N₀ : Nat, ∀ N ≥ N₀, ∀ s : Nat,
      1 / ((DecimalUniformEscape.sharpDigitSumEscapeBound B + 1 : Nat) : ℝ) - ε ≤
        intervalDensity (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t)) s N :=
  count_intervalDensity_eventually_lower_bound
    (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t))
    (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) (by omega)
    (digitSum_interval_count n hn B) ε hε

/-- Excursions above any natural threshold have the stated real lower Banach density. -/
theorem digitSum_lowerBanachDensity (n : Nat) (hn : 0 < n) (B : Nat) :
    1 / ((DecimalUniformEscape.sharpDigitSumEscapeBound B + 1 : Nat) : ℝ) ≤
      lowerBanachDensity
        (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t)) :=
  count_lowerBanachDensity
    (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t))
    (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) (by omega)
    (digitSum_interval_count n hn B)

/-- The same lower bound holds for the actual lower asymptotic density. -/
theorem digitSum_lowerAsymptoticDensity (n : Nat) (hn : 0 < n) (B : Nat) :
    1 / ((DecimalUniformEscape.sharpDigitSumEscapeBound B + 1 : Nat) : ℝ) ≤
      lowerAsymptoticDensity
        (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t)) :=
  count_lowerAsymptoticDensity
    (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t))
    (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) (by omega)
    (digitSum_interval_count n hn B)

/-- The quantitative lower Banach density is strictly positive. -/
theorem digitSum_lowerBanachDensity_pos (n : Nat) (hn : 0 < n) (B : Nat) :
    0 < lowerBanachDensity
      (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t)) := by
  have h : (0 : ℝ) <
      1 / ((DecimalUniformEscape.sharpDigitSumEscapeBound B + 1 : Nat) : ℝ) := by
    positivity
  exact h.trans_le (digitSum_lowerBanachDensity n hn B)

/-- The quantitative lower asymptotic density is strictly positive. -/
theorem digitSum_lowerAsymptoticDensity_pos (n : Nat) (hn : 0 < n) (B : Nat) :
    0 < lowerAsymptoticDensity
      (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t)) := by
  exact (digitSum_lowerBanachDensity_pos n hn B).trans_le
    (lowerBanachDensity_le_lowerAsymptoticDensity _)

/-- The unconditional real lower Banach density bound for the ordinary orbit of 196. -/
theorem digitSum_lowerBanachDensity_196 (B : Nat) :
    1 / ((DecimalUniformEscape.sharpDigitSumEscapeBound B + 1 : Nat) : ℝ) ≤
      lowerBanachDensity
        (fun t => B < DecimalMass.digitSum (Lychrel196.orbit 196 t)) :=
  digitSum_lowerBanachDensity 196 (by decide) B

/-- The unconditional real lower asymptotic density bound for the ordinary orbit of 196. -/
theorem digitSum_lowerAsymptoticDensity_196 (B : Nat) :
    1 / ((DecimalUniformEscape.sharpDigitSumEscapeBound B + 1 : Nat) : ℝ) ≤
      lowerAsymptoticDensity
        (fun t => B < DecimalMass.digitSum (Lychrel196.orbit 196 t)) :=
  digitSum_lowerAsymptoticDensity 196 (by decide) B

#print axioms digitSum_intervalDensity_lower_bound
#print axioms digitSum_intervalDensity_eventually_lower_bound
#print axioms digitSum_lowerBanachDensity
#print axioms digitSum_lowerAsymptoticDensity
#print axioms digitSum_lowerBanachDensity_pos
#print axioms digitSum_lowerAsymptoticDensity_pos
#print axioms digitSum_lowerBanachDensity_196
#print axioms digitSum_lowerAsymptoticDensity_196

end P196.Agent52.Density
