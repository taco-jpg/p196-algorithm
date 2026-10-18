import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0996 : leaf0996.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0997 : leaf0997.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0998 : leaf0998.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0999 : leaf0999.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0996 : checkRow ranks (fastLongPred 7) [14,17,8,2,17,8,12] 3 = true := by decide +kernel
theorem row_branch0997 : checkRow ranks (fastLongPred 7) [14,17,8,12,8,18,6] 3 = true := by decide +kernel
theorem row_branch0998 : checkRow ranks (fastLongPred 7) [14,17,13,2,0,13,7] 3 = true := by decide +kernel
theorem row_branch0999 : checkRow ranks (fastLongPred 7) [14,17,13,1,4,16,16] 3 = true := by decide +kernel
end SevenColumn.Certificate739
