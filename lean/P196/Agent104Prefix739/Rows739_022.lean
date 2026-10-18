import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0088 : leaf0088.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0089 : leaf0089.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0090 : leaf0090.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0091 : leaf0091.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0088 : checkRow ranks (fastLongPred 7) [1,15,16,10,10,5,6] 0 = true := by decide +kernel
theorem row_branch0089 : checkRow ranks (fastLongPred 7) [1,15,16,10,11,1,15] 0 = true := by decide +kernel
theorem row_branch0090 : checkRow ranks (fastLongPred 7) [1,15,16,10,10,14,5] 0 = true := by decide +kernel
theorem row_branch0091 : checkRow ranks (fastLongPred 7) [1,15,16,10,9,16,1] 0 = true := by decide +kernel
end SevenColumn.Certificate739
