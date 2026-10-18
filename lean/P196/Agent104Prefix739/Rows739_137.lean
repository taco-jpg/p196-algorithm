import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0548 : leaf0548.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0549 : leaf0549.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0550 : leaf0550.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0551 : leaf0551.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0548 : checkRow ranks (fastLongPred 7) [7,3,9,1,2,7,8] 2 = true := by decide +kernel
theorem row_branch0549 : checkRow ranks (fastLongPred 7) [7,3,9,1,5,6,4] 2 = true := by decide +kernel
theorem row_branch0550 : checkRow ranks (fastLongPred 7) [7,3,9,1,6,7,8] 2 = true := by decide +kernel
theorem row_branch0551 : checkRow ranks (fastLongPred 7) [7,3,9,1,6,2,1] 2 = true := by decide +kernel
end SevenColumn.Certificate739
