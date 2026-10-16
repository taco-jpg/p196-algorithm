import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0140 : leaf0140.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0141 : leaf0141.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0142 : leaf0142.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0143 : leaf0143.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0140 : checkRow ranks (fastLongPred 7) [1,17,3,8,9,12,9] 0 = true := by decide +kernel
theorem row_branch0141 : checkRow ranks (fastLongPred 7) [1,17,2,6,2,17,0] 0 = true := by decide +kernel
theorem row_branch0142 : checkRow ranks (fastLongPred 7) [2,1,2,12,2,0,2] 0 = true := by decide +kernel
theorem row_branch0143 : checkRow ranks (fastLongPred 7) [2,4,17,14,17,18,10] 5 = true := by decide +kernel
end SevenColumn.Certificate739
