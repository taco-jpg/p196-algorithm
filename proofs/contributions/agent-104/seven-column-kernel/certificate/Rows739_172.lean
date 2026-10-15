import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0688 : leaf0688.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0689 : leaf0689.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0690 : leaf0690.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0691 : leaf0691.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0688 : checkRow ranks (fastLongPred 7) [7,3,9,9,6,7,6] 11 = true := by decide +kernel
theorem row_branch0689 : checkRow ranks (fastLongPred 7) [7,3,9,9,6,1,9] 2 = true := by decide +kernel
theorem row_branch0690 : checkRow ranks (fastLongPred 7) [7,3,9,9,5,0,5] 2 = true := by decide +kernel
theorem row_branch0691 : checkRow ranks (fastLongPred 7) [7,3,9,9,7,9,1] 11 = true := by decide +kernel
end SevenColumn.Certificate739
