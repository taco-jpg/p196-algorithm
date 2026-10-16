import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0356 : leaf0356.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0357 : leaf0357.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0358 : leaf0358.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0359 : leaf0359.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0356 : checkRow ranks (fastLongPred 7) [3,14,6,10,6,14,0] 0 = true := by decide +kernel
theorem row_branch0357 : checkRow ranks (fastLongPred 7) [3,14,6,12,16,14,1] 1 = true := by decide +kernel
theorem row_branch0358 : checkRow ranks (fastLongPred 7) [3,14,6,12,11,12,9] 1 = true := by decide +kernel
theorem row_branch0359 : checkRow ranks (fastLongPred 7) [3,14,7,17,5,9,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
