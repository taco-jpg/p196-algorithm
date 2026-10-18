import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0396 : leaf0396.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0397 : leaf0397.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0398 : leaf0398.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0399 : leaf0399.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0396 : checkRow ranks (fastLongPred 7) [5,13,16,16,6,8,4] 2 = true := by decide +kernel
theorem row_branch0397 : checkRow ranks (fastLongPred 7) [6,0,12,13,3,2,18] 2 = true := by decide +kernel
theorem row_branch0398 : checkRow ranks (fastLongPred 7) [6,0,12,13,4,5,5] 2 = true := by decide +kernel
theorem row_branch0399 : checkRow ranks (fastLongPred 7) [6,0,12,13,3,8,1] 2 = true := by decide +kernel
end SevenColumn.Certificate739
