import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0828 : leaf0828.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0829 : leaf0829.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0830 : leaf0830.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0831 : leaf0831.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0828 : checkRow ranks (fastLongPred 7) [12,1,14,5,13,15,7] 3 = true := by decide +kernel
theorem row_branch0829 : checkRow ranks (fastLongPred 7) [12,8,6,12,1,1,10] 1 = true := by decide +kernel
theorem row_branch0830 : checkRow ranks (fastLongPred 7) [12,8,6,12,9,3,18] 3 = true := by decide +kernel
theorem row_branch0831 : checkRow ranks (fastLongPred 7) [12,8,6,12,1,12,16] 1 = true := by decide +kernel
end SevenColumn.Certificate739
