import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0924 : leaf0924.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0925 : leaf0925.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0926 : leaf0926.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0927 : leaf0927.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0924 : checkRow ranks (fastLongPred 7) [12,10,14,7,16,7,2] 3 = true := by decide +kernel
theorem row_branch0925 : checkRow ranks (fastLongPred 7) [12,10,14,7,18,5,3] 0 = true := by decide +kernel
theorem row_branch0926 : checkRow ranks (fastLongPred 7) [12,10,14,7,16,13,7] 3 = true := by decide +kernel
theorem row_branch0927 : checkRow ranks (fastLongPred 7) [12,10,14,7,18,18,16] 0 = true := by decide +kernel
end SevenColumn.Certificate739
