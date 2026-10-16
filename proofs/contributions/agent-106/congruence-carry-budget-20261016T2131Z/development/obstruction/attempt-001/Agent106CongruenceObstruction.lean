import Agent106CarryBudget
import Agent106CongruenceSeed
import Agent106SparseTarget

/-!
The exact sparse entry jump of CONGRUENCE_PATHS.md §3 violates the
ordinary-decimal carry budget.  The family parameter is the original
floor(7R/4)+1 and the R=3 boundary is retained explicitly.
-/
namespace Agent106.CongruenceBudget

open Lychrel196 DecimalMass DecimalQuantitativeMass

def familyIndex (R : Nat) : Nat := 7 * R / 4 + 1
def familyWidth (R : Nat) : Nat := familyIndex R + 2
def familySource (R : Nat) : Nat := 11 * (10 ^ familyIndex R - 1)

theorem familyIndex_ge_two (R : Nat) (hR : 3 ≤ R) :
    2 ≤ familyIndex R := by
  unfold familyIndex
  omega

/-- The true next iterate cannot shed more digit sum than its actual
number of outgoing carry positions permits. -/
theorem dense_step_digitSum_lower (k : Nat) (hk : 2 ≤ k) :
    9 * (k + 2) ≤ digitSum (step (11 * (10 ^ k - 1))) + 36 := by
  have h := (digitSum_step_budget (11 * (10 ^ k - 1))).2
  rw [denseOutput_digitSum k hk, denseOutput_decimalLength k hk] at h
  omega

/-- The artificial entry target is strictly below that necessary interval,
including R=3, whose width eight is outside the generic tail estimate. -/
theorem sparse_family_digitSum_gap (R : Nat) (hR : 3 ≤ R) :
    digitSum (sparse (familyWidth R)) + 36 < 9 * familyWidth R := by
  by_cases he : R = 3
  · subst R
    change digitSum (sparse 8) + 36 < 9 * 8
    rw [sparse_eight_digitSum]
    decide
  · have ha : 9 ≤ familyWidth R := by
      unfold familyWidth familyIndex
      omega
    have h := sparse_digitSum_bound (familyWidth R) ha
    omega

/-- Exact two-sided separation from the actual reverse-and-add step. -/
theorem congruence_sparse_jump_separation (R : Nat) (hR : 3 ≤ R) :
    digitSum (sparse (familyWidth R)) + 36 < 9 * familyWidth R ∧
      9 * familyWidth R ≤ digitSum (step (familySource R)) + 36 := by
  constructor
  · exact sparse_family_digitSum_gap R hR
  · exact dense_step_digitSum_lower (familyIndex R) (familyIndex_ge_two R hR)

/-- The original sparse target fails the generic actual-step budget in
its unshifted form, with the true canonical width of the source. -/
theorem sparse_family_violates_actual_budget (R : Nat) (hR : 3 ≤ R) :
    digitSum (sparse (familyWidth R)) + 9 * decimalLength (familySource R) <
      2 * digitSum (familySource R) := by
  have hg := sparse_family_digitSum_gap R hR
  have hk := familyIndex_ge_two R hR
  unfold familySource
  rw [denseOutput_digitSum _ hk, denseOutput_decimalLength _ hk]
  unfold familyWidth at hg
  omega

/-- For every R≥3, the claimed sparse entry jump is not an edge of the
ordinary integer reverse-and-add dynamics. -/
theorem congruence_sparse_jump_ne_actual (R : Nat) (hR : 3 ≤ R) :
    sparse (familyWidth R) ≠ step (familySource R) := by
  exact not_step_of_digitSum_budget (familySource R) (sparse (familyWidth R))
    (sparse_family_violates_actual_budget R hR)

#print axioms familyIndex_ge_two
#print axioms dense_step_digitSum_lower
#print axioms sparse_family_digitSum_gap
#print axioms congruence_sparse_jump_separation
#print axioms sparse_family_violates_actual_budget
#print axioms congruence_sparse_jump_ne_actual

end Agent106.CongruenceBudget
