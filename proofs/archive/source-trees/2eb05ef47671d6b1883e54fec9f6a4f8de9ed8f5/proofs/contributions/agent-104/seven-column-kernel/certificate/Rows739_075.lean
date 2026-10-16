import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0300 : leaf0300.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0301 : leaf0301.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0302 : leaf0302.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0303 : leaf0303.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0300 : checkRow ranks (fastLongPred 7) [3,11,14,2,11,3,12] 1 = true := by decide +kernel
theorem row_branch0301 : checkRow ranks (fastLongPred 7) [3,11,14,3,1,0,0] 1 = true := by decide +kernel
theorem row_branch0302 : checkRow ranks (fastLongPred 7) [3,11,14,3,1,14,13] 1 = true := by decide +kernel
theorem row_branch0303 : checkRow ranks (fastLongPred 7) [3,11,14,3,1,9,11] 1 = true := by decide +kernel
end SevenColumn.Certificate739
