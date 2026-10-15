import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf1000 : leaf1000.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1001 : leaf1001.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1002 : leaf1002.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1003 : leaf1003.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch1000 : checkRow ranks (fastLongPred 7) [14,17,8,11,17,4,1] 3 = true := by decide +kernel
theorem row_branch1001 : checkRow ranks (fastLongPred 7) [14,17,4,11,0,12,7] 3 = true := by decide +kernel
theorem row_branch1002 : checkRow ranks (fastLongPred 7) [14,17,13,11,0,4,9] 0 = true := by decide +kernel
theorem row_branch1003 : checkRow ranks (fastLongPred 7) [14,17,17,2,17,7,16] 3 = true := by decide +kernel
end SevenColumn.Certificate739
