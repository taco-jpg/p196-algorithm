import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0220 : leaf0220.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0221 : leaf0221.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0222 : leaf0222.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0223 : leaf0223.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0220 : checkRow ranks (fastLongPred 7) [3,2,11,5,15,16,5] 1 = true := by decide +kernel
theorem row_branch0221 : checkRow ranks (fastLongPred 7) [3,2,13,13,3,9,17] 1 = true := by decide +kernel
theorem row_branch0222 : checkRow ranks (fastLongPred 7) [3,2,13,13,13,11,14] 1 = true := by decide +kernel
theorem row_branch0223 : checkRow ranks (fastLongPred 7) [3,2,13,13,11,7,13] 1 = true := by decide +kernel
end SevenColumn.Certificate739
