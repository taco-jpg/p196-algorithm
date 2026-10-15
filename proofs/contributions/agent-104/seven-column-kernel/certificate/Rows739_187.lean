import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0748 : leaf0748.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0749 : leaf0749.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0750 : leaf0750.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0751 : leaf0751.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0748 : checkRow ranks (fastLongPred 7) [11,7,14,2,2,12,9] 5 = true := by decide +kernel
theorem row_branch0749 : checkRow ranks (fastLongPred 7) [11,7,5,13,4,16,2] 3 = true := by decide +kernel
theorem row_branch0750 : checkRow ranks (fastLongPred 7) [11,7,14,11,11,5,13] 3 = true := by decide +kernel
theorem row_branch0751 : checkRow ranks (fastLongPred 7) [11,16,5,2,2,12,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
