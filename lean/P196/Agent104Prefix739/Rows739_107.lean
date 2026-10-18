import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0428 : leaf0428.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0429 : leaf0429.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0430 : leaf0430.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0431 : leaf0431.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0428 : checkRow ranks (fastLongPred 7) [6,4,3,1,10,4,2] 2 = true := by decide +kernel
theorem row_branch0429 : checkRow ranks (fastLongPred 7) [6,4,3,1,15,0,15] 0 = true := by decide +kernel
theorem row_branch0430 : checkRow ranks (fastLongPred 7) [6,4,3,1,10,10,5] 2 = true := by decide +kernel
theorem row_branch0431 : checkRow ranks (fastLongPred 7) [6,4,3,6,0,6,13] 0 = true := by decide +kernel
end SevenColumn.Certificate739
