import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0348 : leaf0348.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0349 : leaf0349.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0350 : leaf0350.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0351 : leaf0351.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0348 : checkRow ranks (fastLongPred 7) [3,11,14,9,0,14,14] 0 = true := by decide +kernel
theorem row_branch0349 : checkRow ranks (fastLongPred 7) [3,12,2,17,15,8,14] 1 = true := by decide +kernel
theorem row_branch0350 : checkRow ranks (fastLongPred 7) [3,12,3,17,16,8,10] 1 = true := by decide +kernel
theorem row_branch0351 : checkRow ranks (fastLongPred 7) [3,12,3,15,13,12,12] 1 = true := by decide +kernel
end SevenColumn.Certificate739
