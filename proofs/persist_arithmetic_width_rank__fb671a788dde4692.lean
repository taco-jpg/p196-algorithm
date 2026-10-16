import Std

/-!
Generic width-rank lemma for a canonical neutral core.
Concrete compensation facts are hypotheses, not verified here.
-/
namespace NeutralCoreRank

theorem bounded_width
    (c j : Nat → Nat)
    (step : ∀ t, c (t + 1) + 2 * j t = c t + 4)
    (positive : ∀ t, 1 ≤ j t)
    (not_two : ∀ t, j t ≠ 2)
    (separated : ∀ t, j t = 1 → j (t + 1) ≠ 1) :
    ∀ t, c t ≤ c 0 + 2 := by
  have stronger : ∀ t, c (t + 1) ≤ c 0 + (if j t = 1 then 2 else 0) := by
    intro t
    induction t with
    | zero =>
      have hs := step 0
      have hp := positive 0
      have hn := not_two 0
      by_cases hj : j 0 = 1
      · simp only [hj, ite_true]
        omega
      · simp only [hj, ite_false]
        omega
    | succ t ih =>
      have hs := step (t + 1)
      have hp := positive (t + 1)
      have hn := not_two (t + 1)
      have hsep := separated t
      by_cases hj : j (t + 1) = 1
      · have old : j t ≠ 1 := by
          intro hold
          exact hsep hold hj
        simp only [old, ite_false, Nat.add_zero] at ih
        simpa only [Nat.succ_eq_add_one, hj, ite_true] using
          (show c (t + 1 + 1) ≤ c 0 + 2 by omega)
      · have bound : c (t + 1) ≤ c 0 + 2 := by
          split at ih <;> omega
        simpa only [Nat.succ_eq_add_one, hj, ite_false, Nat.add_zero] using
          (show c (t + 1 + 1) ≤ c 0 by omega)
  intro t
  cases t with
  | zero => omega
  | succ t =>
    have h := stronger t
    split at h <;> omega

#print axioms bounded_width
end NeutralCoreRank
