import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0228 : leaf0228.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0229 : leaf0229.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0230 : leaf0230.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0231 : leaf0231.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0228 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,8] 7 = true := by decide +kernel
theorem row_branch0229 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,13] 1 = true := by decide +kernel
theorem row_branch0230 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,6] 7 = true := by decide +kernel
theorem row_branch0231 : checkRow ranks (fastLongPred 7) [3,4,8,15,11,17,14] 1 = true := by decide +kernel
end SevenColumn.Certificate739
