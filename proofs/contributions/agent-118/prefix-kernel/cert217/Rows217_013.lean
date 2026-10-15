import Rank217
import PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf0081 : checkRowsBlock ranks (fastLongPred 7) leaf0081 = true := by decide +kernel
theorem row_branch0081 : checkRow ranks (fastLongPred 7) [1,0,13,10,14,0,9] 0 = true := by decide +kernel
theorem checked_leaf0082 : checkRowsBlock ranks (fastLongPred 7) leaf0082 = true := by decide +kernel
theorem row_branch0082 : checkRow ranks (fastLongPred 7) [1,0,13,11,0,3,12] 0 = true := by decide +kernel
theorem checked_leaf0083 : checkRowsBlock ranks (fastLongPred 7) leaf0083 = true := by decide +kernel
theorem row_branch0083 : checkRow ranks (fastLongPred 7) [1,0,13,10,14,9,1] 8 = true := by decide +kernel
end Agent118.Cert217
