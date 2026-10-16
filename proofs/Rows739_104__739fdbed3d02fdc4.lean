import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0416 : leaf0416.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0417 : leaf0417.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0418 : leaf0418.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0419 : leaf0419.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0416 : checkRow ranks (fastLongPred 7) [6,0,17,3,4,13,5] 2 = true := by decide +kernel
theorem row_branch0417 : checkRow ranks (fastLongPred 7) [6,0,17,3,8,6,3] 2 = true := by decide +kernel
theorem row_branch0418 : checkRow ranks (fastLongPred 7) [6,0,17,3,8,1,8] 2 = true := by decide +kernel
theorem row_branch0419 : checkRow ranks (fastLongPred 7) [6,0,17,3,3,16,0] 2 = true := by decide +kernel
end SevenColumn.Certificate739
