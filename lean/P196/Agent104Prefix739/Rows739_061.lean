import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0244 : leaf0244.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0245 : leaf0245.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0246 : leaf0246.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0247 : leaf0247.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0244 : checkRow ranks (fastLongPred 7) [3,11,14,0,9,11,10] 1 = true := by decide +kernel
theorem row_branch0245 : checkRow ranks (fastLongPred 7) [3,11,14,0,4,11,14] 1 = true := by decide +kernel
theorem row_branch0246 : checkRow ranks (fastLongPred 7) [3,11,14,0,10,11,9] 1 = true := by decide +kernel
theorem row_branch0247 : checkRow ranks (fastLongPred 7) [3,11,14,0,11,11,13] 1 = true := by decide +kernel
end SevenColumn.Certificate739
