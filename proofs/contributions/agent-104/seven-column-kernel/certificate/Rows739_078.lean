import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0312 : leaf0312.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0313 : leaf0313.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0314 : leaf0314.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0315 : leaf0315.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0312 : checkRow ranks (fastLongPred 7) [3,11,14,3,12,9,9] 1 = true := by decide +kernel
theorem row_branch0313 : checkRow ranks (fastLongPred 7) [3,11,14,3,11,14,3] 1 = true := by decide +kernel
theorem row_branch0314 : checkRow ranks (fastLongPred 7) [3,11,14,3,10,13,14] 1 = true := by decide +kernel
theorem row_branch0315 : checkRow ranks (fastLongPred 7) [3,11,14,3,4,4,11] 1 = true := by decide +kernel
end SevenColumn.Certificate739
