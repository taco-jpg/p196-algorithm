import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0404 : leaf0404.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0405 : leaf0405.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0406 : leaf0406.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0407 : leaf0407.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0404 : checkRow ranks (fastLongPred 7) [6,0,12,16,16,3,14] 2 = true := by decide +kernel
theorem row_branch0405 : checkRow ranks (fastLongPred 7) [6,0,12,17,13,6,8] 2 = true := by decide +kernel
theorem row_branch0406 : checkRow ranks (fastLongPred 7) [6,0,12,17,13,1,13] 2 = true := by decide +kernel
theorem row_branch0407 : checkRow ranks (fastLongPred 7) [6,0,12,17,17,15,11] 2 = true := by decide +kernel
end SevenColumn.Certificate739
