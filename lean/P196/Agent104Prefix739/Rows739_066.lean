import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0264 : leaf0264.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0265 : leaf0265.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0266 : leaf0266.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0267 : leaf0267.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0264 : checkRow ranks (fastLongPred 7) [3,11,14,1,2,3,9] 1 = true := by decide +kernel
theorem row_branch0265 : checkRow ranks (fastLongPred 7) [3,11,14,1,3,12,14] 1 = true := by decide +kernel
theorem row_branch0266 : checkRow ranks (fastLongPred 7) [3,11,14,1,4,12,12] 1 = true := by decide +kernel
theorem row_branch0267 : checkRow ranks (fastLongPred 7) [3,11,14,1,4,3,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
