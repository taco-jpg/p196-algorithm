import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0520 : leaf0520.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0521 : leaf0521.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0522 : leaf0522.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0523 : leaf0523.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0520 : checkRow ranks (fastLongPred 7) [6,8,17,15,10,5,8] 2 = true := by decide +kernel
theorem row_branch0521 : checkRow ranks (fastLongPred 7) [7,2,0,4,14,11,14] 0 = true := by decide +kernel
theorem row_branch0522 : checkRow ranks (fastLongPred 7) [7,3,9,0,0,7,8] 0 = true := by decide +kernel
theorem row_branch0523 : checkRow ranks (fastLongPred 7) [7,3,9,0,0,2,1] 0 = true := by decide +kernel
end SevenColumn.Certificate739
