import Rank217
import PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf1906 : checkRowsBlock ranks (fastLongPred 7) leaf1906 = true := by decide +kernel
theorem row_branch1906 : checkRow ranks (fastLongPred 7) [5,12,15,9,11,14,12] 2 = true := by decide +kernel
theorem checked_leaf1907 : checkRowsBlock ranks (fastLongPred 7) leaf1907 = true := by decide +kernel
theorem row_branch1907 : checkRow ranks (fastLongPred 7) [5,12,15,9,11,11,0] 0 = true := by decide +kernel
end Agent118.Cert217
