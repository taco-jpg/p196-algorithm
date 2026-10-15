import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0168 : leaf0168.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0169 : leaf0169.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0170 : leaf0170.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0171 : leaf0171.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0168 : checkRow ranks (fastLongPred 7) [3,0,8,11,0,12,4] 1 = true := by decide +kernel
theorem row_branch0169 : checkRow ranks (fastLongPred 7) [3,0,8,11,11,8,2] 1 = true := by decide +kernel
theorem row_branch0170 : checkRow ranks (fastLongPred 7) [3,0,8,11,3,17,6] 1 = true := by decide +kernel
theorem row_branch0171 : checkRow ranks (fastLongPred 7) [3,0,6,8,18,17,17] 1 = true := by decide +kernel
end SevenColumn.Certificate739
