import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0860 : leaf0860.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0861 : leaf0861.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0862 : leaf0862.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0863 : leaf0863.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0860 : checkRow ranks (fastLongPred 7) [12,9,1,14,1,8,14] 3 = true := by decide +kernel
theorem row_branch0861 : checkRow ranks (fastLongPred 7) [12,9,1,14,4,4,13] 3 = true := by decide +kernel
theorem row_branch0862 : checkRow ranks (fastLongPred 7) [12,9,1,14,2,0,14] 3 = true := by decide +kernel
theorem row_branch0863 : checkRow ranks (fastLongPred 7) [12,9,1,14,11,9,5] 3 = true := by decide +kernel
end SevenColumn.Certificate739
