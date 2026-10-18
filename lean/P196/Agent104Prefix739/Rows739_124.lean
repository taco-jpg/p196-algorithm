import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0496 : leaf0496.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0497 : leaf0497.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0498 : leaf0498.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0499 : leaf0499.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0496 : checkRow ranks (fastLongPred 7) [6,5,7,7,8,14,14] 2 = true := by decide +kernel
theorem row_branch0497 : checkRow ranks (fastLongPred 7) [6,5,7,7,2,3,7] 2 = true := by decide +kernel
theorem row_branch0498 : checkRow ranks (fastLongPred 7) [6,5,7,8,8,4,0] 2 = true := by decide +kernel
theorem row_branch0499 : checkRow ranks (fastLongPred 7) [6,5,7,8,9,8,9] 2 = true := by decide +kernel
end SevenColumn.Certificate739
