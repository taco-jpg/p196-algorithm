import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0316 : leaf0316.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0317 : leaf0317.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0318 : leaf0318.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0319 : leaf0319.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0316 : checkRow ranks (fastLongPred 7) [3,11,14,3,0,9,12] 0 = true := by decide +kernel
theorem row_branch0317 : checkRow ranks (fastLongPred 7) [3,11,14,2,2,13,13] 1 = true := by decide +kernel
theorem row_branch0318 : checkRow ranks (fastLongPred 7) [3,11,14,3,13,9,14] 1 = true := by decide +kernel
theorem row_branch0319 : checkRow ranks (fastLongPred 7) [3,11,14,3,14,10,3] 1 = true := by decide +kernel
end SevenColumn.Certificate739
