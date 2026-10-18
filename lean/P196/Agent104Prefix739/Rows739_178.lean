import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0712 : leaf0712.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0713 : leaf0713.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0714 : leaf0714.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0715 : leaf0715.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0712 : checkRow ranks (fastLongPred 7) [7,8,12,4,12,3,15] 2 = true := by decide +kernel
theorem row_branch0713 : checkRow ranks (fastLongPred 7) [7,8,12,0,10,1,17] 2 = true := by decide +kernel
theorem row_branch0714 : checkRow ranks (fastLongPred 7) [7,8,4,0,0,2,9] 0 = true := by decide +kernel
theorem row_branch0715 : checkRow ranks (fastLongPred 7) [7,4,8,11,8,2,0] 2 = true := by decide +kernel
end SevenColumn.Certificate739
