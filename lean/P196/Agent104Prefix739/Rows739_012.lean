import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0048 : leaf0048.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0049 : leaf0049.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0050 : leaf0050.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0051 : leaf0051.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0048 : checkRow ranks (fastLongPred 7) [1,11,5,4,6,18,17] 0 = true := by decide +kernel
theorem row_branch0049 : checkRow ranks (fastLongPred 7) [1,11,6,5,13,2,17] 0 = true := by decide +kernel
theorem row_branch0050 : checkRow ranks (fastLongPred 7) [1,11,6,5,14,12,17] 0 = true := by decide +kernel
theorem row_branch0051 : checkRow ranks (fastLongPred 7) [1,11,6,5,14,4,15] 0 = true := by decide +kernel
end SevenColumn.Certificate739
