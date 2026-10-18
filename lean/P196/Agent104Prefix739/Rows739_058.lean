import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0232 : leaf0232.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0233 : leaf0233.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0234 : leaf0234.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0235 : leaf0235.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0232 : checkRow ranks (fastLongPred 7) [3,4,8,17,16,10,3] 1 = true := by decide +kernel
theorem row_branch0233 : checkRow ranks (fastLongPred 7) [3,4,8,17,14,8,16] 1 = true := by decide +kernel
theorem row_branch0234 : checkRow ranks (fastLongPred 7) [3,4,8,15,9,12,6] 1 = true := by decide +kernel
theorem row_branch0235 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,6,17] 7 = true := by decide +kernel
end SevenColumn.Certificate739
