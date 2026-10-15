import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0208 : leaf0208.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0209 : leaf0209.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0210 : leaf0210.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0211 : leaf0211.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0208 : checkRow ranks (fastLongPred 7) [3,2,11,8,0,16,6] 1 = true := by decide +kernel
theorem row_branch0209 : checkRow ranks (fastLongPred 7) [3,2,11,8,11,13,0] 1 = true := by decide +kernel
theorem row_branch0210 : checkRow ranks (fastLongPred 7) [3,2,11,8,3,4,7] 1 = true := by decide +kernel
theorem row_branch0211 : checkRow ranks (fastLongPred 7) [3,2,11,6,8,18,5] 1 = true := by decide +kernel
end SevenColumn.Certificate739
