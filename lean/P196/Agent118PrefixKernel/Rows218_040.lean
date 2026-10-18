import P196.Agent118PrefixKernel.Rank218
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert218
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf0542 : checkRowsBlock ranks (fastLongPred 7) leaf0542 = true := by decide +kernel
theorem row_branch0542 : checkRow ranks (fastLongPred 7) [2,7,8,9,5,16,3] 1 = true := by decide +kernel
theorem checked_leaf0543 : checkRowsBlock ranks (fastLongPred 7) leaf0543 = true := by decide +kernel
theorem row_branch0543 : checkRow ranks (fastLongPred 7) [2,12,5,6,8,17,9] 1 = true := by decide +kernel
theorem checked_leaf0544 : checkRowsBlock ranks (fastLongPred 7) leaf0544 = true := by decide +kernel
theorem row_branch0544 : checkRow ranks (fastLongPred 7) [2,12,5,5,5,8,5] 1 = true := by decide +kernel
end Agent118.Cert218
