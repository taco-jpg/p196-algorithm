import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0600 : leaf0600.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0601 : leaf0601.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0602 : leaf0602.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0603 : leaf0603.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0600 : checkRow ranks (fastLongPred 7) [7,3,9,4,6,4,8] 2 = true := by decide +kernel
theorem row_branch0601 : checkRow ranks (fastLongPred 7) [7,3,9,4,5,9,1] 1 = true := by decide +kernel
theorem row_branch0602 : checkRow ranks (fastLongPred 7) [7,3,9,4,4,7,7] 2 = true := by decide +kernel
theorem row_branch0603 : checkRow ranks (fastLongPred 7) [7,3,9,4,2,4,8] 2 = true := by decide +kernel
end SevenColumn.Certificate739
