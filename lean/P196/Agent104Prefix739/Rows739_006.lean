import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0024 : leaf0024.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0025 : leaf0025.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0026 : leaf0026.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0027 : leaf0027.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0024 : checkRow ranks (fastLongPred 7) [1,10,3,16,12,4,7] 0 = true := by decide +kernel
theorem row_branch0025 : checkRow ranks (fastLongPred 7) [1,10,9,0,7,13,2] 0 = true := by decide +kernel
theorem row_branch0026 : checkRow ranks (fastLongPred 7) [1,11,0,5,8,12,0] 0 = true := by decide +kernel
theorem row_branch0027 : checkRow ranks (fastLongPred 7) [1,11,0,5,7,5,17] 0 = true := by decide +kernel
end SevenColumn.Certificate739
