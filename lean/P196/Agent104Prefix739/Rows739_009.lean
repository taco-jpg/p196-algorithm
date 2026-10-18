import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0036 : leaf0036.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0037 : leaf0037.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0038 : leaf0038.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0039 : leaf0039.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0036 : checkRow ranks (fastLongPred 7) [1,11,2,3,5,9,1] 0 = true := by decide +kernel
theorem row_branch0037 : checkRow ranks (fastLongPred 7) [1,11,1,9,4,11,17] 0 = true := by decide +kernel
theorem row_branch0038 : checkRow ranks (fastLongPred 7) [1,11,2,4,4,0,7] 0 = true := by decide +kernel
theorem row_branch0039 : checkRow ranks (fastLongPred 7) [1,11,2,8,6,16,3] 0 = true := by decide +kernel
end SevenColumn.Certificate739
