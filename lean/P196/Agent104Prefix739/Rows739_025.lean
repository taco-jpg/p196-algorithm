import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0100 : leaf0100.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0101 : leaf0101.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0102 : leaf0102.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0103 : leaf0103.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0100 : checkRow ranks (fastLongPred 7) [1,15,16,10,15,10,0] 0 = true := by decide +kernel
theorem row_branch0101 : checkRow ranks (fastLongPred 7) [1,15,16,11,0,12,4] 0 = true := by decide +kernel
theorem row_branch0102 : checkRow ranks (fastLongPred 7) [1,15,16,11,1,9,9] 0 = true := by decide +kernel
theorem row_branch0103 : checkRow ranks (fastLongPred 7) [1,15,16,11,1,1,9] 0 = true := by decide +kernel
end SevenColumn.Certificate739
