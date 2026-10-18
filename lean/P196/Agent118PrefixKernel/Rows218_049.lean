import P196.Agent118PrefixKernel.Rank218
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert218
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf0598 : checkRowsBlock ranks (fastLongPred 7) leaf0598 = true := by decide +kernel
theorem row_branch0598 : checkRow ranks (fastLongPred 7) [3,11,17,15,2,2,3] 1 = true := by decide +kernel
end Agent118.Cert218
