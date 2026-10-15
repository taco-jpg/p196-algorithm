import Rank777
import PrefixChecksBase
namespace Agent118.Cert777
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf2738 : checkRowsBlock ranks (fastLongPred 7) leaf2738 = true := by decide +kernel
theorem row_branch2738 : checkRow ranks (fastLongPred 7) [10,9,2,11,8,16,6] 3 = true := by decide +kernel
theorem checked_leaf2739 : checkRowsBlock ranks (fastLongPred 7) leaf2739 = true := by decide +kernel
theorem row_branch2739 : checkRow ranks (fastLongPred 7) [10,9,2,11,17,2,11] 3 = true := by decide +kernel
theorem checked_leaf2740 : checkRowsBlock ranks (fastLongPred 7) leaf2740 = true := by decide +kernel
theorem row_branch2740 : checkRow ranks (fastLongPred 7) [10,9,2,11,17,0,2] 3 = true := by decide +kernel
theorem checked_leaf2741 : checkRowsBlock ranks (fastLongPred 7) leaf2741 = true := by decide +kernel
theorem row_branch2741 : checkRow ranks (fastLongPred 7) [10,9,2,11,17,9,3] 5 = true := by decide +kernel
end Agent118.Cert777
