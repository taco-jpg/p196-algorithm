import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0640 : leaf0640.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0641 : leaf0641.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0642 : leaf0642.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0643 : leaf0643.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0640 : checkRow ranks (fastLongPred 7) [7,3,9,6,6,4,8] 2 = true := by decide +kernel
theorem row_branch0641 : checkRow ranks (fastLongPred 7) [7,3,9,6,8,2,0] 2 = true := by decide +kernel
theorem row_branch0642 : checkRow ranks (fastLongPred 7) [7,3,9,6,9,3,4] 2 = true := by decide +kernel
theorem row_branch0643 : checkRow ranks (fastLongPred 7) [7,3,9,6,8,7,7] 2 = true := by decide +kernel
end SevenColumn.Certificate739
