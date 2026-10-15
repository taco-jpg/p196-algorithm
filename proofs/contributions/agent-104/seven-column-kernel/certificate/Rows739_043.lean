import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0172 : leaf0172.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0173 : leaf0173.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0174 : leaf0174.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0175 : leaf0175.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0172 : checkRow ranks (fastLongPred 7) [3,0,6,6,14,11,0] 1 = true := by decide +kernel
theorem row_branch0173 : checkRow ranks (fastLongPred 7) [3,0,8,11,13,13,6] 1 = true := by decide +kernel
theorem row_branch0174 : checkRow ranks (fastLongPred 7) [3,0,8,13,7,16,17] 1 = true := by decide +kernel
theorem row_branch0175 : checkRow ranks (fastLongPred 7) [3,0,8,11,14,9,3] 1 = true := by decide +kernel
end SevenColumn.Certificate739
