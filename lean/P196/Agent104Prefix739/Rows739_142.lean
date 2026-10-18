import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0568 : leaf0568.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0569 : leaf0569.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0570 : leaf0570.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0571 : leaf0571.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0568 : checkRow ranks (fastLongPred 7) [7,3,9,2,8,2,0] 2 = true := by decide +kernel
theorem row_branch0569 : checkRow ranks (fastLongPred 7) [7,3,9,2,7,6,3] 2 = true := by decide +kernel
theorem row_branch0570 : checkRow ranks (fastLongPred 7) [7,3,9,2,6,4,9] 2 = true := by decide +kernel
theorem row_branch0571 : checkRow ranks (fastLongPred 7) [7,3,9,2,4,2,0] 2 = true := by decide +kernel
end SevenColumn.Certificate739
