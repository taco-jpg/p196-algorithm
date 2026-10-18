import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0904 : leaf0904.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0905 : leaf0905.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0906 : leaf0906.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0907 : leaf0907.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0904 : checkRow ranks (fastLongPred 7) [12,10,5,16,7,14,4] 3 = true := by decide +kernel
theorem row_branch0905 : checkRow ranks (fastLongPred 7) [12,10,5,16,7,7,12] 6 = true := by decide +kernel
theorem row_branch0906 : checkRow ranks (fastLongPred 7) [12,10,5,14,13,15,13] 3 = true := by decide +kernel
theorem row_branch0907 : checkRow ranks (fastLongPred 7) [12,10,5,7,18,14,1] 6 = true := by decide +kernel
end SevenColumn.Certificate739
