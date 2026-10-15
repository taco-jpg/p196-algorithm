import Rank217
import PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf0103 : checkRowsBlock ranks (fastLongPred 7) leaf0103 = true := by decide +kernel
theorem row_branch0103 : checkRow ranks (fastLongPred 7) [1,0,13,11,12,9,12] 21 = true := by decide +kernel
theorem checked_leaf0104 : checkRowsBlock ranks (fastLongPred 7) leaf0104 = true := by decide +kernel
theorem row_branch0104 : checkRow ranks (fastLongPred 7) [1,0,13,11,13,12,2] 0 = true := by decide +kernel
theorem checked_leaf0105 : checkRowsBlock ranks (fastLongPred 7) leaf0105 = true := by decide +kernel
theorem row_branch0105 : checkRow ranks (fastLongPred 7) [1,0,13,12,0,0,14] 0 = true := by decide +kernel
end Agent118.Cert217
