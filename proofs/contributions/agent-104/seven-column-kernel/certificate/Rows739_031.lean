import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0124 : leaf0124.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0125 : leaf0125.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0126 : leaf0126.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0127 : leaf0127.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0124 : checkRow ranks (fastLongPred 7) [1,15,16,11,5,15,4] 0 = true := by decide +kernel
theorem row_branch0125 : checkRow ranks (fastLongPred 7) [1,15,16,10,11,10,5] 0 = true := by decide +kernel
theorem row_branch0126 : checkRow ranks (fastLongPred 7) [1,12,3,17,14,9,7] 0 = true := by decide +kernel
theorem row_branch0127 : checkRow ranks (fastLongPred 7) [1,16,0,6,8,6,14] 0 = true := by decide +kernel
end SevenColumn.Certificate739
