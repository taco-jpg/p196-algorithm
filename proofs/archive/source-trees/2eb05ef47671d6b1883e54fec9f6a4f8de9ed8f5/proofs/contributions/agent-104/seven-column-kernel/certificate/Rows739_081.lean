import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0324 : leaf0324.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0325 : leaf0325.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0326 : leaf0326.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0327 : leaf0327.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0324 : checkRow ranks (fastLongPred 7) [3,11,14,4,0,0,14] 1 = true := by decide +kernel
theorem row_branch0325 : checkRow ranks (fastLongPred 7) [3,11,14,4,2,10,3] 1 = true := by decide +kernel
theorem row_branch0326 : checkRow ranks (fastLongPred 7) [3,11,14,4,3,10,1] 1 = true := by decide +kernel
theorem row_branch0327 : checkRow ranks (fastLongPred 7) [3,11,14,4,3,0,9] 0 = true := by decide +kernel
end SevenColumn.Certificate739
