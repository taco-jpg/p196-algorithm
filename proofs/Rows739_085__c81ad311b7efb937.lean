import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0340 : leaf0340.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0341 : leaf0341.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0342 : leaf0342.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0343 : leaf0343.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0340 : checkRow ranks (fastLongPred 7) [3,11,18,16,11,13,5] 1 = true := by decide +kernel
theorem row_branch0341 : checkRow ranks (fastLongPred 7) [3,12,0,12,12,16,9] 0 = true := by decide +kernel
theorem row_branch0342 : checkRow ranks (fastLongPred 7) [3,12,0,10,9,10,8] 0 = true := by decide +kernel
theorem row_branch0343 : checkRow ranks (fastLongPred 7) [3,12,1,10,16,10,9] 1 = true := by decide +kernel
end SevenColumn.Certificate739
