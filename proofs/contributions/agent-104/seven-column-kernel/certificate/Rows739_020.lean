import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0080 : leaf0080.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0081 : leaf0081.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0082 : leaf0082.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0083 : leaf0083.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0080 : checkRow ranks (fastLongPred 7) [1,15,16,10,1,5,10] 0 = true := by decide +kernel
theorem row_branch0081 : checkRow ranks (fastLongPred 7) [1,15,16,10,4,14,15] 0 = true := by decide +kernel
theorem row_branch0082 : checkRow ranks (fastLongPred 7) [1,15,16,10,5,10,5] 0 = true := by decide +kernel
theorem row_branch0083 : checkRow ranks (fastLongPred 7) [1,15,16,10,5,1,17] 0 = true := by decide +kernel
end SevenColumn.Certificate739
