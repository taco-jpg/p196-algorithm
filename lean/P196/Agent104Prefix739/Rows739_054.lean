import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0216 : leaf0216.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0217 : leaf0217.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0218 : leaf0218.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0219 : leaf0219.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0216 : checkRow ranks (fastLongPred 7) [3,2,13,11,8,14,11] 1 = true := by decide +kernel
theorem row_branch0217 : checkRow ranks (fastLongPred 7) [3,2,13,11,8,10,11] 1 = true := by decide +kernel
theorem row_branch0218 : checkRow ranks (fastLongPred 7) [3,2,13,11,4,8,14] 1 = true := by decide +kernel
theorem row_branch0219 : checkRow ranks (fastLongPred 7) [3,2,11,8,13,16,11] 1 = true := by decide +kernel
end SevenColumn.Certificate739
