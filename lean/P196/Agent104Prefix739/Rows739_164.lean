import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0656 : leaf0656.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0657 : leaf0657.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0658 : leaf0658.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0659 : leaf0659.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0656 : checkRow ranks (fastLongPred 7) [7,3,9,7,7,3,4] 2 = true := by decide +kernel
theorem row_branch0657 : checkRow ranks (fastLongPred 7) [7,3,9,7,8,4,8] 2 = true := by decide +kernel
theorem row_branch0658 : checkRow ranks (fastLongPred 7) [7,3,9,7,7,9,1] 2 = true := by decide +kernel
theorem row_branch0659 : checkRow ranks (fastLongPred 7) [7,3,9,7,6,7,7] 2 = true := by decide +kernel
end SevenColumn.Certificate739
