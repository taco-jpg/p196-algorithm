import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0684 : leaf0684.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0685 : leaf0685.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0686 : leaf0686.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0687 : leaf0687.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0684 : checkRow ranks (fastLongPred 7) [7,3,9,9,3,3,4] 2 = true := by decide +kernel
theorem row_branch0685 : checkRow ranks (fastLongPred 7) [7,3,9,9,4,4,8] 2 = true := by decide +kernel
theorem row_branch0686 : checkRow ranks (fastLongPred 7) [7,3,9,9,3,9,1] 2 = true := by decide +kernel
theorem row_branch0687 : checkRow ranks (fastLongPred 7) [7,3,9,9,5,6,2] 2 = true := by decide +kernel
end SevenColumn.Certificate739
