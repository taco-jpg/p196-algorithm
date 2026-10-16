import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0932 : leaf0932.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0933 : leaf0933.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0934 : leaf0934.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0935 : leaf0935.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0932 : checkRow ranks (fastLongPred 7) [12,10,14,16,7,14,9] 3 = true := by decide +kernel
theorem row_branch0933 : checkRow ranks (fastLongPred 7) [12,10,14,16,7,7,16] 3 = true := by decide +kernel
theorem row_branch0934 : checkRow ranks (fastLongPred 7) [12,10,14,16,16,7,2] 3 = true := by decide +kernel
theorem row_branch0935 : checkRow ranks (fastLongPred 7) [12,10,14,16,18,5,3] 2 = true := by decide +kernel
end SevenColumn.Certificate739
