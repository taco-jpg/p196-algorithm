import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0332 : leaf0332.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0333 : leaf0333.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0334 : leaf0334.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0335 : leaf0335.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0332 : checkRow ranks (fastLongPred 7) [3,11,14,4,2,0,10] 1 = true := by decide +kernel
theorem row_branch0333 : checkRow ranks (fastLongPred 7) [3,11,14,9,1,9,11] 1 = true := by decide +kernel
theorem row_branch0334 : checkRow ranks (fastLongPred 7) [3,11,14,9,2,9,9] 10 = true := by decide +kernel
theorem row_branch0335 : checkRow ranks (fastLongPred 7) [3,11,14,9,1,14,13] 1 = true := by decide +kernel
end SevenColumn.Certificate739
