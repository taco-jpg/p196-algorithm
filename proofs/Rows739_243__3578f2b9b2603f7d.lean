import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0972 : leaf0972.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0973 : leaf0973.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0974 : leaf0974.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0975 : leaf0975.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0972 : checkRow ranks (fastLongPred 7) [14,8,4,11,0,4,17] 2 = true := by decide +kernel
theorem row_branch0973 : checkRow ranks (fastLongPred 7) [14,8,4,10,4,16,3] 2 = true := by decide +kernel
theorem row_branch0974 : checkRow ranks (fastLongPred 7) [14,8,8,2,17,8,7] 3 = true := by decide +kernel
theorem row_branch0975 : checkRow ranks (fastLongPred 7) [14,8,8,11,8,17,17] 3 = true := by decide +kernel
end SevenColumn.Certificate739
