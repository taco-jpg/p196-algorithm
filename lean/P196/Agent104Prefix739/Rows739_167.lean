import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0668 : leaf0668.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0669 : leaf0669.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0670 : leaf0670.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0671 : leaf0671.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0668 : checkRow ranks (fastLongPred 7) [7,3,9,7,4,4,8] 2 = true := by decide +kernel
theorem row_branch0669 : checkRow ranks (fastLongPred 7) [7,3,9,8,4,2,0] 2 = true := by decide +kernel
theorem row_branch0670 : checkRow ranks (fastLongPred 7) [7,3,9,8,5,3,4] 2 = true := by decide +kernel
theorem row_branch0671 : checkRow ranks (fastLongPred 7) [7,3,9,8,4,7,7] 2 = true := by decide +kernel
end SevenColumn.Certificate739
