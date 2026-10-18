import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0376 : leaf0376.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0377 : leaf0377.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0378 : leaf0378.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0379 : leaf0379.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0376 : checkRow ranks (fastLongPred 7) [5,7,14,13,15,14,17] 2 = true := by decide +kernel
theorem row_branch0377 : checkRow ranks (fastLongPred 7) [5,4,10,16,3,2,6] 2 = true := by decide +kernel
theorem row_branch0378 : checkRow ranks (fastLongPred 7) [4,9,16,15,5,6,15] 2 = true := by decide +kernel
theorem row_branch0379 : checkRow ranks (fastLongPred 7) [3,14,8,17,13,11,8] 1 = true := by decide +kernel
end SevenColumn.Certificate739
