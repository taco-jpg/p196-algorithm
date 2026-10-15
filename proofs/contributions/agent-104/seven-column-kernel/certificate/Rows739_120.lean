import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0480 : leaf0480.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0481 : leaf0481.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0482 : leaf0482.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0483 : leaf0483.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0480 : checkRow ranks (fastLongPred 7) [6,5,2,18,7,9,9] 5 = true := by decide +kernel
theorem row_branch0481 : checkRow ranks (fastLongPred 7) [6,5,2,18,3,4,13] 5 = true := by decide +kernel
theorem row_branch0482 : checkRow ranks (fastLongPred 7) [6,5,2,17,6,2,17] 2 = true := by decide +kernel
theorem row_branch0483 : checkRow ranks (fastLongPred 7) [6,5,2,18,7,18,8] 1 = true := by decide +kernel
end SevenColumn.Certificate739
