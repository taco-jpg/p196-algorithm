import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0096 : leaf0096.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0097 : leaf0097.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0098 : leaf0098.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0099 : leaf0099.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0096 : checkRow ranks (fastLongPred 7) [1,15,16,10,14,11,5] 0 = true := by decide +kernel
theorem row_branch0097 : checkRow ranks (fastLongPred 7) [1,15,16,10,16,0,9] 0 = true := by decide +kernel
theorem row_branch0098 : checkRow ranks (fastLongPred 7) [1,15,16,10,16,16,4] 0 = true := by decide +kernel
theorem row_branch0099 : checkRow ranks (fastLongPred 7) [1,15,16,10,16,6,11] 0 = true := by decide +kernel
end SevenColumn.Certificate739
