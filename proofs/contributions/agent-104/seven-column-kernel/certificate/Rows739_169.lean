import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0676 : leaf0676.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0677 : leaf0677.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0678 : leaf0678.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0679 : leaf0679.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0676 : checkRow ranks (fastLongPred 7) [7,3,9,8,8,7,7] 2 = true := by decide +kernel
theorem row_branch0677 : checkRow ranks (fastLongPred 7) [7,3,9,8,9,9,1] 2 = true := by decide +kernel
theorem row_branch0678 : checkRow ranks (fastLongPred 7) [7,3,9,8,9,3,4] 2 = true := by decide +kernel
theorem row_branch0679 : checkRow ranks (fastLongPred 7) [7,3,9,9,1,0,5] 2 = true := by decide +kernel
end SevenColumn.Certificate739
