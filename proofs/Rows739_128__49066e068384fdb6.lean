import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0512 : leaf0512.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0513 : leaf0513.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0514 : leaf0514.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0515 : leaf0515.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0512 : checkRow ranks (fastLongPred 7) [6,8,13,5,10,11,2] 2 = true := by decide +kernel
theorem row_branch0513 : checkRow ranks (fastLongPred 7) [6,8,13,5,10,4,16] 2 = true := by decide +kernel
theorem row_branch0514 : checkRow ranks (fastLongPred 7) [6,8,13,5,15,0,9] 0 = true := by decide +kernel
theorem row_branch0515 : checkRow ranks (fastLongPred 7) [6,8,17,11,4,9,11] 2 = true := by decide +kernel
end SevenColumn.Certificate739
