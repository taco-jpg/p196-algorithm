import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0880 : leaf0880.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0881 : leaf0881.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0882 : leaf0882.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0883 : leaf0883.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0880 : checkRow ranks (fastLongPred 7) [12,9,3,16,8,12,18] 3 = true := by decide +kernel
theorem row_branch0881 : checkRow ranks (fastLongPred 7) [12,9,3,8,10,8,0] 3 = true := by decide +kernel
theorem row_branch0882 : checkRow ranks (fastLongPred 7) [12,9,3,17,1,14,2] 1 = true := by decide +kernel
theorem row_branch0883 : checkRow ranks (fastLongPred 7) [12,9,3,17,10,14,10] 1 = true := by decide +kernel
end SevenColumn.Certificate739
