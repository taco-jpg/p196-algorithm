import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0528 : leaf0528.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0529 : leaf0529.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0530 : leaf0530.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0531 : leaf0531.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0528 : checkRow ranks (fastLongPred 7) [7,3,9,0,2,5,0] 0 = true := by decide +kernel
theorem row_branch0529 : checkRow ranks (fastLongPred 7) [7,3,9,0,4,2,1] 0 = true := by decide +kernel
theorem row_branch0530 : checkRow ranks (fastLongPred 7) [7,3,9,0,5,3,5] 0 = true := by decide +kernel
theorem row_branch0531 : checkRow ranks (fastLongPred 7) [7,3,9,0,4,7,8] 0 = true := by decide +kernel
end SevenColumn.Certificate739
