import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0612 : leaf0612.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0613 : leaf0613.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0614 : leaf0614.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0615 : leaf0615.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0612 : checkRow ranks (fastLongPred 7) [7,3,9,5,2,2,0] 2 = true := by decide +kernel
theorem row_branch0613 : checkRow ranks (fastLongPred 7) [7,3,9,5,3,3,4] 2 = true := by decide +kernel
theorem row_branch0614 : checkRow ranks (fastLongPred 7) [7,3,9,5,2,7,7] 2 = true := by decide +kernel
theorem row_branch0615 : checkRow ranks (fastLongPred 7) [7,3,9,5,4,4,8] 2 = true := by decide +kernel
end SevenColumn.Certificate739
