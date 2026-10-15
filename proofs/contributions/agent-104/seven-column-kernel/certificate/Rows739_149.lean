import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0596 : leaf0596.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0597 : leaf0597.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0598 : leaf0598.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0599 : leaf0599.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0596 : checkRow ranks (fastLongPred 7) [7,3,9,4,3,0,6] 2 = true := by decide +kernel
theorem row_branch0597 : checkRow ranks (fastLongPred 7) [7,3,9,4,4,2,0] 2 = true := by decide +kernel
theorem row_branch0598 : checkRow ranks (fastLongPred 7) [7,3,9,4,3,6,3] 2 = true := by decide +kernel
theorem row_branch0599 : checkRow ranks (fastLongPred 7) [7,3,9,4,5,3,4] 2 = true := by decide +kernel
end SevenColumn.Certificate739
