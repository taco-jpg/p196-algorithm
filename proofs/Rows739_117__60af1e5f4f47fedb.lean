import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0468 : leaf0468.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0469 : leaf0469.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0470 : leaf0470.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0471 : leaf0471.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0468 : checkRow ranks (fastLongPred 7) [6,5,2,12,11,17,0] 0 = true := by decide +kernel
theorem row_branch0469 : checkRow ranks (fastLongPred 7) [6,4,11,18,4,17,14] 0 = true := by decide +kernel
theorem row_branch0470 : checkRow ranks (fastLongPred 7) [6,5,2,13,13,2,6] 5 = true := by decide +kernel
theorem row_branch0471 : checkRow ranks (fastLongPred 7) [6,5,2,13,14,3,17] 5 = true := by decide +kernel
end SevenColumn.Certificate739
