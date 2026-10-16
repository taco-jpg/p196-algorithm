import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0280 : leaf0280.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0281 : leaf0281.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0282 : leaf0282.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0283 : leaf0283.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0280 : checkRow ranks (fastLongPred 7) [3,11,14,2,1,4,4] 1 = true := by decide +kernel
theorem row_branch0281 : checkRow ranks (fastLongPred 7) [3,11,14,2,2,4,2] 1 = true := by decide +kernel
theorem row_branch0282 : checkRow ranks (fastLongPred 7) [3,11,14,2,1,14,0] 1 = true := by decide +kernel
theorem row_branch0283 : checkRow ranks (fastLongPred 7) [3,11,14,2,0,14,2] 1 = true := by decide +kernel
end SevenColumn.Certificate739
