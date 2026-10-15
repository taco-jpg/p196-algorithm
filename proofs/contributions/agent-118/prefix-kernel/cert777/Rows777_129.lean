import Rank777
import PrefixChecksBase
namespace Agent118.Cert777
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf1545 : checkRowsBlock ranks (fastLongPred 7) leaf1545 = true := by decide +kernel
theorem row_branch1545 : checkRow ranks (fastLongPred 7) [5,4,11,5,8,1,17] 2 = true := by decide +kernel
theorem checked_leaf1546 : checkRowsBlock ranks (fastLongPred 7) leaf1546 = true := by decide +kernel
theorem row_branch1546 : checkRow ranks (fastLongPred 7) [5,4,11,5,4,6,10] 4 = true := by decide +kernel
theorem checked_leaf1547 : checkRowsBlock ranks (fastLongPred 7) leaf1547 = true := by decide +kernel
theorem row_branch1547 : checkRow ranks (fastLongPred 7) [5,4,11,5,4,1,2] 4 = true := by decide +kernel
theorem checked_leaf1548 : checkRowsBlock ranks (fastLongPred 7) leaf1548 = true := by decide +kernel
theorem row_branch1548 : checkRow ranks (fastLongPred 7) [5,4,11,3,11,8,8] 2 = true := by decide +kernel
end Agent118.Cert777
