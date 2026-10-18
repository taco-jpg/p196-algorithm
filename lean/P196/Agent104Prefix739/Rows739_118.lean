import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0472 : leaf0472.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0473 : leaf0473.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0474 : leaf0474.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0475 : leaf0475.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0472 : checkRow ranks (fastLongPred 7) [6,5,2,13,13,6,18] 2 = true := by decide +kernel
theorem row_branch0473 : checkRow ranks (fastLongPred 7) [6,5,2,12,16,7,0] 1 = true := by decide +kernel
theorem row_branch0474 : checkRow ranks (fastLongPred 7) [6,4,11,18,0,1,15] 0 = true := by decide +kernel
theorem row_branch0475 : checkRow ranks (fastLongPred 7) [6,4,10,17,16,2,2] 2 = true := by decide +kernel
end SevenColumn.Certificate739
