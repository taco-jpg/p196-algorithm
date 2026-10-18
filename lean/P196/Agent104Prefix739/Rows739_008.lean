import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0032 : leaf0032.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0033 : leaf0033.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0034 : leaf0034.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0035 : leaf0035.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0032 : checkRow ranks (fastLongPred 7) [1,11,1,9,1,11,10] 0 = true := by decide +kernel
theorem row_branch0033 : checkRow ranks (fastLongPred 7) [1,11,1,9,0,14,15] 0 = true := by decide +kernel
theorem row_branch0034 : checkRow ranks (fastLongPred 7) [1,11,2,3,1,4,13] 0 = true := by decide +kernel
theorem row_branch0035 : checkRow ranks (fastLongPred 7) [1,11,2,3,6,11,12] 0 = true := by decide +kernel
end SevenColumn.Certificate739
