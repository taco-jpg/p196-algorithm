import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0576 : leaf0576.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0577 : leaf0577.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0578 : leaf0578.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0579 : leaf0579.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0576 : checkRow ranks (fastLongPred 7) [7,3,9,2,9,9,2] 2 = true := by decide +kernel
theorem row_branch0577 : checkRow ranks (fastLongPred 7) [7,3,9,3,1,6,3] 1 = true := by decide +kernel
theorem row_branch0578 : checkRow ranks (fastLongPred 7) [7,3,9,3,2,7,7] 2 = true := by decide +kernel
theorem row_branch0579 : checkRow ranks (fastLongPred 7) [7,3,9,3,2,2,0] 2 = true := by decide +kernel
end SevenColumn.Certificate739
