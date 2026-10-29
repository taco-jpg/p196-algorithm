import P196.F1Semigroup.F1MinDefs
/-! Pairwise separation of representatives, rows d in [120,170) (kernel check). -/
namespace F1

theorem sepOK_2 : ∀ d, d < 170 → 120 ≤ d → sepOK d = true := by decide +kernel

end F1
