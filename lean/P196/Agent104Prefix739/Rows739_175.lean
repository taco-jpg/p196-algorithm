import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0700 : leaf0700.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0701 : leaf0701.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0702 : leaf0702.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0703 : leaf0703.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0700 : checkRow ranks (fastLongPred 7) [7,3,9,8,3,6,2] 2 = true := by decide +kernel
theorem row_branch0701 : checkRow ranks (fastLongPred 7) [7,4,2,5,16,18,17] 1 = true := by decide +kernel
theorem row_branch0702 : checkRow ranks (fastLongPred 7) [7,4,4,5,14,3,13] 2 = true := by decide +kernel
theorem row_branch0703 : checkRow ranks (fastLongPred 7) [7,4,4,1,8,18,5] 1 = true := by decide +kernel
end SevenColumn.Certificate739
