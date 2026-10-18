import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0336 : leaf0336.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0337 : leaf0337.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0338 : leaf0338.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0339 : leaf0339.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0336 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,4,13] 10 = true := by decide +kernel
theorem row_branch0337 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,4,11] 37 = true := by decide +kernel
theorem row_branch0338 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,14,9] 1 = true := by decide +kernel
theorem row_branch0339 : checkRow ranks (fastLongPred 7) [3,11,14,9,2,14,11] 10 = true := by decide +kernel
end SevenColumn.Certificate739
