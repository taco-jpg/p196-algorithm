import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0756 : leaf0756.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0757 : leaf0757.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0758 : leaf0758.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0759 : leaf0759.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0756 : checkRow ranks (fastLongPred 7) [11,16,5,13,13,16,12] 1 = true := by decide +kernel
theorem row_branch0757 : checkRow ranks (fastLongPred 7) [11,16,14,13,4,18,1] 1 = true := by decide +kernel
theorem row_branch0758 : checkRow ranks (fastLongPred 7) [11,18,5,17,8,1,9] 0 = true := by decide +kernel
theorem row_branch0759 : checkRow ranks (fastLongPred 7) [11,18,5,6,14,7,11] 0 = true := by decide +kernel
end SevenColumn.Certificate739
