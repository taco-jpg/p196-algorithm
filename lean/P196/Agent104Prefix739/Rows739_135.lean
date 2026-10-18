import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0540 : leaf0540.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0541 : leaf0541.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0542 : leaf0542.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0543 : leaf0543.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0540 : checkRow ranks (fastLongPred 7) [7,3,9,0,5,9,2] 0 = true := by decide +kernel
theorem row_branch0541 : checkRow ranks (fastLongPred 7) [7,3,9,0,1,3,5] 0 = true := by decide +kernel
theorem row_branch0542 : checkRow ranks (fastLongPred 7) [7,3,9,1,1,0,7] 2 = true := by decide +kernel
theorem row_branch0543 : checkRow ranks (fastLongPred 7) [7,3,9,1,2,2,1] 2 = true := by decide +kernel
end SevenColumn.Certificate739
