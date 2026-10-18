import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0488 : leaf0488.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0489 : leaf0489.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0490 : leaf0490.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0491 : leaf0491.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0488 : checkRow ranks (fastLongPred 7) [6,5,7,3,9,12,13] 2 = true := by decide +kernel
theorem row_branch0489 : checkRow ranks (fastLongPred 7) [6,5,7,2,12,3,13] 5 = true := by decide +kernel
theorem row_branch0490 : checkRow ranks (fastLongPred 7) [6,5,2,18,7,13,12] 5 = true := by decide +kernel
theorem row_branch0491 : checkRow ranks (fastLongPred 7) [6,5,7,3,14,12,9] 2 = true := by decide +kernel
end SevenColumn.Certificate739
