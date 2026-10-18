import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0260 : leaf0260.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0261 : leaf0261.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0262 : leaf0262.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0263 : leaf0263.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0260 : checkRow ranks (fastLongPred 7) [3,11,14,1,0,3,12] 0 = true := by decide +kernel
theorem row_branch0261 : checkRow ranks (fastLongPred 7) [3,11,14,0,14,3,3] 1 = true := by decide +kernel
theorem row_branch0262 : checkRow ranks (fastLongPred 7) [3,11,14,1,1,13,3] 1 = true := by decide +kernel
theorem row_branch0263 : checkRow ranks (fastLongPred 7) [3,11,14,1,2,13,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
