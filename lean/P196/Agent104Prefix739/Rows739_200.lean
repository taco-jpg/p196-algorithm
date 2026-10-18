import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0800 : leaf0800.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0801 : leaf0801.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0802 : leaf0802.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0803 : leaf0803.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0800 : checkRow ranks (fastLongPred 7) [12,1,14,7,9,10,0] 0 = true := by decide +kernel
theorem row_branch0801 : checkRow ranks (fastLongPred 7) [12,1,14,7,16,7,16] 3 = true := by decide +kernel
theorem row_branch0802 : checkRow ranks (fastLongPred 7) [12,1,14,7,16,2,18] 3 = true := by decide +kernel
theorem row_branch0803 : checkRow ranks (fastLongPred 7) [12,1,14,7,9,5,8] 3 = true := by decide +kernel
end SevenColumn.Certificate739
