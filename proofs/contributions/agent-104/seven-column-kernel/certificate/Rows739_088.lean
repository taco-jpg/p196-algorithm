import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0352 : leaf0352.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0353 : leaf0353.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0354 : leaf0354.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0355 : leaf0355.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0352 : checkRow ranks (fastLongPred 7) [3,13,4,14,14,0,7] 1 = true := by decide +kernel
theorem row_branch0353 : checkRow ranks (fastLongPred 7) [3,14,5,10,5,9,10] 1 = true := by decide +kernel
theorem row_branch0354 : checkRow ranks (fastLongPred 7) [3,14,3,14,16,17,15] 1 = true := by decide +kernel
theorem row_branch0355 : checkRow ranks (fastLongPred 7) [3,13,4,9,9,10,14] 1 = true := by decide +kernel
end SevenColumn.Certificate739
