import P196.Foundations.LychrelDigitSums

/-! Exact ordinary-decimal carry-budget bounds. The operation, digit sum and
canonical width are the unchanged project definitions. This module quantifies
the size restriction which is lost on passing to the mod-nine congruence. -/
namespace Agent106.CongruenceBudget

open DecimalDigits DecimalMass DecimalQuantitativeMass Lychrel196

/-- A finite sum of coefficients bounded by `M` has its literal length bound. -/
theorem wordSum_le_constant (q : Nat → Nat) (L M : Nat)
    (hq : ∀ i, i < L → q i ≤ M) : wordSum q L ≤ M * L := by
  induction L with
  | zero => simp [wordSum]
  | succ L ih =>
      have hprev := ih (fun i hi => hq i (by omega))
      have hlast := hq L (by omega)
      simp only [wordSum, Nat.mul_succ]
      omega

/-- All actual outgoing carries, including the terminal carry, are counted. -/
theorem carryCount_le_width (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) : carryCount q L ≤ L := by
  have h := wordSum_le_constant (fun i => carry q (i + 1)) L 1
    (fun i hi => carry_bounded q L hq (i + 1) (by omega))
  simpa only [carryCount, Nat.one_mul] using h

/-- Both endpoints of the exact mass interval for a canonical numeral. -/
theorem digitSum_step_budget_of_canonical (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    digitSum (step n) ≤ 2 * digitSum n ∧
      2 * digitSum n ≤ digitSum (step n) + 9 * L := by
  have hb := digitSum_step_balance d L hc.2.1 (Or.inr hc.2.2.1)
  rw [hc.2.2.2] at hb
  have hcount := carryCount_le_width (columnSum d L) L
    (columnSum_bounded d L hc.2.1)
  constructor <;> omega

/-- An unconditional necessary condition for every actual ordinary integer step.
The zero convention is included, and no palindrome or congruence is assumed. -/
theorem digitSum_step_budget (n : Nat) :
    digitSum (step n) ≤ 2 * digitSum n ∧
      2 * digitSum n ≤ digitSum (step n) + 9 * decimalLength n := by
  by_cases hn : n = 0
  · subst n
    have hz : step 0 = 0 := rfl
    simp only [hz, digitSum_zero, decimalLength_zero]
    omega
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    rw [decimalLength_of_canonical n d L hc]
    exact digitSum_step_budget_of_canonical n d L hc

/-- A proposed successor below the actual carry budget cannot be a true step. -/
theorem not_step_of_digitSum_budget (n m : Nat)
    (hm : digitSum m + 9 * decimalLength n < 2 * digitSum n) :
    m ≠ step n := by
  intro he
  rw [he] at hm
  have hb := (digitSum_step_budget n).2
  omega

end Agent106.CongruenceBudget

#print axioms Agent106.CongruenceBudget.wordSum_le_constant
#print axioms Agent106.CongruenceBudget.carryCount_le_width
#print axioms Agent106.CongruenceBudget.digitSum_step_budget_of_canonical
#print axioms Agent106.CongruenceBudget.digitSum_step_budget
#print axioms Agent106.CongruenceBudget.not_step_of_digitSum_budget
