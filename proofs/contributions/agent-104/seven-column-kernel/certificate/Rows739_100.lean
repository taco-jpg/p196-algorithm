import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0400 : leaf0400.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0401 : leaf0401.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0402 : leaf0402.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0403 : leaf0403.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0400 : checkRow ranks (fastLongPred 7) [6,0,12,13,7,17,5] 2 = true := by decide +kernel
theorem row_branch0401 : checkRow ranks (fastLongPred 7) [6,0,12,13,9,4,7] 2 = true := by decide +kernel
theorem row_branch0402 : checkRow ranks (fastLongPred 7) [6,0,12,13,8,17,8] 2 = true := by decide +kernel
theorem row_branch0403 : checkRow ranks (fastLongPred 7) [6,0,12,13,7,12,11] 2 = true := by decide +kernel
end SevenColumn.Certificate739
