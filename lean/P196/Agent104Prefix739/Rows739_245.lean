import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0980 : leaf0980.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0981 : leaf0981.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0982 : leaf0982.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0983 : leaf0983.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0980 : checkRow ranks (fastLongPred 7) [14,8,13,2,0,12,18] 0 = true := by decide +kernel
theorem row_branch0981 : checkRow ranks (fastLongPred 7) [14,8,13,11,13,18,3] 3 = true := by decide +kernel
theorem row_branch0982 : checkRow ranks (fastLongPred 7) [14,8,17,3,8,18,14] 2 = true := by decide +kernel
theorem row_branch0983 : checkRow ranks (fastLongPred 7) [14,8,17,2,17,7,7] 3 = true := by decide +kernel
end SevenColumn.Certificate739
