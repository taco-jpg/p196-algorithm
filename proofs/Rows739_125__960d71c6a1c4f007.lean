import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0500 : leaf0500.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0501 : leaf0501.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0502 : leaf0502.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0503 : leaf0503.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0500 : checkRow ranks (fastLongPred 7) [6,5,7,8,8,9,4] 2 = true := by decide +kernel
theorem row_branch0501 : checkRow ranks (fastLongPred 7) [6,8,13,1,0,1,5] 2 = true := by decide +kernel
theorem row_branch0502 : checkRow ranks (fastLongPred 7) [6,8,13,1,5,0,2] 0 = true := by decide +kernel
theorem row_branch0503 : checkRow ranks (fastLongPred 7) [6,8,13,1,0,10,0] 8 = true := by decide +kernel
end SevenColumn.Certificate739
