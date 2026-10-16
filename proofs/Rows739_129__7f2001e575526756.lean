import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0516 : leaf0516.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0517 : leaf0517.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0518 : leaf0518.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0519 : leaf0519.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0516 : checkRow ranks (fastLongPred 7) [6,8,17,11,0,0,1] 35 = true := by decide +kernel
theorem row_branch0517 : checkRow ranks (fastLongPred 7) [6,8,13,5,14,11,2] 2 = true := by decide +kernel
theorem row_branch0518 : checkRow ranks (fastLongPred 7) [6,8,17,15,9,15,4] 2 = true := by decide +kernel
theorem row_branch0519 : checkRow ranks (fastLongPred 7) [6,8,17,15,14,5,1] 2 = true := by decide +kernel
end SevenColumn.Certificate739
