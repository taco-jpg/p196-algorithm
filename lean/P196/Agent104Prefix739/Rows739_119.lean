import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0476 : leaf0476.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0477 : leaf0477.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0478 : leaf0478.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0479 : leaf0479.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0476 : checkRow ranks (fastLongPred 7) [6,5,2,13,17,16,2] 2 = true := by decide +kernel
theorem row_branch0477 : checkRow ranks (fastLongPred 7) [6,5,2,17,1,13,3] 2 = true := by decide +kernel
theorem row_branch0478 : checkRow ranks (fastLongPred 7) [6,5,2,13,18,13,10] 2 = true := by decide +kernel
theorem row_branch0479 : checkRow ranks (fastLongPred 7) [6,5,2,18,3,0,0] 5 = true := by decide +kernel
end SevenColumn.Certificate739
