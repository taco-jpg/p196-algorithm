import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0248 : leaf0248.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0249 : leaf0249.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0250 : leaf0250.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0251 : leaf0251.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0248 : checkRow ranks (fastLongPred 7) [3,11,14,0,11,2,1] 1 = true := by decide +kernel
theorem row_branch0249 : checkRow ranks (fastLongPred 7) [3,11,14,0,10,1,12] 1 = true := by decide +kernel
theorem row_branch0250 : checkRow ranks (fastLongPred 7) [3,11,14,0,3,12,0] 1 = true := by decide +kernel
theorem row_branch0251 : checkRow ranks (fastLongPred 7) [3,4,8,17,16,16,10] 1 = true := by decide +kernel
end SevenColumn.Certificate739
