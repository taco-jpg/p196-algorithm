import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0068 : leaf0068.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0069 : leaf0069.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0070 : leaf0070.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0071 : leaf0071.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0068 : checkRow ranks (fastLongPred 7) [1,15,16,9,10,16,15] 0 = true := by decide +kernel
theorem row_branch0069 : checkRow ranks (fastLongPred 7) [1,15,16,9,10,1,4] 0 = true := by decide +kernel
theorem row_branch0070 : checkRow ranks (fastLongPred 7) [1,15,16,9,14,6,11] 0 = true := by decide +kernel
theorem row_branch0071 : checkRow ranks (fastLongPred 7) [1,15,16,9,15,5,11] 0 = true := by decide +kernel
end SevenColumn.Certificate739
