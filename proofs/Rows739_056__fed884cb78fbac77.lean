import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0224 : leaf0224.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0225 : leaf0225.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0226 : leaf0226.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0227 : leaf0227.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0224 : checkRow ranks (fastLongPred 7) [3,2,14,3,15,8,14] 1 = true := by decide +kernel
theorem row_branch0225 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,1,16] 1 = true := by decide +kernel
theorem row_branch0226 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,12,16] 7 = true := by decide +kernel
theorem row_branch0227 : checkRow ranks (fastLongPred 7) [3,2,13,13,14,3,2] 1 = true := by decide +kernel
end SevenColumn.Certificate739
