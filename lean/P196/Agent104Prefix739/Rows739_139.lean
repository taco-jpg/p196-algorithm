import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0556 : leaf0556.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0557 : leaf0557.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0558 : leaf0558.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0559 : leaf0559.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0556 : checkRow ranks (fastLongPred 7) [7,3,9,1,5,0,6] 2 = true := by decide +kernel
theorem row_branch0557 : checkRow ranks (fastLongPred 7) [7,3,9,2,0,2,1] 2 = true := by decide +kernel
theorem row_branch0558 : checkRow ranks (fastLongPred 7) [7,3,9,2,1,3,5] 2 = true := by decide +kernel
theorem row_branch0559 : checkRow ranks (fastLongPred 7) [7,3,9,2,0,7,8] 2 = true := by decide +kernel
end SevenColumn.Certificate739
