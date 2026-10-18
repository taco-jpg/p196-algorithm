import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0084 : leaf0084.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0085 : leaf0085.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0086 : leaf0086.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0087 : leaf0087.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0084 : checkRow ranks (fastLongPred 7) [1,15,16,10,4,6,1] 0 = true := by decide +kernel
theorem row_branch0085 : checkRow ranks (fastLongPred 7) [1,15,16,10,6,6,7] 0 = true := by decide +kernel
theorem row_branch0086 : checkRow ranks (fastLongPred 7) [1,15,16,10,9,6,12] 0 = true := by decide +kernel
theorem row_branch0087 : checkRow ranks (fastLongPred 7) [1,15,16,10,6,15,10] 0 = true := by decide +kernel
end SevenColumn.Certificate739
