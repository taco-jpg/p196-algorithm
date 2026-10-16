import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0304 : leaf0304.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0305 : leaf0305.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0306 : leaf0306.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0307 : leaf0307.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0304 : checkRow ranks (fastLongPred 7) [3,11,14,3,2,14,11] 1 = true := by decide +kernel
theorem row_branch0305 : checkRow ranks (fastLongPred 7) [3,11,14,3,3,14,9] 1 = true := by decide +kernel
theorem row_branch0306 : checkRow ranks (fastLongPred 7) [3,11,14,3,3,4,13] 1 = true := by decide +kernel
theorem row_branch0307 : checkRow ranks (fastLongPred 7) [3,11,14,3,2,9,9] 1 = true := by decide +kernel
end SevenColumn.Certificate739
