import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0724 : leaf0724.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0725 : leaf0725.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0726 : leaf0726.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0727 : leaf0727.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0724 : checkRow ranks (fastLongPred 7) [8,0,13,13,3,0,6] 0 = true := by decide +kernel
theorem row_branch0725 : checkRow ranks (fastLongPred 7) [7,8,18,15,18,6,10] 2 = true := by decide +kernel
theorem row_branch0726 : checkRow ranks (fastLongPred 7) [8,0,18,3,3,10,4] 3 = true := by decide +kernel
theorem row_branch0727 : checkRow ranks (fastLongPred 7) [8,4,10,8,14,14,18] 24 = true := by decide +kernel
end SevenColumn.Certificate739
