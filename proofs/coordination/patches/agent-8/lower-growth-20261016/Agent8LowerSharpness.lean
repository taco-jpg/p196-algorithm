import Agent8LowerOrbitBridge
import Agent8LowerGrowth

namespace P196.Agent8.LowerBound
open P196.Agent4.Saturation P196.Agent4.WholeWord
open DecimalDigits FoldedDecimal OverflowCarryNormalization

/-- Ordinary least-significant-first decimal digits used for concrete fixtures. -/
def fixtureDigits (n i : Nat) : Nat := n / 10^i % 10

theorem fixtureDigits_bounded (n i : Nat) : fixtureDigits n i ≤ 9 := by
  unfold fixtureDigits
  have h := Nat.mod_lt (n / 10^i) (by decide : 0 < 10)
  omega

theorem canonical120 : Canonical 120 (fixtureDigits 120) 3 := by
  refine ⟨by decide, ?_, by decide, by decide +kernel⟩
  intro i _
  exact fixtureDigits_bounded 120 i

/-- The strict potential improvement is attained by canonical decimal digits. -/
theorem realized_strict_allowance :
    prefix3 (columnSum (fixtureDigits 120) 3) = ⟨1,4,1⟩ ∧
    lower3 (prefix3 (columnSum (fixtureDigits 120) 3)) = 3 ∧
    DecimalWidthGrowth.lowerPotential 1 = 4 := by decide +kernel

/-- A concrete unconditional improvement of the initial-boundary width bound. -/
theorem orbit120_width_bound (K : Nat) :
    ∃ e W, Canonical (Lychrel196.orbit 120 K) e W ∧ K + 9 ≤ 4*W := by
  obtain ⟨e,W,hcan,hw⟩ := numeric_width_lower3 120 (fixtureDigits 120) 3 K
    canonical120 (by decide)
  have h := realized_strict_allowance.2.1
  rw [h] at hw
  exact ⟨e,W,hcan,by omega⟩

theorem canonical100 : Canonical 100 (fixtureDigits 100) 3 := by
  refine ⟨by decide, ?_, by decide, by decide +kernel⟩
  intro i _
  exact fixtureDigits_bounded 100 i

theorem canonical808 : Canonical 808 (fixtureDigits 808) 3 := by
  refine ⟨by decide, ?_, by decide, by decide +kernel⟩
  intro i _
  exact fixtureDigits_bounded 808 i

theorem orbit100_four : Lychrel196.orbit 100 4 = 808 := by decide +kernel

/-- The uniform additive constant cannot be less than four for ordinary orbits
continued through palindromes. This is not an asymptotic slope obstruction for
actual orbits, and it is not a statement about palindrome-avoiding trajectories. -/
theorem uniform_additive_constant_sharp (C : Nat)
    (h : ∀ n d L K e W, Canonical n d L → 3 ≤ L →
      Canonical (Lychrel196.orbit n K) e W → K + 4*L ≤ 4*W + C) :
    4 ≤ C := by
  have ht : Canonical (Lychrel196.orbit 100 4) (fixtureDigits 808) 3 := by
    rw [orbit100_four]
    exact canonical808
  have hc := h 100 (fixtureDigits 100) 3 4 (fixtureDigits 808) 3
    canonical100 (by decide) ht
  omega

/-- The abstract four-step boundary cycle has this finite ordinary realization.
Its third iterate is a palindrome, so the example supplies no safe infinite
orbit and does not justify periodic continuation of the abstract cycle. -/
theorem slow_cycle_finite_orbit :
    Lychrel196.orbit 159100 1 = 161051 ∧
    Lychrel196.orbit 159100 2 = 311212 ∧
    Lychrel196.orbit 159100 3 = 523325 ∧
    Lychrel196.orbit 159100 4 = 1046650 ∧
    Lychrel196.Palindrome (Lychrel196.orbit 159100 3) := by decide +kernel

theorem slow_cycle_canonical_endpoints :
    Canonical 159100 (fixtureDigits 159100) 6 ∧
    Canonical 1046650 (fixtureDigits 1046650) 7 ∧
    prefix3 (columnSum (fixtureDigits 159100) 6) = ⟨1,5,10⟩ ∧
    prefix3 (columnSum (fixtureDigits 1046650) 7) = ⟨1,5,10⟩ := by
  refine ⟨⟨by decide, ?_, by decide, by decide +kernel⟩,
    ⟨by decide, ?_, by decide, by decide +kernel⟩, by decide +kernel, by decide +kernel⟩
  · intro i _; exact fixtureDigits_bounded 159100 i
  · intro i _; exact fixtureDigits_bounded 1046650 i

#print axioms fixtureDigits_bounded
#print axioms canonical120
#print axioms realized_strict_allowance
#print axioms orbit120_width_bound
#print axioms canonical100
#print axioms canonical808
#print axioms orbit100_four
#print axioms uniform_additive_constant_sharp
#print axioms slow_cycle_finite_orbit
#print axioms slow_cycle_canonical_endpoints
end P196.Agent8.LowerBound
