import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0812 : leaf0812.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0813 : leaf0813.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0814 : leaf0814.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0815 : leaf0815.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0812 : checkRow ranks (fastLongPred 7) [12,1,14,16,7,16,2] 3 = true := by decide +kernel
theorem row_branch0813 : checkRow ranks (fastLongPred 7) [12,1,14,16,16,7,18] 3 = true := by decide +kernel
theorem row_branch0814 : checkRow ranks (fastLongPred 7) [12,1,14,16,16,3,0] 1 = true := by decide +kernel
theorem row_branch0815 : checkRow ranks (fastLongPred 7) [12,1,14,16,18,5,17] 0 = true := by decide +kernel
end SevenColumn.Certificate739
