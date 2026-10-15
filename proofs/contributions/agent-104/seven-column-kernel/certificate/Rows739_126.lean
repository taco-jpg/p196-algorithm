import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0504 : leaf0504.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0505 : leaf0505.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0506 : leaf0506.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0507 : leaf0507.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0504 : checkRow ranks (fastLongPred 7) [6,5,8,8,10,13,12] 2 = true := by decide +kernel
theorem row_branch0505 : checkRow ranks (fastLongPred 7) [6,5,7,8,3,18,7] 2 = true := by decide +kernel
theorem row_branch0506 : checkRow ranks (fastLongPred 7) [6,5,7,3,13,15,0] 2 = true := by decide +kernel
theorem row_branch0507 : checkRow ranks (fastLongPred 7) [6,5,2,13,17,11,6] 2 = true := by decide +kernel
end SevenColumn.Certificate739
