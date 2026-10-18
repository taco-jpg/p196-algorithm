import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0624 : leaf0624.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0625 : leaf0625.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0626 : leaf0626.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0627 : leaf0627.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0624 : checkRow ranks (fastLongPred 7) [7,3,9,6,0,1,9] 2 = true := by decide +kernel
theorem row_branch0625 : checkRow ranks (fastLongPred 7) [7,3,9,5,9,6,2] 1 = true := by decide +kernel
theorem row_branch0626 : checkRow ranks (fastLongPred 7) [7,3,9,5,8,4,8] 2 = true := by decide +kernel
theorem row_branch0627 : checkRow ranks (fastLongPred 7) [7,3,9,6,1,3,4] 2 = true := by decide +kernel
end SevenColumn.Certificate739
