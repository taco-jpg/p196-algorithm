import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0256 : leaf0256.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0257 : leaf0257.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0258 : leaf0258.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0259 : leaf0259.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0256 : checkRow ranks (fastLongPred 7) [3,11,14,0,13,12,11] 1 = true := by decide +kernel
theorem row_branch0257 : checkRow ranks (fastLongPred 7) [3,11,14,0,13,2,14] 1 = true := by decide +kernel
theorem row_branch0258 : checkRow ranks (fastLongPred 7) [3,11,14,0,14,13,1] 1 = true := by decide +kernel
theorem row_branch0259 : checkRow ranks (fastLongPred 7) [3,11,14,1,0,13,4] 0 = true := by decide +kernel
end SevenColumn.Certificate739
