import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf0130 : checkRowsBlock ranks (fastLongPred 7) leaf0130 = true := by decide +kernel
theorem row_branch0130 : checkRow ranks (fastLongPred 7) [1,0,13,12,13,9,9] 5 = true := by decide +kernel
theorem checked_leaf0131 : checkRowsBlock ranks (fastLongPred 7) leaf0131 = true := by decide +kernel
theorem row_branch0131 : checkRow ranks (fastLongPred 7) [1,0,13,12,14,3,2] 0 = true := by decide +kernel
theorem checked_leaf0132 : checkRowsBlock ranks (fastLongPred 7) leaf0132 = true := by decide +kernel
theorem row_branch0132 : checkRow ranks (fastLongPred 7) [1,0,13,12,13,13,10] 13 = true := by decide +kernel
theorem checked_leaf0133 : checkRowsBlock ranks (fastLongPred 7) leaf0133 = true := by decide +kernel
theorem row_branch0133 : checkRow ranks (fastLongPred 7) [1,0,13,12,13,0,12] 0 = true := by decide +kernel
end Agent118.Cert217
