import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0288 : leaf0288.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0289 : leaf0289.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0290 : leaf0290.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0291 : leaf0291.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0288 : checkRow ranks (fastLongPred 7) [3,11,14,2,3,13,12] 1 = true := by decide +kernel
theorem row_branch0289 : checkRow ranks (fastLongPred 7) [3,11,14,2,9,13,2] 1 = true := by decide +kernel
theorem row_branch0290 : checkRow ranks (fastLongPred 7) [3,11,14,2,10,13,1] 1 = true := by decide +kernel
theorem row_branch0291 : checkRow ranks (fastLongPred 7) [3,11,14,2,10,3,4] 1 = true := by decide +kernel
end SevenColumn.Certificate739
