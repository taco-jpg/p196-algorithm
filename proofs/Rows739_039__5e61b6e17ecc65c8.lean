import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0156 : leaf0156.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0157 : leaf0157.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0158 : leaf0158.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0159 : leaf0159.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0156 : checkRow ranks (fastLongPred 7) [2,11,14,14,1,5,7] 1 = true := by decide +kernel
theorem row_branch0157 : checkRow ranks (fastLongPred 7) [2,0,3,8,15,11,8] 1 = true := by decide +kernel
theorem row_branch0158 : checkRow ranks (fastLongPred 7) [2,16,17,17,12,13,10] 1 = true := by decide +kernel
theorem row_branch0159 : checkRow ranks (fastLongPred 7) [3,0,6,6,3,2,2] 1 = true := by decide +kernel
end SevenColumn.Certificate739
