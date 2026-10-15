import Rank777
import PrefixChecksBase
namespace Agent118.Cert777
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf1901 : checkRowsBlock ranks (fastLongPred 7) leaf1901 = true := by decide +kernel
theorem row_branch1901 : checkRow ranks (fastLongPred 7) [7,7,7,8,2,6,1] 2 = true := by decide +kernel
theorem checked_leaf1902 : checkRowsBlock ranks (fastLongPred 7) leaf1902 = true := by decide +kernel
theorem row_branch1902 : checkRow ranks (fastLongPred 7) [7,7,7,8,3,3,5] 11 = true := by decide +kernel
theorem checked_leaf1903 : checkRowsBlock ranks (fastLongPred 7) leaf1903 = true := by decide +kernel
theorem row_branch1903 : checkRow ranks (fastLongPred 7) [7,7,7,8,2,9,8] 11 = true := by decide +kernel
theorem checked_leaf1904 : checkRowsBlock ranks (fastLongPred 7) leaf1904 = true := by decide +kernel
theorem row_branch1904 : checkRow ranks (fastLongPred 7) [7,7,7,8,2,2,4] 11 = true := by decide +kernel
end Agent118.Cert777
