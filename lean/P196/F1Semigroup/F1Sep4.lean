import P196.F1Semigroup.F1MinDefs
/-! Pairwise separation of representatives, rows d in [208,241) (kernel check). -/
namespace F1

theorem sepOK_4 : ∀ d, d < 241 → 208 ≤ d → sepOK d = true := by decide +kernel

end F1
