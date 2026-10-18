import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0716 : leaf0716.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0717 : leaf0717.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0718 : leaf0718.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0719 : leaf0719.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0716 : checkRow ranks (fastLongPred 7) [7,8,14,0,18,11,14] 2 = true := by decide +kernel
theorem row_branch0717 : checkRow ranks (fastLongPred 7) [7,8,14,5,8,18,15] 2 = true := by decide +kernel
theorem row_branch0718 : checkRow ranks (fastLongPred 7) [7,8,14,5,4,2,5] 2 = true := by decide +kernel
theorem row_branch0719 : checkRow ranks (fastLongPred 7) [7,8,16,10,11,18,14] 2 = true := by decide +kernel
end SevenColumn.Certificate739
