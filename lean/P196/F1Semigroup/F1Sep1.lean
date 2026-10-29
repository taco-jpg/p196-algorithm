import P196.F1Semigroup.F1MinDefs
/-! Pairwise separation of representatives, rows d in [0,120) (kernel check). -/
namespace F1

theorem sepOK_1 : ∀ d, d < 120 → 0 ≤ d → sepOK d = true := by decide +kernel

end F1
