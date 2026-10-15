import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0444 : leaf0444.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0445 : leaf0445.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0446 : leaf0446.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0447 : leaf0447.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0444 : checkRow ranks (fastLongPred 7) [6,0,13,18,4,14,0] 0 = true := by decide +kernel
theorem row_branch0445 : checkRow ranks (fastLongPred 7) [6,4,10,12,0,9,3] 2 = true := by decide +kernel
theorem row_branch0446 : checkRow ranks (fastLongPred 7) [6,4,10,12,5,0,7] 2 = true := by decide +kernel
theorem row_branch0447 : checkRow ranks (fastLongPred 7) [6,4,10,12,1,12,5] 2 = true := by decide +kernel
end SevenColumn.Certificate739
