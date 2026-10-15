import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0112 : leaf0112.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0113 : leaf0113.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0114 : leaf0114.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0115 : leaf0115.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0112 : checkRow ranks (fastLongPred 7) [1,15,16,11,10,1,5] 0 = true := by decide +kernel
theorem row_branch0113 : checkRow ranks (fastLongPred 7) [1,15,16,11,10,16,16] 0 = true := by decide +kernel
theorem row_branch0114 : checkRow ranks (fastLongPred 7) [1,15,16,11,10,9,10] 0 = true := by decide +kernel
theorem row_branch0115 : checkRow ranks (fastLongPred 7) [1,15,16,11,9,11,6] 0 = true := by decide +kernel
end SevenColumn.Certificate739
