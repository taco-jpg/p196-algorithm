import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0148 : leaf0148.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0149 : leaf0149.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0150 : leaf0150.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0151 : leaf0151.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0148 : checkRow ranks (fastLongPred 7) [2,4,18,7,0,8,4] 1 = true := by decide +kernel
theorem row_branch0149 : checkRow ranks (fastLongPred 7) [2,12,4,18,3,8,7] 1 = true := by decide +kernel
theorem row_branch0150 : checkRow ranks (fastLongPred 7) [2,14,9,9,13,13,9] 1 = true := by decide +kernel
theorem row_branch0151 : checkRow ranks (fastLongPred 7) [2,13,16,16,5,0,15] 1 = true := by decide +kernel
end SevenColumn.Certificate739
