import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0028 : leaf0028.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0029 : leaf0029.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0030 : leaf0030.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0031 : leaf0031.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0028 : checkRow ranks (fastLongPred 7) [1,10,3,16,18,15,9] 0 = true := by decide +kernel
theorem row_branch0029 : checkRow ranks (fastLongPred 7) [1,10,3,15,15,3,16] 0 = true := by decide +kernel
theorem row_branch0030 : checkRow ranks (fastLongPred 7) [1,10,2,13,1,2,3] 0 = true := by decide +kernel
theorem row_branch0031 : checkRow ranks (fastLongPred 7) [1,11,1,7,17,5,10] 0 = true := by decide +kernel
end SevenColumn.Certificate739
