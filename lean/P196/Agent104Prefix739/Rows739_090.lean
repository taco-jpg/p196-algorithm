import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0360 : leaf0360.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0361 : leaf0361.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0362 : leaf0362.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0363 : leaf0363.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0360 : checkRow ranks (fastLongPred 7) [3,14,8,15,11,4,5] 1 = true := by decide +kernel
theorem row_branch0361 : checkRow ranks (fastLongPred 7) [3,14,7,17,14,2,12] 1 = true := by decide +kernel
theorem row_branch0362 : checkRow ranks (fastLongPred 7) [3,14,7,15,4,9,2] 1 = true := by decide +kernel
theorem row_branch0363 : checkRow ranks (fastLongPred 7) [3,14,5,12,7,18,16] 0 = true := by decide +kernel
end SevenColumn.Certificate739
