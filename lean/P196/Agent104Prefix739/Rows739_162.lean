import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0648 : leaf0648.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0649 : leaf0649.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0650 : leaf0650.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0651 : leaf0651.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0648 : checkRow ranks (fastLongPred 7) [7,3,9,7,2,7,7] 2 = true := by decide +kernel
theorem row_branch0649 : checkRow ranks (fastLongPred 7) [7,3,9,7,3,9,1] 2 = true := by decide +kernel
theorem row_branch0650 : checkRow ranks (fastLongPred 7) [7,3,9,7,3,3,4] 2 = true := by decide +kernel
theorem row_branch0651 : checkRow ranks (fastLongPred 7) [7,3,9,7,2,2,0] 2 = true := by decide +kernel
end SevenColumn.Certificate739
