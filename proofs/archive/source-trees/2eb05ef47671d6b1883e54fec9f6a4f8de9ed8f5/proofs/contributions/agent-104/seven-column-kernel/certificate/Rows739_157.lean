import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0628 : leaf0628.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0629 : leaf0629.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0630 : leaf0630.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0631 : leaf0631.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0628 : checkRow ranks (fastLongPred 7) [7,3,9,6,2,4,8] 2 = true := by decide +kernel
theorem row_branch0629 : checkRow ranks (fastLongPred 7) [7,3,9,6,1,9,1] 2 = true := by decide +kernel
theorem row_branch0630 : checkRow ranks (fastLongPred 7) [7,3,9,6,3,6,2] 2 = true := by decide +kernel
theorem row_branch0631 : checkRow ranks (fastLongPred 7) [7,3,9,6,4,7,6] 2 = true := by decide +kernel
end SevenColumn.Certificate739
