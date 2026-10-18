import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0116 : leaf0116.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0117 : leaf0117.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0118 : leaf0118.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0119 : leaf0119.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0116 : checkRow ranks (fastLongPred 7) [1,15,16,11,11,15,4] 0 = true := by decide +kernel
theorem row_branch0117 : checkRow ranks (fastLongPred 7) [1,15,16,14,0,10,16] 0 = true := by decide +kernel
theorem row_branch0118 : checkRow ranks (fastLongPred 7) [1,15,16,14,0,4,9] 0 = true := by decide +kernel
theorem row_branch0119 : checkRow ranks (fastLongPred 7) [1,15,16,14,1,6,10] 0 = true := by decide +kernel
end SevenColumn.Certificate739
