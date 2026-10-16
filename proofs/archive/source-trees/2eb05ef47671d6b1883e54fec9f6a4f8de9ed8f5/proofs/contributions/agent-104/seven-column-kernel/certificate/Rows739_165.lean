import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0660 : leaf0660.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0661 : leaf0661.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0662 : leaf0662.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0663 : leaf0663.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0660 : checkRow ranks (fastLongPred 7) [7,3,9,7,9,6,3] 2 = true := by decide +kernel
theorem row_branch0661 : checkRow ranks (fastLongPred 7) [7,3,9,8,0,7,7] 2 = true := by decide +kernel
theorem row_branch0662 : checkRow ranks (fastLongPred 7) [7,3,9,8,0,2,0] 2 = true := by decide +kernel
theorem row_branch0663 : checkRow ranks (fastLongPred 7) [7,3,9,8,1,9,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
