import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0176 : leaf0176.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0177 : leaf0177.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0178 : leaf0178.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0179 : leaf0179.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0176 : checkRow ranks (fastLongPred 7) [3,0,8,13,18,11,7] 1 = true := by decide +kernel
theorem row_branch0177 : checkRow ranks (fastLongPred 7) [3,2,1,10,14,11,11] 1 = true := by decide +kernel
theorem row_branch0178 : checkRow ranks (fastLongPred 7) [3,0,9,1,17,11,6] 9 = true := by decide +kernel
theorem row_branch0179 : checkRow ranks (fastLongPred 7) [3,0,8,13,16,7,2] 1 = true := by decide +kernel
end SevenColumn.Certificate739
