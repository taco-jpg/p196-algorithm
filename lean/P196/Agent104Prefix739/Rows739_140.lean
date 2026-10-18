import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0560 : leaf0560.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0561 : leaf0561.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0562 : leaf0562.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0563 : leaf0563.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0560 : checkRow ranks (fastLongPred 7) [7,3,9,2,2,4,9] 2 = true := by decide +kernel
theorem row_branch0561 : checkRow ranks (fastLongPred 7) [7,3,9,2,3,6,3] 2 = true := by decide +kernel
theorem row_branch0562 : checkRow ranks (fastLongPred 7) [7,3,9,2,3,0,6] 2 = true := by decide +kernel
theorem row_branch0563 : checkRow ranks (fastLongPred 7) [7,3,9,2,1,9,2] 2 = true := by decide +kernel
end SevenColumn.Certificate739
