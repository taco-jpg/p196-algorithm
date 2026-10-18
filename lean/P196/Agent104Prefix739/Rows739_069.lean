import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0276 : leaf0276.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0277 : leaf0277.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0278 : leaf0278.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0279 : leaf0279.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0276 : checkRow ranks (fastLongPred 7) [3,11,14,1,11,12,12] 1 = true := by decide +kernel
theorem row_branch0277 : checkRow ranks (fastLongPred 7) [3,11,14,1,14,4,2] 1 = true := by decide +kernel
theorem row_branch0278 : checkRow ranks (fastLongPred 7) [3,11,14,2,0,4,10] 1 = true := by decide +kernel
theorem row_branch0279 : checkRow ranks (fastLongPred 7) [3,11,14,1,14,13,14] 1 = true := by decide +kernel
end SevenColumn.Certificate739
