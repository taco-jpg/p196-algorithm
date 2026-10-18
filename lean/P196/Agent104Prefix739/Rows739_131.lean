import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0524 : leaf0524.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0525 : leaf0525.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0526 : leaf0526.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0527 : leaf0527.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0524 : checkRow ranks (fastLongPred 7) [6,8,17,15,14,11,7] 2 = true := by decide +kernel
theorem row_branch0525 : checkRow ranks (fastLongPred 7) [6,8,17,11,4,16,9] 2 = true := by decide +kernel
theorem row_branch0526 : checkRow ranks (fastLongPred 7) [7,3,9,0,1,9,3] 0 = true := by decide +kernel
theorem row_branch0527 : checkRow ranks (fastLongPred 7) [7,3,9,0,3,0,7] 0 = true := by decide +kernel
end SevenColumn.Certificate739
