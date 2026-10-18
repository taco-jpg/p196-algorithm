import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf0100 : checkRowsBlock ranks (fastLongPred 7) leaf0100 = true := by decide +kernel
theorem row_branch0100 : checkRow ranks (fastLongPred 7) [1,0,13,11,10,0,4] 0 = true := by decide +kernel
theorem checked_leaf0101 : checkRowsBlock ranks (fastLongPred 7) leaf0101 = true := by decide +kernel
theorem row_branch0101 : checkRow ranks (fastLongPred 7) [1,0,13,11,12,1,1] 0 = true := by decide +kernel
theorem checked_leaf0102 : checkRowsBlock ranks (fastLongPred 7) leaf0102 = true := by decide +kernel
theorem row_branch0102 : checkRow ranks (fastLongPred 7) [1,0,13,11,12,13,14] 19 = true := by decide +kernel
end Agent118.Cert217
