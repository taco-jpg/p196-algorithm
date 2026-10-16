import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0824 : leaf0824.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0825 : leaf0825.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0826 : leaf0826.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0827 : leaf0827.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0824 : checkRow ranks (fastLongPred 7) [12,8,6,3,10,11,1] 2 = true := by decide +kernel
theorem row_branch0825 : checkRow ranks (fastLongPred 7) [12,8,6,3,1,3,16] 3 = true := by decide +kernel
theorem row_branch0826 : checkRow ranks (fastLongPred 7) [12,1,16,17,1,8,3] 3 = true := by decide +kernel
theorem row_branch0827 : checkRow ranks (fastLongPred 7) [12,1,14,16,7,9,15] 3 = true := by decide +kernel
end SevenColumn.Certificate739
