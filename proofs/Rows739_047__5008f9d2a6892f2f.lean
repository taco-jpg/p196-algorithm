import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0188 : leaf0188.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0189 : leaf0189.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0190 : leaf0190.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0191 : leaf0191.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0188 : checkRow ranks (fastLongPred 7) [3,0,8,11,11,18,1] 1 = true := by decide +kernel
theorem row_branch0189 : checkRow ranks (fastLongPred 7) [2,16,17,15,5,8,16] 1 = true := by decide +kernel
theorem row_branch0190 : checkRow ranks (fastLongPred 7) [3,2,3,18,9,9,3] 1 = true := by decide +kernel
theorem row_branch0191 : checkRow ranks (fastLongPred 7) [3,2,5,6,2,12,18] 1 = true := by decide +kernel
end SevenColumn.Certificate739
