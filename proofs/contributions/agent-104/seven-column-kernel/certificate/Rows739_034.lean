import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0136 : leaf0136.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0137 : leaf0137.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0138 : leaf0138.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0139 : leaf0139.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0136 : checkRow ranks (fastLongPred 7) [1,17,2,16,6,8,6] 0 = true := by decide +kernel
theorem row_branch0137 : checkRow ranks (fastLongPred 7) [1,17,3,8,15,15,15] 0 = true := by decide +kernel
theorem row_branch0138 : checkRow ranks (fastLongPred 7) [1,17,3,18,16,6,9] 0 = true := by decide +kernel
theorem row_branch0139 : checkRow ranks (fastLongPred 7) [1,17,3,17,15,2,7] 0 = true := by decide +kernel
end SevenColumn.Certificate739
