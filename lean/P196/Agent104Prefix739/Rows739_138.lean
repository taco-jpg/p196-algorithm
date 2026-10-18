import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0552 : leaf0552.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0553 : leaf0553.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0554 : leaf0554.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0555 : leaf0555.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0552 : checkRow ranks (fastLongPred 7) [7,3,9,1,7,9,2] 2 = true := by decide +kernel
theorem row_branch0553 : checkRow ranks (fastLongPred 7) [7,3,9,1,9,0,6] 2 = true := by decide +kernel
theorem row_branch0554 : checkRow ranks (fastLongPred 7) [7,3,9,1,8,4,9] 2 = true := by decide +kernel
theorem row_branch0555 : checkRow ranks (fastLongPred 7) [7,3,9,1,7,3,5] 2 = true := by decide +kernel
end SevenColumn.Certificate739
