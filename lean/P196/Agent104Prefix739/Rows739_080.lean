import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0320 : leaf0320.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0321 : leaf0321.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0322 : leaf0322.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0323 : leaf0323.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0320 : checkRow ranks (fastLongPred 7) [3,11,14,3,14,0,10] 1 = true := by decide +kernel
theorem row_branch0321 : checkRow ranks (fastLongPred 7) [3,11,14,4,0,10,10] 1 = true := by decide +kernel
theorem row_branch0322 : checkRow ranks (fastLongPred 7) [3,11,14,4,1,10,4] 1 = true := by decide +kernel
theorem row_branch0323 : checkRow ranks (fastLongPred 7) [3,11,14,4,1,0,12] 0 = true := by decide +kernel
end SevenColumn.Certificate739
