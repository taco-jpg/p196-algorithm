import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0976 : leaf0976.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0977 : leaf0977.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0978 : leaf0978.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0979 : leaf0979.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0976 : checkRow ranks (fastLongPred 7) [14,8,8,3,17,14,0] 3 = true := by decide +kernel
theorem row_branch0977 : checkRow ranks (fastLongPred 7) [14,8,4,11,13,18,12] 2 = true := by decide +kernel
theorem row_branch0978 : checkRow ranks (fastLongPred 7) [14,8,13,1,4,16,11] 3 = true := by decide +kernel
theorem row_branch0979 : checkRow ranks (fastLongPred 7) [14,8,13,10,4,8,8] 3 = true := by decide +kernel
end SevenColumn.Certificate739
