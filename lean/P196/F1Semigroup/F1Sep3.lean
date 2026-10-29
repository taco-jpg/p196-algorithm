import P196.F1Semigroup.F1MinDefs
/-! Pairwise separation of representatives, rows d in [170,208) (kernel check). -/
namespace F1

theorem sepOK_3 : ∀ d, d < 208 → 170 ≤ d → sepOK d = true := by decide +kernel

end F1
