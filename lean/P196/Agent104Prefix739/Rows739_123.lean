import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0492 : leaf0492.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0493 : leaf0493.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0494 : leaf0494.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0495 : leaf0495.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0492 : checkRow ranks (fastLongPred 7) [6,5,7,3,18,6,2] 2 = true := by decide +kernel
theorem row_branch0493 : checkRow ranks (fastLongPred 7) [6,5,7,3,18,1,6] 2 = true := by decide +kernel
theorem row_branch0494 : checkRow ranks (fastLongPred 7) [6,5,7,7,6,13,3] 2 = true := by decide +kernel
theorem row_branch0495 : checkRow ranks (fastLongPred 7) [6,5,7,8,3,13,11] 2 = true := by decide +kernel
end SevenColumn.Certificate739
