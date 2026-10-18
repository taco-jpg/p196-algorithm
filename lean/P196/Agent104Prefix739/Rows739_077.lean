import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0308 : leaf0308.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0309 : leaf0309.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0310 : leaf0310.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0311 : leaf0311.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0308 : checkRow ranks (fastLongPred 7) [3,11,14,3,4,14,4] 1 = true := by decide +kernel
theorem row_branch0309 : checkRow ranks (fastLongPred 7) [3,11,14,3,10,4,2] 1 = true := by decide +kernel
theorem row_branch0310 : checkRow ranks (fastLongPred 7) [3,11,14,3,9,14,0] 1 = true := by decide +kernel
theorem row_branch0311 : checkRow ranks (fastLongPred 7) [3,11,14,3,11,9,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
