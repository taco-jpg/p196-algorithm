import FourColumnConclusion

/-! Reviewer checks: (d) GrowthPrefix is exactly {110,111,121,122} on decimal
digit triples; usability of the headline theorems on concrete entries. -/

open FourColumnKernel FourColumnKernel.Certificate Lychrel196

theorem growth_exact :
    ∀ a, a < 10 → ∀ b, b < 10 → ∀ c, c < 10 →
      (GrowthPrefix a b c ↔ (100 * a + 10 * b + c = 110 ∨ 100 * a + 10 * b + c = 111 ∨
        100 * a + 10 * b + c = 121 ∨ 100 * a + 10 * b + c = 122)) := by
  decide +kernel

theorem growth_not_in_table : ∀ e ∈ table4, ¬ GrowthPrefix e.1 e.2.1 e.2.2.1 := by
  decide +kernel

theorem table4_bounds_le_14 : ∀ e ∈ table4, 1 ≤ e.2.2.2 ∧ e.2.2.2 ≤ 14 := by
  decide +kernel

/-- Concrete instance: prefix 310, bound 13 (the largest-but-one entry). -/
example : ∀ A P t, 0 < A → PalindromeStarts3 3 1 0 P → orbit A t = P → t ≤ 13 :=
  ancestry_bound (by decide)

/-- Concrete instance: prefix 561, bound 14. -/
example : ∀ t, ¬ PalindromeStarts3 5 6 1 (orbit 196 t) := no_196 (B := 14) (by decide)

#print axioms growth_exact
#print axioms growth_not_in_table
#print axioms table4_bounds_le_14
