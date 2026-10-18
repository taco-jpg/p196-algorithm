import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem checked_leaf0046 : checkRowsBlock ranks (fastLongPred 7) leaf0046 = true := by decide +kernel
theorem row_branch0046 : checkRow ranks (fastLongPred 7) [1,0,13,9,10,3,0] 0 = true := by decide +kernel
end Agent118.Cert217
