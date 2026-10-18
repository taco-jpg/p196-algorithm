import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0052 : leaf0052.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0053 : leaf0053.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0054 : leaf0054.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0055 : leaf0055.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0052 : checkRow ranks (fastLongPred 7) [1,11,6,5,9,13,11] 0 = true := by decide +kernel
theorem row_branch0053 : checkRow ranks (fastLongPred 7) [1,11,6,6,16,14,10] 0 = true := by decide +kernel
theorem row_branch0054 : checkRow ranks (fastLongPred 7) [1,12,2,15,4,6,3] 0 = true := by decide +kernel
theorem row_branch0055 : checkRow ranks (fastLongPred 7) [1,11,6,6,17,1,12] 0 = true := by decide +kernel
end SevenColumn.Certificate739
