import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0164 : leaf0164.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0165 : leaf0165.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0166 : leaf0166.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0167 : leaf0167.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0164 : checkRow ranks (fastLongPred 7) [3,0,6,6,9,12,15] 1 = true := by decide +kernel
theorem row_branch0165 : checkRow ranks (fastLongPred 7) [3,0,6,8,5,18,9] 1 = true := by decide +kernel
theorem row_branch0166 : checkRow ranks (fastLongPred 7) [3,0,6,8,16,14,9] 1 = true := by decide +kernel
theorem row_branch0167 : checkRow ranks (fastLongPred 7) [3,0,6,8,16,10,6] 1 = true := by decide +kernel
end SevenColumn.Certificate739
