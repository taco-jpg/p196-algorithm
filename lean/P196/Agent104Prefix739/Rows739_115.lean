import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0460 : leaf0460.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0461 : leaf0461.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0462 : leaf0462.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0463 : leaf0463.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0460 : checkRow ranks (fastLongPred 7) [6,4,10,17,16,8,0] 2 = true := by decide +kernel
theorem row_branch0461 : checkRow ranks (fastLongPred 7) [6,4,11,13,8,1,8] 2 = true := by decide +kernel
theorem row_branch0462 : checkRow ranks (fastLongPred 7) [6,4,10,17,17,14,10] 2 = true := by decide +kernel
theorem row_branch0463 : checkRow ranks (fastLongPred 7) [6,4,11,13,10,7,6] 2 = true := by decide +kernel
end SevenColumn.Certificate739
