import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0184 : leaf0184.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0185 : leaf0185.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0186 : leaf0186.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0187 : leaf0187.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0184 : checkRow ranks (fastLongPred 7) [3,2,3,18,1,17,11] 1 = true := by decide +kernel
theorem row_branch0185 : checkRow ranks (fastLongPred 7) [3,2,3,18,1,11,4] 1 = true := by decide +kernel
theorem row_branch0186 : checkRow ranks (fastLongPred 7) [3,2,3,15,14,9,17] 1 = true := by decide +kernel
theorem row_branch0187 : checkRow ranks (fastLongPred 7) [3,2,1,10,14,17,5] 1 = true := by decide +kernel
end SevenColumn.Certificate739
