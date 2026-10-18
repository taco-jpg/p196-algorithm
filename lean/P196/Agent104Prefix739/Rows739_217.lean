import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0868 : leaf0868.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0869 : leaf0869.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0870 : leaf0870.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0871 : leaf0871.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0868 : checkRow ranks (fastLongPred 7) [12,9,1,16,13,5,7] 3 = true := by decide +kernel
theorem row_branch0869 : checkRow ranks (fastLongPred 7) [12,9,1,16,6,17,11] 3 = true := by decide +kernel
theorem row_branch0870 : checkRow ranks (fastLongPred 7) [12,9,1,16,13,18,2] 3 = true := by decide +kernel
theorem row_branch0871 : checkRow ranks (fastLongPred 7) [12,9,3,7,8,5,1] 3 = true := by decide +kernel
end SevenColumn.Certificate739
