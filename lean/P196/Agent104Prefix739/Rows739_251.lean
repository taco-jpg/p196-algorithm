import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf1004 : leaf1004.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1005 : leaf1005.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1006 : leaf1006.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1007 : leaf1007.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch1004 : checkRow ranks (fastLongPred 7) [14,17,13,11,13,18,9] 3 = true := by decide +kernel
theorem row_branch1005 : checkRow ranks (fastLongPred 7) [14,17,17,11,8,17,11] 3 = true := by decide +kernel
theorem row_branch1006 : checkRow ranks (fastLongPred 7) [16,1,7,2,16,8,6] 4 = true := by decide +kernel
theorem row_branch1007 : checkRow ranks (fastLongPred 7) [14,17,17,12,8,14,10] 3 = true := by decide +kernel
end SevenColumn.Certificate739
