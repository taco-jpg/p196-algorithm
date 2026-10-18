import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0436 : leaf0436.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0437 : leaf0437.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0438 : leaf0438.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0439 : leaf0439.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0436 : checkRow ranks (fastLongPred 7) [6,4,7,11,14,10,18] 1 = true := by decide +kernel
theorem row_branch0437 : checkRow ranks (fastLongPred 7) [6,4,7,11,10,0,15] 2 = true := by decide +kernel
theorem row_branch0438 : checkRow ranks (fastLongPred 7) [6,4,7,16,4,1,1] 2 = true := by decide +kernel
theorem row_branch0439 : checkRow ranks (fastLongPred 7) [6,4,7,16,4,16,3] 1 = true := by decide +kernel
end SevenColumn.Certificate739
