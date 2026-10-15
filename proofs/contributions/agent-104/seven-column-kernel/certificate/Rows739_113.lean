import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0452 : leaf0452.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0453 : leaf0453.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0454 : leaf0454.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0455 : leaf0455.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0452 : checkRow ranks (fastLongPred 7) [6,4,10,13,7,14,11] 2 = true := by decide +kernel
theorem row_branch0453 : checkRow ranks (fastLongPred 7) [6,4,10,16,11,12,6] 2 = true := by decide +kernel
theorem row_branch0454 : checkRow ranks (fastLongPred 7) [6,4,10,16,10,9,11] 2 = true := by decide +kernel
theorem row_branch0455 : checkRow ranks (fastLongPred 7) [6,4,10,16,16,2,0] 2 = true := by decide +kernel
end SevenColumn.Certificate739
