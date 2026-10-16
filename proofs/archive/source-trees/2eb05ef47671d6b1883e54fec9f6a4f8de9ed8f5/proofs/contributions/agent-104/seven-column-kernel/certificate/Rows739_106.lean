import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0424 : leaf0424.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0425 : leaf0425.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0426 : leaf0426.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0427 : leaf0427.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0424 : checkRow ranks (fastLongPred 7) [6,0,17,7,18,9,6] 2 = true := by decide +kernel
theorem row_branch0425 : checkRow ranks (fastLongPred 7) [6,0,17,7,18,4,9] 2 = true := by decide +kernel
theorem row_branch0426 : checkRow ranks (fastLongPred 7) [6,0,17,7,13,13,8] 2 = true := by decide +kernel
theorem row_branch0427 : checkRow ranks (fastLongPred 7) [6,0,17,3,9,3,13] 2 = true := by decide +kernel
end SevenColumn.Certificate739
