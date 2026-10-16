import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0968 : leaf0968.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0969 : leaf0969.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0970 : leaf0970.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0971 : leaf0971.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0968 : checkRow ranks (fastLongPred 7) [14,4,0,18,18,13,3] 1 = true := by decide +kernel
theorem row_branch0969 : checkRow ranks (fastLongPred 7) [12,17,15,12,10,2,0] 3 = true := by decide +kernel
theorem row_branch0970 : checkRow ranks (fastLongPred 7) [12,17,15,12,1,0,3] 0 = true := by decide +kernel
theorem row_branch0971 : checkRow ranks (fastLongPred 7) [14,8,4,2,0,13,17] 2 = true := by decide +kernel
end SevenColumn.Certificate739
