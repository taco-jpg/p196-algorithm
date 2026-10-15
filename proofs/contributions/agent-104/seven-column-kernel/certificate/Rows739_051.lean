import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0204 : leaf0204.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0205 : leaf0205.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0206 : leaf0206.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0207 : leaf0207.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0204 : checkRow ranks (fastLongPred 7) [3,2,5,8,5,18,5] 0 = true := by decide +kernel
theorem row_branch0205 : checkRow ranks (fastLongPred 7) [3,2,11,6,6,9,11] 4 = true := by decide +kernel
theorem row_branch0206 : checkRow ranks (fastLongPred 7) [3,2,11,6,8,9,15] 4 = true := by decide +kernel
theorem row_branch0207 : checkRow ranks (fastLongPred 7) [3,2,11,6,6,13,13] 1 = true := by decide +kernel
end SevenColumn.Certificate739
