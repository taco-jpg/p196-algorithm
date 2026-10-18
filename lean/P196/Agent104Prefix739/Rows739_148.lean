import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0592 : leaf0592.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0593 : leaf0593.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0594 : leaf0594.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0595 : leaf0595.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0592 : checkRow ranks (fastLongPred 7) [7,3,9,4,0,7,7] 2 = true := by decide +kernel
theorem row_branch0593 : checkRow ranks (fastLongPred 7) [7,3,9,4,1,9,1] 1 = true := by decide +kernel
theorem row_branch0594 : checkRow ranks (fastLongPred 7) [7,3,9,4,1,3,4] 2 = true := by decide +kernel
theorem row_branch0595 : checkRow ranks (fastLongPred 7) [7,3,9,4,0,2,0] 2 = true := by decide +kernel
end SevenColumn.Certificate739
