import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0484 : leaf0484.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0485 : leaf0485.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0486 : leaf0486.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0487 : leaf0487.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0484 : checkRow ranks (fastLongPred 7) [6,5,3,18,10,3,18] 2 = true := by decide +kernel
theorem row_branch0485 : checkRow ranks (fastLongPred 7) [6,5,2,18,8,18,10] 2 = true := by decide +kernel
theorem row_branch0486 : checkRow ranks (fastLongPred 7) [6,5,7,2,16,13,4] 2 = true := by decide +kernel
theorem row_branch0487 : checkRow ranks (fastLongPred 7) [6,5,7,3,13,9,17] 1 = true := by decide +kernel
end SevenColumn.Certificate739
