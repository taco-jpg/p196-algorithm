import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0128 : leaf0128.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0129 : leaf0129.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0130 : leaf0130.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0131 : leaf0131.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0128 : checkRow ranks (fastLongPred 7) [1,16,0,18,15,16,4] 0 = true := by decide +kernel
theorem row_branch0129 : checkRow ranks (fastLongPred 7) [1,16,0,17,12,3,17] 0 = true := by decide +kernel
theorem row_branch0130 : checkRow ranks (fastLongPred 7) [1,16,1,9,0,14,6] 0 = true := by decide +kernel
theorem row_branch0131 : checkRow ranks (fastLongPred 7) [1,17,2,5,0,5,18] 0 = true := by decide +kernel
end SevenColumn.Certificate739
