import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0544 : leaf0544.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0545 : leaf0545.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0546 : leaf0546.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0547 : leaf0547.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0544 : checkRow ranks (fastLongPred 7) [7,3,9,1,1,6,4] 2 = true := by decide +kernel
theorem row_branch0545 : checkRow ranks (fastLongPred 7) [7,3,9,1,3,3,5] 2 = true := by decide +kernel
theorem row_branch0546 : checkRow ranks (fastLongPred 7) [7,3,9,1,4,4,9] 2 = true := by decide +kernel
theorem row_branch0547 : checkRow ranks (fastLongPred 7) [7,3,9,1,3,9,2] 2 = true := by decide +kernel
end SevenColumn.Certificate739
