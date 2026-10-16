import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0632 : leaf0632.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0633 : leaf0633.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0634 : leaf0634.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0635 : leaf0635.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0632 : checkRow ranks (fastLongPred 7) [7,3,9,6,4,1,9] 2 = true := by decide +kernel
theorem row_branch0633 : checkRow ranks (fastLongPred 7) [7,3,9,6,3,0,5] 2 = true := by decide +kernel
theorem row_branch0634 : checkRow ranks (fastLongPred 7) [7,3,9,6,0,7,6] 2 = true := by decide +kernel
theorem row_branch0635 : checkRow ranks (fastLongPred 7) [7,3,9,5,6,1,9] 1 = true := by decide +kernel
end SevenColumn.Certificate739
