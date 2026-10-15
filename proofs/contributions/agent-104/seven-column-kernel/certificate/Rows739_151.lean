import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0604 : leaf0604.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0605 : leaf0605.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0606 : leaf0606.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0607 : leaf0607.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0604 : checkRow ranks (fastLongPred 7) [7,3,9,3,7,9,1] 2 = true := by decide +kernel
theorem row_branch0605 : checkRow ranks (fastLongPred 7) [7,3,9,4,7,6,3] 2 = true := by decide +kernel
theorem row_branch0606 : checkRow ranks (fastLongPred 7) [7,3,9,4,8,7,7] 2 = true := by decide +kernel
theorem row_branch0607 : checkRow ranks (fastLongPred 7) [7,3,9,4,8,2,0] 2 = true := by decide +kernel
end SevenColumn.Certificate739
