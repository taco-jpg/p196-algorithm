import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0160 : leaf0160.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0161 : leaf0161.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0162 : leaf0162.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0163 : leaf0163.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0160 : checkRow ranks (fastLongPred 7) [2,18,12,6,14,16,11] 1 = true := by decide +kernel
theorem row_branch0161 : checkRow ranks (fastLongPred 7) [3,0,6,6,11,12,13] 1 = true := by decide +kernel
theorem row_branch0162 : checkRow ranks (fastLongPred 7) [3,0,6,6,13,17,18] 0 = true := by decide +kernel
theorem row_branch0163 : checkRow ranks (fastLongPred 7) [3,0,6,6,13,14,4] 1 = true := by decide +kernel
end SevenColumn.Certificate739
