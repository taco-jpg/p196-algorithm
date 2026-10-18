import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0040 : leaf0040.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0041 : leaf0041.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0042 : leaf0042.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0043 : leaf0043.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0040 : checkRow ranks (fastLongPred 7) [1,11,2,4,9,0,14] 0 = true := by decide +kernel
theorem row_branch0041 : checkRow ranks (fastLongPred 7) [1,11,5,2,17,17,8] 0 = true := by decide +kernel
theorem row_branch0042 : checkRow ranks (fastLongPred 7) [1,11,5,3,4,8,9] 0 = true := by decide +kernel
theorem row_branch0043 : checkRow ranks (fastLongPred 7) [1,11,5,3,3,6,18] 0 = true := by decide +kernel
end SevenColumn.Certificate739
