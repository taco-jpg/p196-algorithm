import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0296 : leaf0296.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0297 : leaf0297.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0298 : leaf0298.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0299 : leaf0299.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0296 : checkRow ranks (fastLongPred 7) [3,11,14,2,13,14,3] 1 = true := by decide +kernel
theorem row_branch0297 : checkRow ranks (fastLongPred 7) [3,11,14,3,0,0,1] 0 = true := by decide +kernel
theorem row_branch0298 : checkRow ranks (fastLongPred 7) [3,11,14,2,14,9,9] 1 = true := by decide +kernel
theorem row_branch0299 : checkRow ranks (fastLongPred 7) [3,11,14,2,13,9,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
