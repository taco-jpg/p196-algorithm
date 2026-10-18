import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0792 : leaf0792.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0793 : leaf0793.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0794 : leaf0794.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0795 : leaf0795.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0792 : checkRow ranks (fastLongPred 7) [12,1,14,5,13,5,13] 3 = true := by decide +kernel
theorem row_branch0793 : checkRow ranks (fastLongPred 7) [12,1,14,5,4,8,17] 3 = true := by decide +kernel
theorem row_branch0794 : checkRow ranks (fastLongPred 7) [12,1,7,8,10,18,9] 2 = true := by decide +kernel
theorem row_branch0795 : checkRow ranks (fastLongPred 7) [12,1,5,16,16,14,4] 3 = true := by decide +kernel
end SevenColumn.Certificate739
