import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0292 : leaf0292.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0293 : leaf0293.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0294 : leaf0294.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0295 : leaf0295.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0292 : checkRow ranks (fastLongPred 7) [3,11,14,2,4,13,10] 1 = true := by decide +kernel
theorem row_branch0293 : checkRow ranks (fastLongPred 7) [3,11,14,2,11,13,10] 1 = true := by decide +kernel
theorem row_branch0294 : checkRow ranks (fastLongPred 7) [3,11,14,2,12,13,14] 1 = true := by decide +kernel
theorem row_branch0295 : checkRow ranks (fastLongPred 7) [3,11,14,2,12,4,2] 1 = true := by decide +kernel
end SevenColumn.Certificate739
