import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0580 : leaf0580.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0581 : leaf0581.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0582 : leaf0582.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0583 : leaf0583.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0580 : checkRow ranks (fastLongPred 7) [7,3,9,3,1,0,6] 1 = true := by decide +kernel
theorem row_branch0581 : checkRow ranks (fastLongPred 7) [7,3,9,3,3,9,2] 2 = true := by decide +kernel
theorem row_branch0582 : checkRow ranks (fastLongPred 7) [7,3,9,3,5,0,6] 2 = true := by decide +kernel
theorem row_branch0583 : checkRow ranks (fastLongPred 7) [7,3,9,3,4,4,9] 2 = true := by decide +kernel
end SevenColumn.Certificate739
