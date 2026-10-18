import P196.Agent118PrefixKernel.Rank217
import P196.Agent118PrefixKernel.PrefixChecksBase
namespace Agent118.Cert217
open SevenColumn.Certificate Agent118.PrefixKernel
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem row_leaf0976_41 : checkRow ranks (fastLongPred 7) [2,7,8,3,8,13,7] 9 = true := by decide +kernel
theorem row_leaf0976_42 : checkRow ranks (fastLongPred 7) [2,7,8,3,8,13,8] 9 = true := by decide +kernel
theorem row_leaf0976_43 : checkRow ranks (fastLongPred 7) [2,7,8,3,8,13,9] 9 = true := by decide +kernel
theorem row_leaf0976_44 : checkRow ranks (fastLongPred 7) [2,7,8,3,8,13,10] 9 = true := by decide +kernel
end Agent118.Cert217
