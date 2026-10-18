import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0772 : leaf0772.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0773 : leaf0773.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0774 : leaf0774.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0775 : leaf0775.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0772 : checkRow ranks (fastLongPred 7) [12,1,5,5,13,15,2] 3 = true := by decide +kernel
theorem row_branch0773 : checkRow ranks (fastLongPred 7) [12,1,5,7,9,9,12] 3 = true := by decide +kernel
theorem row_branch0774 : checkRow ranks (fastLongPred 7) [12,1,5,7,16,7,13] 3 = true := by decide +kernel
theorem row_branch0775 : checkRow ranks (fastLongPred 7) [12,1,5,7,16,2,14] 3 = true := by decide +kernel
end SevenColumn.Certificate739
