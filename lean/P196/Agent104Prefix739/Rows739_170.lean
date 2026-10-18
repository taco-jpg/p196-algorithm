import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0680 : leaf0680.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0681 : leaf0681.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0682 : leaf0682.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0683 : leaf0683.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0680 : checkRow ranks (fastLongPred 7) [7,3,9,9,2,1,9] 1 = true := by decide +kernel
theorem row_branch0681 : checkRow ranks (fastLongPred 7) [7,3,9,9,1,6,2] 1 = true := by decide +kernel
theorem row_branch0682 : checkRow ranks (fastLongPred 7) [7,3,9,9,0,4,8] 2 = true := by decide +kernel
theorem row_branch0683 : checkRow ranks (fastLongPred 7) [7,3,9,8,8,1,9] 2 = true := by decide +kernel
end SevenColumn.Certificate739
