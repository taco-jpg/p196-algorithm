import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0408 : leaf0408.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0409 : leaf0409.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0410 : leaf0410.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0411 : leaf0411.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0408 : checkRow ranks (fastLongPred 7) [6,0,13,13,10,3,17] 2 = true := by decide +kernel
theorem row_branch0409 : checkRow ranks (fastLongPred 7) [6,0,12,17,18,13,4] 0 = true := by decide +kernel
theorem row_branch0410 : checkRow ranks (fastLongPred 7) [6,0,12,17,17,11,0] 0 = true := by decide +kernel
theorem row_branch0411 : checkRow ranks (fastLongPred 7) [6,0,12,16,11,13,18] 2 = true := by decide +kernel
end SevenColumn.Certificate739
