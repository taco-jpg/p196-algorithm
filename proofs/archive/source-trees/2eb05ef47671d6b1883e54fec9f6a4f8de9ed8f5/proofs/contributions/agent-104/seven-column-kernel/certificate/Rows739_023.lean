import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0092 : leaf0092.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0093 : leaf0093.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0094 : leaf0094.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0095 : leaf0095.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0092 : checkRow ranks (fastLongPred 7) [1,15,16,10,6,0,5] 0 = true := by decide +kernel
theorem row_branch0093 : checkRow ranks (fastLongPred 7) [1,15,16,10,0,7,7] 0 = true := by decide +kernel
theorem row_branch0094 : checkRow ranks (fastLongPred 7) [1,15,16,10,14,4,14] 0 = true := by decide +kernel
theorem row_branch0095 : checkRow ranks (fastLongPred 7) [1,15,16,10,15,1,7] 0 = true := by decide +kernel
end SevenColumn.Certificate739
