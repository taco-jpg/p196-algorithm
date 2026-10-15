import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0152 : leaf0152.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0153 : leaf0153.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0154 : leaf0154.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0155 : leaf0155.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0152 : checkRow ranks (fastLongPred 7) [2,14,11,17,3,14,17] 1 = true := by decide +kernel
theorem row_branch0153 : checkRow ranks (fastLongPred 7) [2,16,15,12,10,11,4] 1 = true := by decide +kernel
theorem row_branch0154 : checkRow ranks (fastLongPred 7) [2,16,15,9,17,7,7] 3 = true := by decide +kernel
theorem row_branch0155 : checkRow ranks (fastLongPred 7) [2,14,9,9,16,18,8] 1 = true := by decide +kernel
end SevenColumn.Certificate739
