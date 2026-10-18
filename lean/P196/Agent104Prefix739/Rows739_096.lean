import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0384 : leaf0384.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0385 : leaf0385.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0386 : leaf0386.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0387 : leaf0387.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0384 : checkRow ranks (fastLongPred 7) [5,9,4,14,18,3,13] 2 = true := by decide +kernel
theorem row_branch0385 : checkRow ranks (fastLongPred 7) [5,13,12,6,2,3,12] 4 = true := by decide +kernel
theorem row_branch0386 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,11,10] 0 = true := by decide +kernel
theorem row_branch0387 : checkRow ranks (fastLongPred 7) [5,13,16,10,15,5,9] 2 = true := by decide +kernel
end SevenColumn.Certificate739
