import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0440 : leaf0440.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0441 : leaf0441.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0442 : leaf0442.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0443 : leaf0443.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0440 : checkRow ranks (fastLongPred 7) [6,4,7,16,4,9,6] 2 = true := by decide +kernel
theorem row_branch0441 : checkRow ranks (fastLongPred 7) [6,4,7,16,0,1,0] 0 = true := by decide +kernel
theorem row_branch0442 : checkRow ranks (fastLongPred 7) [6,4,3,6,5,4,16] 2 = true := by decide +kernel
theorem row_branch0443 : checkRow ranks (fastLongPred 7) [6,0,18,8,0,18,10] 13 = true := by decide +kernel
end SevenColumn.Certificate739
