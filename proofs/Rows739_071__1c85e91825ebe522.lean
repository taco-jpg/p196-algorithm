import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0284 : leaf0284.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0285 : leaf0285.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0286 : leaf0286.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0287 : leaf0287.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0284 : checkRow ranks (fastLongPred 7) [3,11,14,1,13,13,9] 1 = true := by decide +kernel
theorem row_branch0285 : checkRow ranks (fastLongPred 7) [3,11,14,1,9,12,4] 1 = true := by decide +kernel
theorem row_branch0286 : checkRow ranks (fastLongPred 7) [3,11,14,2,3,4,1] 1 = true := by decide +kernel
theorem row_branch0287 : checkRow ranks (fastLongPred 7) [3,11,14,2,4,3,14] 1 = true := by decide +kernel
end SevenColumn.Certificate739
