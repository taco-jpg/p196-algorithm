import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0372 : leaf0372.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0373 : leaf0373.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0374 : leaf0374.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0375 : leaf0375.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0372 : checkRow ranks (fastLongPred 7) [5,3,10,8,18,10,18] 2 = true := by decide +kernel
theorem row_branch0373 : checkRow ranks (fastLongPred 7) [4,14,16,5,3,13,10] 2 = true := by decide +kernel
theorem row_branch0374 : checkRow ranks (fastLongPred 7) [5,5,3,14,18,9,11] 0 = true := by decide +kernel
theorem row_branch0375 : checkRow ranks (fastLongPred 7) [5,8,0,9,9,6,11] 0 = true := by decide +kernel
end SevenColumn.Certificate739
