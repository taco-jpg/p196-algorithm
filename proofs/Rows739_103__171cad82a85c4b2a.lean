import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0412 : leaf0412.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0413 : leaf0413.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0414 : leaf0414.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0415 : leaf0415.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0412 : checkRow ranks (fastLongPred 7) [6,0,12,12,6,8,3] 2 = true := by decide +kernel
theorem row_branch0413 : checkRow ranks (fastLongPred 7) [6,0,17,2,2,7,10] 2 = true := by decide +kernel
theorem row_branch0414 : checkRow ranks (fastLongPred 7) [6,0,17,3,3,11,6] 2 = true := by decide +kernel
theorem row_branch0415 : checkRow ranks (fastLongPred 7) [6,0,17,2,6,17,8] 2 = true := by decide +kernel
end SevenColumn.Certificate739
