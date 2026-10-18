import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0144 : leaf0144.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0145 : leaf0145.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0146 : leaf0146.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0147 : leaf0147.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0144 : checkRow ranks (fastLongPred 7) [2,1,7,0,0,18,13] 1 = true := by decide +kernel
theorem row_branch0145 : checkRow ranks (fastLongPred 7) [2,7,7,12,13,1,16] 1 = true := by decide +kernel
theorem row_branch0146 : checkRow ranks (fastLongPred 7) [2,9,12,9,8,11,10] 6 = true := by decide +kernel
theorem row_branch0147 : checkRow ranks (fastLongPred 7) [2,7,8,2,14,0,10] 0 = true := by decide +kernel
end SevenColumn.Certificate739
