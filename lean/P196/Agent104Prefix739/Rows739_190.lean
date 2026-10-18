import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0760 : leaf0760.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0761 : leaf0761.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0762 : leaf0762.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0763 : leaf0763.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0760 : checkRow ranks (fastLongPred 7) [11,16,14,11,2,3,10] 1 = true := by decide +kernel
theorem row_branch0761 : checkRow ranks (fastLongPred 7) [11,16,5,4,4,18,14] 1 = true := by decide +kernel
theorem row_branch0762 : checkRow ranks (fastLongPred 7) [11,7,5,2,11,14,11] 7 = true := by decide +kernel
theorem row_branch0763 : checkRow ranks (fastLongPred 7) [8,5,3,15,13,3,13] 3 = true := by decide +kernel
end SevenColumn.Certificate739
