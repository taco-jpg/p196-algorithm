import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0368 : leaf0368.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0369 : leaf0369.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0370 : leaf0370.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0371 : leaf0371.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0368 : checkRow ranks (fastLongPred 7) [4,9,15,15,6,18,16] 0 = true := by decide +kernel
theorem row_branch0369 : checkRow ranks (fastLongPred 7) [4,9,15,10,12,3,15] 2 = true := by decide +kernel
theorem row_branch0370 : checkRow ranks (fastLongPred 7) [4,2,11,16,8,4,18] 2 = true := by decide +kernel
theorem row_branch0371 : checkRow ranks (fastLongPred 7) [4,14,15,5,7,4,2] 2 = true := by decide +kernel
end SevenColumn.Certificate739
