import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0000 : leaf0000.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0001 : leaf0001.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0002 : leaf0002.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0003 : leaf0003.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0000 : checkRow ranks (fastLongPred 7) [1,0,2,5,4,10,15] 0 = true := by decide +kernel
theorem row_branch0001 : checkRow ranks (fastLongPred 7) [1,2,8,18,10,18,2] 0 = true := by decide +kernel
theorem row_branch0002 : checkRow ranks (fastLongPred 7) [1,0,13,9,9,14,8] 0 = true := by decide +kernel
theorem row_branch0003 : checkRow ranks (fastLongPred 7) [1,4,16,1,9,9,10] 0 = true := by decide +kernel
end SevenColumn.Certificate739
