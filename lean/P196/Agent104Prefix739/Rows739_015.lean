import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0060 : leaf0060.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0061 : leaf0061.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0062 : leaf0062.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0063 : leaf0063.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0060 : checkRow ranks (fastLongPred 7) [1,11,6,6,11,14,7] 0 = true := by decide +kernel
theorem row_branch0061 : checkRow ranks (fastLongPred 7) [1,11,5,4,0,8,5] 0 = true := by decide +kernel
theorem row_branch0062 : checkRow ranks (fastLongPred 7) [1,11,0,6,11,0,18] 0 = true := by decide +kernel
theorem row_branch0063 : checkRow ranks (fastLongPred 7) [1,12,3,18,16,13,2] 0 = true := by decide +kernel
end SevenColumn.Certificate739
