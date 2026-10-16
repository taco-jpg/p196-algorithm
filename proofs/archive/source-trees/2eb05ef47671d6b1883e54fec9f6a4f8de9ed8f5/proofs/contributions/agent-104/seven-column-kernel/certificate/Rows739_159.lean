import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0636 : leaf0636.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0637 : leaf0637.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0638 : leaf0638.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0639 : leaf0639.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0636 : checkRow ranks (fastLongPred 7) [7,3,9,4,7,0,5] 2 = true := by decide +kernel
theorem row_branch0637 : checkRow ranks (fastLongPred 7) [7,3,9,2,8,7,7] 2 = true := by decide +kernel
theorem row_branch0638 : checkRow ranks (fastLongPred 7) [7,3,9,6,5,9,1] 2 = true := by decide +kernel
theorem row_branch0639 : checkRow ranks (fastLongPred 7) [7,3,9,6,7,0,5] 2 = true := by decide +kernel
end SevenColumn.Certificate739
