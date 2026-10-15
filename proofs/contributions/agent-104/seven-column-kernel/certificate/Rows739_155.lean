import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0620 : leaf0620.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0621 : leaf0621.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0622 : leaf0622.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0623 : leaf0623.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0620 : checkRow ranks (fastLongPred 7) [7,3,9,5,6,7,7] 2 = true := by decide +kernel
theorem row_branch0621 : checkRow ranks (fastLongPred 7) [7,3,9,5,7,9,1] 2 = true := by decide +kernel
theorem row_branch0622 : checkRow ranks (fastLongPred 7) [7,3,9,5,7,3,4] 2 = true := by decide +kernel
theorem row_branch0623 : checkRow ranks (fastLongPred 7) [7,3,9,5,9,0,5] 2 = true := by decide +kernel
end SevenColumn.Certificate739
