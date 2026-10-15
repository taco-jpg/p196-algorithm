import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0272 : leaf0272.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0273 : leaf0273.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0274 : leaf0274.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0275 : leaf0275.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0272 : checkRow ranks (fastLongPred 7) [3,11,14,1,10,12,4] 1 = true := by decide +kernel
theorem row_branch0273 : checkRow ranks (fastLongPred 7) [3,11,14,1,12,3,4] 1 = true := by decide +kernel
theorem row_branch0274 : checkRow ranks (fastLongPred 7) [3,11,14,1,13,3,12] 1 = true := by decide +kernel
theorem row_branch0275 : checkRow ranks (fastLongPred 7) [3,11,14,1,12,13,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
