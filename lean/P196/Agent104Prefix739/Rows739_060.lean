import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0240 : leaf0240.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0241 : leaf0241.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0242 : leaf0242.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0243 : leaf0243.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0240 : checkRow ranks (fastLongPred 7) [3,11,14,0,3,2,4] 1 = true := by decide +kernel
theorem row_branch0241 : checkRow ranks (fastLongPred 7) [3,11,14,0,2,12,2] 1 = true := by decide +kernel
theorem row_branch0242 : checkRow ranks (fastLongPred 7) [3,11,14,0,1,12,4] 1 = true := by decide +kernel
theorem row_branch0243 : checkRow ranks (fastLongPred 7) [3,11,14,0,4,2,3] 1 = true := by decide +kernel
end SevenColumn.Certificate739
