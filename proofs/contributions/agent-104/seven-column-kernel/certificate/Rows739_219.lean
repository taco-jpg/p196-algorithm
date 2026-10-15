import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0876 : leaf0876.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0877 : leaf0877.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0878 : leaf0878.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0879 : leaf0879.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0876 : checkRow ranks (fastLongPred 7) [12,9,3,8,1,15,7] 3 = true := by decide +kernel
theorem row_branch0877 : checkRow ranks (fastLongPred 7) [12,9,3,8,1,5,13] 3 = true := by decide +kernel
theorem row_branch0878 : checkRow ranks (fastLongPred 7) [12,9,3,9,13,14,18] 3 = true := by decide +kernel
theorem row_branch0879 : checkRow ranks (fastLongPred 7) [12,9,3,16,17,12,0] 3 = true := by decide +kernel
end SevenColumn.Certificate739
