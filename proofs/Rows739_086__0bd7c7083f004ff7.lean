import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0344 : leaf0344.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0345 : leaf0345.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0346 : leaf0346.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0347 : leaf0347.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0344 : checkRow ranks (fastLongPred 7) [3,12,2,15,5,6,13] 1 = true := by decide +kernel
theorem row_branch0345 : checkRow ranks (fastLongPred 7) [3,12,1,12,18,16,4] 1 = true := by decide +kernel
theorem row_branch0346 : checkRow ranks (fastLongPred 7) [3,12,0,12,17,18,18] 0 = true := by decide +kernel
theorem row_branch0347 : checkRow ranks (fastLongPred 7) [3,11,14,9,9,9,4] 10 = true := by decide +kernel
end SevenColumn.Certificate739
