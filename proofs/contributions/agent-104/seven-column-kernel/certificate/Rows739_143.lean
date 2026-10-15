import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0572 : leaf0572.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0573 : leaf0573.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0574 : leaf0574.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0575 : leaf0575.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0572 : checkRow ranks (fastLongPred 7) [7,3,9,1,9,6,3] 2 = true := by decide +kernel
theorem row_branch0573 : checkRow ranks (fastLongPred 7) [7,3,9,1,0,4,9] 2 = true := by decide +kernel
theorem row_branch0574 : checkRow ranks (fastLongPred 7) [7,3,9,2,9,3,5] 2 = true := by decide +kernel
theorem row_branch0575 : checkRow ranks (fastLongPred 7) [7,3,9,3,0,4,9] 1 = true := by decide +kernel
end SevenColumn.Certificate739
