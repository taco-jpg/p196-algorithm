import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0804 : leaf0804.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0805 : leaf0805.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0806 : leaf0806.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0807 : leaf0807.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0804 : checkRow ranks (fastLongPred 7) [12,1,14,7,18,5,17] 1 = true := by decide +kernel
theorem row_branch0805 : checkRow ranks (fastLongPred 7) [12,1,14,14,4,6,2] 3 = true := by decide +kernel
theorem row_branch0806 : checkRow ranks (fastLongPred 7) [12,1,14,7,18,15,0] 3 = true := by decide +kernel
theorem row_branch0807 : checkRow ranks (fastLongPred 7) [12,1,14,14,13,7,16] 3 = true := by decide +kernel
end SevenColumn.Certificate739
