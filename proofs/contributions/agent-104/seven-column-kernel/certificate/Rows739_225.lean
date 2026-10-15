import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0900 : leaf0900.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0901 : leaf0901.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0902 : leaf0902.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0903 : leaf0903.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0900 : checkRow ranks (fastLongPred 7) [12,10,5,7,18,18,8] 6 = true := by decide +kernel
theorem row_branch0901 : checkRow ranks (fastLongPred 7) [12,10,5,14,13,6,1] 3 = true := by decide +kernel
theorem row_branch0902 : checkRow ranks (fastLongPred 7) [12,10,5,14,4,14,4] 3 = true := by decide +kernel
theorem row_branch0903 : checkRow ranks (fastLongPred 7) [12,10,5,16,7,2,13] 3 = true := by decide +kernel
end SevenColumn.Certificate739
