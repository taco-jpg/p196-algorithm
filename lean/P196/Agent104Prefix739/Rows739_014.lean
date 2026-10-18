import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0056 : leaf0056.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0057 : leaf0057.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0058 : leaf0058.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0059 : leaf0059.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0056 : checkRow ranks (fastLongPred 7) [1,12,2,16,6,9,12] 0 = true := by decide +kernel
theorem row_branch0057 : checkRow ranks (fastLongPred 7) [1,12,2,16,7,18,11] 0 = true := by decide +kernel
theorem row_branch0058 : checkRow ranks (fastLongPred 7) [1,12,2,16,6,16,1] 0 = true := by decide +kernel
theorem row_branch0059 : checkRow ranks (fastLongPred 7) [1,12,2,15,6,3,15] 0 = true := by decide +kernel
end SevenColumn.Certificate739
