import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0328 : leaf0328.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0329 : leaf0329.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0330 : leaf0330.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0331 : leaf0331.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0328 : checkRow ranks (fastLongPred 7) [3,11,14,4,4,9,14] 1 = true := by decide +kernel
theorem row_branch0329 : checkRow ranks (fastLongPred 7) [3,11,14,9,0,9,12] 0 = true := by decide +kernel
theorem row_branch0330 : checkRow ranks (fastLongPred 7) [3,11,14,9,0,0,1] 0 = true := by decide +kernel
theorem row_branch0331 : checkRow ranks (fastLongPred 7) [3,11,14,4,4,0,3] 1 = true := by decide +kernel
end SevenColumn.Certificate739
