import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0732 : leaf0732.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0733 : leaf0733.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0734 : leaf0734.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0735 : leaf0735.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0732 : checkRow ranks (fastLongPred 7) [8,5,3,18,7,10,7] 1 = true := by decide +kernel
theorem row_branch0733 : checkRow ranks (fastLongPred 7) [8,5,8,8,8,0,2] 0 = true := by decide +kernel
theorem row_branch0734 : checkRow ranks (fastLongPred 7) [8,5,8,3,18,4,5] 3 = true := by decide +kernel
theorem row_branch0735 : checkRow ranks (fastLongPred 7) [9,9,13,2,16,7,11] 3 = true := by decide +kernel
end SevenColumn.Certificate739
