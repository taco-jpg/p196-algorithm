import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0776 : leaf0776.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0777 : leaf0777.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0778 : leaf0778.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0779 : leaf0779.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0776 : checkRow ranks (fastLongPred 7) [12,1,5,7,18,5,13] 3 = true := by decide +kernel
theorem row_branch0777 : checkRow ranks (fastLongPred 7) [12,1,5,14,4,5,16] 3 = true := by decide +kernel
theorem row_branch0778 : checkRow ranks (fastLongPred 7) [12,1,5,7,18,14,15] 3 = true := by decide +kernel
theorem row_branch0779 : checkRow ranks (fastLongPred 7) [12,1,5,7,16,14,4] 3 = true := by decide +kernel
end SevenColumn.Certificate739
