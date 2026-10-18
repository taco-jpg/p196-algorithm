import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0236 : leaf0236.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0237 : leaf0237.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0238 : leaf0238.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0239 : leaf0239.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0236 : checkRow ranks (fastLongPred 7) [3,11,14,0,0,2,14] 1 = true := by decide +kernel
theorem row_branch0237 : checkRow ranks (fastLongPred 7) [3,11,14,0,1,2,12] 1 = true := by decide +kernel
theorem row_branch0238 : checkRow ranks (fastLongPred 7) [3,11,14,0,0,12,10] 1 = true := by decide +kernel
theorem row_branch0239 : checkRow ranks (fastLongPred 7) [3,11,14,0,2,2,10] 1 = true := by decide +kernel
end SevenColumn.Certificate739
