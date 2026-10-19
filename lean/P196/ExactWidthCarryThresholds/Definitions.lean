import P196.ExactSmallWidthCarryThresholds.Definitions

/-!
The complete-carry thresholds for fixed initial widths one through seventeen.
The two reconstruction predicates and the small-width threshold are imported
unchanged. The classification is restricted to positive widths at most
seventeen; the total function below makes no claim outside that domain.
-/

namespace ExactWidthCarryThresholds

/-- Reuse the exact small-width table, with the additional width-ten drop
and the eight- and nine-observation ranges in the classified domain. -/
def exactWidthThreshold (L : Nat) : Nat :=
  if L ≤ 8 then ExactSmallWidthCarryThresholds.exactWidthThreshold L
  else if L = 10 then 7
  else if L ≤ 16 then 8
  else 9

end ExactWidthCarryThresholds
