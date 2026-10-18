import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0432 : leaf0432.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0433 : leaf0433.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0434 : leaf0434.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0435 : leaf0435.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0432 : checkRow ranks (fastLongPred 7) [6,4,3,6,4,15,1] 2 = true := by decide +kernel
theorem row_branch0433 : checkRow ranks (fastLongPred 7) [6,4,3,6,3,1,10] 2 = true := by decide +kernel
theorem row_branch0434 : checkRow ranks (fastLongPred 7) [6,4,3,6,0,0,9] 0 = true := by decide +kernel
theorem row_branch0435 : checkRow ranks (fastLongPred 7) [6,4,7,11,9,11,12] 2 = true := by decide +kernel
end SevenColumn.Certificate739
