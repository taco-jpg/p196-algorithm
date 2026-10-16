import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0212 : leaf0212.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0213 : leaf0213.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0214 : leaf0214.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0215 : leaf0215.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0212 : checkRow ranks (fastLongPred 7) [3,2,11,8,14,8,9] 4 = true := by decide +kernel
theorem row_branch0213 : checkRow ranks (fastLongPred 7) [3,2,13,10,17,17,16] 1 = true := by decide +kernel
theorem row_branch0214 : checkRow ranks (fastLongPred 7) [3,2,11,18,16,18,16] 1 = true := by decide +kernel
theorem row_branch0215 : checkRow ranks (fastLongPred 7) [3,2,13,11,6,8,14] 1 = true := by decide +kernel
end SevenColumn.Certificate739
