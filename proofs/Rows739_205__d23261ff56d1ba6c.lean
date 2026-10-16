import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0820 : leaf0820.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0821 : leaf0821.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0822 : leaf0822.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0823 : leaf0823.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0820 : checkRow ranks (fastLongPred 7) [12,8,6,3,0,13,15] 3 = true := by decide +kernel
theorem row_branch0821 : checkRow ranks (fastLongPred 7) [12,8,6,3,0,4,14] 3 = true := by decide +kernel
theorem row_branch0822 : checkRow ranks (fastLongPred 7) [12,8,6,3,10,0,18] 0 = true := by decide +kernel
theorem row_branch0823 : checkRow ranks (fastLongPred 7) [12,8,6,12,0,2,7] 1 = true := by decide +kernel
end SevenColumn.Certificate739
