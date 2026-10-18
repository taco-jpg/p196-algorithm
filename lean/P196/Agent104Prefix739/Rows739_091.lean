import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0364 : leaf0364.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0365 : leaf0365.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0366 : leaf0366.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0367 : leaf0367.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0364 : checkRow ranks (fastLongPred 7) [4,0,6,15,8,6,17] 2 = true := by decide +kernel
theorem row_branch0365 : checkRow ranks (fastLongPred 7) [4,2,5,2,0,0,9] 0 = true := by decide +kernel
theorem row_branch0366 : checkRow ranks (fastLongPred 7) [4,0,6,18,18,9,7] 2 = true := by decide +kernel
theorem row_branch0367 : checkRow ranks (fastLongPred 7) [4,2,14,0,4,2,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
