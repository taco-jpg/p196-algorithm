import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0192 : leaf0192.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0193 : leaf0193.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0194 : leaf0194.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0195 : leaf0195.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0192 : checkRow ranks (fastLongPred 7) [3,2,5,6,0,15,14] 1 = true := by decide +kernel
theorem row_branch0193 : checkRow ranks (fastLongPred 7) [3,2,5,6,11,9,8] 1 = true := by decide +kernel
theorem row_branch0194 : checkRow ranks (fastLongPred 7) [3,2,5,8,5,4,13] 1 = true := by decide +kernel
theorem row_branch0195 : checkRow ranks (fastLongPred 7) [3,2,5,6,13,9,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
