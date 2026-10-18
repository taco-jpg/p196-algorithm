import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0392 : leaf0392.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0393 : leaf0393.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0394 : leaf0394.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0395 : leaf0395.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0392 : checkRow ranks (fastLongPred 7) [5,18,6,15,15,1,5] 0 = true := by decide +kernel
theorem row_branch0393 : checkRow ranks (fastLongPred 7) [6,0,12,12,1,18,3] 0 = true := by decide +kernel
theorem row_branch0394 : checkRow ranks (fastLongPred 7) [5,18,6,16,16,8,15] 0 = true := by decide +kernel
theorem row_branch0395 : checkRow ranks (fastLongPred 7) [5,18,6,12,1,9,11] 0 = true := by decide +kernel
end SevenColumn.Certificate739
