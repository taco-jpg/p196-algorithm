import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0832 : leaf0832.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0833 : leaf0833.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0834 : leaf0834.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0835 : leaf0835.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0832 : checkRow ranks (fastLongPred 7) [12,8,6,12,10,3,6] 2 = true := by decide +kernel
theorem row_branch0833 : checkRow ranks (fastLongPred 7) [12,8,15,3,0,4,14] 3 = true := by decide +kernel
theorem row_branch0834 : checkRow ranks (fastLongPred 7) [12,8,6,12,15,3,15] 3 = true := by decide +kernel
theorem row_branch0835 : checkRow ranks (fastLongPred 7) [12,8,6,12,9,13,5] 3 = true := by decide +kernel
end SevenColumn.Certificate739
