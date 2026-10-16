import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0388 : leaf0388.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0389 : leaf0389.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0390 : leaf0390.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0391 : leaf0391.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0388 : checkRow ranks (fastLongPred 7) [5,13,12,1,12,8,16] 2 = true := by decide +kernel
theorem row_branch0389 : checkRow ranks (fastLongPred 7) [5,18,2,1,1,2,15] 0 = true := by decide +kernel
theorem row_branch0390 : checkRow ranks (fastLongPred 7) [5,18,2,6,12,8,15] 0 = true := by decide +kernel
theorem row_branch0391 : checkRow ranks (fastLongPred 7) [5,18,2,2,6,18,1] 0 = true := by decide +kernel
end SevenColumn.Certificate739
