import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0616 : leaf0616.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0617 : leaf0617.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0618 : leaf0618.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0619 : leaf0619.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0616 : checkRow ranks (fastLongPred 7) [7,3,9,5,5,6,2] 1 = true := by decide +kernel
theorem row_branch0617 : checkRow ranks (fastLongPred 7) [7,3,9,5,5,0,5] 2 = true := by decide +kernel
theorem row_branch0618 : checkRow ranks (fastLongPred 7) [7,3,9,5,3,9,1] 2 = true := by decide +kernel
theorem row_branch0619 : checkRow ranks (fastLongPred 7) [7,3,9,5,1,6,2] 1 = true := by decide +kernel
end SevenColumn.Certificate739
