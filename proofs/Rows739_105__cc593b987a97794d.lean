import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0420 : leaf0420.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0421 : leaf0421.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0422 : leaf0422.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0423 : leaf0423.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0420 : checkRow ranks (fastLongPred 7) [6,0,17,6,12,2,11] 2 = true := by decide +kernel
theorem row_branch0421 : checkRow ranks (fastLongPred 7) [6,0,17,6,18,14,0] 0 = true := by decide +kernel
theorem row_branch0422 : checkRow ranks (fastLongPred 7) [6,0,17,6,16,12,4] 2 = true := by decide +kernel
theorem row_branch0423 : checkRow ranks (fastLongPred 7) [6,0,17,7,13,18,13] 2 = true := by decide +kernel
end SevenColumn.Certificate739
