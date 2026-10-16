import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0196 : leaf0196.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0197 : leaf0197.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0198 : leaf0198.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0199 : leaf0199.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0196 : checkRow ranks (fastLongPred 7) [3,2,5,6,10,16,6] 1 = true := by decide +kernel
theorem row_branch0197 : checkRow ranks (fastLongPred 7) [3,2,5,8,8,0,4] 1 = true := by decide +kernel
theorem row_branch0198 : checkRow ranks (fastLongPred 7) [3,2,5,8,18,0,16] 1 = true := by decide +kernel
theorem row_branch0199 : checkRow ranks (fastLongPred 7) [3,2,5,8,15,18,0] 0 = true := by decide +kernel
end SevenColumn.Certificate739
