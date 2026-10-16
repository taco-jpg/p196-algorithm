import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0872 : leaf0872.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0873 : leaf0873.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0874 : leaf0874.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0875 : leaf0875.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0872 : checkRow ranks (fastLongPred 7) [12,9,1,16,15,18,18] 0 = true := by decide +kernel
theorem row_branch0873 : checkRow ranks (fastLongPred 7) [12,9,1,16,13,14,6] 3 = true := by decide +kernel
theorem row_branch0874 : checkRow ranks (fastLongPred 7) [12,9,1,16,4,9,9] 3 = true := by decide +kernel
theorem row_branch0875 : checkRow ranks (fastLongPred 7) [12,9,3,7,17,14,8] 3 = true := by decide +kernel
end SevenColumn.Certificate739
